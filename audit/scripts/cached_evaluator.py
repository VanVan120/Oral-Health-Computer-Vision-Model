"""Exact cached evaluator for Model B (spec Phase 1).

The idea: run ultralytics' own validator once, capture for every image exactly
the arrays it hands to its metric accumulator, then compute metrics for any
subset of images by replaying those arrays through the *same* metric function
the validator calls.

Nothing about the matching is re-implemented. `DetectionValidator.update_metrics`
builds `{tp, conf, pred_cls, target_cls, target_img}` per image and appends it to
`DetMetrics.stats`; we record the appended entry and key it by `im_file`. Subset
metrics come from a fresh `DetMetrics` fed those same entries and processed with
`DetMetrics.process`, which is the call `get_stats` makes.

Why this is safe to trust only after the gate: Phase 1.2 compares `evaluate()`
against real `val(batch=1)` runs on the full split, on ND and on two seeded
random subsets, and requires agreement to 1e-9 on every reported metric.
"""
from __future__ import annotations

import argparse
import json
import pickle
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
import torch
import yaml
from ultralytics import YOLO
from ultralytics.models.yolo.detect import DetectionValidator
from ultralytics.utils import ops
from ultralytics.utils.metrics import DetMetrics

# The pinned evaluation settings. Everything downstream depends on these being
# identical between the cache run and every val() the gate compares against.
VAL_ARGS: dict[str, Any] = dict(
    imgsz=640,
    conf=0.001,
    iou=0.7,
    max_det=300,
    device="cpu",
    half=False,
    rect=True,
    save_json=False,
    save_txt=False,
    plots=False,
    verbose=False,
)

STAT_KEYS = ("tp", "conf", "pred_cls", "target_cls", "target_img")


class CachingValidator(DetectionValidator):
    """DetectionValidator that records per-image metric inputs and boxes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache: dict[str, dict[str, np.ndarray]] = {}
        self.boxes: dict[str, dict[str, np.ndarray]] = {}

    def update_metrics(self, preds, batch) -> None:
        # DetMetrics.update_stats appends exactly one entry per image, in order,
        # and does so before the no-prediction early-continue, so the mapping
        # from position to image is simply the enumeration order of `preds`.
        start = len(self.metrics.stats["tp"])
        super().update_metrics(preds, batch)

        for si, pred in enumerate(preds):
            pbatch = self._prepare_batch(si, batch)
            im_file = str(pbatch["im_file"])
            idx = start + si

            entry = {}
            for k in self.metrics.stats:          # whatever this version accumulates
                v = self.metrics.stats[k][idx]
                entry[k] = np.asarray(v.cpu() if isinstance(v, torch.Tensor) else v)
            # ultralytics 8.4.118 does not store im_name in stats, but its
            # update_stats() requires it in the dict passed in, for
            # Metric.update_image_metrics. Caching it keeps one evaluator
            # working under both pinned versions.
            entry["im_name"] = Path(im_file).name
            self.cache[im_file] = entry

            # Boxes in ORIGINAL image coordinates, via the validator's own
            # scaling so the mapping matches what it would export.
            predn = self._prepare_pred(pred)
            scaled = self.scale_preds(predn, pbatch)
            gt = pbatch["bboxes"]
            gt_ori = (
                ops.scale_boxes(pbatch["imgsz"], gt.clone(), pbatch["ori_shape"], ratio_pad=pbatch["ratio_pad"])
                if gt.shape[0]
                else gt
            )
            self.boxes[im_file] = {
                "pred_xyxy": scaled["bboxes"].cpu().numpy().astype(np.float32),
                "pred_conf": scaled["conf"].cpu().numpy().astype(np.float32),
                "pred_cls": scaled["cls"].cpu().numpy().astype(np.float32),
                "gt_xyxy": np.asarray(gt_ori.cpu(), dtype=np.float32),
                "gt_cls": np.asarray(pbatch["cls"].cpu(), dtype=np.float32),
                "ori_shape": np.asarray(pbatch["ori_shape"], dtype=np.int32),
            }


def _val_arg_dict(weights: str, data: str, split: str, batch: int) -> dict[str, Any]:
    """Exactly the argument set model.val() would build.

    model.val() does `custom = {"rect": True}` then
    `args = {**overrides, **custom, **kwargs, "mode": "val"}`, constructs the
    validator with it, and calls `validator(model=self.model)`. We reproduce
    that rather than calling model.val(), because model.val() instantiates the
    validator class itself and never hands the instance back, and the instance
    is precisely what holds the cache.
    """
    return dict(model=weights, data=data, split=split, batch=batch, mode="val", **VAL_ARGS)


def build_cache(weights: str, data: str, split: str, batch: int = 1) -> CachingValidator:
    """Run one real validation pass and return the populated validator."""
    validator = CachingValidator(args=_val_arg_dict(weights, data, split, batch))
    # Pass the nn.Module, as model.val() does -- not the path -- so AutoBackend
    # takes the same branch.
    validator(model=YOLO(weights).model)
    return validator


class Evaluator:
    """Replay cached per-image stats through ultralytics' own metric function."""

    def __init__(self, cache: dict[str, dict[str, np.ndarray]], names: dict[int, str]):
        self.cache = cache
        self.names = names

    @classmethod
    def load(cls, path: Path) -> "Evaluator":
        with open(path, "rb") as fh:
            blob = pickle.load(fh)
        return cls(blob["cache"], blob["names"])

    def evaluate(self, image_multiset: Iterable[str]) -> dict[str, Any]:
        """Metrics for a multiset of images.

        A multiset, not a set: the bootstrap resamples images with replacement,
        and an image drawn twice must contribute its detections twice.
        """
        metrics = DetMetrics(names=self.names)
        n = 0
        for im in image_multiset:
            # Pass the whole cached entry. Keys this version does not accumulate
            # are ignored by update_stats, and keys it needs beyond `stats`
            # (im_name, in 8.4.118) are present.
            metrics.update_stats(self.cache[im])
            n += 1
        if n == 0:
            raise ValueError("empty image multiset")

        metrics.process(save_dir=Path("."), plot=False, on_plot=None)
        mp, mr, map50, map5095 = metrics.mean_results()

        per_class = {}
        for i, c in enumerate(metrics.ap_class_index):
            p, r, ap50, ap = metrics.class_result(i)
            per_class[self.names[int(c)]] = {
                "class_index": int(c),
                "instances": int(metrics.nt_per_class[int(c)]),
                "images": int(metrics.nt_per_image[int(c)]),
                "P": float(p),
                "R": float(r),
                "AP50": float(ap50),
                "AP50_95": float(ap),
            }
        return {
            "n_images": n,
            "n_instances": int(metrics.nt_per_class.sum()),
            "P": float(mp),
            "R": float(mr),
            "mAP50": float(map50),
            "mAP50_95": float(map5095),
            "fitness": float(metrics.fitness),
            "per_class": per_class,
        }

    def images(self) -> list[str]:
        return sorted(self.cache)


