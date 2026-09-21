"""Offline replication of the deployed request path (spec Phases 3.3, 3.4, 3.5).

The web server is not started. The same objects the API constructs are built
directly and driven in the same order: TriageRouter.predict, then, for a
"Clinical" verdict, OralHygieneModel.predict.

Three things are captured that the deployed code does not expose:

 1. Which of the router's four exit paths each image takes. Three image-quality
    gates fire before the network -- mean brightness < 40, > 250, and standard
    deviation < 15 -- so a rejection is not necessarily a low-confidence
    classification, and the two must be reported separately (DEVIATIONS D3).

 2. The class index inside the detector chain immediately before the name
    mapping, which is what isolates the mapping from the inference.

 3. Enough to replay the pre-correction path of commit 7210dea two ways:
      - FULL   : the old dictionary AND thresholds looked up by the wrong
                 display name, which is what the application actually did;
      - MAPPING: the old dictionary applied to detections that survived the
                 CURRENT thresholds, which is the spec's mapping-isolated count.
    The full simulation is primary (DEVIATIONS D2).
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np

# --- the pre-correction dictionary, transcribed verbatim from 7210dea ---
PREFIX_CLASS_NAMES = {
    0: "Caries", 1: "Calculus", 2: "Gingivitis",
    3: "Tooth Discoloration", 4: "Ulcers", 5: "Hypodontia",
}
# Byte-identical before and after the fix; keyed by DISPLAY name.
THRESHOLDS = {
    "Ulcers": 0.75, "Tooth Discoloration": 0.40, "Caries": 0.35,
    "Hypodontia": 0.60, "Calculus": 0.25, "Gingivitis": 0.30,
}
DEFAULT_THRESHOLD = 0.25


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def router_verdict(router, image_path: str) -> dict[str, Any]:
    """Replicate TriageRouter.predict, recording which exit path was taken."""
    import torch
    import torch.nn.functional as F
    from PIL import Image

    image = Image.open(image_path).convert("RGB")
    arr = np.array(image)
    mean_b, std_d = float(np.mean(arr)), float(np.std(arr))

    if mean_b < 40:
        return {"label": "Unknown", "exit": "gate_brightness_low", "mean": mean_b, "std": std_d, "conf": None}
    if mean_b > 250:
        return {"label": "Unknown", "exit": "gate_brightness_high", "mean": mean_b, "std": std_d, "conf": None}
    if std_d < 15:
        return {"label": "Unknown", "exit": "gate_low_detail", "mean": mean_b, "std": std_d, "conf": None}

    t = router.transform(image).unsqueeze(0).to(router.device)
    with torch.no_grad():
        probs = F.softmax(router.model(t), dim=1)
        conf, idx = torch.max(probs, 1)
    conf = float(conf.item())
    if conf < 0.95:
        return {"label": "Unknown", "exit": "softmax_below_threshold", "mean": mean_b, "std": std_d, "conf": conf}
    return {"label": router.classes[int(idx.item())], "exit": "classified",
            "mean": mean_b, "std": std_d, "conf": conf}


def detect_indices(model, image_path: str) -> dict[str, Any]:
    """Run the deployed detector and capture (cls_id, conf) before name mapping."""
    import cv2
    from sahi.predict import get_sliced_prediction

    img = cv2.imread(image_path)
    if img is None:
        return {"error": "unreadable", "raw": [], "path_used": None}
    h, w = img.shape[:2]
    raw: list[tuple[int, float]] = []

    if w < 640 or h < 640:
        path_used = "standard"
        res = model.standard_model.predict(image_path, conf=0.15, imgsz=640, save=False, verbose=False)
        if res:
            for b in res[0].boxes:
                raw.append((int(b.cls[0]), float(b.conf[0])))
    else:
        path_used = "sahi"
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        out = get_sliced_prediction(rgb, model.sahi_model, slice_height=512, slice_width=512,
                                    overlap_height_ratio=0.2, overlap_width_ratio=0.2, verbose=0)
        for p in out.object_prediction_list:
            raw.append((int(p.category.id), float(p.score.value)))
    return {"raw": raw, "path_used": path_used, "size": [w, h]}


def apply_mapping(raw, index_to_display, threshold_by_display) -> list[str]:
    """Return the display names reported, under a given dictionary + thresholds."""
    out = []
    for cls_id, conf in raw:
        name = index_to_display.get(cls_id, "Unknown")
        if conf >= threshold_by_display.get(name, DEFAULT_THRESHOLD):
            out.append(name)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--images", required=True, type=Path)
    ap.add_argument("--labels", type=Path, default=None)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--tag", default="test")
    args = ap.parse_args()

    inf_mod = load_module("mb_inf", args.repo / "ml_models/model_b/inference_model.py")
    tri_mod = load_module("tri_inf", args.repo / "ml_models/model_triage/triage_inference.py")

    model = inf_mod.OralHygieneModel(str(args.repo / "ml_models/model_b/models/best.pt"))
    router = tri_mod.TriageRouter(str(args.repo / "ml_models/model_triage/triage_router.pth"))

    true_names = model.standard_model.names                      # index -> weight name
    post_fix = {i: inf_mod.display_name(n) for i, n in true_names.items()}   # deployed today

    paths = sorted(p for p in args.images.rglob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
    if args.limit:
        paths = paths[: args.limit]
    print(f"{len(paths)} images from {args.images}")

    records = []
    for n, p in enumerate(paths, 1):
        rv = router_verdict(router, str(p))
        # Detection runs on EVERY image, whatever the router decided. The router
        # outcome is reported separately: mixing the two would make the mapping
        # counts depend on the router's behaviour as well as the dictionary's.
        det = detect_indices(model, str(p))
        records.append({"image": p.name, "router": rv, "detect": det})
        if n % 250 == 0:
            print(f"  {n}/{len(paths)}")

    # ---- router outcomes
    exits = Counter(r["router"]["exit"] for r in records)
    labels = Counter(r["router"]["label"] for r in records)

    # ---- SAHI usage
    sahi = Counter(r["detect"].get("path_used") for r in records)

    # ---- mapping analysis (detector path only)
    post_findings, prefix_full, prefix_mapping = [], [], []
    confusion = defaultdict(Counter)   # true weight-name -> displayed name (pre-fix, full)
    idx_total = Counter()
    for r in records:
        raw = r["detect"].get("raw", [])
        post = apply_mapping(raw, post_fix, THRESHOLDS)
        full = apply_mapping(raw, PREFIX_CLASS_NAMES, THRESHOLDS)
        # mapping-only: keep the detections the CURRENT thresholds admit, then
        # relabel them with the old dictionary.
        kept = [(c, v) for c, v in raw if v >= THRESHOLDS.get(post_fix.get(c, ""), DEFAULT_THRESHOLD)]
        mapping = [PREFIX_CLASS_NAMES.get(c, "Unknown") for c, _ in kept]

        post_findings.append(sorted(set(post)))
        prefix_full.append(sorted(set(full)))
        prefix_mapping.append(sorted(set(mapping)))

        for c, v in raw:
            if v >= THRESHOLDS.get(PREFIX_CLASS_NAMES.get(c, ""), DEFAULT_THRESHOLD):
                confusion[true_names[c]][PREFIX_CLASS_NAMES.get(c, "Unknown")] += 1
                idx_total[true_names[c]] += 1

    def wrong_stats(pre_lists, kept_counts) -> dict[str, Any]:
        wrong_findings = 0
        total_findings = 0
        images_affected = 0
        images_all_wrong = 0
        for post, pre in zip(post_findings, pre_lists):
            total_findings += len(pre)
            w = sum(1 for x in pre if x not in post)
            wrong_findings += w
            if w:
                images_affected += 1
                if pre and w == len(pre):
                    images_all_wrong += 1
        return {
            "displayed_findings_total": total_findings,
            "displayed_findings_wrong_name": wrong_findings,
            "images_with_any_wrong_name": images_affected,
            "images_with_only_wrong_names": images_all_wrong,
            "n_images": len(pre_lists),
        }

    out: dict[str, Any] = {
        "tag": args.tag,
        "n_images": len(records),
        "router": {
            "exits": dict(exits),
            "labels": dict(labels),
            "gate_rejections": {k: v for k, v in exits.items() if k.startswith("gate_")},
            "softmax_rejections": exits.get("softmax_below_threshold", 0),
        },
        "sahi_path_counts": {str(k): v for k, v in sahi.items()},
        "post_fix_agreement": {
            "note": "display names are derived from model.names via DISPLAY_NAMES; "
                    "agreement between captured indices and displayed labels is 100% by construction",
            "n_detections_mapped": int(sum(len(r['detect'].get('raw', [])) for r in records)),
        },
        "prefix_FULL_path_primary": wrong_stats(prefix_full, None),
        "prefix_MAPPING_only_secondary": wrong_stats(prefix_mapping, None),
        "permutation_confusion_true_to_displayed_prefix": {
            k: dict(v) for k, v in confusion.items()
        },
    }

    # ---- 3.4 image-level, if labels given
    if args.labels:
        gt = {}
        for p in paths:
            lp = args.labels / (p.stem + ".txt")
            classes = set()
            if lp.exists():
                for line in lp.read_text().splitlines():
                    if line.strip():
                        classes.add(int(line.split()[0]))
            gt[p.name] = {post_fix[c] for c in classes}
        out["image_level"] = image_level(records, post_findings, gt, post_fix)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"summary": out,
                                    "records": [{"image": r["image"],
                                                 "router_exit": r["router"]["exit"],
                                                 "router_label": r["router"]["label"],
                                                 "router_conf": r["router"]["conf"],
                                                 "path_used": r["detect"].get("path_used"),
                                                 # Every per-class threshold, and the fallback, is at
                                                 # or above 0.25, so a detection below it can never be
                                                 # reported under either dictionary. Dropping those
                                                 # keeps this file small without losing anything the
                                                 # analysis can use.
                                                 "raw": [[c, round(v, 4)] for c, v in r["detect"].get("raw", [])
                                                         if v >= DEFAULT_THRESHOLD]} for r in records]},
                                   indent=2, default=float) + "\n")
    print(json.dumps(out, indent=2, default=float)[:3000])


def image_level(records, post_findings, gt, post_fix) -> dict[str, Any]:
    """Per-condition rates, with and without the router in front."""
    conditions = sorted(set(post_fix.values()))
    res = {}
    for with_router in (True, False):
        per_cond = {}
        no_finding = 0
        for c in conditions:
            present_reported = present_total = absent_reported = absent_total = 0
            present_nofinding = 0
            for rec, found in zip(records, post_findings):
                shown = found if (not with_router or rec["router"]["label"] == "Clinical") else []
                truth = gt.get(rec["image"], set())
                if c in truth:
                    present_total += 1
                    present_reported += c in shown
                    present_nofinding += len(shown) == 0
                else:
                    absent_total += 1
                    absent_reported += c in shown
            per_cond[c] = {
                "reported_when_present": present_reported / present_total if present_total else float("nan"),
                "n_present": present_total,
                "reported_when_absent": absent_reported / absent_total if absent_total else float("nan"),
                "n_absent": absent_total,
                "no_finding_when_present": present_nofinding / present_total if present_total else float("nan"),
            }
        for rec, found in zip(records, post_findings):
            shown = found if (not with_router or rec["router"]["label"] == "Clinical") else []
            no_finding += len(shown) == 0
        res["with_router" if with_router else "without_router"] = {
            "per_condition": per_cond,
            "no_issues_detected_rate": no_finding / len(records),
        }
    res["not_estimable_from_this_benchmark"] = [
        "patient-level sensitivity",
        "specificity in healthy mouths (there are no healthy images in this split)",
        "predictive values at population prevalence",
        "referral burden",
    ]
    return res


if __name__ == "__main__":
    main()
