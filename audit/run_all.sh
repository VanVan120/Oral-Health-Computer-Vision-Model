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
# NOTE: this revision is incomplete. The steps below are the ones that exist.
# The phases that are still blocked are listed at the bottom, and the script
# says so rather than pretending to have run them.
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
cat <<'EOF'

=== NOT YET IMPLEMENTED ===

The following phases have no script in this directory yet, because they were
blocked before they could be written and tested against real data:

  Phase 1    cached exact evaluator and its 1e-9 exactness gate
  Phase 2    contamination statistics (clusters, bootstrap, randomization,
             per-class contrasts, memorisation diagnostics, validation
             contamination, photometric tier, library-version comparison)
  Phase 3.3  full end-to-end run over the 1,500 test images
  Phase 3.4  user-facing image-level metrics
  Phase 3.5  router evaluation on the three sets
  Phase 4    histopathology reproduction and source audit
  Phase 5.3  warm-start overlap measurement
  Phase 5.4  dataset lineage from the Roboflow API

See audit/results/PROGRESS.md and audit/results/SUMMARY_R1.md.
EOF
