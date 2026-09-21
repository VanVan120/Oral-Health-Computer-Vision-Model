"""Photometric duplicate tier (spec Phase 2.8) -- a sensitivity analysis.

The published rule compares raw grey levels, so a pair that differs only by a
global brightness or contrast change scores far above threshold and is missed.
Standardising each thumbnail (subtract its mean, divide by its standard
deviation) removes exactly those two degrees of freedom, and nothing else.

Candidates found that way are then verified at FULL resolution, also after
standardisation, against a null built from random test-train pairs. A tier that
does not separate from its null is reported and dropped rather than used.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image

from near_duplicates import TRANSFORMS, apply_transform, build_bank, list_images

SEED = 20260921
FULL = (256, 256)


def zscore(a: np.ndarray, axis=None) -> np.ndarray:
    mu = a.mean(axis=axis, keepdims=True)
    sd = a.std(axis=axis, keepdims=True)
    return (a - mu) / np.maximum(sd, 1e-6)


def min_z_rms(query: np.ndarray, ref: np.ndarray, chunk: int = 512):
    """Min RMS over the dihedral group, both sides standardised."""
    d = query.shape[1]
    side = int(round(d**0.5))
    refz = zscore(ref, axis=1)
    ref_sq = (refz**2).sum(axis=1)[None, :]
    best = np.full(query.shape[0], np.inf, dtype=np.float32)
    best_j = np.full(query.shape[0], -1, dtype=np.int64)
    best_t = np.full(query.shape[0], -1, dtype=np.int64)

    for ti, (_n, op) in enumerate(TRANSFORMS):
        q = query if op is None else np.stack(
            [apply_transform(r.reshape(side, side), op).ravel() for r in query])
        qz = zscore(q, axis=1)
        q_sq = (qz**2).sum(axis=1)[:, None]
        for s in range(0, query.shape[0], chunk):
            e = min(s + chunk, query.shape[0])
            d2 = q_sq[s:e] + ref_sq - 2.0 * (qz[s:e] @ refz.T)
            np.maximum(d2, 0.0, out=d2)
            rms = np.sqrt(d2 / d, dtype=np.float32)
            j = rms.argmin(axis=1)
            v = rms[np.arange(e - s), j]
            better = v < best[s:e]
            idx = np.nonzero(better)[0]
            if idx.size:
                best[s + idx] = v[idx]; best_j[s + idx] = j[idx]; best_t[s + idx] = ti
    return best, best_j, best_t


def full_res(path: Path) -> np.ndarray:
    with Image.open(path) as im:
        return np.asarray(im.convert("L").resize(FULL, Image.BILINEAR), dtype=np.float64)


# Numpy equivalents of the dihedral transforms, applied in float space so the
# standardised values are not round-tripped through uint8.
NP_TF = {
    "identity": lambda a: a,
    "hflip": lambda a: a[:, ::-1],
    "vflip": lambda a: a[::-1, :],
    "rot180": lambda a: a[::-1, ::-1],
    "rot90": lambda a: np.rot90(a, 1),
    "rot270": lambda a: np.rot90(a, 3),
    "transpose": lambda a: a.T,
    "transverse": lambda a: np.rot90(a, 2).T,
}


def verify(tp: Path, rp: Path, tname: str) -> dict[str, float]:
    """Full-resolution check after standardisation.

    For two standardised images, RMS^2 = 2(1 - r), so the RMS and the Pearson
    correlation carry the same information; both are reported because the RMS is
    what the thumbnail screen uses and r is what the decision uses.
    """
    a = zscore(NP_TF[tname](full_res(tp)))
    b = zscore(full_res(rp))
    return {"full_res_z_rms": float(np.sqrt(((a - b) ** 2).mean())),
            "pearson_r": float(np.corrcoef(a.ravel(), b.ravel())[0, 1])}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--test-dir", required=True, type=Path)
    ap.add_argument("--train-dir", required=True, type=Path)
    ap.add_argument("--d-csv", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--tier-csv", required=True, type=Path)
    ap.add_argument("--null-pairs", type=int, default=600)
    args = ap.parse_args()

    tps, rps = list_images(args.test_dir), list_images(args.train_dir)
    tb, rb = build_bank(tps), build_bank(rps)
    with args.d_csv.open(newline="") as fh:
        d_names = {r["test_image"] for r in csv.DictReader(fh)}

    best, bj, bt = min_z_rms(tb, rb)
    order = np.argsort(best)

    # Null: random test-train pairs, same standardised statistic.
    rng = np.random.default_rng(SEED)
    null = []
    for _ in range(args.null_pairs):
        i, j = int(rng.integers(len(tps))), int(rng.integers(len(rps)))
        a, b = zscore(tb[i]), zscore(rb[j])
        null.append(float(np.sqrt(((a - b) ** 2).mean())))
    null = np.array(null)
    # For standardised vectors RMS^2 = 2(1 - r), so the null median of ~1.41
    # is simply r = 0. The 0.5th percentile of the null sits near r = 0.80,
    # which is far too loose to call a photometric duplicate -- it admits
    # hundreds of merely similar clinical photographs. The screen is therefore
    # set at r >= 0.90 (RMS <= 0.447), and the decision is made by the
    # full-resolution check at r >= 0.95. The null is reported for calibration:
    # nothing random comes anywhere near either cut.
    null_cut = float(np.percentile(null, 0.5))
    cut = float(np.sqrt(2 * (1 - 0.90)))

    cand = [i for i in order if tps[i].name not in d_names and best[i] < cut]
    print(f"null: median {np.median(null):.3f} (r=0), 0.5th pct {null_cut:.3f}, min {null.min():.3f}")
    print(f"screen cut {cut:.3f} (r>=0.90)")
    print(f"{len(cand)} photometric-only candidates beyond D")

    rows, verified = [], 0
    for i in cand:
        tname = TRANSFORMS[bt[i]][0]
        v = verify(tps[i], rps[bj[i]], tname)
        ok = v["pearson_r"] >= 0.95
        verified += ok
        rows.append({"test_image": tps[i].name, "train_image": rps[bj[i]].name,
                     "matching_transform": tname, "thumb_z_rms": float(best[i]),
                     **v, "verified_full_res": "yes" if ok else "no"})

    args.tier_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.tier_csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else
                           ["test_image", "train_image", "matching_transform", "thumb_z_rms",
                            "full_res_z_rms", "pearson_r", "verified_full_res"])
        w.writeheader(); w.writerows(rows)

    out = {
        "method": "per-thumbnail standardisation (mean 0, sd 1) removes exactly a global "
                  "brightness and contrast change; minimum over the dihedral group as before",
        "null_pairs": args.null_pairs,
        "null_median": float(np.median(null)), "null_min": float(null.min()),
        "null_0.5th_percentile": null_cut,
        "screen_cut_used": cut,
        "screen_cut_meaning": "thumbnail standardised RMS <= sqrt(2(1-0.90)), i.e. r >= 0.90",
        "n_candidates_beyond_D": len(cand),
        "n_verified_full_resolution": verified,
        "verification_rule": "Pearson r >= 0.95 between standardised 256x256 greyscale images",
        "expected_by_spec": {"extra_pairs": 63, "tier_total": 322},
        "tier_total_if_used": len(d_names) + verified,
        "csv": str(args.tier_csv),
    }
    args.out.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
