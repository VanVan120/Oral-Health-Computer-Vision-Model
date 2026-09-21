"""Evaluate the domain router at its deployed threshold (spec Phase 3.5).

Three sets, with the expected route for each:

    Model B test split (1,500)   -> Clinical
    all Model A images (544)     -> Histopathological
    COCO128 (128), out of domain -> rejected, i.e. "Unknown"

Reported as proportions with Wilson 95% intervals. The three image-quality gates
that fire before the network are counted separately from softmax rejections
(DEVIATIONS D3): an image rejected because it is too dark was never classified
at all, and folding the two together would make the proportion uninterpretable.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

from end_to_end import load_module, router_verdict

EXTS = {".jpg", ".jpeg", ".png", ".bmp"}


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z / d * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, c - h), min(1.0, c + h))


def prop(k: int, n: int) -> dict[str, Any]:
    lo, hi = wilson(k, n)
    return {"k": k, "n": n, "proportion": k / n if n else float("nan"), "wilson95": [lo, hi]}


def source_of(name: str) -> str:
    return name.split(".rf.")[0] if ".rf." in name else name


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--test-dir", required=True, type=Path)
    ap.add_argument("--model-a-root", required=True, type=Path)
    ap.add_argument("--coco128", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    tri = load_module("tri", args.repo / "ml_models/model_triage/triage_inference.py")
    router = tri.TriageRouter(str(args.repo / "ml_models/model_triage/triage_router.pth"))

    sets = {
        "model_b_test": (sorted(p for p in args.test_dir.rglob("*") if p.suffix.lower() in EXTS), "Clinical"),
        "model_a_all": (sorted(p for p in args.model_a_root.rglob("*") if p.suffix.lower() in EXTS and "images" in p.parts), "Histopathological"),
        "coco128_ood": (sorted(p for p in args.coco128.rglob("*") if p.suffix.lower() in EXTS), "Unknown"),
    }

    report: dict[str, Any] = {"deployed_threshold": 0.95}
    for tag, (paths, expected) in sets.items():
        print(f"{tag}: {len(paths)} images (expected route: {expected})")
        exits, labels = Counter(), Counter()
        recs = []
        for p in paths:
            v = router_verdict(router, str(p))
            exits[v["exit"]] += 1
            labels[v["label"]] += 1
            recs.append((p.name, v["exit"], v["label"], v["conf"]))
        n = len(paths)
        correct = labels[expected] if expected != "Unknown" else labels["Unknown"]
        wrong_route = sum(c for lab, c in labels.items() if lab not in (expected, "Unknown")) \
            if expected != "Unknown" else sum(c for lab, c in labels.items() if lab != "Unknown")
        unknown = labels["Unknown"]

        entry = {
            "n": n,
            "expected_route": expected,
            "labels": dict(labels),
            "exits": dict(exits),
            "correct": prop(correct, n),
            "wrong_route": prop(wrong_route, n),
            "unknown": prop(unknown, n),
            "gate_rejections": {k: v for k, v in exits.items() if k.startswith("gate_")},
            "gate_rejections_total": prop(sum(v for k, v in exits.items() if k.startswith("gate_")), n),
            "softmax_rejections": prop(exits.get("softmax_below_threshold", 0), n),
        }
        if tag == "model_a_all":
            srcs = {source_of(p.name) for p in paths}
            entry["distinct_sources"] = len(srcs)
            entry["note"] = ("image-level proportions; the 544 images are 3 Roboflow-augmented "
                             "versions of a smaller set of source fields, so images are not independent")
        report[tag] = entry
        print(f"   correct {correct}/{n}  unknown {unknown}  gates {entry['gate_rejections']}")

    report["overlap_with_training_data"] = (
        "UNKNOWN. The router's training data is ./dataset, assembled by hand and never "
        "committed at any point in the repository's history. Overlap with any of these "
        "three sets cannot be determined from the records that exist."
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, default=float) + "\n")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
