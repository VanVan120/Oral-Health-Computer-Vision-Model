"""Contamination statistics for Model B (spec Phase 2.2-2.4).

Primary estimand: the removal effect  Delta = M(ND) - M(All),  computed
separately for M = mAP@0.5 and M = mAP@0.5:0.95, which are never compared with
each other.

  2.2  headline table for All / ND / D
  2.3  Delta with a 95% cluster-bootstrap CI (10,000 resamples, stratified by
       whether a cluster contains any image of D)
  2.4  stratified and unstratified randomization tests (10,000 controls each),
       with a balance table and the minimum detectable effect

Seed 20260921 throughout. Workers are seeded deterministically from it, so the
result does not depend on how many cores the machine has.
"""
from __future__ import annotations

import argparse
import csv
import json
import multiprocessing as mp
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from cached_evaluator import Evaluator

SEED = 20260921
N_RESAMPLES = 10_000
BINS = [(1, 1), (2, 3), (4, 7), (8, 15), (16, 10**9)]
BIN_LABELS = ["1", "2-3", "4-7", "8-15", ">=16"]

_EV: Evaluator | None = None


def _init_worker(cache_path: str) -> None:
    global _EV
    _EV = Evaluator.load(Path(cache_path))


def bin_of(n: int) -> str:
    for (lo, hi), lab in zip(BINS, BIN_LABELS):
        if lo <= n <= hi:
            return lab
    raise ValueError(n)


def image_meta(ev: Evaluator) -> dict[str, dict[str, Any]]:
    """Per-image instance count, dominant class and stratum."""
    meta = {}
    for im, entry in ev.cache.items():
        tc = np.asarray(entry["target_cls"]).astype(int)
        n = int(tc.size)
        if n:
            counts = Counter(tc.tolist())
            # Ties go to the lower class index.
            dom = min(counts, key=lambda c: (-counts[c], c))
        else:
            dom = -1
        meta[im] = {
            "n_instances": n,
            "dominant_class": int(dom),
            "bin": bin_of(n) if n else "0",
            "stratum": f"{dom}|{bin_of(n) if n else '0'}",
            "class_counts": {int(k): int(v) for k, v in Counter(tc.tolist()).items()},
        }
    return meta


# ----------------------------------------------------------------- workers


def _slim(r: dict) -> dict:
    """Only what the resampling needs, so workers return little."""
    return {
        "mAP50": r["mAP50"], "mAP50_95": r["mAP50_95"],
        "per_class": {k: {"AP50": v["AP50"], "AP50_95": v["AP50_95"], "instances": v["instances"]}
                      for k, v in r["per_class"].items()},
    }


def _eval_three(args: tuple[list[str], list[str], list[str]]) -> tuple[dict, dict, dict]:
    """All / ND / D for one resample, so both contrasts come from one draw."""
    a, b, c = args
    return _slim(_EV.evaluate(a)), _slim(_EV.evaluate(b)), (_slim(_EV.evaluate(c)) if c else None)


def _eval_one(images: list[str]) -> tuple[float, float]:
    r = _EV.evaluate(images)
    return r["mAP50"], r["mAP50_95"]


# ----------------------------------------------------------------- 2.3