def write_subset_yaml(images: Sequence[str], data_yaml: Path, out_dir: Path, tag: str) -> Path:
    """A data yaml whose split points at a txt list, for a real val() run."""
    out_dir.mkdir(parents=True, exist_ok=True)
    txt = out_dir / f"{tag}.txt"
    txt.write_text("\n".join(str(Path(p).resolve()) for p in images) + "\n")

    base = yaml.safe_load(data_yaml.read_text())
    cfg = {
        "path": str(out_dir.resolve()),
        "train": str(txt.resolve()),
        "val": str(txt.resolve()),
        "test": str(txt.resolve()),
        "nc": base["nc"],
        "names": base["names"],
    }
    y = out_dir / f"{tag}.yaml"
    y.write_text(yaml.safe_dump(cfg, sort_keys=False))
    return y


def real_val(weights: str, data_yaml: Path, split: str = "test", batch: int = 1) -> dict[str, Any]:
    """A genuine val() run, reported in the same shape as Evaluator.evaluate."""
    v = DetectionValidator(args=_val_arg_dict(weights, str(data_yaml), split, batch))
    v(model=YOLO(weights).model)
    m = v.metrics
    mp, mr, map50, map5095 = m.mean_results()
    per_class = {}
    for i, c in enumerate(m.ap_class_index):
        p, r, ap50, ap = m.class_result(i)
        per_class[v.names[int(c)]] = {
            "class_index": int(c),
            "instances": int(m.nt_per_class[int(c)]),
            "images": int(m.nt_per_image[int(c)]),
            "P": float(p), "R": float(r), "AP50": float(ap50), "AP50_95": float(ap),
        }
    return {
        "n_images": int(v.seen),
        "n_instances": int(m.nt_per_class.sum()),
        "P": float(mp), "R": float(mr), "mAP50": float(map50), "mAP50_95": float(map5095),
        "fitness": float(m.fitness), "per_class": per_class,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--weights", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--split", default="test")
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--boxes-out", type=Path, default=None)
    args = ap.parse_args()

    v = build_cache(args.weights, args.data, args.split, args.batch)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "wb") as fh:
        pickle.dump({"cache": v.cache, "names": v.names, "split": args.split,
                     "batch": args.batch, "data": args.data, "weights": args.weights}, fh,
                    protocol=pickle.HIGHEST_PROTOCOL)
    if args.boxes_out:
        with open(args.boxes_out, "wb") as fh:
            pickle.dump({"boxes": v.boxes, "names": v.names}, fh, protocol=pickle.HIGHEST_PROTOCOL)

    ev = Evaluator(v.cache, v.names)
    full = ev.evaluate(ev.images())
    print(json.dumps({"cached_images": len(v.cache), "full_split": {k: full[k] for k in
                      ("n_images", "n_instances", "P", "R", "mAP50", "mAP50_95")}}, indent=2))


if __name__ == "__main__":
    main()
