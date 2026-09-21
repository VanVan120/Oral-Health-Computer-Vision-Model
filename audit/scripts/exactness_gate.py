"""Phase 1.2 exactness gate, and Phase 1.3 batch sensitivity.

The cached evaluator is only usable if it reproduces a genuine val(batch=1) run.
This compares them on four image sets -- the full split, ND, and two seeded
random 1,241-image subsets -- across every metric the evaluator reports,
including per-class P, R, AP50 and AP50-95.

The gate is 1e-9. "Close enough" is not acceptable: every contamination
statistic downstream is a difference between two of these numbers, and the
effect being measured is itself of order 1e-3.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

from cached_evaluator import CachingValidator, Evaluator, _val_arg_dict, write_subset_yaml
from ultralytics import YOLO

SEED = 20260921
TOL = 1e-9


def flatten(m: dict) -> dict[str, float]:
    """Every reported number as one flat name -> value map."""
    out = {k: float(m[k]) for k in ("P", "R", "mAP50", "mAP50_95", "fitness")}
    out["n_images"] = float(m["n_images"])
    out["n_instances"] = float(m["n_instances"])
    for name, pc in m["per_class"].items():
        for k in ("P", "R", "AP50", "AP50_95", "instances"):
            out[f"{name}/{k}"] = float(pc[k])
    return out


def compare(a: dict, b: dict) -> tuple[float, str, dict]:
    fa, fb = flatten(a), flatten(b)
    keys = sorted(set(fa) | set(fb))
    worst, worst_key, diffs = 0.0, "", {}
    for k in keys:
        if k not in fa or k not in fb:
            diffs[k] = "MISSING"
            worst, worst_key = float("inf"), k
            continue
        d = abs(fa[k] - fb[k])
        diffs[k] = d
        if d > worst:
            worst, worst_key = d, k
    return worst, worst_key, diffs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cache", required=True, type=Path)
    ap.add_argument("--weights", required=True)
    ap.add_argument("--data", required=True, type=Path)
    ap.add_argument("--d-csv", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    ev = Evaluator.load(args.cache)
    all_images = ev.images()
    by_name = {Path(p).name: p for p in all_images}

    with args.d_csv.open(newline="") as fh:
        d_names = {r["test_image"] for r in csv.DictReader(fh)}
    d_images = sorted(by_name[n] for n in d_names if n in by_name)
    nd_images = sorted(set(all_images) - set(d_images))
    assert len(d_images) == 259, len(d_images)
    assert len(nd_images) == 1241, len(nd_images)

    rng = random.Random(SEED)
    ctrl1 = sorted(rng.sample(all_images, 1241))
    ctrl2 = sorted(rng.sample(all_images, 1241))

    sets = {
        "full": all_images,
        "ND": nd_images,
        "ctrl1": ctrl1,
        "ctrl2": ctrl2,
    }

    results = {}
    passed = True
    for tag, imgs in sets.items():
        print(f"\n=== {tag}: {len(imgs)} images ===")
        yml = write_subset_yaml(imgs, args.data, args.work, tag)

        # Run the real val() through a CachingValidator so the SAME pass yields
        # both the reference metrics and the order its dataloader used.
        v = CachingValidator(args=_val_arg_dict(args.weights, str(yml), "test", 1))
        v(model=YOLO(args.weights).model)
        m = v.metrics
        mp, mr, map50, map5095 = m.mean_results()
        per_class = {}
        for i, c in enumerate(m.ap_class_index):
            pp, rr, a50, a95 = m.class_result(i)
            per_class[v.names[int(c)]] = {
                "class_index": int(c), "instances": int(m.nt_per_class[int(c)]),
                "images": int(m.nt_per_image[int(c)]), "P": float(pp), "R": float(rr),
                "AP50": float(a50), "AP50_95": float(a95)}
        actual = {"n_images": int(v.seen), "n_instances": int(m.nt_per_class.sum()),
                  "P": float(mp), "R": float(mr), "mAP50": float(map50),
                  "mAP50_95": float(map5095), "fitness": float(m.fitness),
                  "per_class": per_class}

        # rect=True sorts the dataloader by aspect ratio, and this split has 338
        # distinct image sizes, so dataloader order != filename order. Feeding
        # the cached entries in filename order changes only the ORDER of the
        # float32 cumulative sums inside ap_per_class, which moves AP in the
        # last couple of digits. Replaying in the validator's own order removes
        # that difference entirely; both are reported.
        order = list(v.cache.keys())
        assert sorted(order) == sorted(imgs), "subset run visited a different image set"
        cached = ev.evaluate(order)
        cached_sorted = ev.evaluate(sorted(imgs))

        worst, worst_key, diffs = compare(cached, actual)
        worst_s, worst_key_s, _ = compare(cached_sorted, actual)
        print(f"  [filename-order replay] max |diff| = {worst_s:.3e} on {worst_key_s!r}")
        ok = worst <= TOL
        passed &= ok
        print(f"  cached : P {cached['P']:.10f} R {cached['R']:.10f} mAP50 {cached['mAP50']:.10f} mAP50-95 {cached['mAP50_95']:.10f}")
        print(f"  val()  : P {actual['P']:.10f} R {actual['R']:.10f} mAP50 {actual['mAP50']:.10f} mAP50-95 {actual['mAP50_95']:.10f}")
        print(f"  max |diff| = {worst:.3e} on {worst_key!r}  -> {'PASS' if ok else 'FAIL'}")
        results[tag] = {
            "n_images": len(imgs),
            "max_abs_diff": worst,
            "max_abs_diff_filename_order_replay": worst_s,
            "worst_key_filename_order_replay": worst_key_s,
            "worst_key": worst_key,
            "pass": ok,
            "cached": cached,
            "val": actual,
            "per_key_diffs": {k: (v if isinstance(v, str) else float(v)) for k, v in diffs.items()},
        }

    out = {"tolerance": TOL, "seed": SEED, "all_pass": passed, "sets": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nGATE {'PASSED' if passed else 'FAILED'}  -> {args.out}")


if __name__ == "__main__":
    main()
