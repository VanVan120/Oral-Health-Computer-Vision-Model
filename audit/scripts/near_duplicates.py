"""Near-duplicate detection between two image sets (spec Phase 0.4).

The published rule, reproduced exactly:
  - 32x32 greyscale thumbnails, built with PIL draft mode then bilinear resampling;
  - RMS distance on the 0-255 scale;
  - the distance between two images is the MINIMUM over all 8 elements of the
    dihedral group applied to one of them;
  - a query image is a near-duplicate of a reference set if that minimum is
    below 6.0.

The dihedral group is applied to the query thumbnail. That is equivalent to
applying it to the reference thumbnail, because the group is closed under
inversion and RMS is symmetric, so the minimum over the group is the same
either way.

Why the transform list is asserted rather than trusted: PIL's transpose
constants start at zero -- Image.FLIP_LEFT_RIGHT == 0 -- so a truthiness test
such as `if transform:` silently skips the horizontal flip. The August sweep hit
exactly that bug. assert_transforms_distinct() below fails loudly instead.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image

THUMB = (32, 32)
THRESHOLD = 6.0

# The 8 elements of the dihedral group of order 8. None means identity; the
# others are PIL transpose constants. Order is fixed so that the recorded
# transform name is reproducible.
TRANSFORMS: list[tuple[str, int | None]] = [
    ("identity", None),
    ("hflip", Image.FLIP_LEFT_RIGHT),   # == 0, hence the assertion below
    ("vflip", Image.FLIP_TOP_BOTTOM),
    ("rot90", Image.ROTATE_90),
    ("rot180", Image.ROTATE_180),
    ("rot270", Image.ROTATE_270),
    ("transpose", Image.TRANSPOSE),
    ("transverse", Image.TRANSVERSE),
]

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


# JPEG draft mode is DISABLED, deliberately. See thumbnail() below.
USE_DRAFT = False


def thumbnail(path: Path) -> np.ndarray:
    """32x32 greyscale thumbnail as float32 on the 0-255 scale.

    draft() is not used, and that is load-bearing rather than incidental.

    draft() asks libjpeg for a DCT-scaled decode, which decodes each 8x8 block
    to 1x1 at scale 1/8. When a dimension is not a multiple of 8 the encoder
    padded the final block, and that padding sits only on the right and bottom
    edges. The decoded thumbnail therefore carries an asymmetric edge artifact.

    That artifact does not commute with reflection. For a pair of images related
    by a horizontal flip, drafting both and then flipping one compares a padded
    edge against a real edge, which is why enabling draft here inflates the
    distance for reflected pairs by an order of magnitude while leaving
    identity pairs almost untouched. Measured on this dataset, whose images are
    612x408 (612 = 76*8 + 4, so the width has a partial block):

        calculus-598 vs calculus-742, rot180
            draft on  : RMS 6.9408   -> above the 6.0 threshold, pair missed
            draft off : RMS 0.3903   -> exactly the published S2 distance

    Across the full published S2, enabling draft moves the mean absolute
    deviation from the published distances from 0.145 to 2.793, and costs 31 of
    the 259 pairs. With draft off the regenerated sets reproduce the published
    ones exactly.
    """
    with Image.open(path) as im:
        if USE_DRAFT:
            im.draft("L", THUMB)
        im = im.convert("L").resize(THUMB, Image.BILINEAR)
        return np.asarray(im, dtype=np.float32)


def apply_transform(arr: np.ndarray, op: int | None) -> np.ndarray:
    if op is None:
        return arr
    im = Image.fromarray(arr.astype(np.uint8), mode="L").transpose(op)
    return np.asarray(im, dtype=np.float32)


def assert_transforms_distinct() -> None:
    """Every transform must actually change a generic thumbnail (spec 0.4.2).

    A generic, asymmetric probe is used: a ramp with distinct row and column
    structure, so no transform coincides with another or with the identity.
    """
    probe = np.arange(THUMB[0] * THUMB[1], dtype=np.float32).reshape(THUMB)
    probe = probe + (np.arange(THUMB[0], dtype=np.float32)[:, None] ** 2)
    probe = (probe % 251).astype(np.float32)  # keep it inside uint8 range

    seen: dict[bytes, str] = {}
    for name, op in TRANSFORMS:
        out = apply_transform(probe, op)
        if name != "identity" and np.array_equal(out, probe):
            raise AssertionError(
                f"transform {name!r} (PIL constant {op!r}) left the probe unchanged -- "
                "it is being skipped, most likely by a truthiness test on the constant"
            )
        key = out.tobytes()
        if key in seen:
            raise AssertionError(f"transforms {seen[key]!r} and {name!r} produced identical output")
        seen[key] = name
    if len(seen) != 8:
        raise AssertionError(f"expected 8 distinct transforms, got {len(seen)}")


def list_images(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.suffix.lower() in IMAGE_SUFFIXES and p.is_file())


def build_bank(paths: list[Path]) -> np.ndarray:
    """(n, 1024) float32 matrix of flattened thumbnails."""
    bank = np.empty((len(paths), THUMB[0] * THUMB[1]), dtype=np.float32)
    for i, p in enumerate(paths):
        bank[i] = thumbnail(p).ravel()
    return bank


def min_rms(
    query: np.ndarray,
    ref: np.ndarray,
    transforms: list[tuple[str, int | None]] | None = None,
    chunk: int = 2048,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """For each query row, the min RMS to any ref row under any transform.

    Returns (best_rms, best_ref_index, best_transform_index). The transform
    index is into `transforms`, which defaults to the full dihedral group.

    Uses ||a-b||^2 = ||a||^2 + ||b||^2 - 2 a.b so the whole sweep is one matmul
    per transform per chunk, rather than a Python loop over pairs.
    """
    transforms = TRANSFORMS if transforms is None else transforms
    d = THUMB[0] * THUMB[1]
    n_q = query.shape[0]
    ref_sq = (ref ** 2).sum(axis=1)[None, :]

    best_rms = np.full(n_q, np.inf, dtype=np.float32)
    best_ref = np.full(n_q, -1, dtype=np.int64)
    best_tf = np.full(n_q, -1, dtype=np.int64)

    for tf_idx, (_name, op) in enumerate(transforms):
        if op is None:
            q_t = query
        else:
            q_t = np.stack([apply_transform(row.reshape(THUMB), op).ravel() for row in query])
        q_sq = (q_t ** 2).sum(axis=1)[:, None]

        for start in range(0, n_q, chunk):
            stop = min(start + chunk, n_q)
            d2 = q_sq[start:stop] + ref_sq - 2.0 * (q_t[start:stop] @ ref.T)
            np.maximum(d2, 0.0, out=d2)  # clamp float error before sqrt
            rms = np.sqrt(d2 / d, dtype=np.float32)

            local_ref = rms.argmin(axis=1)
            local_val = rms[np.arange(stop - start), local_ref]
            better = local_val < best_rms[start:stop]
            idx = np.nonzero(better)[0]
            if idx.size:
                best_rms[start + idx] = local_val[idx]
                best_ref[start + idx] = local_ref[idx]
                best_tf[start + idx] = tf_idx
    return best_rms, best_ref, best_tf


def source_of(name: str) -> str:
    """Roboflow encodes the pre-augmentation identity before '.rf.'."""
    return name.split(".rf.")[0] if ".rf." in name else name


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--query-dir", required=True, type=Path, help="e.g. the test split images")
    ap.add_argument("--ref-dir", required=True, type=Path, help="e.g. the train split images")
    ap.add_argument("--out-csv", required=True, type=Path)
    ap.add_argument("--threshold", type=float, default=THRESHOLD)
    args = ap.parse_args()

    assert_transforms_distinct()

    q_paths = list_images(args.query_dir)
    r_paths = list_images(args.ref_dir)
    print(f"query images: {len(q_paths)}   reference images: {len(r_paths)}")

    q_bank = build_bank(q_paths)
    r_bank = build_bank(r_paths)

    # Two passes. The dihedral pass gives the S2-equivalent set and the single
    # best-scoring transform per image. The identity-only pass gives the
    # S1-equivalent set.
    #
    # These are NOT the same thing as filtering the dihedral pass on
    # matching_transform == "identity". 124 test images fall below threshold
    # under identity, but for 61 of them a reflection scores lower still, so
    # identity is the *best* transform for only 63. The published S0 README says
    # this explicitly, and the supplementary bears it out: S1 (124 rows) equals
    # the S2 rows flagged also_found_by_aligned_only = yes, not the 63 rows with
    # matching_transform = identity. Getting this wrong understates the
    # fixed-alignment set by half.
    best_rms, best_ref, best_tf = min_rms(q_bank, r_bank, TRANSFORMS)
    id_rms, id_ref, _ = min_rms(q_bank, r_bank, [TRANSFORMS[0]])

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    n_hit = 0
    n_aligned = 0
    tf_tally: dict[str, int] = {}
    with args.out_csv.open("w", newline="") as fh:
        w = csv.writer(fh)
        # Column order matches the published S2 so the two can be diffed directly.
        w.writerow([
            "test_image", "train_image", "matching_transform", "rms_distance",
            "also_found_by_aligned_only", "test_source", "train_source",
        ])
        for i, qp in enumerate(q_paths):
            if not best_rms[i] < args.threshold:
                continue
            n_hit += 1
            tf_name = TRANSFORMS[best_tf[i]][0]
            tf_tally[tf_name] = tf_tally.get(tf_name, 0) + 1
            aligned = bool(id_rms[i] < args.threshold)
            n_aligned += aligned
            tp = r_paths[best_ref[i]].name
            w.writerow([
                qp.name, tp, tf_name, f"{best_rms[i]:.4f}",
                "yes" if aligned else "no",
                source_of(qp.name), source_of(tp),
            ])

    # Per-transform yields, counting every transform that puts an image below
    # threshold. An image can qualify under several, so these sum to more than
    # the union. The README reports both tallies; so do we.
    yields: dict[str, int] = {}
    for tf_idx, (name, _op) in enumerate(TRANSFORMS):
        rms_tf, _r, _t = min_rms(q_bank, r_bank, [TRANSFORMS[tf_idx]])
        yields[name] = int((rms_tf < args.threshold).sum())

    summary = {
        "query_dir": str(args.query_dir),
        "ref_dir": str(args.ref_dir),
        "n_query": len(q_paths),
        "n_ref": len(r_paths),
        "threshold": args.threshold,
        "n_duplicates_dihedral": n_hit,
        "n_duplicates_identity_only": n_aligned,
        "best_transform_tally": tf_tally,
        "per_transform_yield": yields,
        "out_csv": str(args.out_csv),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
