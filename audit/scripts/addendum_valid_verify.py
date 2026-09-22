"""Addendum R1b item 8: verify the validation duplicate pairs at full resolution.

S7 reports 256 validation-training pairs found by the published 32x32 rule. That
rule is a screen. This re-checks every pair at full resolution against the same
random-pair null construction used for the test-side photometric analysis (S40):
600 random pairs, per-image standardisation, minimum over the dihedral group.

The same procedure is run on the 259 test pairs so the validation pass rate has a
reference point measured the same way.

Reads images and existing CSVs only. No inference.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from addendum_concordance import NP_TF, TF_NAMES

SEED = 20260921
FULL = (256, 256)
VERIFY_R = 0.95          # the S40 full-resolution decision rule


def zscore(a: np.ndarray) -> np.ndarray:
    return (a - a.mean()) / max(a.std(), 1e-6)


def grey_full(path: Path) -> np.ndarray:
    with Image.open(path) as im:
        return np.asarray(im.convert("L").resize(FULL, Image.BILINEAR), dtype=np.float64)


def best_pair(a: np.ndarray, b: np.ndarray) -> tuple[str, float, float]:
    """Best dihedral transform at full resolution, standardised.

    Returns (transform, standardised RMS, Pearson r). For standardised vectors
    RMS^2 = 2(1 - r), so the two are the same information; both are reported
    because S40's screen used the RMS and its decision used r.
    """
    bz = zscore(b)
    best = (None, np.inf, -1.0)
    for t in TF_NAMES:
        az = zscore(np.ascontiguousarray(NP_TF[t](a)))
        rms = float(np.sqrt(((az - bz) ** 2).mean()))
        if rms < best[1]:
            r = float(np.corrcoef(az.ravel(), bz.ravel())[0, 1])
            best = (t, rms, r)
    return best


def build_null(q_paths, r_paths, n, rng) -> np.ndarray:
    out = []
    for _ in range(n):
        a = grey_full(q_paths[int(rng.integers(len(q_paths)))])
        b = grey_full(r_paths[int(rng.integers(len(r_paths)))])
        out.append(best_pair(a, b)[1])
    return np.array(out)


EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def listimgs(d: Path) -> list[Path]:
    return sorted(p for p in d.rglob("*") if p.suffix.lower() in EXTS)


def analyse(tag: str, pairs: list[dict], q_dir: Path, r_dir: Path,
            null_n: int, rng) -> dict[str, Any]:
    qs, rs = listimgs(q_dir), listimgs(r_dir)
    print(f"{tag}: {len(pairs)} pairs; null from {len(qs)}x{len(rs)} images")
    null = build_null(qs, rs, null_n, rng)
    null_med = float(np.median(null))
    null_min = float(null.min())
    null_p05 = float(np.percentile(null, 0.5))

    rows = []
    for p in pairs:
        qn = p.get("test_image") or p.get("valid_image")
        rn = p["train_image"]
        a, b = grey_full(q_dir / qn), grey_full(r_dir / rn)
        t, rms, r = best_pair(a, b)
        rows.append({"query_image": qn, "train_image": rn,
                     "thumb_transform": p.get("matching_transform", ""),
                     "fullres_transform": t, "fullres_z_rms": rms, "pearson_r": r,
                     "passes_r95": int(r >= VERIFY_R),
                     "below_null_min": int(rms < null_min)})
    rr = np.array([x["pearson_r"] for x in rows])
    n_pass = int(sum(x["passes_r95"] for x in rows))
    res = {
        "n_pairs": len(rows),
        "null": {"n": null_n, "median_z_rms": null_med, "min_z_rms": null_min,
                 "pct0.5_z_rms": null_p05,
                 "median_as_r": float(1 - null_med ** 2 / 2),
                 "min_as_r": float(1 - null_min ** 2 / 2)},
        "verified_full_resolution_r>=0.95": n_pass,
        "verified_proportion": n_pass / len(rows) if rows else float("nan"),
        "below_null_minimum": int(sum(x["below_null_min"] for x in rows)),
        "pearson_r": {"min": float(rr.min()), "p05": float(np.percentile(rr, 5)),
                      "median": float(np.median(rr)), "max": float(rr.max())},
        "transform_agreement_thumb_vs_fullres": int(sum(
            1 for x in rows if x["thumb_transform"] and x["thumb_transform"] == x["fullres_transform"])),
    }
    print(f"   verified at r>=0.95: {n_pass}/{len(rows)} = {res['verified_proportion']:.4f}")
    print(f"   null median {null_med:.4f} (r={res['null']['median_as_r']:.3f}), "
          f"min {null_min:.4f} (r={res['null']['min_as_r']:.3f})")
    print(f"   all {len(rows)} below null minimum: {res['below_null_minimum']}")
    return res, rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--valid-csv", required=True, type=Path)
    ap.add_argument("--test-csv", required=True, type=Path)
    ap.add_argument("--valid-dir", required=True, type=Path)
    ap.add_argument("--test-dir", required=True, type=Path)
    ap.add_argument("--train-dir", required=True, type=Path)
    ap.add_argument("--null-pairs", type=int, default=600)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--csv-out", required=True, type=Path)
    args = ap.parse_args()

    rng = np.random.default_rng(SEED)
    v_pairs = list(csv.DictReader(args.valid_csv.open(newline="")))
    t_pairs = list(csv.DictReader(args.test_csv.open(newline="")))

    v_res, v_rows = analyse("validation", v_pairs, args.valid_dir, args.train_dir,
                            args.null_pairs, rng)
    t_res, t_rows = analyse("test (reference)", t_pairs, args.test_dir, args.train_dir,
                            args.null_pairs, rng)

    args.csv_out.parent.mkdir(parents=True, exist_ok=True)
    with args.csv_out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["split"] + list(v_rows[0]))
        w.writeheader()
        for r in v_rows:
            w.writerow({"split": "valid", **r})
        for r in t_rows:
            w.writerow({"split": "test", **r})

    args.out.write_text(json.dumps({
        "method": "full resolution 256x256 greyscale, each image standardised to mean 0 "
                  "sd 1, minimum over the dihedral group; null = 600 random query-train "
                  "pairs scored identically. Decision rule r >= 0.95, the same rule S40 "
                  "used to verify photometric candidates.",
        "seed": SEED, "verify_rule_r": VERIFY_R,
        "validation": v_res, "test_reference": t_res,
        "csv": str(args.csv_out),
    }, indent=2, default=float) + "\n")
    print(f"\nwrote {args.out} and {args.csv_out}")


if __name__ == "__main__":
    main()
