"""Download the two pinned Roboflow dataset versions (spec Phase 0.3).

Pinned, never "latest", and never regenerating a version:
  segp-fcn6m/oral-diseases-5ctay-h9oye  version 1   (Model B, detection)
  segp-fcn6m/oral-cancer-1mnve-n5yij    version 2   (Model A, histopathology)

The API key is read from the environment variable ROBOFLOW_API_KEY and is never
printed, logged, or written to any file. It is passed to the API as a query
parameter, so the request URL itself is never echoed either.

Uses the REST API rather than the `roboflow` pip package so that the version is
pinned explicitly in the URL and no client-side "latest" resolution can occur.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

DATASETS = [
    {
        "key": "model_b",
        "workspace": "segp-fcn6m",
        "project": "oral-diseases-5ctay-h9oye",
        "version": 1,
        "format": "yolov8",
        "expect": {"train": 7000, "valid": 1500, "test": 1500},
    },
    {
        "key": "model_a",
        "workspace": "segp-fcn6m",
        "project": "oral-cancer-1mnve-n5yij",
        "version": 2,
        "format": "yolov8",
        "expect_total": 544,
    },
]


def get_key() -> str:
    key = os.environ.get("ROBOFLOW_API_KEY", "").strip()
    if not key:
        sys.exit(
            "ROBOFLOW_API_KEY is not set.\n"
            "Set it in your terminal, not in a chat window:\n"
            "    export ROBOFLOW_API_KEY=...\n"
        )
    return key


def fetch_export_link(ds: dict, key: str) -> str:
    url = (
        f"https://api.roboflow.com/{ds['workspace']}/{ds['project']}/{ds['version']}/{ds['format']}"
        f"?api_key={urllib.parse.quote(key)}"
    )
    with urllib.request.urlopen(url, timeout=120) as resp:
        payload = json.load(resp)
    link = payload.get("export", {}).get("link")
    if not link:
        # Never include the payload verbatim -- it can echo the key back.
        raise RuntimeError(
            f"no export link returned for {ds['project']} v{ds['version']}; "
            f"response keys: {sorted(payload)}"
        )
    return link


def download(link: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    zip_path = dest.with_suffix(".zip")
    with urllib.request.urlopen(link, timeout=1800) as resp, zip_path.open("wb") as fh:
        while chunk := resp.read(1 << 20):
            fh.write(chunk)
    return zip_path


def extract(zip_path: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest)


def count_images(root: Path) -> dict[str, int]:
    out = {}
    for split in ("train", "valid", "test"):
        d = root / split / "images"
        out[split] = len(list(d.glob("*"))) if d.is_dir() else 0
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-root", type=Path, default=Path("/Users/dev1/Desktop/Oral/r1-scratch/datasets"))
    ap.add_argument("--only", choices=["model_a", "model_b"], default=None)
    args = ap.parse_args()

    key = get_key()
    report = {}

    for ds in DATASETS:
        if args.only and ds["key"] != args.only:
            continue
        dest = args.out_root / ds["key"]
        print(f"=== {ds['project']} v{ds['version']} ({ds['format']}) -> {dest}")
        if dest.exists() and any(dest.iterdir()):
            print("   already present, skipping download")
        else:
            link = fetch_export_link(ds, key)
            zip_path = download(link, dest)
            sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
            print(f"   zip sha256 {sha}")
            extract(zip_path, dest)
        counts = count_images(dest)
        total = sum(counts.values())
        print(f"   counts {counts}  total {total}")
        report[ds["key"]] = {
            "project": ds["project"],
            "version": ds["version"],
            "counts": counts,
            "total": total,
            "path": str(dest),
        }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
