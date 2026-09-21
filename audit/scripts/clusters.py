"""Duplicate-graph clusters over the test split (spec Phase 2.1).

Nodes are the 1,500 test images. Edges come from two sources:

  (a) test-test near-duplicate pairs, under the same published rule;
  (b) two test images that share a training near-duplicate.

Clusters are the connected components. They are the resampling unit for the
cluster bootstrap in Phase 2.3: images inside one component are not independent,
so resampling individual images would understate the variance.

Note (b) needs the FULL set of training matches per test image, not the single
best-scoring partner that the S2 export records. Two test images can share a
training twin without either naming it as its argmin, and missing those edges
would split clusters that are really joined.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from near_duplicates import (
    THRESHOLD,
    TRANSFORMS,
    apply_transform,
    assert_transforms_distinct,
    build_bank,
    list_images,
)


def min_rms_matrix(query: np.ndarray, ref: np.ndarray, chunk: int = 512) -> np.ndarray:
    """(n_query, n_ref) matrix of min RMS over the dihedral group."""
    d = query.shape[1]
    ref_sq = (ref**2).sum(axis=1)[None, :]
    out = np.full((query.shape[0], ref.shape[0]), np.inf, dtype=np.float32)

    thumb_side = int(round(d**0.5))
    for _name, op in TRANSFORMS:
        if op is None:
            q_t = query
        else:
            q_t = np.stack([apply_transform(r.reshape(thumb_side, thumb_side), op).ravel() for r in query])
        q_sq = (q_t**2).sum(axis=1)[:, None]
        for s in range(0, query.shape[0], chunk):
            e = min(s + chunk, query.shape[0])
            d2 = q_sq[s:e] + ref_sq - 2.0 * (q_t[s:e] @ ref.T)
            np.maximum(d2, 0.0, out=d2)
            np.minimum(out[s:e], np.sqrt(d2 / d, dtype=np.float32), out=out[s:e])
    return out


def connected_components(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """Union-find, so the component count does not depend on edge order."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    groups: dict[int, list[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return sorted(groups.values(), key=lambda g: (-len(g), g[0]))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--test-dir", required=True, type=Path)
    ap.add_argument("--train-dir", required=True, type=Path)
    ap.add_argument("--d-csv", required=True, type=Path, help="regenerated D, to tag clusters")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--threshold", type=float, default=THRESHOLD)
    args = ap.parse_args()

    assert_transforms_distinct()

    test_paths = list_images(args.test_dir)
    train_paths = list_images(args.train_dir)
    print(f"test {len(test_paths)}  train {len(train_paths)}")

    test_bank = build_bank(test_paths)
    train_bank = build_bank(train_paths)

    # (b) shared training twin
    tt = min_rms_matrix(test_bank, train_bank)
    below_train = tt < args.threshold
    n_train_matches = below_train.sum(axis=1)

    edges: list[tuple[int, int]] = []
    shared_edges = 0
    for j in range(below_train.shape[1]):
        members = np.nonzero(below_train[:, j])[0]
        if members.size > 1:
            for k in range(1, members.size):
                edges.append((int(members[0]), int(members[k])))
                shared_edges += 1

    # (a) test-test duplicates
    ss = min_rms_matrix(test_bank, test_bank)
    np.fill_diagonal(ss, np.inf)  # an image is not its own duplicate
    ii, jj = np.nonzero(ss < args.threshold)
    tt_edges = 0
    for a, b in zip(ii, jj):
        if a < b:
            edges.append((int(a), int(b)))
            tt_edges += 1

    comps = connected_components(len(test_paths), edges)

    d_names = set()
    import csv

    with args.d_csv.open(newline="") as fh:
        for r in csv.DictReader(fh):
            d_names.add(r["test_image"])

    names = [p.name for p in test_paths]
    sizes: dict[int, int] = {}
    clusters = []
    for ci, comp in enumerate(comps):
        members = [names[i] for i in comp]
        n_d = sum(1 for m in members if m in d_names)
        clusters.append(
            {
                "cluster_id": ci,
                "size": len(members),
                "n_in_D": n_d,
                "contains_D": n_d > 0,
                "members": members,
            }
        )
        sizes[len(members)] = sizes.get(len(members), 0) + 1

    n_with_d = sum(1 for c in clusters if c["contains_D"])
    summary = {
        "n_test_images": len(test_paths),
        "n_clusters": len(clusters),
        "size_distribution": {str(k): sizes[k] for k in sorted(sizes)},
        "largest_cluster": max(c["size"] for c in clusters),
        "n_singletons": sizes.get(1, 0),
        "n_clusters_containing_D": n_with_d,
        "n_clusters_no_D": len(clusters) - n_with_d,
        "edges_from_shared_train_twin": shared_edges,
        "edges_from_test_test_duplicates": tt_edges,
        "test_images_with_any_train_match": int((n_train_matches > 0).sum()),
        "threshold": args.threshold,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"summary": summary, "clusters": clusters}, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