def cluster_bootstrap(
    cache_path: Path,
    clusters: list[list[str]],
    d_set: set[str],
    n_resamples: int,
    workers: int,
) -> dict[str, Any]:
    """Resample clusters with replacement, stratified by contains-D."""
    with_d = [c for c in clusters if any(m in d_set for m in c)]
    without_d = [c for c in clusters if not any(m in d_set for m in c)]

    rng = np.random.default_rng(SEED)
    jobs = []
    for _ in range(n_resamples):
        pick = [with_d[i] for i in rng.integers(0, len(with_d), len(with_d))]
        pick += [without_d[i] for i in rng.integers(0, len(without_d), len(without_d))]
        allimgs = [m for c in pick for m in c]
        ndimgs = [m for m in allimgs if m not in d_set]
        dimgs = [m for m in allimgs if m in d_set]
        jobs.append((allimgs, ndimgs, dimgs))

    with mp.Pool(workers, initializer=_init_worker, initargs=(str(cache_path),)) as pool:
        out = pool.map(_eval_three, jobs, chunksize=8)

    d50 = np.array([b["mAP50"] - a["mAP50"] for a, b, _ in out], dtype=np.float64)
    d5095 = np.array([b["mAP50_95"] - a["mAP50_95"] for a, b, _ in out], dtype=np.float64)

    # Per-class Delta AP for 2.3 (ND - All) and 2.5 (D - ND).
    classes = sorted({k for a, _, _ in out for k in a["per_class"]})
    per_class_removal, per_class_dvnd = {}, {}
    for cname in classes:
        for key, store, f in (("AP50", per_class_removal, lambda a, b, d: _get(b, cname, "AP50") - _get(a, cname, "AP50")),
                              ("AP50_95", per_class_removal, lambda a, b, d: _get(b, cname, "AP50_95") - _get(a, cname, "AP50_95"))):
            vals = np.array([f(a, b, d) for a, b, d in out], dtype=np.float64)
            vals = vals[np.isfinite(vals)]
            store.setdefault(cname, {})[key] = _ci(vals) if vals.size else None
        for key in ("AP50", "AP50_95"):
            vals = np.array([(_get(d, cname, key) - _get(b, cname, key)) if d else np.nan
                             for a, b, d in out], dtype=np.float64)
            vals = vals[np.isfinite(vals)]
            per_class_dvnd.setdefault(cname, {})[key] = _ci(vals) if vals.size else None

    return {
        "n_resamples": n_resamples,
        "n_clusters_with_D": len(with_d),
        "n_clusters_without_D": len(without_d),
        "mAP50": _ci(d50),
        "mAP50_95": _ci(d5095),
        "per_class_delta_ND_minus_All": per_class_removal,
        "per_class_delta_D_minus_ND": per_class_dvnd,
        "_draws50": d50,
        "_draws5095": d5095,
    }


def _get(r: dict, cname: str, key: str) -> float:
    pc = r["per_class"].get(cname)
    return float(pc[key]) if pc else float("nan")


def _ci(x: np.ndarray) -> dict[str, float]:
    return {
        "mean": float(x.mean()),
        "sd": float(x.std(ddof=1)),
        "ci_lo": float(np.percentile(x, 2.5)),
        "ci_hi": float(np.percentile(x, 97.5)),
    }


# ----------------------------------------------------------------- 2.4


def build_strata(meta: dict[str, dict], images: Sequence[str]) -> dict[str, list[str]]:
    s = defaultdict(list)
    for im in images:
        s[meta[im]["stratum"]].append(im)
    return dict(s)


def plan_strata(
    meta: dict[str, dict], d_images: Sequence[str], nd_images: Sequence[str]
) -> tuple[dict[str, int], dict[str, list[str]], list[str]]:
    """Stratum counts to match, and the ND donor pool for each.

    Returns the raw need and pool. Widening is decided per draw inside
    `draw_control`, against a used-set, so that two strata can never be handed
    the same image and a stratum is never emptied by an earlier one.
    """
    need = dict(Counter(meta[im]["stratum"] for im in d_images))
    pool = build_strata(meta, nd_images)
    shortfalls = [
        f"{k}: needs {v}, ND has {len(pool.get(k, []))}"
        for k, v in sorted(need.items()) if len(pool.get(k, [])) < v
    ]
    return need, pool, shortfalls


def _widen_order(stratum: str) -> list[str]:
    """Donor strata to fall back on, nearest instance-count bin first."""
    dom, lab = stratum.split("|")
    if lab not in BIN_LABELS:
        return []
    i = BIN_LABELS.index(lab)
    out = []
    for step in range(1, len(BIN_LABELS)):
        for nb in (i - step, i + step):
            if 0 <= nb < len(BIN_LABELS):
                out.append(f"{dom}|{BIN_LABELS[nb]}")
    return out


def draw_control(
    rng, need: dict[str, int], pool: dict[str, list[str]], nd_images: Sequence[str],
    record: list[str] | None = None,
) -> set[str]:
    """One stratified control set of 259 images drawn from ND.

    Strata are filled scarcest-first so the tight ones get their own donors
    before a looser stratum can take them. A stratum short of donors widens to
    the adjacent instance-count bins of the same dominant class, then to any bin
    of that class, and only then to ND at large -- and every widening is
    recorded rather than applied silently.
    """
    used: set[str] = set()
    order = sorted(need, key=lambda k: (len(pool.get(k, [])) - need[k], k))
    for stratum in order:
        k = need[stratum]
        donors = [im for im in pool.get(stratum, []) if im not in used]
        if len(donors) < k:
            for cand in _widen_order(stratum):
                donors += [im for im in pool.get(cand, []) if im not in used and im not in donors]
                if record is not None and pool.get(cand):
                    record.append(f"{stratum} <- {cand}")
                if len(donors) >= k:
                    break
        if len(donors) < k:
            extra = [im for im in nd_images if im not in used and im not in donors]
            if record is not None:
                record.append(f"{stratum} <- GLOBAL ND ({k - len(donors)} short)")
            donors += extra
        idx = rng.choice(len(donors), k, replace=False)
        picked = {donors[i] for i in idx}
        used |= picked
    return used


