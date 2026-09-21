#!/usr/bin/env bash
# Phases 2-4 in order, after the caches exist. Each step is skipped if its
# output is already present, so the script can be re-run after an interruption.
set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRATCH="${R1_SCRATCH:-/Users/dev1/Desktop/Oral/r1-scratch}"
V1="$SCRATCH/venvs/ul8.3.231"
V2="$SCRATCH/venvs/ul8.4.118"
D="$SCRATCH/datasets"
C="$SCRATCH/work/caches"
CACHES_DIR="$C"
R="$REPO/audit/results"
cd "$REPO"
export PYTHONPATH="$REPO/audit/scripts"
. "$V1/pinned-env.sh"

step() { printf '\n======== %s ========\n' "$*"; }
have() { [ -s "$1" ]; }

# The train and valid caches may still be building when this starts. Wait for
# them rather than failing three steps in. The bracket keeps the pattern from
# matching this script's own command line.
wait_for() {
  local f="$1" waited=0
  while [ ! -s "$f" ]; do
    if ! ps -eo command | grep -q '[c]ached_evaluator.py'; then
      echo "MISSING $f and no cache build running -- aborting"; exit 1
    fi
    sleep 15; waited=$((waited+15))
    [ $((waited % 120)) -eq 0 ] && echo "  still waiting for $(basename "$f") (${waited}s)"
  done
}
for f in test_b1 valid_b1 train_b1; do wait_for "$CACHES_DIR/$f.pkl"; done
echo "all caches present"

# ---------------------------------------------------------------- 2.7 pairs
step "valid-vs-train near duplicates (S7)"
if have "$R/S7_valid_train_pairs.csv"; then echo "skip"; else
caffeinate -i "$V1/bin/python" audit/scripts/near_duplicates.py \
  --query-dir "$D/model_b/valid/images" --ref-dir "$D/model_b/train/images" \
  --out-csv "$R/S7_valid_train_pairs.csv" 2>&1 | tail -22
fi

# ---------------------------------------------------------------- 2.2-2.4
step "contamination statistics (2.2, 2.3, 2.4)"
if have "$R/S29_contamination_stats.json"; then echo "skip"; else
caffeinate -i "$V1/bin/python" audit/scripts/contamination_stats.py \
  --cache "$C/test_b1.pkl" --d-csv "$R/S2_regenerated_test_train_pairs.csv" \
  --clusters "$R/S25_clusters.json" --out "$R/S29_contamination_stats.json" \
  --controls-csv "$R/S30_control_deltas.csv" 2>&1 | tail -12
fi

# ---------------------------------------------------------------- 2.6
step "memorisation diagnostics (2.6)"
if have "$R/S31_memorisation.json"; then echo "skip"; else
caffeinate -i "$V1/bin/python" audit/scripts/memorisation.py \
  --test-cache "$C/test_b1.pkl" --test-boxes "$C/test_b1_boxes.pkl" \
  --train-cache "$C/train_b1.pkl" --train-boxes "$C/train_b1_boxes.pkl" \
  --valid-cache "$C/valid_b1.pkl" \
  --d-csv "$R/S2_regenerated_test_train_pairs.csv" \
  --out "$R/S31_memorisation.json" \
  --draw-dir "$SCRATCH/work/concordance_pairs" 2>&1 | tail -12
fi

# ---------------------------------------------------------------- 2.5, 2.7
step "per-class contrasts and validation contamination (2.5, 2.7)"
if have "$R/S32_secondary.json"; then echo "skip"; else
caffeinate -i "$V1/bin/python" audit/scripts/phase2_secondary.py \
  --test-cache "$C/test_b1.pkl" --valid-cache "$C/valid_b1.pkl" \
  --d-csv "$R/S2_regenerated_test_train_pairs.csv" \
  --valid-dup-csv "$R/S7_valid_train_pairs.csv" \
  --clusters "$R/S25_clusters.json" --out "$R/S32_secondary.json" 2>&1 | tail -14
