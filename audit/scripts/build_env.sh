#!/usr/bin/env bash
# Build one of the two pinned evaluation environments (Phase 0.1).
# Usage: build_env.sh <ultralytics-version> <venv-path>
# Everything else is held identical between the two venvs so that the only
# difference is the ultralytics version (spec Phase 2.9 depends on that).
set -euo pipefail
UL_VERSION="$1"
VENV="$2"

uv venv --python 3.12 "$VENV"
export VIRTUAL_ENV="$VENV"

uv pip install --python "$VENV/bin/python" \
  "ultralytics==${UL_VERSION}" \
  "torch==2.7.1" "torchvision==0.22.1" \
  "sahi==0.11.15" \
  numpy scipy pandas scikit-learn pillow opencv-python-headless matplotlib
