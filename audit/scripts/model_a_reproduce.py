"""Reproduce the Model A evaluation with the DEPLOYED checkpoint (spec Phase 4.1).

The notebook's stored metrics were produced by `model_a_best.pth`, which is not
preserved anywhere. The application serves `model_a.pth`. This script runs
`model_a.pth` on the reproduced validation split and reports its metrics as the
deployed model's, alongside the stored ones.

Three reproducibility hazards are handled explicitly rather than papered over:

1. The pooled row order comes from `os.listdir`, which is filesystem-ordered,
   not sorted. `random_split` permutes *indices*, so a different enumeration
   order gives a different 435/109 membership. Both a sorted ordering and the
   raw `os.listdir` ordering are tried, and each is scored against the 96
   validation filenames recorded in the published S5.

2. `full_dataset` is built with `train_transform` -- RandomHorizontalFlip,
   RandomVerticalFlip, RandomRotation(15), ColorJitter -- and `val_transform` is
   defined but never used. The validation metrics were therefore computed on
   randomly augmented images. We evaluate deterministically (val_transform, the
   correct choice) and also under the augmented pipeline, to show the spread.

3. TVNT is not a histopathological label. Cell 2 sets
   `tvnt = 1 if counts['has_objects'] else 0`, i.e. "this image has at least one
   annotated box". A TVNT negative is an unannotated field, not non-tumour tissue.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision import models, transforms

SEED = 20260921
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


class OSCCMultiTaskModel(nn.Module):
    """Architecture copied from ml_models/model_a/inference_model.py.

    Note the Dropout in every head. It carries no parameters but it occupies an
    index in the Sequential, so omitting it shifts the final Linear from .3 to
    .2 and the state dict no longer matches. The deployed loader uses
    strict=False, which would swallow exactly that mismatch and leave the final
    layers randomly initialised; we load strictly so any such error is loud.
    """

    def __init__(self):
        super().__init__()
        self.backbone = models.densenet169(weights=None)
        num_ftrs = self.backbone.classifier.in_features
        self.backbone.classifier = nn.Identity()
        self.head_tvnt = nn.Sequential(nn.Linear(num_ftrs, 256), nn.ReLU(), nn.Dropout(0.3), nn.Linear(256, 2))
        self.head_mitotic = nn.Sequential(nn.Linear(num_ftrs, 128), nn.ReLU(), nn.Dropout(0.2), nn.Linear(128, 1))
        self.head_nucleol = nn.Sequential(nn.Linear(num_ftrs, 128), nn.ReLU(), nn.Dropout(0.2), nn.Linear(128, 1))
        self.head_hyperchrom = nn.Sequential(nn.Linear(num_ftrs, 128), nn.ReLU(), nn.Dropout(0.2), nn.Linear(128, 1))

    def forward(self, x):
        f = self.backbone.features(x)
        pooled = torch.nn.functional.relu(f, inplace=False)
        pooled = torch.nn.functional.adaptive_avg_pool2d(pooled, (1, 1)).flatten(1)
        return {
            "tvnt": self.head_tvnt(pooled),
            "mitotic": self.head_mitotic(pooled),
            "nucleol": self.head_nucleol(pooled),
            "hyperchrom": self.head_hyperchrom(pooled),
        }


def build_records(root: Path, order: str) -> list[dict[str, Any]]:
    """Reproduce cell 2's pooling. order='sorted' or 'listdir'."""
    import os

    recs = []
    for split in ("train", "valid", "test"):
        img_dir, lab_dir = root / split / "images", root / split / "labels"
        if not img_dir.is_dir():
            continue
        files = [f for f in os.listdir(img_dir) if Path(f).suffix.lower() in IMAGE_EXTS]
        if order == "sorted":
            files = sorted(files)
        for f in files:
            lp = lab_dir / (Path(f).stem + ".txt")
            c = {"mitotic": 0, "nucleol": 0, "hyperchrom": 0}
            has = False
            if lp.exists():
                for line in lp.read_text().splitlines():
                    p = line.strip().split()
                    if len(p) >= 5:
                        has = True
                        cid = int(p[0])
                        c["mitotic"] += cid == 0
                        c["nucleol"] += cid == 1
                        c["hyperchrom"] += cid == 2
            recs.append({"filename": f, "path": str(img_dir / f), "tvnt": int(has), **c})
    return recs


class RecDataset(Dataset):
    def __init__(self, recs, transform):
        self.recs, self.transform = recs, transform

    def __len__(self):
        return len(self.recs)

    def __getitem__(self, i):
        r = self.recs[i]
        img = Image.open(r["path"]).convert("RGB")
        return self.transform(img), r["tvnt"], r["mitotic"], r["nucleol"], r["hyperchrom"], i


