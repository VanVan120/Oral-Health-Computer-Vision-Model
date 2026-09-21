#!/usr/bin/env bash
#
# Regenerate audit/results/ from the datasets and the weights.
#
# Run from the repository root:
#     bash audit/run_all.sh
#
# Long steps are wrapped in `caffeinate -i` so the Mac does not sleep partway
# through. Every step is idempotent: re-running skips work already on disk.
#
# Needs ROBOFLOW_API_KEY in the environment (never in a chat window) and the
# git-lfs objects fetched. Stops with an explicit message if either is missing.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRATCH="${R1_SCRATCH:-/Users/dev1/Desktop/Oral/r1-scratch}"
VENV_MAIN="$SCRATCH/venvs/ul8.3.231"
VENV_ALT="$SCRATCH/venvs/ul8.4.118"
DATA="$SCRATCH/datasets"
RESULTS="$REPO_ROOT/audit/results"
ENVDIR="$REPO_ROOT/audit/env"

cd "$REPO_ROOT"
mkdir -p "$RESULTS" "$ENVDIR" "$SCRATCH"/{datasets,venvs,work}

step() { printf '\n=== %s ===\n' "$*"; }
die()  { printf '\nSTOP: %s\n' "$*" >&2; exit 1; }

# --------------------------------------------------------------------------
step "0.2  weights"
# --------------------------------------------------------------------------
BEST=ml_models/model_b/models/best.pt
if head -c 40 "$BEST" | grep -q 'version https://git-lfs'; then
  echo "weights are LFS pointers; fetching"
  git lfs install --local
  git lfs pull
fi
shasum -a 256 "$BEST" ml_models/model_a/model_a.pth ml_models/model_triage/triage_router.pth \
  | tee "$ENVDIR/weight-sha256.txt"

BEST_SHA="$(shasum -a 256 "$BEST" | cut -d' ' -f1)"
case "$BEST_SHA" in
  4de8714f*7aad0cc) echo "best.pt identity: MATCH" ;;
  *) die "best.pt is $BEST_SHA, which is not the released checkpoint (expected 4de8714f...7aad0cc)" ;;
esac

# --------------------------------------------------------------------------
step "0.1  environments"
# --------------------------------------------------------------------------
[ -x "$VENV_MAIN/bin/python" ] || bash audit/scripts/build_env.sh 8.3.231 "$VENV_MAIN"
[ -x "$VENV_ALT/bin/python" ]  || bash audit/scripts/build_env.sh 8.4.118 "$VENV_ALT"

uv pip freeze --python "$VENV_MAIN/bin/python" > "$ENVDIR/lock-ul8.3.231.txt"
uv pip freeze --python "$VENV_ALT/bin/python"  > "$ENVDIR/lock-ul8.4.118.txt"
"$VENV_MAIN/bin/python" audit/scripts/record_env.py > "$ENVDIR/env-ul8.3.231.json"
"$VENV_ALT/bin/python"  audit/scripts/record_env.py > "$ENVDIR/env-ul8.4.118.json"

# --------------------------------------------------------------------------
step "0.3  datasets"
# --------------------------------------------------------------------------
if [ -z "${ROBOFLOW_API_KEY:-}" ]; then
  die "ROBOFLOW_API_KEY is unset.
     Export it in a terminal, never in a chat window:
         export ROBOFLOW_API_KEY=...
     Everything from here on needs the image data."
fi
caffeinate -i "$VENV_MAIN/bin/python" audit/scripts/download_datasets.py --out-root "$DATA"