def randomization(
    cache_path: Path,
    all_images: Sequence[str],
    nd_images: Sequence[str],
    need: dict[str, int] | None,
    pool: dict[str, list[str]] | None,
    n_resamples: int,
    workers: int,
    seed_offset: int,
) -> dict[str, Any]:
    """Controls that remove 259 images drawn from ND."""
    rng = np.random.default_rng(SEED + seed_offset)
    all_set = list(all_images)
    jobs = []
    removed_sets = []
    widenings: list[str] = []
    for r in range(n_resamples):
        if need is None:
            idx = rng.choice(len(nd_images), 259, replace=False)
            ctrl = {nd_images[i] for i in idx}
        else:
            ctrl = draw_control(rng, need, pool, nd_images, widenings if r == 0 else None)
        assert len(ctrl) == 259, f"control set has {len(ctrl)} images, expected 259"
        removed_sets.append(ctrl)
        jobs.append([im for im in all_set if im not in ctrl])

    with mp.Pool(workers, initializer=_init_worker, initargs=(str(cache_path),)) as pool_:
        out = pool_.map(_eval_one, jobs, chunksize=16)
    return {"draws": out, "removed": removed_sets, "widenings": widenings}


def summarise_controls(draws: list[tuple[float, float]], base: dict[str, float], delta: dict[str, float]) -> dict[str, Any]:
    res = {}
    for key, idx in (("mAP50", 0), ("mAP50_95", 1)):
        dc = np.array([d[idx] for d in draws], dtype=np.float64) - base[key]
        med = float(np.median(dc))
        obs = delta[key]
        # Two-sided p about the control median, as pre-specified.
        extreme = int(np.sum(np.abs(dc - med) >= abs(obs - med)))
        res[key] = {
            "control_mean": float(dc.mean()),
            "control_sd": float(dc.std(ddof=1)),
            "control_median": med,
            "pct_2.5": float(np.percentile(dc, 2.5)),
            "pct_97.5": float(np.percentile(dc, 97.5)),
            "observed_delta": obs,
            "percentile_rank_of_delta": float((np.sum(dc < obs) + 0.5 * np.sum(dc == obs)) / len(dc) * 100),
            "p_two_sided": float((1 + extreme) / (1 + len(dc))),
            "MDE": float((1.96 + 0.84) * dc.std(ddof=1)),
            "_draws": dc,
        }
    return res


def balance_table(meta: dict[str, dict], d_images: Sequence[str], removed_sets: list[set[str]]) -> dict[str, Any]:
    def stats(imgs) -> dict[str, Any]:
        n_inst = sum(meta[i]["n_instances"] for i in imgs)
        per_class = Counter()
        for i in imgs:
            for c, k in meta[i]["class_counts"].items():
                per_class[c] += k
        return {
            "n_images": len(imgs),
            "instances_removed": n_inst,
            "mean_instances_per_image": n_inst / len(imgs),
            "per_class_instances_removed": {str(c): int(per_class[c]) for c in sorted(per_class)},
        }

    d_stats = stats(d_images)
    ctrl = [stats(s) for s in removed_sets]
    mean_ctrl = {
        "n_images": float(np.mean([c["n_images"] for c in ctrl])),
        "instances_removed": float(np.mean([c["instances_removed"] for c in ctrl])),
        "mean_instances_per_image": float(np.mean([c["mean_instances_per_image"] for c in ctrl])),
        "per_class_instances_removed": {
            str(c): float(np.mean([x["per_class_instances_removed"].get(str(c), 0) for x in ctrl]))
            for c in range(6)
        },
    }
    return {"D": d_stats, "control_mean": mean_ctrl}