VAL_TF = transforms.Compose([
    transforms.Resize((224, 224)), transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
TRAIN_TF = transforms.Compose([
    transforms.Resize((224, 224)), transforms.RandomHorizontalFlip(), transforms.RandomVerticalFlip(),
    transforms.RandomRotation(15), transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1),
    transforms.ToTensor(), transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    from scipy.stats import beta
    if n == 0:
        return (float("nan"), float("nan"))
    lo = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
    return lo, hi


def run_inference(model, recs, idx, tf, device) -> dict[str, np.ndarray]:
    ds = RecDataset([recs[i] for i in idx], tf)
    dl = DataLoader(ds, batch_size=8, shuffle=False, num_workers=0)
    P, Y, M, N, H, PM, PN, PH = [], [], [], [], [], [], [], []
    with torch.no_grad():
        for x, y, m, n, h, _ in dl:
            o = model(x.to(device))
            P.append(torch.softmax(o["tvnt"], 1)[:, 1].cpu().numpy())
            Y.append(y.numpy()); M.append(m.numpy()); N.append(n.numpy()); H.append(h.numpy())
            PM.append(o["mitotic"].squeeze(-1).cpu().numpy())
            PN.append(o["nucleol"].squeeze(-1).cpu().numpy())
            PH.append(o["hyperchrom"].squeeze(-1).cpu().numpy())
    cat = lambda xs: np.concatenate(xs)
    return {"score": cat(P), "y": cat(Y), "mitotic": cat(M), "nucleol": cat(N), "hyperchrom": cat(H),
            "pred_mitotic": cat(PM), "pred_nucleol": cat(PN), "pred_hyperchrom": cat(PH)}


def classifier_metrics(y: np.ndarray, score: np.ndarray, n_boot: int = 10_000) -> dict[str, Any]:
    from sklearn.metrics import average_precision_score, matthews_corrcoef, roc_auc_score

    pred = (score >= 0.5).astype(int)
    tp = int(((y == 1) & (pred == 1)).sum()); tn = int(((y == 0) & (pred == 0)).sum())
    fp = int(((y == 0) & (pred == 1)).sum()); fn = int(((y == 1) & (pred == 0)).sum())
    n_pos, n_neg = tp + fn, tn + fp
    sens = tp / n_pos if n_pos else float("nan")
    spec = tn / n_neg if n_neg else float("nan")

    auc = float(roc_auc_score(y, score)) if n_pos and n_neg else float("nan")
    # Bootstrap stratified by class, so every resample keeps both classes present.
    rng = np.random.default_rng(SEED)
    pos_i, neg_i = np.flatnonzero(y == 1), np.flatnonzero(y == 0)
    draws = []
    for _ in range(n_boot):
        s = np.concatenate([rng.choice(pos_i, len(pos_i), True), rng.choice(neg_i, len(neg_i), True)])
        if len(np.unique(y[s])) < 2:
            continue
        draws.append(roc_auc_score(y[s], score[s]))
    draws = np.array(draws)

    denom = [tp + fp, tp + fn, tn + fp, tn + fn]
    mcc_defined = all(d > 0 for d in denom)
    return {
        "confusion": {"TN": tn, "FP": fp, "FN": fn, "TP": tp},
        "n": int(len(y)), "n_positive": n_pos, "n_negative": n_neg,
        "base_rate_positive": n_pos / len(y),
        "accuracy": (tp + tn) / len(y),
        "sensitivity": sens, "sensitivity_CP95": clopper_pearson(tp, n_pos),
        "specificity": spec, "specificity_CP95": clopper_pearson(tn, n_neg),
        "balanced_accuracy": (sens + spec) / 2,
        "roc_auc": auc,
        "roc_auc_boot95": [float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))] if len(draws) else None,
        "roc_auc_boot_n": int(len(draws)),
        "average_precision_positive_target": float(average_precision_score(y, score)) if n_pos and n_neg else None,
        "average_precision_negative_target": float(average_precision_score(1 - y, -score)) if n_pos and n_neg else None,
        "mcc": float(matthews_corrcoef(y, pred)) if mcc_defined else None,
        "mcc_note": None if mcc_defined else f"undefined: zero factor in denominator {denom}; sklearn returns 0.0 by convention",
        "predicted_positive_for_every_image": (tn == 0 and fn == 0),
    }


def regression_metrics(true: np.ndarray, pred: np.ndarray) -> dict[str, float]:
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    pc = np.maximum(pred, 0)
    pr = np.round(pc)
    return {
        "mae": float(mean_absolute_error(true, pc)),
        "rmse": float(np.sqrt(mean_squared_error(true, pc))),
        "r2": float(r2_score(true, pc)) if np.var(true) > 0 else None,
        "exact_match_rate": float((pr == true).mean()),
        "within_1": float((np.abs(pr - true) <= 1).mean()),
        "within_2": float((np.abs(pr - true) <= 2).mean()),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dataset", required=True, type=Path)
    ap.add_argument("--weights", required=True, type=Path)
    ap.add_argument("--s5", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--scores-csv", required=True, type=Path)
    args = ap.parse_args()

    device = torch.device("cpu")
    model = OSCCMultiTaskModel().to(device)
    model.load_state_dict(torch.load(args.weights, map_location=device, weights_only=True))
    model.eval()

    import csv as _csv
    s5_val = {r["validation_image"] for r in _csv.DictReader(open(args.s5))}

    report: dict[str, Any] = {"weights": str(args.weights), "n_s5_validation_images": len(s5_val)}
    best_order, best_hits, best = None, -1, None

    for order in ("sorted", "listdir"):
        recs = build_records(args.dataset, order)
        assert len(recs) == 544, len(recs)
        g = torch.Generator().manual_seed(42)
        tr, va = random_split(range(len(recs)), [int(0.8 * len(recs)), len(recs) - int(0.8 * len(recs))], generator=g)
        va_idx = list(va)
        val_names = {recs[i]["filename"] for i in va_idx}
        hits = len(val_names & s5_val)
        report[f"split_{order}"] = {
            "n_train": len(tr), "n_val": len(va_idx),
            "val_names_matching_S5": hits, "S5_total": len(s5_val),
        }
        print(f"order={order}: train {len(tr)} val {len(va_idx)}, S5 overlap {hits}/{len(s5_val)}")
        if hits > best_hits:
            best_order, best_hits, best = order, hits, (recs, list(tr), va_idx)

    recs, tr_idx, va_idx = best
    report["chosen_order"] = best_order
    report["tvnt_distribution_all_544"] = {
        "normal": int(sum(1 for r in recs if r["tvnt"] == 0)),
        "abnormal": int(sum(1 for r in recs if r["tvnt"] == 1)),
    }

    # Deterministic evaluation -- val_transform, which the notebook defined but never used.
    det = run_inference(model, recs, va_idx, VAL_TF, device)
    report["validation_deterministic"] = classifier_metrics(det["y"], det["score"])
    report["validation_regression"] = {
        t: regression_metrics(det[t], det[f"pred_{t}"]) for t in ("mitotic", "nucleol", "hyperchrom")
    }
    tr_det = run_inference(model, recs, tr_idx, VAL_TF, device)
    report["training_deterministic"] = classifier_metrics(tr_det["y"], tr_det["score"])

    # The notebook's own (augmented) pipeline, repeated to show the spread.
    torch.manual_seed(SEED)
    aug_runs = []
    for _ in range(5):
        a = run_inference(model, recs, va_idx, TRAIN_TF, device)
        m = classifier_metrics(a["y"], a["score"], n_boot=0)
        aug_runs.append({"confusion": m["confusion"], "accuracy": m["accuracy"], "roc_auc": m["roc_auc"]})
    report["validation_augmented_repeats"] = aug_runs

    # The 13 validation images with no training sibling (descriptive only).
    unleaked = [i for i in va_idx if recs[i]["filename"] not in s5_val]
    report["unleaked_subset"] = {"n": len(unleaked)}
    if unleaked:
        u = run_inference(model, recs, unleaked, VAL_TF, device)
        report["unleaked_subset"].update(classifier_metrics(u["y"], u["score"], n_boot=0))

    # Source-level counts: source = filename stem before '.rf.'
    def source_of(n: str) -> str:
        return n.split(".rf.")[0] if ".rf." in n else n
    report["source_level"] = {
        "validation_images": len(va_idx),
        "validation_distinct_sources": len({source_of(recs[i]["filename"]) for i in va_idx}),
        "all_544_distinct_sources": len({source_of(r["filename"]) for r in recs}),
    }

    # Per-image scores, so AP and the AUC CI can be recomputed without a rerun.
    args.scores_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.scores_csv.open("w", newline="") as fh:
        w = _csv.writer(fh)
        w.writerow(["filename", "source", "split", "tvnt_true", "tvnt_score",
                    "mitotic_true", "mitotic_pred", "nucleol_true", "nucleol_pred",
                    "hyperchrom_true", "hyperchrom_pred"])
        for tag, idxs, d in (("val", va_idx, det), ("train", tr_idx, tr_det)):
            for k, i in enumerate(idxs):
                r = recs[i]
                w.writerow([r["filename"], source_of(r["filename"]), tag, int(d["y"][k]), f"{d['score'][k]:.8f}",
                            int(d["mitotic"][k]), f"{d['pred_mitotic'][k]:.6f}",
                            int(d["nucleol"][k]), f"{d['pred_nucleol'][k]:.6f}",
                            int(d["hyperchrom"][k]), f"{d['pred_hyperchrom'][k]:.6f}"])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, default=float) + "\n")
    print(json.dumps({k: report[k] for k in ("chosen_order", "tvnt_distribution_all_544")}, indent=2))
    print("validation confusion:", report["validation_deterministic"]["confusion"],
          "AUC", round(report["validation_deterministic"]["roc_auc"], 4))


if __name__ == "__main__":
    main()
