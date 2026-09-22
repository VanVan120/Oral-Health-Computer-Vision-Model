"""Addendum R1b, items 1-3: full-resolution transforms, and what they change.

The published duplicate rule picks the best dihedral transform on 32x32
thumbnails. That is a screen, not a registration: at 32x32 a reflection and a
rotation of a roughly symmetric clinical photograph can score almost the same.
Item 1 re-determines the transform at 256x256 and asks whether the box-level
concordance of 2.6(b) was measuring annotation disagreement or a misregistered
frame.

Conventions are inherited from memorisation.py so the numbers stay comparable:
rows of the IoU matrix are the TWIN (treated as the "prediction"), columns are
the TEST image (treated as truth), so precision = tp / n_twin and
recall = tp / n_test. A pair has "identical label sets" when every box matches
one-to-one and every matched class agrees.

Everything runs off the existing caches. No inference is performed.
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

SEED = 20260921
FULL = (256, 256)
# The four transforms the published rule can produce that preserve the axes.
AXIS_SAFE = ("identity", "hflip", "vflip", "rot180")

# Array ops, on a[row, col] = a[y, x].
NP_TF = {
    "identity":   lambda a: a,
    "hflip":      lambda a: a[:, ::-1],
    "vflip":      lambda a: a[::-1, :],
    "rot180":     lambda a: a[::-1, ::-1],
    "rot90":      lambda a: np.rot90(a, 1),
    "rot270":     lambda a: np.rot90(a, 3),
    "transpose":  lambda a: a.T,
    "transverse": lambda a: np.rot90(a, 2).T,
}
TF_NAMES = tuple(NP_TF)

# Point maps on the unit square, matching the array ops above: if
# B = NP_TF[t](A) then a feature at normalised (u, v) in A sits at
# PT_TF[t](u, v) in B. Derived by hand and asserted against the array ops in
# _self_test().
PT_TF = {
    "identity":   lambda u, v: (u, v),
    "hflip":      lambda u, v: (1.0 - u, v),
    "vflip":      lambda u, v: (u, 1.0 - v),
    "rot180":     lambda u, v: (1.0 - u, 1.0 - v),
    "rot90":      lambda u, v: (v, 1.0 - u),
    "rot270":     lambda u, v: (1.0 - v, u),
    "transpose":  lambda u, v: (v, u),
    "transverse": lambda u, v: (1.0 - v, 1.0 - u),
}
INVERSE = {"identity": "identity", "hflip": "hflip", "vflip": "vflip",
           "rot180": "rot180", "transpose": "transpose", "transverse": "transverse",
           "rot90": "rot270", "rot270": "rot90"}


def _self_test() -> None:
    """Assert PT_TF agrees with NP_TF, and that INVERSE really inverts."""
    rng = np.random.default_rng(0)
    a = rng.integers(0, 255, size=(17, 29)).astype(np.float64)   # deliberately non-square
    h, w = a.shape
    for t in TF_NAMES:
        b = np.ascontiguousarray(NP_TF[t](a))
        hb, wb = b.shape
        for r in (0, 3, h - 1):
            for c in (0, 5, w - 1):
                u, v = (c + 0.5) / w, (r + 0.5) / h
                u2, v2 = PT_TF[t](u, v)
                r2, c2 = int(v2 * hb), int(u2 * wb)
                assert b[r2, c2] == a[r, c], f"PT_TF[{t}] disagrees with NP_TF[{t}]"
        # inverse
        for u in (0.1, 0.5, 0.9):
            for v in (0.2, 0.7):
                u2, v2 = PT_TF[t](u, v)
                u3, v3 = PT_TF[INVERSE[t]](u2, v2)
                assert abs(u3 - u) < 1e-12 and abs(v3 - v) < 1e-12, f"INVERSE[{t}] wrong"
    # Distinctness guard: PIL's FLIP_LEFT_RIGHT == 0 bug class.
    assert len(set(TF_NAMES)) == 8


def map_norm_boxes(boxes_n: np.ndarray, transform: str) -> np.ndarray:
    """Map normalised xyxy boxes through a dihedral transform on the unit square."""
    if boxes_n.size == 0:
        return boxes_n
    f = PT_TF[transform]
    x1, y1, x2, y2 = boxes_n[:, 0], boxes_n[:, 1], boxes_n[:, 2], boxes_n[:, 3]
    xs, ys = [], []
    for cx, cy in ((x1, y1), (x2, y1), (x1, y2), (x2, y2)):
        ux, uy = f(cx, cy)
        xs.append(ux); ys.append(uy)
    xs, ys = np.stack(xs), np.stack(ys)
    return np.stack([xs.min(0), ys.min(0), xs.max(0), ys.max(0)], axis=1)


def normalise(boxes: np.ndarray, shape_hw) -> np.ndarray:
    if boxes.size == 0:
        return boxes.reshape(0, 4)
    h, w = float(shape_hw[0]), float(shape_hw[1])
    return boxes.astype(np.float64) / np.array([w, h, w, h])


def iou_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if a.size == 0 or b.size == 0:
        return np.zeros((len(a), len(b)))
    area_a = np.clip(a[:, 2] - a[:, 0], 0, None) * np.clip(a[:, 3] - a[:, 1], 0, None)
    area_b = np.clip(b[:, 2] - b[:, 0], 0, None) * np.clip(b[:, 3] - b[:, 1], 0, None)
    lt = np.maximum(a[:, None, :2], b[None, :, :2])
    rb = np.minimum(a[:, None, 2:], b[None, :, 2:])
    wh = np.clip(rb - lt, 0, None)
    inter = wh[..., 0] * wh[..., 1]
    return inter / np.maximum(area_a[:, None] + area_b[None, :] - inter, 1e-12)


def greedy_match(iou: np.ndarray, thr: float = 0.5) -> list[tuple[int, int, float]]:
    pairs = []
    if iou.size == 0:
        return pairs
    order = np.dstack(np.unravel_index(np.argsort(iou, axis=None)[::-1], iou.shape))[0]
    ua, ub = set(), set()
    for i, j in order:
        v = iou[i, j]
        if v < thr:
            break
        if i in ua or j in ub:
            continue
        ua.add(int(i)); ub.add(int(j))
        pairs.append((int(i), int(j), float(v)))
    return pairs


def prf(tp: int, n_pred: int, n_true: int) -> dict[str, float]:
    p = tp / n_pred if n_pred else float("nan")
    r = tp / n_true if n_true else float("nan")
    f = 2 * p * r / (p + r) if (n_pred and n_true and (p + r) > 0) else float("nan")
    return {"precision": p, "recall": r, "f1": f}


def f1_from(tp: int, n_pred: int, n_true: int) -> float:
    if n_pred == 0 and n_true == 0:
        return float("nan")          # nothing on either side: undefined, not perfect
    if n_pred == 0 or n_true == 0:
        return 0.0
    p, r = tp / n_pred, tp / n_true
    return 2 * p * r / (p + r) if (p + r) > 0 else 0.0


def grey256(path: Path) -> np.ndarray:
    with Image.open(path) as im:
        return np.asarray(im.convert("L").resize(FULL, Image.BILINEAR), dtype=np.float64)


def best_full_transform(a: np.ndarray, b: np.ndarray) -> tuple[str, dict[str, float]]:
    """Transform t minimising RMS(t(a), b), plus every transform's RMS."""
    out = {}
    for t in TF_NAMES:
        d = np.ascontiguousarray(NP_TF[t](a)) - b
        out[t] = float(np.sqrt((d * d).mean()))
    return min(out, key=out.get), out


