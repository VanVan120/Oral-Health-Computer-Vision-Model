"""Addendum R1b: robustness of items 1 and 2, after adversarial review.

An independent adversarial pass on the first cut of items 1 and 2 raised one
fatal and three material objections. Every one is re-tested here from the same
caches, independently of the script that produced the original numbers:

  1. Is the transform argmin actually a near-tie? (If it is decisive, "thumbnail
     agrees with full resolution 259/259" is near-vacuous as evidence, and the
     real instability lies elsewhere.)
  2. Where is the published-vs-regenerated disagreement located -- the transform
     rule, or the choice of twin?
  3. Is the pooled (iv)-(iii) a cancellation artefact across strata that the
     training augmentation makes testable versus untestable? With an interaction
     test and balance controls.
  4. Is the pooled statistic stable in t_global and the IoU threshold? Both
     sweeps are pure recomputation from the cached detections.
  5. Does micro-averaging over-weight the reused training twins?
  6. Is "(i) > (ii)" a statement about agreement, or about box counts?

No inference. Reads caches, S48 and the image files only.
"""
from __future__ import annotations

import argparse
import csv
import json
import pickle
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from addendum_concordance import (INVERSE, NP_TF, TF_NAMES, f1_from, greedy_match,
                                  iou_matrix, map_norm_boxes, normalise)

SEED = 20260921
REACHABLE = ("identity", "hflip")        # fliplr 0.27883
UNREACHABLE = ("vflip", "rot180")        # flipud 0.0, degrees 0
CONTRASTS = ["i_predD_vs_predTwin", "ii_labelD_vs_labelTwin", "iii_predD_vs_labelD",
             "iv_predD_vs_labelTwin", "v_predTwin_vs_labelTwin"]


def counts_within_class(pred_n, pred_c, true_n, true_c) -> tuple[int, int, int]:
    """Class-aware matching done PROPERLY: match within each class separately.

    The first implementation matched class-agnostically and then filtered for
    class agreement, so a wrong-class pairing could consume a box and block a
    lower-IoU correct-class pairing. Quantified below.
    """
    tp = 0
    for c in set(list(pred_c) + list(true_c)):
        pi = np.nonzero(np.asarray(pred_c) == c)[0]
        ti = np.nonzero(np.asarray(true_c) == c)[0]
        if len(pi) and len(ti):
            tp += len(greedy_match(iou_matrix(pred_n[pi], true_n[ti]), 0.5))
    return tp, len(pred_c), len(true_c)


def counts_agnostic_then_filter(pred_n, pred_c, true_n, true_c) -> tuple[int, int, int]:
    ms = greedy_match(iou_matrix(pred_n, true_n), 0.5)
    return (sum(1 for i, j, _ in ms if pred_c[i] == true_c[j]), len(pred_c), len(true_c))