fi

# ---------------------------------------------------------------- 2.9
step "library version comparison, ultralytics 8.4.118 (2.9)"
if have "$R/S33_version_8.4.118.json"; then echo "skip"; else
(
  . "$V2/pinned-env.sh"
  caffeinate -i "$V2/bin/python" audit/scripts/cached_evaluator.py \
    --weights "$REPO/ml_models/model_b/models/best.pt" --data "$D/model_b/data.yaml" \
    --split test --batch 1 --out "$C/test_b1_ul84.pkl" 2>&1 | tail -3
  caffeinate -i "$V2/bin/python" - <<'PY' 2>&1 | tail -20
import csv, json
from pathlib import Path
from cached_evaluator import Evaluator, real_val
ev = Evaluator.load(Path("/Users/dev1/Desktop/Oral/r1-scratch/work/caches/test_b1_ul84.pkl"))
allimg = ev.images()
by = {Path(p).name: p for p in allimg}
d = {r["test_image"] for r in csv.DictReader(open("audit/results/S2_regenerated_test_train_pairs.csv"))}
nd = sorted(set(allimg) - {by[n] for n in d})
A, N = ev.evaluate(allimg), ev.evaluate(nd)
b16 = real_val("ml_models/model_b/models/best.pt",
               Path("/Users/dev1/Desktop/Oral/r1-scratch/datasets/model_b/data.yaml"),
               split="test", batch=16)
out = {
 "ultralytics": "8.4.118",
 "full_batch1": {k: A[k] for k in ("n_images","n_instances","P","R","mAP50","mAP50_95")},
 "ND_batch1":   {k: N[k] for k in ("n_images","n_instances","P","R","mAP50","mAP50_95")},
 "full_batch16":{k: b16[k] for k in ("n_images","n_instances","P","R","mAP50","mAP50_95")},
 "delta_ND_minus_All": {"mAP50": N["mAP50"]-A["mAP50"], "mAP50_95": N["mAP50_95"]-A["mAP50_95"]},
 "per_class_full": A["per_class"],
}
Path("audit/results/S33_version_8.4.118.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps({k: out[k] for k in ("full_batch1","ND_batch1","full_batch16","delta_ND_minus_All")}, indent=2))
PY
)
fi

# ---------------------------------------------------------------- 3.3, 3.4
step "end-to-end over the 1,500 test images (3.3, 3.4)"
if have "$R/S34_end_to_end_test.json"; then echo "skip"; else
caffeinate -i "$V1/bin/python" audit/scripts/end_to_end.py \
  --repo "$REPO" --images "$D/model_b/test/images" --labels "$D/model_b/test/labels" \
  --out "$R/S34_end_to_end_test.json" --tag test 2>&1 | tail -40
fi

# ---------------------------------------------------------------- 3.5
step "router evaluation on three sets (3.5)"
if have "$R/S35_router_eval.json"; then echo "skip"; else
caffeinate -i "$V1/bin/python" audit/scripts/router_eval.py \
  --repo "$REPO" --test-dir "$D/model_b/test/images" \
  --model-a-root "$D/model_a" --coco128 "$SCRATCH/work/coco128" \
  --out "$R/S35_router_eval.json" 2>&1 | tail -14
fi

# ---------------------------------------------------------------- 4.1
step "Model A reproduction with the deployed checkpoint (4.1)"
if have "$R/S36_model_a_reproduction.json"; then echo "skip"; else
caffeinate -i "$V1/bin/python" audit/scripts/model_a_reproduce.py \
  --dataset "$D/model_a" --weights "$REPO/ml_models/model_a/model_a.pth" \
  --s5 "$R/reference/S5_histopathology_leaked_validation.csv" \
  --out "$R/S36_model_a_reproduction.json" \
  --scores-csv "$R/S37_model_a_per_image_scores.csv" 2>&1 | tail -20
fi

step "DONE"
ls -la "$R" | tail -25
