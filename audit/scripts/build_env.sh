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

# Pin the two pieces of ambient state that otherwise leak between the venvs:
#   OMP_NUM_THREADS - ultralytics sets this to 1 at import time if it is unset,
#     so torch's CPU thread count would otherwise depend on import order (4 vs 1
#     on this machine). Threaded reductions are order-sensitive, and the Phase
#     1.2 exactness gate compares to 1e-9, so this must be fixed, not inherited.
#   YOLO_CONFIG_DIR - both versions otherwise share one global settings.json and
#     rewrite each other's schema, which defeats the point of a version comparison.
cat > "$VENV/pinned-env.sh" <<EOF
export OMP_NUM_THREADS=\${OMP_NUM_THREADS:-4}
export YOLO_CONFIG_DIR="$VENV/.yolo-config"
EOF
mkdir -p "$VENV/.yolo-config"

uv pip install --python "$VENV/bin/python" \
  "ultralytics==${UL_VERSION}" \
  "torch==2.7.1" "torchvision==0.22.1" \
  "sahi==0.11.15" \
  numpy scipy pandas scikit-learn pillow opencv-python-headless matplotlib