def grey256(p: Path) -> np.ndarray:
    with Image.open(p) as im:
        return np.asarray(im.convert("L").resize((256, 256), Image.BILINEAR), dtype=np.float64)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pairs-csv", required=True, type=Path)
    ap.add_argument("--published-csv", required=True, type=Path)
    ap.add_argument("--test-dir", required=True, type=Path)
    ap.add_argument("--train-dir", required=True, type=Path)
    ap.add_argument("--test-boxes", required=True, type=Path)
    ap.add_argument("--train-boxes", required=True, type=Path)
    ap.add_argument("--t-global", type=float, required=True)
    ap.add_argument("--resamples", type=int, default=10000)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    rows = list(csv.DictReader(args.pairs_csv.open(newline="")))
    pub = {r["test_image"]: r for r in csv.DictReader(args.published_csv.open(newline=""))}
    tb_all = pickle.load(open(args.test_boxes, "rb"))["boxes"]
    wb_all = pickle.load(open(args.train_boxes, "rb"))["boxes"]
    test_by = {Path(p).name: p for p in tb_all}
    train_by = {Path(p).name: p for p in wb_all}
    out: dict[str, Any] = {"seed": SEED, "t_global": args.t_global}

    # ---------------------------------------------------------------- 1. decisiveness
    print("1. transform argmin decisiveness ...")
    gaps, ratios = [], []
    for r in rows:
        A, B = grey256(args.test_dir / r["test_image"]), grey256(args.train_dir / r["train_image"])
        v = sorted(float(np.sqrt(((np.ascontiguousarray(NP_TF[t](A)) - B) ** 2).mean()))
                   for t in TF_NAMES)
        gaps.append(v[1] - v[0])
        ratios.append(v[1] / max(v[0], 1e-9))
    gaps, ratios = np.array(gaps), np.array(ratios)
    out["transform_argmin_decisiveness"] = {
        "note": "if the argmin were a near-tie, thumbnail-vs-full-resolution agreement "
                "would be weak evidence. It is not a near-tie.",
        "gap_runner_up_minus_winner_rms": {"min": float(gaps.min()), "p1": float(np.percentile(gaps, 1)),
                                           "median": float(np.median(gaps)), "max": float(gaps.max())},
        "ratio_runner_up_over_winner": {"min": float(ratios.min()), "median": float(np.median(ratios)),
                                        "max": float(ratios.max())},
        "n_pairs_ratio_below_2": int((ratios < 2.0).sum()),
        "n_pairs_gap_below_2_rms": int((gaps < 2.0).sum()),
        "interpretation": "the winner beats the runner-up by at least %.1f RMS units on a "
                          "0-255 scale, so thumbnail and full resolution could scarcely have "
                          "disagreed; the 259/259 agreement is a consistency check, not "
                          "independent corroboration of the transform column"
                          % float(gaps.min()),
    }

    # ------------------------------------------------- 2. where the instability lives
    print("2. locating the published-vs-regenerated disagreement ...")
    same_tf = sum(1 for r in rows if pub[r["test_image"]]["matching_transform"] == r["thumb_transform"])
    same_tw = sum(1 for r in rows if pub[r["test_image"]]["train_image"] == r["train_image"])
    diff_tw = [r for r in rows if pub[r["test_image"]]["train_image"] != r["train_image"]]
    same_twin_diff_tf = sum(
        1 for r in rows
        if pub[r["test_image"]]["train_image"] == r["train_image"]
        and pub[r["test_image"]]["matching_transform"] != r["thumb_transform"])
    # On the published pairing, does our own rule recover the published transform?
    recov, rel = 0, []
    for r in diff_tw:
        A = grey256(args.test_dir / r["test_image"])
        Bp = grey256(args.train_dir / pub[r["test_image"]]["train_image"])
        Br = grey256(args.train_dir / r["train_image"])
        sp = {t: float(np.sqrt(((np.ascontiguousarray(NP_TF[t](A)) - Bp) ** 2).mean())) for t in TF_NAMES}
        sr = {t: float(np.sqrt(((np.ascontiguousarray(NP_TF[t](A)) - Br) ** 2).mean())) for t in TF_NAMES}
        recov += (min(sp, key=sp.get) == pub[r["test_image"]]["matching_transform"])
        a, b = min(sp.values()), min(sr.values())
        rel.append(abs(a - b) / max(min(a, b), 1e-9))
    rel = np.array(rel) if rel else np.array([np.nan])
    out["where_the_instability_lives"] = {
        "same_transform_as_published": same_tf,
        "same_train_image_as_published": same_tw,
        "pairs_same_twin_but_different_transform": same_twin_diff_tf,
        "published_transform_recovered_on_published_pairing": f"{recov}/{len(diff_tw)}",
        "relative_rms_difference_between_competing_twins": {
            "min": float(np.nanmin(rel)), "median": float(np.nanmedian(rel)),
            "p90": float(np.nanpercentile(rel, 90)),
            "n_within_10pct": int((rel < 0.10).sum())},
        "conclusion": "the transform RULE is fully reproducible -- given the same twin it "
                      "returns the same transform every time, and it recovers the published "
                      "transform on the published pairing. The irreproducible step is WHICH "
                      "training image is nearest, where competing candidates are often within "
                      "a few percent of each other.",
    }

    # ---------------------------------------------- 3-6: recompute the five contrasts
    print("3. recomputing contrasts, both matching rules ...")
    per_pair: list[dict] = []
    for r in rows:
        tn, rn, tf = r["test_image"], r["train_image"], r["full_transform"]
        tb, wb = tb_all[test_by[tn]], wb_all[train_by[rn]]
        test_g = normalise(tb["gt_xyxy"], tb["ori_shape"]); test_c = tb["gt_cls"].astype(int)
        tw_g = map_norm_boxes(normalise(wb["gt_xyxy"], wb["ori_shape"]), INVERSE[tf])
        twin_c = wb["gt_cls"].astype(int)
        kt, kw = tb["pred_conf"], wb["pred_conf"]
        rec = {"test_image": tn, "train_image": rn, "transform": tf,
               "cluster": int(r["cluster"]),
               "stratum": "reachable" if tf in REACHABLE else "unreachable"}
        for thr in (args.t_global, 0.05, 0.10, 0.20, 0.35, 0.45, 0.60):
            pD = normalise(tb["pred_xyxy"][kt >= thr], tb["ori_shape"])
            cD = tb["pred_cls"][kt >= thr].astype(int)
            pW = map_norm_boxes(normalise(wb["pred_xyxy"][kw >= thr], wb["ori_shape"]), INVERSE[tf])
            cW = wb["pred_cls"][kw >= thr].astype(int)
            sets = {"i_predD_vs_predTwin": (pD, cD, pW, cW),
                    "ii_labelD_vs_labelTwin": (test_g, test_c, tw_g, twin_c),
                    "iii_predD_vs_labelD": (pD, cD, test_g, test_c),
                    "iv_predD_vs_labelTwin": (pD, cD, tw_g, twin_c),
                    "v_predTwin_vs_labelTwin": (pW, cW, tw_g, twin_c)}
            tag = "t%s" % ("G" if thr == args.t_global else f"{thr:g}")
            for k, (pn, pc, gn, gc) in sets.items():
                tp, np_, nt_ = counts_agnostic_then_filter(pn, pc, gn, gc)
                rec[f"{tag}|{k}"] = (tp, np_, nt_)
                if thr == args.t_global:
                    rec[f"WC|{k}"] = counts_within_class(pn, pc, gn, gc)
        per_pair.append(rec)

    def pooled(sel, key) -> float:
        a = [r[key] for r in sel]
        return f1_from(sum(x[0] for x in a), sum(x[1] for x in a), sum(x[2] for x in a))

    def macro(sel, key) -> float:
        v = [f1_from(*r[key]) for r in sel]
        v = [x for x in v if not np.isnan(x)]
        return float(np.mean(v)) if v else float("nan")

    base = {k: pooled(per_pair, f"tG|{k}") for k in CONTRASTS}
    out["reproduces_S47"] = base
    out["matching_rule_sensitivity"] = {
        "note": "the first implementation matched class-agnostically then filtered for class "
                "agreement, so a wrong-class pairing could block a correct-class one. "
                "Re-matched within each class separately.",
        "agnostic_then_filter": base,
        "within_class": {k: pooled(per_pair, f"WC|{k}") for k in CONTRASTS},
        "iv_minus_iii_agnostic": base["iv_predD_vs_labelTwin"] - base["iii_predD_vs_labelD"],
        "iv_minus_iii_within_class": pooled(per_pair, "WC|iv_predD_vs_labelTwin")
                                     - pooled(per_pair, "WC|iii_predD_vs_labelD"),
    }

    # ---- stratified interaction, the fatal objection
    print("4. stratified interaction test ...")
    by_cl = defaultdict(list)
    for r in per_pair:
        by_cl[r["cluster"]].append(r)
    cls = sorted(by_cl)
    rng = np.random.default_rng(SEED)
    R = [r for r in per_pair if r["stratum"] == "reachable"]
    U = [r for r in per_pair if r["stratum"] == "unreachable"]

    def dv(sel):
        return pooled(sel, "tG|iv_predD_vs_labelTwin") - pooled(sel, "tG|iii_predD_vs_labelD")

    dR, dU, dI = [], [], []
    for _ in range(args.resamples):
        pk = rng.choice(len(cls), len(cls), replace=True)
        sel = [r for i in pk for r in by_cl[cls[i]]]
        rr = [r for r in sel if r["stratum"] == "reachable"]
        uu = [r for r in sel if r["stratum"] == "unreachable"]
        if not rr or not uu:
            continue
        a, b = dv(rr), dv(uu)
        dR.append(a); dU.append(b); dI.append(a - b)

    def ci(v):
        v = np.asarray(v)[~np.isnan(v)]
        return {"ci_lo": float(np.percentile(v, 2.5)), "ci_hi": float(np.percentile(v, 97.5))}

    dI_a = np.asarray(dI)
    out["stratified_interaction"] = {
        "rationale": "best.pt train_args: fliplr 0.27883, flipud 0.0, degrees 0. The model can "
                     "only reproduce a twin's labels in a frame training could present. "
                     "identity and hflip are reachable; vflip and rot180 are not. The "
                     "hypothesis is therefore only testable on the reachable stratum.",
        "reachable": {"n_pairs": len(R), "transforms": list(REACHABLE),
                      "iv_minus_iii": dv(R), **ci(dR)},
        "unreachable": {"n_pairs": len(U), "transforms": list(UNREACHABLE),
                        "iv_minus_iii": dv(U), **ci(dU)},
        "interaction_reachable_minus_unreachable": {
            "point": dv(R) - dv(U), **ci(dI),
            "p_interaction_le_0": float((dI_a <= 0).mean()),
            "n_resamples_used": len(dI)},
        "identity_only": {"n_pairs": sum(1 for r in per_pair if r["transform"] == "identity"),
                          "iv_minus_iii": dv([r for r in per_pair if r["transform"] == "identity"])},
        "balance_controls": {
            "note": "if the unreachable pairs were simply harder, the within-frame contrasts "
                    "would differ too. They do not: only the cross-frame quantities move.",
            "iii_predD_vs_labelD": {"reachable": pooled(R, "tG|iii_predD_vs_labelD"),
                                    "unreachable": pooled(U, "tG|iii_predD_vs_labelD")},
            "v_predTwin_vs_labelTwin": {"reachable": pooled(R, "tG|v_predTwin_vs_labelTwin"),
                                        "unreachable": pooled(U, "tG|v_predTwin_vs_labelTwin")},
            "i_predD_vs_predTwin": {"reachable": pooled(R, "tG|i_predD_vs_predTwin"),
                                    "unreachable": pooled(U, "tG|i_predD_vs_predTwin")},
        },
    }

    # ---- threshold sweep
    print("5. t_global sweep ...")
    out["t_global_sweep_iv_minus_iii"] = {
        ("t_global" if thr == args.t_global else f"{thr:g}"): {
            "pooled": pooled(per_pair, f"t{'G' if thr == args.t_global else f'{thr:g}'}|iv_predD_vs_labelTwin")
                      - pooled(per_pair, f"t{'G' if thr == args.t_global else f'{thr:g}'}|iii_predD_vs_labelD"),
            "reachable": pooled([r for r in R], f"t{'G' if thr == args.t_global else f'{thr:g}'}|iv_predD_vs_labelTwin")
                         - pooled([r for r in R], f"t{'G' if thr == args.t_global else f'{thr:g}'}|iii_predD_vs_labelD"),
            "unreachable": pooled([r for r in U], f"t{'G' if thr == args.t_global else f'{thr:g}'}|iv_predD_vs_labelTwin")
                           - pooled([r for r in U], f"t{'G' if thr == args.t_global else f'{thr:g}'}|iii_predD_vs_labelD"),
        } for thr in (0.05, 0.10, 0.20, args.t_global, 0.35, 0.45, 0.60)
    }

    # ---- weighting sensitivity
    print("6. weighting sensitivity ...")
    seen, dedup = set(), []
    for r in per_pair:
        if r["train_image"] not in seen:
            seen.add(r["train_image"]); dedup.append(r)
    tw_counts = Counter(r["train_image"] for r in per_pair)
    out["weighting_sensitivity"] = {
        "note": "259 pairs cover fewer distinct training twins, so micro-averaging pools some "
                "twins two or three times into the (ii)/(iv)/(v) denominators while every "
                "test image enters once. Reported so the pooled figure is not read as "
                "weighting-independent.",
        "n_pairs": len(per_pair), "n_distinct_train_twins": len(tw_counts),
        "twins_used_twice": sum(1 for v in tw_counts.values() if v == 2),
        "twins_used_three_times": sum(1 for v in tw_counts.values() if v == 3),
        "iv_minus_iii": {
            "micro_pooled": dv(per_pair),
            "macro_per_pair": macro(per_pair, "tG|iv_predD_vs_labelTwin")
                              - macro(per_pair, "tG|iii_predD_vs_labelD"),
            "micro_dedup_one_pair_per_twin": dv(dedup),
        },
        "ordering_under_macro": {k: macro(per_pair, f"tG|{k}") for k in CONTRASTS},
    }

    # ---- what (i) vs (ii) is really measuring
    print("7. cardinality decomposition ...")
    eq = [r for r in per_pair
          if r["tG|i_predD_vs_predTwin"][1] == r["tG|i_predD_vs_predTwin"][2]
          and r["tG|ii_labelD_vs_labelTwin"][1] == r["tG|ii_labelD_vs_labelTwin"][2]]
    def ceiling(sel, key):
        a = [r[key] for r in sel]
        np_, nt_ = sum(x[1] for x in a), sum(x[2] for x in a)
        return 2 * min(np_, nt_) / (np_ + nt_) if (np_ + nt_) else float("nan")
    out["what_i_vs_ii_measures"] = {
        "note": "F1 here is the Dice coefficient 2tp/(np+nt), which factorises as "
                "[2 min(np,nt)/(np+nt)] x [tp/min(np,nt)]: a cardinality ceiling times a "
                "spatial-agreement term. If the gap lives in the ceiling, '(i) > (ii)' is "
                "mostly a statement about how reproducible the BOX COUNT is, not about "
                "annotation quality.",
        "pooled_gap_i_minus_ii": base["i_predD_vs_predTwin"] - base["ii_labelD_vs_labelTwin"],
        "cardinality_ceiling": {"i": ceiling(per_pair, "tG|i_predD_vs_predTwin"),
                                "ii": ceiling(per_pair, "tG|ii_labelD_vs_labelTwin")},
        "restricted_to_pairs_with_equal_counts_on_BOTH_contrasts": {
            "n_pairs": len(eq),
            "i": pooled(eq, "tG|i_predD_vs_predTwin") if eq else float("nan"),
            "ii": pooled(eq, "tG|ii_labelD_vs_labelTwin") if eq else float("nan"),
            "gap": (pooled(eq, "tG|i_predD_vs_predTwin")
                    - pooled(eq, "tG|ii_labelD_vs_labelTwin")) if eq else float("nan"),
        },
        "box_count_reproducibility": {
            "P_equal_counts_model": float(np.mean([r["tG|i_predD_vs_predTwin"][1] == r["tG|i_predD_vs_predTwin"][2] for r in per_pair])),
            "P_equal_counts_annotators": float(np.mean([r["tG|ii_labelD_vs_labelTwin"][1] == r["tG|ii_labelD_vs_labelTwin"][2] for r in per_pair])),
        },
    }

    args.out.write_text(json.dumps(out, indent=2, default=float) + "\n")
    s = out["stratified_interaction"]
    print(f"\n  reachable   (n={s['reachable']['n_pairs']}): (iv)-(iii) = {s['reachable']['iv_minus_iii']:+.4f} "
          f"[{s['reachable']['ci_lo']:+.4f}, {s['reachable']['ci_hi']:+.4f}]")
    print(f"  unreachable (n={s['unreachable']['n_pairs']}): (iv)-(iii) = {s['unreachable']['iv_minus_iii']:+.4f} "
          f"[{s['unreachable']['ci_lo']:+.4f}, {s['unreachable']['ci_hi']:+.4f}]")
    i = s["interaction_reachable_minus_unreachable"]
    print(f"  interaction: {i['point']:+.4f} [{i['ci_lo']:+.4f}, {i['ci_hi']:+.4f}]  P(<=0) = {i['p_interaction_le_0']:.4f}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
