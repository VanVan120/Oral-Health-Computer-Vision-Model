"""Addendum R1b item 4: decompose the "No Issues Detected" rate.

The R1 summary reported a with-router "No Issues Detected" rate of 26.9% without
saying that it is two different events added together: an image the router
refused ("not a valid oral health image") and an image the router accepted on
which the detector found nothing. Those mean opposite things to a user, and the
second is the only one that is a detector miss.

Four mutually exclusive, exhaustive outcomes per image, per condition:
    1 rejected by the router or a gate
    2 accepted, no finding
    3 accepted, that condition reported
    4 accepted, other findings only

Runs entirely off the cached per-image records in S34. No inference.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

SEED = 20260921
DISPLAY = {0: "Calculus", 1: "Caries", 2: "Gingivitis",
           3: "Hypodontia", 4: "Tooth Discoloration", 5: "Ulcers"}
THRESHOLDS = {"Ulcers": 0.75, "Tooth Discoloration": 0.40, "Caries": 0.35,
              "Hypodontia": 0.60, "Calculus": 0.25, "Gingivitis": 0.30}
DEFAULT_THRESHOLD = 0.25
OUTCOMES = ("rejected_router_or_gate", "accepted_no_finding",
            "accepted_condition_reported", "accepted_other_findings_only")


def wilson(k: int, n: int, z: float = 1.959963984540054) -> list[float]:
    if n == 0:
        return [float("nan"), float("nan")]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z / d * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [max(0.0, c - h), min(1.0, c + h)]


def shown_for(rec: dict) -> list[str]:
    """Display names the deployed app would show, post-fix, after thresholding."""
    out = set()
    for cls_id, conf in rec["raw"]:
        name = DISPLAY.get(int(cls_id), "Unknown")
        if conf >= THRESHOLDS.get(name, DEFAULT_THRESHOLD):
            out.add(name)
    return sorted(out)


def classify(rec: dict, shown: list[str], cond: str | None) -> str:
    if rec["router_label"] != "Clinical":
        return "rejected_router_or_gate"
    if not shown:
        return "accepted_no_finding"
    if cond is None or cond in shown:
        return "accepted_condition_reported"
    return "accepted_other_findings_only"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--e2e", required=True, type=Path)
    ap.add_argument("--labels", required=True, type=Path)
    ap.add_argument("--clusters", required=True, type=Path)
    ap.add_argument("--d-csv", required=True, type=Path)
    ap.add_argument("--resamples", type=int, default=10000)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    recs = json.load(open(args.e2e))["records"]
    print(f"{len(recs)} cached per-image records")

    # Ground truth: which conditions are present, from the label files.
    gt: dict[str, set[str]] = {}
    for rec in recs:
        stem = Path(rec["image"]).stem
        lp = args.labels / f"{stem}.txt"
        present = set()
        if lp.exists():
            for line in lp.read_text().splitlines():
                p = line.split()
                if p:
                    present.add(DISPLAY[int(p[0])])
        gt[rec["image"]] = present

    shown = {r["image"]: shown_for(r) for r in recs}

    # Cluster map for the pre-specified bootstrap.
    clusters = json.load(open(args.clusters))
    cl_of, members = {}, {}
    for c in clusters["clusters"]:
        members[c["cluster_id"]] = c["members"]
        for m in c["members"]:
            cl_of[m] = c["cluster_id"]
    import csv as _csv
    with args.d_csv.open(newline="") as fh:
        d_names = {r["test_image"] for r in _csv.DictReader(fh)}
    with_d = [cid for cid, ms in members.items() if any(m in d_names for m in ms)]
    without_d = [cid for cid, ms in members.items() if not any(m in d_names for m in ms)]
    print(f"clusters: {len(with_d)} containing D, {len(without_d)} not")

    by_img = {r["image"]: r for r in recs}

    def tally(images: list[str], cond: str | None) -> dict[str, int]:
        t = dict.fromkeys(OUTCOMES, 0)
        for im in images:
            t[classify(by_img[im], shown[im], cond)] += 1
        return t

    rng = np.random.default_rng(SEED)
    # One set of resampled cluster picks, reused for every subset, so the
    # intervals are mutually consistent.
    picks = [np.concatenate([rng.choice(with_d, len(with_d), replace=True),
                             rng.choice(without_d, len(without_d), replace=True)])
             for _ in range(args.resamples)]

    def boot(cond: str | None, subset_filter) -> dict[str, list[float]]:
        draws = {o: [] for o in OUTCOMES}
        for pk in picks:
            imgs = [m for cid in pk for m in members[cid] if subset_filter(m)]
            if not imgs:
                continue
            t = tally(imgs, cond)
            n = sum(t.values())
            for o in OUTCOMES:
                draws[o].append(t[o] / n)
        return {o: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
                if v else [float("nan")] * 2 for o, v in draws.items()}

    all_imgs = [r["image"] for r in recs]
    report: dict[str, Any] = {
        "n_images": len(recs),
        "outcome_definitions": {
            "rejected_router_or_gate": "router_label != Clinical: softmax below 0.95, or "
                                       "one of the three image-quality gates fired",
            "accepted_no_finding": "routed Clinical and the detector reported nothing "
                                   "after per-class thresholding -- the only outcome that "
                                   "is a detector miss",
            "accepted_condition_reported": "routed Clinical and this condition was shown",
            "accepted_other_findings_only": "routed Clinical, something was shown, but not "
                                            "this condition",
        },
        "bootstrap": {"design": "Phase 2.1 cluster bootstrap, stratified by whether a "
                                "cluster contains a D image, as pre-specified in 2.3",
                      "n_resamples": args.resamples},
    }

    # ---- all images (outcome 4 is empty by construction: cond = None)
    t = tally(all_imgs, None)
    n = len(all_imgs)
    cb = boot(None, lambda m: True)
    report["all_images"] = {
        "n": n,
        "note": "with cond=None, outcomes 3 and 4 collapse: 'accepted_condition_reported' "
                "means 'accepted and at least one finding shown', and "
                "'accepted_other_findings_only' is empty by construction",
        "outcomes": {o: {"k": t[o], "proportion": t[o] / n, "wilson95": wilson(t[o], n),
                         "cluster_boot95": cb[o]} for o in OUTCOMES},
    }

    # ---- per condition-present subset
    report["by_condition_present"] = {}
    for cond in sorted(DISPLAY.values()):
        sub = [im for im in all_imgs if cond in gt[im]]
        t = tally(sub, cond)
        n = len(sub)
        cb = boot(cond, lambda m, c=cond: c in gt.get(m, set()))
        report["by_condition_present"][cond] = {
            "n_present": n,
            "outcomes": {o: {"k": t[o], "proportion": t[o] / n if n else float("nan"),
                             "wilson95": wilson(t[o], n),
                             "cluster_boot95": cb[o]} for o in OUTCOMES},
        }
        print(f"  {cond:<20} n={n:<5} "
              + "  ".join(f"{o.split('_',1)[1][:12]} {t[o]/n:.3f}" for o in OUTCOMES))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, default=float) + "\n")
    a = report["all_images"]["outcomes"]
    print(f"\nall images: rejected {a['rejected_router_or_gate']['proportion']:.4f}, "
          f"accepted-no-finding {a['accepted_no_finding']['proportion']:.4f}, "
          f"accepted-with-finding {a['accepted_condition_reported']['proportion']:.4f}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