# Identity gates. These are hard stops: the whole audit is about whether the
# evaluated data is the data the manuscript claims, so a mismatch invalidates
# every number downstream.
count() { find "$1" -type f \( -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' \) 2>/dev/null | wc -l | tr -d ' '; }
B_TRAIN=$(count "$DATA/model_b/train/images")
B_VALID=$(count "$DATA/model_b/valid/images")
B_TEST=$(count "$DATA/model_b/test/images")
echo "Model B: train $B_TRAIN  valid $B_VALID  test $B_TEST"
[ "$B_TRAIN" = 7000 ] && [ "$B_VALID" = 1500 ] && [ "$B_TEST" = 1500 ] \
  || die "Model B split is $B_TRAIN/$B_VALID/$B_TEST, expected 7000/1500/1500"

B_INST=$(cat "$DATA"/model_b/test/labels/*.txt 2>/dev/null | grep -c . || true)
echo "Model B test instances: $B_INST"
[ "$B_INST" = 9688 ] || die "Model B test instances are $B_INST, expected 9688"

A_TOTAL=$(( $(count "$DATA/model_a/train/images") + $(count "$DATA/model_a/valid/images") + $(count "$DATA/model_a/test/images") ))
echo "Model A total: $A_TOTAL"
[ "$A_TOTAL" = 544 ] || die "Model A has $A_TOTAL images, expected 544 (474/44/26)"

# --------------------------------------------------------------------------
step "0.4  near-duplicate regeneration"
# --------------------------------------------------------------------------
caffeinate -i "$VENV_MAIN/bin/python" audit/scripts/near_duplicates.py \
  --query-dir "$DATA/model_b/test/images" \
  --ref-dir   "$DATA/model_b/train/images" \
  --out-csv   "$RESULTS/S2_regenerated_test_train_pairs.csv" \
  | tee "$RESULTS/S2_regenerated_summary.json"

# Must reproduce the published sets exactly, as sets of test images.
"$VENV_MAIN/bin/python" - <<'PY'
import csv, pathlib, sys
res = pathlib.Path("audit/results")
def col(path, name, pred=lambda r: True):
    with open(path, newline="") as fh:
        return {r[name] for r in csv.DictReader(fh) if pred(r)}

new_259 = col(res/"S2_regenerated_test_train_pairs.csv", "test_image")
new_124 = col(res/"S2_regenerated_test_train_pairs.csv", "test_image",
              lambda r: r["also_found_by_aligned_only"] == "yes")
ref_259 = col(res/"reference/S2_orientation_duplicate_pairs.csv", "test_image")
ref_124 = col(res/"reference/S1_aligned_duplicate_pairs.csv", "test_image")

ok = True
for label, new, ref in (("S2 (259)", new_259, ref_259), ("S1 (124)", new_124, ref_124)):
    if new == ref:
        print(f"{label}: MATCH ({len(new)})")
    else:
        ok = False
        print(f"{label}: MISMATCH  regenerated {len(new)} vs published {len(ref)}")
        print(f"   only regenerated: {sorted(new - ref)[:10]}")
        print(f"   only published:   {sorted(ref - new)[:10]}")
sys.exit(0 if ok else 1)
PY

# --------------------------------------------------------------------------
step "1.1  cached evaluator, test / valid / train at batch 1"
# --------------------------------------------------------------------------
CACHES="$SCRATCH/work/caches"; mkdir -p "$CACHES"
export PYTHONPATH="$REPO_ROOT/audit/scripts"
. "$VENV_MAIN/pinned-env.sh"
# Roboflow names the validation split "val" in data.yaml, not "valid".
for split in test val train; do
  [ -s "$CACHES/${split/val/valid}_b1.pkl" ] || caffeinate -i "$VENV_MAIN/bin/python" audit/scripts/cached_evaluator.py \
     --weights "$BEST" --data "$DATA/model_b/data.yaml" --split "$split" --batch 1 \
     --out "$CACHES/${split/val/valid}_b1.pkl" --boxes-out "$CACHES/${split/val/valid}_b1_boxes.pkl"
done

# --------------------------------------------------------------------------
step "1.2  exactness gate (1e-9)"
# --------------------------------------------------------------------------
caffeinate -i "$VENV_MAIN/bin/python" audit/scripts/exactness_gate.py \
  --cache "$CACHES/test_b1.pkl" --weights "$BEST" --data "$DATA/model_b/data.yaml" \
  --d-csv "$RESULTS/S2_regenerated_test_train_pairs.csv" \
  --work "$SCRATCH/work/subsets" --out "$RESULTS/S24_exactness_gate.json"
"$VENV_MAIN/bin/python" -c 'import json,sys; d=json.load(open("audit/results/S24_exactness_gate.json")); print("exactness gate: PASS") if d["all_pass"] else sys.exit("EXACTNESS GATE FAILED -- do not proceed to any statistics")'

# --------------------------------------------------------------------------
step "1.3  batch sensitivity: val(batch=16) on the full split"
# --------------------------------------------------------------------------
[ -s "$RESULTS/S28_batch16_full_split.json" ] || caffeinate -i "$VENV_MAIN/bin/python" -c '
import json, sys; sys.path.insert(0,"audit/scripts")
from pathlib import Path
from cached_evaluator import real_val
import os
r = real_val("ml_models/model_b/models/best.pt", Path(os.environ["DATA"]+"/model_b/data.yaml"), split="test", batch=16)
Path("audit/results/S28_batch16_full_split.json").write_text(json.dumps(r, indent=2)+"\n")'

# --------------------------------------------------------------------------
step "5.1 - 5.2  checkpoint metadata, both detector checkpoints"
# --------------------------------------------------------------------------
# Reads the released best.pt and the superseded warm-start object fetched from
# LFS history. Needs no dataset, only the weights.
[ -s "$RESULTS/S10_best_pt_metadata.json" ] || "$VENV_MAIN/bin/python" audit/scripts/checkpoint_metadata.py \
  --weights ml_models/model_b/models/best.pt > "$RESULTS/S10_best_pt_metadata.json"
# The superseded warm start is not a working-tree file; fetch it from LFS history
# first (see S15) and point --weights at the extracted object to regenerate S14.

# --------------------------------------------------------------------------
step "4.1(3)  Model A metrics from the notebook's stored outputs"
# --------------------------------------------------------------------------
# Transcribes and recomputes from the confusion matrices the notebook stored.
# Distinct from 4.1(1)-(2), which RUN model_a.pth (in run_remaining.sh).
[ -s "$RESULTS/S20_model_a_classifier_metrics.json" ] || "$VENV_MAIN/bin/python" \
  audit/scripts/model_a_classifier_metrics.py > "$RESULTS/S20_model_a_classifier_metrics.json"

# --------------------------------------------------------------------------
step "2.1  duplicate-graph clusters"
# --------------------------------------------------------------------------
[ -s "$RESULTS/S25_clusters.json" ] || caffeinate -i "$VENV_MAIN/bin/python" audit/scripts/clusters.py \
  --test-dir "$DATA/model_b/test/images" --train-dir "$DATA/model_b/train/images" \
  --d-csv "$RESULTS/S2_regenerated_test_train_pairs.csv" --out "$RESULTS/S25_clusters.json"

# --------------------------------------------------------------------------
step "2.2 - 4.1  everything downstream"
# --------------------------------------------------------------------------
bash audit/scripts/run_remaining.sh

# --------------------------------------------------------------------------
step "2.8  photometric tier (sensitivity analysis)"
# --------------------------------------------------------------------------
[ -s "$RESULTS/S38_photometric_tier.json" ] || caffeinate -i "$VENV_MAIN/bin/python" audit/scripts/photometric_tier.py \
  --test-dir "$DATA/model_b/test/images" --train-dir "$DATA/model_b/train/images" \
  --d-csv "$RESULTS/S2_regenerated_test_train_pairs.csv" \
  --out "$RESULTS/S38_photometric_tier.json" --tier-csv "$RESULTS/S39_photometric_pairs.csv"

# --------------------------------------------------------------------------
step "3.2  regression tests"
# --------------------------------------------------------------------------
echo "run the pytest suite in an environment carrying the app requirements:"
echo "  GEMINI_API_KEY=test JWT_SECRET_KEY=test <venv>/bin/python -m pytest tests/ -v"

# --------------------------------------------------------------------------
step "6.3  expert-review packet (scratchpad only, never committed)"
# --------------------------------------------------------------------------
"$VENV_MAIN/bin/python" audit/scripts/expert_packet.py \
  --test-images "$DATA/model_b/test/images" --test-labels "$DATA/model_b/test/labels" \
  --model-a-root "$DATA/model_a" --dest "$SCRATCH/work/expert_packet"

step "ALL DONE"
echo "summary: $RESULTS/SUMMARY_R1.md"
