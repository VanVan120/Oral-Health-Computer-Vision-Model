"""Per-class contrasts and validation contamination (spec Phases 2.5, 2.7).

These are estimation only: 95% CIs, no hypothesis tests. Intervals that exclude
zero among many secondary contrasts are not interpreted individually.

2.5  D versus ND for classes with at least 30 annotated instances in D:
     AP@0.5 and AP@0.5:0.95 (CIs come from the Phase 2.3 cluster bootstrap),
     plus instance recall and precision at two operating points -- t_global,
     the confidence at the peak of ultralytics' smoothed mean-F1 curve on the
     full split, and each class's deployed threshold.

2.7  Validation-split contamination: regenerate the valid-vs-train pairs, export
     them in S2's column format, and report M and fitness on the full validation
     split and on the split with those images removed.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

from cached_evaluator import Evaluator

SEED = 20260921

# Deployed per-class thresholds, keyed by class index via the display name.
DEPLOYED_BY_INDEX = {0: 0.25, 1: 0.35, 2: 0.30, 3: 0.60, 4: 0.40, 5: 0.75}


def t_global_from(ev: Evaluator, images: list[str]) -> float:
    from ultralytics.utils.metrics import DetMetrics, smooth

    m = DetMetrics(names=ev.names)
    for im in images:
        e = ev.cache[im]
        m.update_stats(e)   # whole entry: extra keys ignored, im_name present for 8.4.118
    m.process(save_dir=Path("."), plot=False, on_plot=None)
    px, f1, _, _ = m.box.curves_results[1]
    return float(np.asarray(px)[smooth(np.asarray(f1).mean(0), 0.1).argmax()])


def counts_at(ev: Evaluator, images: list[str], cls: int, thr: float) -> tuple[int, int, int]:
    """(TP at IoU 0.5, n predictions above thr, n ground-truth instances)."""
    tp = npred = ngt = 0
    for im in images:
        e = ev.cache[im]
        pc, cf, t = np.asarray(e["pred_cls"]), np.asarray(e["conf"]), np.asarray(e["tp"])
        sel = (pc == cls) & (cf >= thr)
        npred += int(sel.sum())
        if sel.any() and t.size:
            tp += int(np.asarray(t)[sel, 0].sum())
        ngt += int((np.asarray(e["target_cls"]) == cls).sum())
    return tp, npred, ngt


def rp(tp: int, npred: int, ngt: int) -> dict[str, float]:
    return {
        "recall": tp / ngt if ngt else float("nan"),
        "precision": tp / npred if npred else float("nan"),
        "tp": tp, "n_pred": npred, "n_gt": ngt,
    }


def boot_rp(ev, clusters, d_set, cls, thr, n, rng) -> dict[str, Any]:
    """Cluster-bootstrap CI for the D-minus-ND difference in recall/precision."""
    with_d = [c for c in clusters if any(m in d_set for m in c)]
    without_d = [c for c in clusters if not any(m in d_set for m in c)]
    dr, dp = [], []
    for _ in range(n):
        pick = [with_d[i] for i in rng.integers(0, len(with_d), len(with_d))]
        pick += [without_d[i] for i in rng.integers(0, len(without_d), len(without_d))]
        imgs = [m for c in pick for m in c]
        dd = [m for m in imgs if m in d_set]
        nn = [m for m in imgs if m not in d_set]
        if not dd or not nn:
            continue
        a, b = rp(*counts_at(ev, dd, cls, thr)), rp(*counts_at(ev, nn, cls, thr))
        if np.isfinite(a["recall"]) and np.isfinite(b["recall"]):
            dr.append(a["recall"] - b["recall"])
        if np.isfinite(a["precision"]) and np.isfinite(b["precision"]):
            dp.append(a["precision"] - b["precision"])
    f = lambda v: ({"mean": float(np.mean(v)), "ci_lo": float(np.percentile(v, 2.5)),
                    "ci_hi": float(np.percentile(v, 97.5))} if v else None)
    return {"delta_recall": f(dr), "delta_precision": f(dp)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--test-cache", required=True, type=Path)
    ap.add_argument("--valid-cache", required=True, type=Path)
    ap.add_argument("--d-csv", required=True, type=Path)
    ap.add_argument("--valid-dup-csv", required=True, type=Path)
    ap.add_argument("--clusters", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--boot", type=int, default=2000)
    args = ap.parse_args()

    ev = Evaluator.load(args.test_cache)
    all_images = ev.images()
    by_name = {Path(p).name: p for p in all_images}
    with args.d_csv.open(newline="") as fh:
        d_names = {r["test_image"] for r in csv.DictReader(fh)}
    d_images = sorted(by_name[n] for n in d_names)
    d_set = set(d_images)
    nd_images = sorted(set(all_images) - d_set)

    blob = json.loads(args.clusters.read_text())
    clusters = [[by_name[m] for m in c["members"]] for c in blob["clusters"]]

    tg = t_global_from(ev, all_images)
    print(f"t_global = {tg:.4f}")

    d_eval = ev.evaluate(d_images)
    nd_eval = ev.evaluate(nd_images)

    # Eligible classes: at least 30 annotated instances in D.
    eligible = [c for c, n in ev.names.items()
                if sum(int((np.asarray(ev.cache[i]["target_cls"]) == c).sum()) for i in d_images) >= 30]
    print("eligible classes:", [ev.names[c] for c in eligible])

    rng = np.random.default_rng(SEED)
    contrasts = {}
    for c in eligible:
        name = ev.names[c]
        row: dict[str, Any] = {
            "class_index": c,
            "instances_in_D": sum(int((np.asarray(ev.cache[i]["target_cls"]) == c).sum()) for i in d_images),
            "instances_in_ND": sum(int((np.asarray(ev.cache[i]["target_cls"]) == c).sum()) for i in nd_images),
            "AP50_D": d_eval["per_class"].get(name, {}).get("AP50"),
            "AP50_ND": nd_eval["per_class"].get(name, {}).get("AP50"),
            "AP50_95_D": d_eval["per_class"].get(name, {}).get("AP50_95"),
            "AP50_95_ND": nd_eval["per_class"].get(name, {}).get("AP50_95"),
        }
        for label, thr in (("t_global", tg), ("deployed", DEPLOYED_BY_INDEX[c])):
            dd, nn = rp(*counts_at(ev, d_images, c, thr)), rp(*counts_at(ev, nd_images, c, thr))
            bs = boot_rp(ev, clusters, d_set, c, thr, args.boot, rng)
            # Report the OBSERVED D-minus-ND difference as the point estimate. The
            # bootstrap supplies the interval only; its mean is a resampling
            # artefact and is kept solely for the bias it reveals (deviation D6).
            for q in ("recall", "precision"):
                if bs[f"delta_{q}"] is not None:
                    obs = dd[q] - nn[q]
                    bs[f"delta_{q}"]["observed"] = float(obs)
                    bs[f"delta_{q}"]["boot_mean_minus_observed"] = float(
                        bs[f"delta_{q}"]["mean"] - obs)
            row[label] = {"threshold": thr, "D": dd, "ND": nn, "bootstrap": bs}
        contrasts[name] = row
        print(f"  {name}: AP50 D {row['AP50_D']:.4f} vs ND {row['AP50_ND']:.4f}")

    # ---- 2.7 validation contamination
    vev = Evaluator.load(args.valid_cache)
    v_all = vev.images()
    v_by = {Path(p).name: p for p in v_all}
    with args.valid_dup_csv.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    v_dupe = {r["test_image"] for r in rows}
    v_aligned = {r["test_image"] for r in rows if r["also_found_by_aligned_only"] == "yes"}
    v_clean = sorted(set(v_all) - {v_by[n] for n in v_dupe if n in v_by})

    def fit(m):
        # ultralytics 8.3.231 DetMetrics.fitness uses w = [0, 0, 0, 1] over
        # [P, R, mAP50, mAP50-95], i.e. fitness IS mAP@0.5:0.95. Confirmed against
        # the installed source and against best.pt, whose stored fitness (0.38766)
        # equals its stored mAP50-95 exactly. The plan's 0.1/0.9 weighting is an
        # older ultralytics convention and does not apply here (deviation D7).
        return m["mAP50_95"]

    v_full_m, v_clean_m = vev.evaluate(v_all), vev.evaluate(v_clean)
    valid = {
        "n_validation_images": len(v_all),
        "n_duplicates_dihedral": len(v_dupe),
        "n_duplicates_identity_only": len(v_aligned),
        "expected_by_spec": {"aligned": 120, "dihedral": 256},
        "full": {k: v_full_m[k] for k in ("n_images", "n_instances", "P", "R", "mAP50", "mAP50_95")},
        "deduplicated": {k: v_clean_m[k] for k in ("n_images", "n_instances", "P", "R", "mAP50", "mAP50_95")},
        "fitness_definition": "ultralytics 8.3.231: fitness = mAP@0.5:0.95 "
                              "(DetMetrics.fitness weights [0,0,0,1])",
        "fitness_full": fit(v_full_m),
        "fitness_deduplicated": fit(v_clean_m),
        "delta_fitness": fit(v_clean_m) - fit(v_full_m),
        "delta_mAP50": v_clean_m["mAP50"] - v_full_m["mAP50"],
        "delta_mAP50_95": v_clean_m["mAP50_95"] - v_full_m["mAP50_95"],
    }
    print(f"validation: {len(v_dupe)} dihedral / {len(v_aligned)} aligned duplicates")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(
        {"t_global": tg, "deployed_thresholds_by_index": DEPLOYED_BY_INDEX,
         "eligible_classes": [ev.names[c] for c in eligible],
         "per_class_contrasts_D_vs_ND": contrasts,
         "validation_contamination": valid,
         "bootstrap_resamples_for_rp": args.boot}, indent=2, default=float) + "\n")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
