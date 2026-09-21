"""Memorisation diagnostics (spec Phase 2.6) -- the new evidence for R1.1.

Removing the duplicated test images cannot show what the model would have scored
had it never seen their training twins. These four diagnostics look instead for
direct evidence of memorisation:

  (a) M on training images, the validation split and the test split, all through
      the same evaluator.
  (b) Annotation concordance between each D image and its training twin, after
      mapping the twin's boxes through the matching transform.
  (c) For D, instance recall of the detector's predictions against two label
      sets: the test image's own labels, and its twin's mapped labels. If the
      predictions agree better with the twin's labels, that is a memorisation
      signature.
  (d) M on the training twins against their own labels, next to M on D.
"""
from __future__ import annotations

import argparse
import csv
import json
import pickle
import random
from pathlib import Path
from typing import Any

import numpy as np

from cached_evaluator import Evaluator

SEED = 20260921

# Each of these is its own inverse, which is why S2 can record a single
# transform per pair without an orientation convention.
def map_boxes(boxes: np.ndarray, shape_hw: np.ndarray, transform: str) -> np.ndarray:
    """Map xyxy boxes through a dihedral transform, in pixel coordinates."""
    if boxes.size == 0:
        return boxes
    h, w = float(shape_hw[0]), float(shape_hw[1])
    b = boxes.astype(np.float64).copy()
    x1, y1, x2, y2 = b[:, 0].copy(), b[:, 1].copy(), b[:, 2].copy(), b[:, 3].copy()
    if transform in ("hflip", "rot180"):
        x1, x2 = w - x2, w - x1
    if transform in ("vflip", "rot180"):
        y1, y2 = h - y2, h - y1
    return np.stack([x1, y1, x2, y2], axis=1)


def normalise(boxes: np.ndarray, shape_hw: np.ndarray) -> np.ndarray:
    if boxes.size == 0:
        return boxes
    h, w = float(shape_hw[0]), float(shape_hw[1])
    return boxes / np.array([w, h, w, h], dtype=np.float64)


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
    """Greedy one-to-one matching by descending IoU."""
    pairs = []
    if iou.size == 0:
        return pairs
    order = np.dstack(np.unravel_index(np.argsort(iou, axis=None)[::-1], iou.shape))[0]
    used_a, used_b = set(), set()
    for i, j in order:
        v = iou[i, j]
        if v < thr:
            break
        if i in used_a or j in used_b:
            continue
        used_a.add(int(i)); used_b.add(int(j))
        pairs.append((int(i), int(j), float(v)))
    return pairs


def prf(tp: int, n_pred: int, n_true: int) -> dict[str, float]:
    p = tp / n_pred if n_pred else float("nan")
    r = tp / n_true if n_true else float("nan")
    f = 2 * p * r / (p + r) if (n_pred and n_true and (p + r) > 0) else float("nan")
    return {"precision": p, "recall": r, "f1": f}


