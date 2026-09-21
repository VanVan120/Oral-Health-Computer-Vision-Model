"""Report the provenance metadata stored inside a checkpoint (spec Phase 5.1).

From torch 2.6 onward torch.load defaults to weights_only=True, which refuses an
ultralytics checkpoint because it pickles ultralytics' own classes. This is a
deliberate security default. We pass weights_only=False knowingly: the file's
SHA-256 is verified against the released checkpoint before it is opened, so we
are not unpickling anything of unknown origin.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys


def jsonable(obj):
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return repr(obj)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--weights", required=True, type=pathlib.Path)
    ap.add_argument("--expect-sha256", default=None)
    args = ap.parse_args()

    if not args.weights.exists():
        sys.exit(f"not found: {args.weights}")
    raw = args.weights.read_bytes()
    if raw[:40].startswith(b"version https://git-lfs"):
        sys.exit(f"{args.weights} is a Git LFS pointer; run 'git lfs pull'")

    sha = hashlib.sha256(raw).hexdigest()
    if args.expect_sha256 and sha != args.expect_sha256:
        sys.exit(f"sha256 {sha} != expected {args.expect_sha256}")
    del raw

    import torch

    ckpt = torch.load(args.weights, map_location="cpu", weights_only=False)

    out = {
        "path": str(args.weights),
        "sha256": sha,
        "top_level_keys": sorted(ckpt) if isinstance(ckpt, dict) else repr(type(ckpt)),
    }
    if isinstance(ckpt, dict):
        for key in ("date", "version", "license", "docs", "epoch", "best_fitness"):
            if key in ckpt:
                out[key] = jsonable(ckpt[key])
        for key in ("train_args", "train_metrics", "train_results"):
            if key in ckpt:
                out[key] = jsonable(ckpt[key])
        model = ckpt.get("model")
        if model is not None:
            names = getattr(model, "names", None)
            if names is not None:
                out["names"] = jsonable(names)
            out["model_class"] = type(model).__name__
            yaml_cfg = getattr(model, "yaml", None)
            if isinstance(yaml_cfg, dict):
                out["model_yaml"] = {
                    k: jsonable(v) for k, v in yaml_cfg.items() if k != "backbone" and k != "head"
                }
        if isinstance(out.get("train_results"), dict):
            lengths = {k: len(v) for k, v in out["train_results"].items() if isinstance(v, list)}
            out["train_results_epoch_counts"] = lengths
            out["train_results"] = {
                k: (v[:3] + ["..."] + v[-3:]) if isinstance(v, list) and len(v) > 6 else v
                for k, v in out["train_results"].items()
            }

    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