def counts_for(pred_n, pred_c, true_n, true_c, aware: bool) -> tuple[int, int, int]:
    """(tp, n_pred, n_true) under greedy IoU>=0.5 matching."""
    ms = greedy_match(iou_matrix(pred_n, true_n), 0.5)
    if aware:
        tp = sum(1 for i, j, _ in ms if pred_c[i] == true_c[j])
    else:
        tp = len(ms)
    return tp, len(pred_c), len(true_c)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--d-csv", required=True, type=Path)
    ap.add_argument("--published-csv", type=Path, default=None,
                    help="published S2, to test how reproducible the pairing is")
    ap.add_argument("--test-dir", required=True, type=Path)
    ap.add_argument("--train-dir", required=True, type=Path)
    ap.add_argument("--test-boxes", required=True, type=Path)
    ap.add_argument("--train-boxes", required=True, type=Path)
    ap.add_argument("--clusters", required=True, type=Path)
    ap.add_argument("--t-global", type=float, required=True)
    ap.add_argument("--resamples", type=int, default=10000)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--pairs-csv", required=True, type=Path)
    args = ap.parse_args()

    _self_test()
    print("transform algebra self-test: PASS")

    tb_all = pickle.load(open(args.test_boxes, "rb"))
    wb_all = pickle.load(open(args.train_boxes, "rb"))
    names = tb_all["names"]
    tb_all, wb_all = tb_all["boxes"], wb_all["boxes"]
    test_by = {Path(p).name: p for p in tb_all}
    train_by = {Path(p).name: p for p in wb_all}

    with args.d_csv.open(newline="") as fh:
        pairs = list(csv.DictReader(fh))
    print(f"{len(pairs)} pairs from {args.d_csv.name}")

    published = {}
    if args.published_csv and args.published_csv.exists():
        with args.published_csv.open(newline="") as fh:
            published = {r["test_image"]: r for r in csv.DictReader(fh)}

    clusters = json.load(open(args.clusters))
    cl_of: dict[str, int] = {}
    for c in clusters["clusters"]:
        for m in c["members"]:
            cl_of[m] = c["cluster_id"]

    rows: list[dict[str, Any]] = []
    for r in pairs:
        tn, rn, thumb_tf = r["test_image"], r["train_image"], r["matching_transform"]
        tp_path, rp_path = args.test_dir / tn, args.train_dir / rn
        A, B = grey256(tp_path), grey256(rp_path)
        full_tf, rms_all = best_full_transform(A, B)

        with Image.open(tp_path) as im:
            tw, th = im.size
        with Image.open(rp_path) as im:
            rw, rh = im.size

        tb, wb = tb_all[test_by[tn]], wb_all[train_by[rn]]
        test_g = normalise(tb["gt_xyxy"], tb["ori_shape"])
        test_c = tb["gt_cls"].astype(int)
        twin_g0 = normalise(wb["gt_xyxy"], wb["ori_shape"])
        twin_c = wb["gt_cls"].astype(int)

        # The transform maps TEST -> TRAIN, so its inverse brings the twin's
        # boxes into the test frame.
        def twin_in_test(t: str) -> np.ndarray:
            return map_norm_boxes(twin_g0, INVERSE[t])

        rec: dict[str, Any] = {
            "test_image": tn, "train_image": rn,
            "thumb_transform": thumb_tf, "full_transform": full_tf,
            "full_rms_best": rms_all[full_tf],
            "full_rms_identity": rms_all["identity"],
            "test_w": tw, "test_h": th, "train_w": rw, "train_h": rh,
            "same_dims": int(tw == rw and th == rh),
            "test_ar": tw / th, "train_ar": rw / rh,
            "cluster": cl_of.get(tn, -1),
            "n_test_boxes": int(len(test_c)), "n_twin_boxes": int(len(twin_c)),
        }
        rec["same_ar_1pct"] = int(abs(rec["test_ar"] / rec["train_ar"] - 1.0) <= 0.01)

        # ---- 2.6(b) recomputed with the full-resolution transform
        tw_g = twin_in_test(full_tf)
        ag_tp, ag_np_, ag_nt = counts_for(tw_g, twin_c, test_g, test_c, aware=False)
        aw_tp, _, _ = counts_for(tw_g, twin_c, test_g, test_c, aware=True)
        rec.update(tp_agnostic=ag_tp, tp_aware=aw_tp)
        rec["identical_label_set"] = int(
            len(test_c) == len(twin_c) == ag_tp and aw_tp == ag_tp)

        # ---- upper bound: best achievable box F1 over the four axis-safe transforms
        best_f1, best_t = -1.0, None
        for t in AXIS_SAFE:
            g = twin_in_test(t)
            tp_, np_, nt_ = counts_for(g, twin_c, test_g, test_c, aware=True)
            f = f1_from(tp_, np_, nt_)
            if not np.isnan(f) and f > best_f1:
                best_f1, best_t = f, t
        rec["oracle_best_f1_aware"] = best_f1 if best_f1 >= 0 else float("nan")
        rec["oracle_best_transform"] = best_t
        rec["f1_aware_at_full_tf"] = f1_from(aw_tp, ag_np_, ag_nt)

        # ---- item 2: model consistency vs label consistency, at t_global
        keep_t = tb["pred_conf"] >= args.t_global
        keep_w = wb["pred_conf"] >= args.t_global
        predD_g = normalise(tb["pred_xyxy"][keep_t], tb["ori_shape"])
        predD_c = tb["pred_cls"][keep_t].astype(int)
        predW_g0 = normalise(wb["pred_xyxy"][keep_w], wb["ori_shape"])
        predW_c = wb["pred_cls"][keep_w].astype(int)
        predW_g = map_norm_boxes(predW_g0, INVERSE[full_tf])

        for tag, (pn, pc, gn, gc) in {
            "i_predD_vs_predTwin": (predD_g, predD_c, predW_g, predW_c),
            "ii_labelD_vs_labelTwin": (test_g, test_c, tw_g, twin_c),
            "iii_predD_vs_labelD": (predD_g, predD_c, test_g, test_c),
            "iv_predD_vs_labelTwin": (predD_g, predD_c, tw_g, twin_c),
            "v_predTwin_vs_labelTwin": (predW_g, predW_c, tw_g, twin_c),
        }.items():
            tp_, np_, nt_ = counts_for(pn, pc, gn, gc, aware=True)
            rec[f"{tag}__tp"], rec[f"{tag}__np"], rec[f"{tag}__nt"] = tp_, np_, nt_
        pub = published.get(tn)
        if pub:
            rec["published_transform"] = pub["matching_transform"]
            rec["published_train_image"] = pub["train_image"]
            rec["published_tf_same"] = int(pub["matching_transform"] == thumb_tf)
            rec["published_train_same"] = int(pub["train_image"] == rn)
            pn = pub["train_image"]
            if pn in train_by:
                pb = wb_all[train_by[pn]]
                pub_g0 = normalise(pb["gt_xyxy"], pb["ori_shape"])
                pub_c = pb["gt_cls"].astype(int)
                pub_g = map_norm_boxes(pub_g0, INVERSE[pub["matching_transform"]])
                a_tp, a_np, a_nt = counts_for(pub_g, pub_c, test_g, test_c, aware=False)
                w_tp, _, _ = counts_for(pub_g, pub_c, test_g, test_c, aware=True)
                rec["pub_tp_agnostic"], rec["pub_tp_aware"] = a_tp, w_tp
                rec["pub_n_twin_boxes"] = int(len(pub_c))
                rec["pub_identical_label_set"] = int(
                    len(test_c) == len(pub_c) == a_tp and w_tp == a_tp)
        rows.append(rec)

    # ---------------------------------------------------------------- item 1
    xtab: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        xtab[r["thumb_transform"]][r["full_transform"]] += 1

    def micro(sel, aware_key, np_key, nt_key) -> dict[str, float]:
        tp = sum(r[aware_key] for r in sel)
        return prf(tp, sum(r[np_key] for r in sel), sum(r[nt_key] for r in sel))

    def block(sel: list[dict]) -> dict[str, Any]:
        if not sel:
            return {"n_pairs": 0}
        ident = sum(r["identical_label_set"] for r in sel)
        ok = [r for r in sel if not np.isnan(r["oracle_best_f1_aware"])
              and not np.isnan(r["f1_aware_at_full_tf"])]
        oracle = [r["oracle_best_f1_aware"] for r in ok]
        achieved = [r["f1_aware_at_full_tf"] for r in ok]
        return {
            "n_pairs": len(sel),
            "n_boxes_test": sum(r["n_test_boxes"] for r in sel),
            "n_boxes_twin": sum(r["n_twin_boxes"] for r in sel),
            "class_agnostic": prf(sum(r["tp_agnostic"] for r in sel),
                                  sum(r["n_twin_boxes"] for r in sel),
                                  sum(r["n_test_boxes"] for r in sel)),
            "class_aware": prf(sum(r["tp_aware"] for r in sel),
                               sum(r["n_twin_boxes"] for r in sel),
                               sum(r["n_test_boxes"] for r in sel)),
            "pairs_with_identical_label_sets": ident,
            "proportion_identical_label_sets": ident / len(sel),
            "n_pairs_with_defined_f1": len(ok),
            "per_pair_f1_aware_at_chosen_transform_mean": float(np.mean(achieved)) if achieved else float("nan"),
            "per_pair_f1_aware_at_chosen_transform_median": float(np.median(achieved)) if achieved else float("nan"),
            "oracle_best_f1_aware_mean": float(np.mean(oracle)) if oracle else float("nan"),
            "oracle_best_f1_aware_median": float(np.median(oracle)) if oracle else float("nan"),
            "oracle_gain_mean": float(np.mean(np.array(oracle) - np.array(achieved))) if ok else float("nan"),
            "n_pairs_where_oracle_beats_chosen": int(sum(
                1 for r in ok if r["oracle_best_f1_aware"] > r["f1_aware_at_full_tf"] + 1e-12)),
        }

    item1 = {
        "method": "both images greyscale, resized to 256x256, RMS over all 8 dihedral "
                  "transforms; the transform maps TEST -> TRAIN, so its inverse brings "
                  "the twin's boxes into the test frame",
        "crosstab_thumbnail_vs_fullres": {k: dict(v) for k, v in sorted(xtab.items())},
        "n_agree": sum(1 for r in rows if r["thumb_transform"] == r["full_transform"]),
        "n_pairs": len(rows),
        "identical_pixel_dimensions": sum(r["same_dims"] for r in rows),
        "same_aspect_ratio_1pct": sum(r["same_ar_1pct"] for r in rows),
        "concordance_fullres_overall": block(rows),
        "concordance_fullres_by_transform": {
            t: block([r for r in rows if r["full_transform"] == t])
            for t in TF_NAMES if any(r["full_transform"] == t for r in rows)
        },
        "reproducibility_vs_published_S2": (lambda sel: {
            "note": "D matches published S2 exactly as a SET of test images, but the "
                    "per-pair ASSIGNMENT -- which training image, under which transform "
                    "-- is a near-tie argmin and is only partly reproducible across "
                    "implementations. Reported because it bounds how much weight the "
                    "transform column can carry.",
            "n_with_published_row": len(sel),
            "same_transform": sum(r["published_tf_same"] for r in sel),
            "same_train_image": sum(r["published_train_same"] for r in sel),
            "same_both": sum(1 for r in sel if r["published_tf_same"] and r["published_train_same"]),
            "crosstab_published_vs_regenerated": {
                a: dict(Counter(r["thumb_transform"] for r in sel if r["published_transform"] == a))
                for a in sorted({r["published_transform"] for r in sel})},
            "concordance_under_published_pairing": (lambda ok: {
                "n_pairs": len(ok),
                "class_agnostic_f1": prf(sum(r["pub_tp_agnostic"] for r in ok),
                                         sum(r["pub_n_twin_boxes"] for r in ok),
                                         sum(r["n_test_boxes"] for r in ok))["f1"],
                "class_aware_f1": prf(sum(r["pub_tp_aware"] for r in ok),
                                      sum(r["pub_n_twin_boxes"] for r in ok),
                                      sum(r["n_test_boxes"] for r in ok))["f1"],
                "proportion_identical_label_sets":
                    sum(r["pub_identical_label_set"] for r in ok) / len(ok) if ok else float("nan"),
            })([r for r in sel if "pub_tp_aware" in r]),
        })([r for r in rows if "published_transform" in r]) if published else None,
        "oracle_note": "oracle_best_f1_aware is the best class-aware box F1 achievable "
                       "over the FOUR transforms the published rule can produce "
                       "(identity/hflip/vflip/rot180) -- not over all eight. It bounds what "
                       "a better choice WITHIN the published rule's range could deliver. It "
                       "is not a bound over all registrations: were a pair ever to resolve "
                       "to rot90/rot270/transpose/transverse, this figure could fall below "
                       "f1_aware_at_full_tf. All 259 pairs here resolve to the four "
                       "axis-safe transforms, so the bound is valid as reported.",
    }

    # ---------------------------------------------------------------- item 2
    CONTRASTS = ["i_predD_vs_predTwin", "ii_labelD_vs_labelTwin", "iii_predD_vs_labelD",
                 "iv_predD_vs_labelTwin", "v_predTwin_vs_labelTwin"]

    def pooled_f1(sel: list[dict], tag: str) -> float:
        return f1_from(sum(r[f"{tag}__tp"] for r in sel),
                       sum(r[f"{tag}__np"] for r in sel),
                       sum(r[f"{tag}__nt"] for r in sel))

    by_cluster: dict[int, list[dict]] = defaultdict(list)
    for r in rows:
        by_cluster[r["cluster"]].append(r)
    cl_ids = sorted(by_cluster)
    rng = np.random.default_rng(SEED)
    draws = {t: [] for t in CONTRASTS}
    draws_diff = []
    for _ in range(args.resamples):
        pick = rng.choice(len(cl_ids), len(cl_ids), replace=True)
        sel = [r for i in pick for r in by_cluster[cl_ids[i]]]
        vals = {t: pooled_f1(sel, t) for t in CONTRASTS}
        for t in CONTRASTS:
            draws[t].append(vals[t])
        draws_diff.append(vals["iv_predD_vs_labelTwin"] - vals["iii_predD_vs_labelD"])

    def ci(a) -> dict[str, float]:
        a = np.asarray(a, dtype=np.float64)
        a = a[~np.isnan(a)]
        return {"ci_lo": float(np.percentile(a, 2.5)), "ci_hi": float(np.percentile(a, 97.5)),
                "boot_mean": float(a.mean()), "boot_sd": float(a.std(ddof=1))}

    item2: dict[str, Any] = {
        "t_global": args.t_global,
        "matching": "greedy, IoU >= 0.5, class-aware; micro-averaged (pooled counts)",
        "bootstrap": {
            "design": "cluster bootstrap over the Phase 2.1 connected components that "
                      "contain at least one D image. Clusters with no D image contribute "
                      "no pairs, so drawing them is a no-op and they are omitted; this is "
                      "exactly equivalent to the pre-specified stratified design for a "
                      "pair-level statistic.",
            "n_clusters_resampled": len(cl_ids), "n_resamples": args.resamples,
        },
        "overall": {t: {"point": pooled_f1(rows, t), **ci(draws[t])} for t in CONTRASTS},
        "iv_minus_iii": {"point": pooled_f1(rows, "iv_predD_vs_labelTwin")
                                  - pooled_f1(rows, "iii_predD_vs_labelD"), **ci(draws_diff)},
        "by_transform": {},
        "training_augmentation_note": "best.pt train_args: fliplr 0.27883, flipud 0.0, "
                                      "degrees 0. Horizontal flips were seen in training; "
                                      "vertical flips and 180-degree rotations were not.",
    }
    for t in TF_NAMES:
        sel = [r for r in rows if r["full_transform"] == t]
        if not sel:
            continue
        cl_t = sorted({r["cluster"] for r in sel})
        by_cl_t = defaultdict(list)
        for r in sel:
            by_cl_t[r["cluster"]].append(r)
        rng_t = np.random.default_rng(SEED + 1 + TF_NAMES.index(t))
        dd = []
        for _ in range(args.resamples):
            pk = rng_t.choice(len(cl_t), len(cl_t), replace=True)
            ss = [r for i in pk for r in by_cl_t[cl_t[i]]]
            dd.append(pooled_f1(ss, "iv_predD_vs_labelTwin")
                      - pooled_f1(ss, "iii_predD_vs_labelD"))
        item2["by_transform"][t] = {
            "n_pairs": len(sel),
            **{c: pooled_f1(sel, c) for c in CONTRASTS},
            "iv_minus_iii": {"point": pooled_f1(sel, "iv_predD_vs_labelTwin")
                                      - pooled_f1(sel, "iii_predD_vs_labelD"),
                             **ci(dd)},
            "seen_in_training_augmentation":
                {"identity": "yes (the image itself)", "hflip": "yes (fliplr 0.27883)",
                 "vflip": "no (flipud 0.0)", "rot180": "no (flipud 0.0, degrees 0)"}.get(t, "no"),
        }

    # ---------------------------------------------------------------- outputs
    fields = [k for k in rows[0] if not k.endswith(("__tp", "__np", "__nt"))] + \
             [f"{t}__{s}" for t in CONTRASTS for s in ("tp", "np", "nt")]
    args.pairs_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.pairs_csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    out = {"seed": SEED, "item1_transform_check": item1, "item2_consistency": item2,
           "class_names": {str(k): v for k, v in names.items()}}
    args.out.write_text(json.dumps(out, indent=2, default=float) + "\n")

    print(f"\nthumbnail vs full-res transform agree: {item1['n_agree']}/{item1['n_pairs']}")
    print(f"identical pixel dimensions: {item1['identical_pixel_dimensions']}/{len(rows)}")
    print(f"same aspect ratio (+-1%):   {item1['same_aspect_ratio_1pct']}/{len(rows)}")
    print(f"2.6(b) recomputed: class-aware F1 {item1['concordance_fullres_overall']['class_aware']['f1']:.4f}"
          f"  identical label sets {item1['concordance_fullres_overall']['pairs_with_identical_label_sets']}/{len(rows)}")
    o=item1['concordance_fullres_overall']
    print(f"per-pair F1 at chosen transform: {o['per_pair_f1_aware_at_chosen_transform_mean']:.4f}"
          f"  oracle: {o['oracle_best_f1_aware_mean']:.4f}"
          f"  gain: {o['oracle_gain_mean']:+.4f}"
          f"  pairs improved: {o['n_pairs_where_oracle_beats_chosen']}")
    for t in CONTRASTS:
        v = item2["overall"][t]
        print(f"  {t:<26} F1 {v['point']:.4f}  [{v['ci_lo']:.4f}, {v['ci_hi']:.4f}]")
    d = item2["iv_minus_iii"]
    print(f"  (iv) - (iii) = {d['point']:+.4f}  [{d['ci_lo']:+.4f}, {d['ci_hi']:+.4f}]")
    print(f"\nwrote {args.out} and {args.pairs_csv}")


if __name__ == "__main__":
    main()