def t_global_from(ev: Evaluator, images: list[str]) -> float:
    """Confidence at the peak of ultralytics' smoothed mean-F1 curve."""
    from ultralytics.utils.metrics import DetMetrics, smooth

    m = DetMetrics(names=ev.names)
    for im in images:
        e = ev.cache[im]
        m.update_stats(e)   # whole entry: extra keys ignored, im_name present for 8.4.118
    m.process(save_dir=Path("."), plot=False, on_plot=None)
    px, f1_curve, _, _ = m.box.curves_results[1]
    i = smooth(np.asarray(f1_curve).mean(0), 0.1).argmax()
    return float(np.asarray(px)[i])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--test-cache", required=True, type=Path)
    ap.add_argument("--test-boxes", required=True, type=Path)
    ap.add_argument("--train-cache", required=True, type=Path)
    ap.add_argument("--train-boxes", required=True, type=Path)
    ap.add_argument("--valid-cache", required=True, type=Path)
    ap.add_argument("--d-csv", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--draw-dir", type=Path, default=None)
    args = ap.parse_args()

    test_ev = Evaluator.load(args.test_cache)
    train_ev = Evaluator.load(args.train_cache)
    valid_ev = Evaluator.load(args.valid_cache)
    names = test_ev.names

    with open(args.test_boxes, "rb") as fh:
        test_boxes = pickle.load(fh)["boxes"]
    with open(args.train_boxes, "rb") as fh:
        train_boxes = pickle.load(fh)["boxes"]

    test_by_name = {Path(p).name: p for p in test_ev.images()}
    train_by_name = {Path(p).name: p for p in train_ev.images()}

    with args.d_csv.open(newline="") as fh:
        pairs = list(csv.DictReader(fh))
    d_images = sorted(test_by_name[r["test_image"]] for r in pairs)
    twin_names = sorted({r["train_image"] for r in pairs})
    twin_images = sorted(train_by_name[n] for n in twin_names if n in train_by_name)

    # ---------- (a) train / valid / test
    a = {
        "train": train_ev.evaluate(train_ev.images()),
        "valid": valid_ev.evaluate(valid_ev.images()),
        "test": test_ev.evaluate(test_ev.images()),
    }
    a_small = {k: {m: v[m] for m in ("n_images", "n_instances", "P", "R", "mAP50", "mAP50_95")} for k, v in a.items()}
    print("(a) " + json.dumps(a_small))

    t_global = t_global_from(test_ev, test_ev.images())
    print(f"t_global (full test split) = {t_global:.4f}")

    # ---------- (b) annotation concordance
    tot = {"tp_agnostic": 0, "tp_aware": 0, "n_test": 0, "n_twin": 0}
    identical = 0
    per_class_tp = {int(c): 0 for c in names}
    per_class_test = {int(c): 0 for c in names}
    per_class_twin = {int(c): 0 for c in names}
    disagreements: list[dict[str, Any]] = []
    rows_for_c = []

    for r in pairs:
        tn, rn, tf = r["test_image"], r["train_image"], r["matching_transform"]
        if rn not in train_by_name:
            continue
        tb = test_boxes[test_by_name[tn]]
        wb = train_boxes[train_by_name[rn]]

        test_g = normalise(tb["gt_xyxy"].astype(np.float64), tb["ori_shape"])
        test_c = tb["gt_cls"].astype(int)
        twin_mapped = map_boxes(wb["gt_xyxy"].astype(np.float64), wb["ori_shape"], tf)
        twin_g = normalise(twin_mapped, wb["ori_shape"])
        twin_c = wb["gt_cls"].astype(int)

        iou = iou_matrix(twin_g, test_g)  # rows = twin (treated as "prediction")
        matches = greedy_match(iou, 0.5)
        tp_ag = len(matches)
        tp_aw = sum(1 for i, j, _ in matches if twin_c[i] == test_c[j])

        tot["tp_agnostic"] += tp_ag
        tot["tp_aware"] += tp_aw
        tot["n_test"] += len(test_c)
        tot["n_twin"] += len(twin_c)
        for c in test_c:
            per_class_test[int(c)] += 1
        for c in twin_c:
            per_class_twin[int(c)] += 1
        for i, j, _ in matches:
            if twin_c[i] == test_c[j]:
                per_class_tp[int(test_c[j])] += 1
            else:
                disagreements.append(
                    {"test_image": tn, "train_image": rn, "transform": tf,
                     "twin_class": names[int(twin_c[i])], "test_class": names[int(test_c[j])]}
                )

        same = (len(test_c) == len(twin_c) == tp_ag) and tp_aw == tp_ag
        identical += bool(same)
        rows_for_c.append((tn, rn, tf, test_g, test_c, twin_g, twin_c))

    b = {
        "n_pairs": len(rows_for_c),
        "class_agnostic": prf(tot["tp_agnostic"], tot["n_twin"], tot["n_test"]),
        "class_aware": prf(tot["tp_aware"], tot["n_twin"], tot["n_test"]),
        "n_boxes_test": tot["n_test"],
        "n_boxes_twin": tot["n_twin"],
        "pairs_with_identical_label_sets": identical,
        "proportion_identical_label_sets": identical / max(1, len(rows_for_c)),
        "per_class": {
            names[c]: {"test_boxes": per_class_test[c], "twin_boxes": per_class_twin[c], "matched_same_class": per_class_tp[c]}
            for c in sorted(per_class_test)
        },
        "n_class_disagreements": len(disagreements),
        "class_disagreements": disagreements[:200],
    }
    print(f"(b) class-aware F1 {b['class_aware']['f1']:.4f}; identical label sets {identical}/{len(rows_for_c)}")

    # ---------- (c) recall vs own labels vs twin labels, at t_global
    def recall_against(pred_b, pred_c, gt_b, gt_c) -> tuple[int, int]:
        if len(gt_c) == 0:
            return 0, 0
        iou = iou_matrix(pred_b, gt_b)
        ms = greedy_match(iou, 0.5)
        tp = sum(1 for i, j, _ in ms if pred_c[i] == gt_c[j])
        return tp, len(gt_c)

    own_tp = own_n = twin_tp = twin_n = 0
    dif_own_tp = dif_own_n = dif_twin_tp = dif_twin_n = 0
    for tn, rn, tf, test_g, test_c, twin_g, twin_c in rows_for_c:
        tb = test_boxes[test_by_name[tn]]
        keep = tb["pred_conf"] >= t_global
        pb = normalise(tb["pred_xyxy"][keep].astype(np.float64), tb["ori_shape"])
        pc = tb["pred_cls"][keep].astype(int)

        o_tp, o_n = recall_against(pb, pc, test_g, test_c)
        w_tp, w_n = recall_against(pb, pc, twin_g, twin_c)
        own_tp += o_tp; own_n += o_n; twin_tp += w_tp; twin_n += w_n

        iou = iou_matrix(twin_g, test_g)
        ms = greedy_match(iou, 0.5)
        same = (len(test_c) == len(twin_c) == len(ms)) and all(twin_c[i] == test_c[j] for i, j, _ in ms)
        if not same:
            dif_own_tp += o_tp; dif_own_n += o_n
            dif_twin_tp += w_tp; dif_twin_n += w_n

    c = {
        "t_global": t_global,
        "all_D": {
            "recall_vs_own_labels": own_tp / own_n if own_n else float("nan"),
            "recall_vs_twin_labels": twin_tp / twin_n if twin_n else float("nan"),
            "n_own": own_n, "n_twin": twin_n,
        },
        "differing_label_subset": {
            "n_pairs": len(rows_for_c) - identical,
            "recall_vs_own_labels": dif_own_tp / dif_own_n if dif_own_n else float("nan"),
            "recall_vs_twin_labels": dif_twin_tp / dif_twin_n if dif_twin_n else float("nan"),
            "n_own": dif_own_n, "n_twin": dif_twin_n,
        },
    }
    print(f"(c) recall own {c['all_D']['recall_vs_own_labels']:.4f} vs twin {c['all_D']['recall_vs_twin_labels']:.4f}")

    # ---------- (d) M on twins vs M on D
    d = {
        "twins_own_labels": {k: v for k, v in train_ev.evaluate(twin_images).items() if k != "per_class"},
        "D": {k: v for k, v in test_ev.evaluate(d_images).items() if k != "per_class"},
        "n_unique_twins": len(twin_images),
    }
    print(f"(d) twins mAP50 {d['twins_own_labels']['mAP50']:.4f} vs D mAP50 {d['D']['mAP50']:.4f}")

    # ---------- 12 drawn pairs for a visual check (scratchpad only)
    drawn = []
    if args.draw_dir:
        from PIL import Image, ImageDraw
        args.draw_dir.mkdir(parents=True, exist_ok=True)
        rng = random.Random(SEED)
        for tn, rn, tf, test_g, test_c, twin_g, twin_c in rng.sample(rows_for_c, min(12, len(rows_for_c))):
            tp_ = Path(test_by_name[tn])
            with Image.open(tp_) as im:
                im = im.convert("RGB")
                W, H = im.size
                dr = ImageDraw.Draw(im)
                for bb, cc in zip(test_g, test_c):
                    dr.rectangle([bb[0]*W, bb[1]*H, bb[2]*W, bb[3]*H], outline=(0, 200, 0), width=3)
                    dr.text((bb[0]*W + 3, bb[1]*H + 3), f"own:{names[int(cc)]}", fill=(0, 200, 0))
                for bb, cc in zip(twin_g, twin_c):
                    dr.rectangle([bb[0]*W, bb[1]*H, bb[2]*W, bb[3]*H], outline=(220, 0, 0), width=2)
                    dr.text((bb[0]*W + 3, bb[3]*H - 14), f"twin:{names[int(cc)]}", fill=(220, 0, 0))
                out = args.draw_dir / f"{tf}__{tn}"
                im.save(out)
                drawn.append(str(out))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(
        {"a_train_valid_test": a_small, "a_full": a, "b_concordance": b,
         "c_recall_own_vs_twin": c, "d_twins_vs_D": d, "drawn_pairs": drawn,
         "t_global": t_global}, indent=2, default=float) + "\n")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