# ----------------------------------------------------------------- main


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cache", required=True, type=Path)
    ap.add_argument("--d-csv", required=True, type=Path)
    ap.add_argument("--clusters", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--controls-csv", required=True, type=Path)
    ap.add_argument("--resamples", type=int, default=N_RESAMPLES)
    ap.add_argument("--workers", type=int, default=max(1, mp.cpu_count() - 2))
    args = ap.parse_args()

    ev = Evaluator.load(args.cache)
    all_images = ev.images()
    by_name = {Path(p).name: p for p in all_images}
    with args.d_csv.open(newline="") as fh:
        d_names = {r["test_image"] for r in csv.DictReader(fh)}
    d_images = sorted(by_name[n] for n in d_names)
    d_set = set(d_images)
    nd_images = sorted(set(all_images) - d_set)
    assert (len(all_images), len(d_images), len(nd_images)) == (1500, 259, 1241)

    meta = image_meta(ev)
    blob = json.loads(args.clusters.read_text())
    clusters = [[by_name[m] for m in c["members"]] for c in blob["clusters"]]

    # --- 2.2 headline
    headline = {t: ev.evaluate(s) for t, s in (("All", all_images), ("ND", nd_images), ("D", d_images))}

    # --- 2.3 removal effect
    delta = {
        "mAP50": headline["ND"]["mAP50"] - headline["All"]["mAP50"],
        "mAP50_95": headline["ND"]["mAP50_95"] - headline["All"]["mAP50_95"],
    }
    print(f"Delta mAP50    = {delta['mAP50']:+.6f}")
    print(f"Delta mAP50-95 = {delta['mAP50_95']:+.6f}")

    print(f"cluster bootstrap: {args.resamples} resamples on {args.workers} workers ...")
    boot = cluster_bootstrap(args.cache, clusters, d_set, args.resamples, args.workers)
    boot_draws50, boot_draws5095 = boot.pop("_draws50"), boot.pop("_draws5095")

    # --- 2.4 randomization
    need, pool, shortfalls = plan_strata(meta, d_images, nd_images)
    print(f"stratified randomization ({len(need)} strata, {len(shortfalls)} short of donors) ...")
    strat = randomization(args.cache, all_images, nd_images, need, pool, args.resamples, args.workers, 1)
    print("unstratified randomization ...")
    unstrat = randomization(args.cache, all_images, nd_images, None, None, args.resamples, args.workers, 2)

    base = {"mAP50": headline["All"]["mAP50"], "mAP50_95": headline["All"]["mAP50_95"]}
    strat_sum = summarise_controls(strat["draws"], base, delta)
    unstrat_sum = summarise_controls(unstrat["draws"], base, delta)

    # Save every control Delta so the figure can be drawn.
    args.controls_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.controls_csv.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["design", "replicate", "delta_mAP50", "delta_mAP50_95"])
        for design, s in (("stratified", strat_sum), ("unstratified", unstrat_sum)):
            a, b = s["mAP50"]["_draws"], s["mAP50_95"]["_draws"]
            for i in range(len(a)):
                w.writerow([design, i, f"{a[i]:.10f}", f"{b[i]:.10f}"])
        for i in range(len(boot_draws50)):
            w.writerow(["cluster_bootstrap", i, f"{boot_draws50[i]:.10f}", f"{boot_draws5095[i]:.10f}"])

    for s in (strat_sum, unstrat_sum):
        for k in s:
            s[k].pop("_draws", None)

    out = {
        "seed": SEED,
        "n_resamples": args.resamples,
        "headline": headline,
        "delta": delta,
        "cluster_bootstrap": boot,
        "randomization_stratified": strat_sum,
        "randomization_unstratified": unstrat_sum,
        "strata": {
            "n_strata": len(need),
            "definition": "dominant class (ties to the lower index) x instance-count bin (1, 2-3, 4-7, 8-15, >=16)",
            "need": {k: int(v) for k, v in sorted(need.items())},
            "nd_donors_available": {k: len(pool.get(k, [])) for k in sorted(need)},
            "strata_short_of_donors": shortfalls,
            "widenings_applied_first_replicate": strat.get("widenings", []),
        },
        "balance": balance_table(meta, d_images, strat["removed"]),
    }
    args.out.write_text(json.dumps(out, indent=2, default=float) + "\n")
    print(f"wrote {args.out} and {args.controls_csv}")


if __name__ == "__main__":
    main()
