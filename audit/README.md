# Revision R1 audit

Everything needed to regenerate the numbers in the revised manuscript, in the
order they must be run.

The pre-registered analysis plan is `ANALYSIS_PLAN_R1.md` at the repository
root. It was committed before any environment was built or any new metric was
computed. Deviations are appended under its `DEVIATIONS` heading; the text above
that heading is never edited.

## Status

See `results/SUMMARY_R1.md` for the report and `results/PROGRESS.md` for the
run log. Anything not done is listed under UNFINISHED in the summary, with the
reason.

## Layout

    env/        environment locks and hashes
    scripts/    the analysis scripts, described below
    results/    every derived number, plus the reference sets
    run_all.sh  regenerates results/ from the datasets and weights

## Prerequisites

1. **Weights.** `git lfs install --local && git lfs pull`. The three checkpoints
   are stored as LFS objects; a plain clone leaves 133-byte pointer files in
   their place, and every script that needs them fails with a message saying so
   rather than loading a pointer as a model.

2. **The Roboflow key**, exported in a terminal, never pasted into a chat:

       export ROBOFLOW_API_KEY=...

   It is read from the environment only. No script prints it, logs it, or
   writes it to a file.

3. **The environments.** Two venvs that differ only in the ultralytics version:

       bash scripts/build_env.sh 8.3.231 <scratch>/venvs/ul8.3.231
       bash scripts/build_env.sh 8.4.118 <scratch>/venvs/ul8.4.118

   All headline figures come from **8.3.231 on CPU**, FP32, imgsz 640,
   conf 0.001, NMS IoU 0.7, max_det 300, batch 1. 8.4.118 is used only for the
   library-version comparison. Never compare a number from one venv with a
   number from the other except in that comparison, and never compare an
   mAP@0.5 figure with an mAP@0.5:0.95 figure.

## Scripts, in run order

| script | phase | what it does |
|---|---|---|
| `build_env.sh` | 0.1 | Builds one pinned venv, and writes a `pinned-env.sh` that fixes `OMP_NUM_THREADS` and gives the venv its own `YOLO_CONFIG_DIR`. Run twice, once per ultralytics version. |
| `record_env.py` | 0.1 | Records python, torch, ultralytics, sahi, macOS, CPU and `torch.get_num_threads()` for a venv. |
| `checkpoint_metadata.py` | 5.1 | Reads a checkpoint's `date`, `version`, `train_args`, `train_metrics`, `train_results` and `names`, after verifying its SHA-256. |
| `download_datasets.py` | 0.3, 5.4 | Fetches the two pinned Roboflow versions — `oral-diseases-5ctay-h9oye` v1 and `oral-cancer-1mnve-n5yij` v2 — in yolov8 format, and the project metadata for the lineage question. Version numbers are in the URL, so "latest" can never be resolved by accident. |
| `near_duplicates.py` | 0.4, 2.7 | Regenerates a near-duplicate set under the published rule, in the supplementary's S2 column format. Used for test-vs-train and valid-vs-train. |
| `clusters.py` | 2.1 | Builds the duplicate graph over the test split and its connected components, the resampling unit for the cluster bootstrap. |
| `cached_evaluator.py` | 1.1 | Captures, per image, exactly the arrays ultralytics' validator feeds its metric accumulator, and replays any subset through the same metric function. Works under both pinned ultralytics versions. |
| `exactness_gate.py` | 1.2 | Compares the cached evaluator against real `val(batch=1)` runs on four image sets, to 1e-9. |
| `contamination_stats.py` | 2.2–2.4 | Headline table, removal effect with a cluster-bootstrap CI, and both randomization designs with a balance table and the MDE. |
| `memorisation.py` | 2.6 | Train/valid/test comparison, annotation concordance against the training twin, recall against own-versus-twin labels, and M on the twins. |
| `phase2_secondary.py` | 2.5, 2.7 | Per-class D-versus-ND contrasts at `t_global` and the deployed thresholds, and validation-split contamination. |
| `photometric_tier.py` | 2.8 | The brightness/contrast-invariant tier, verified at full resolution against a random-pair null. |
| `end_to_end.py` | 3.3, 3.4 | Drives the deployed chain offline, records which of the router's four exit paths each image takes, and replays the 7210dea path in full and mapping-only form. |
| `router_eval.py` | 3.5 | The router on the three sets, with Wilson intervals and gate rejections separated from softmax rejections. |
| `model_a_reproduce.py` | 4.1 | Reproduces the pooling and split, runs `model_a.pth`, and reports the classifier and regression statistics with per-image scores. |
| `model_a_classifier_metrics.py` | 4.1 | Exact statistics from a stored 2×2 table alone. |
| `expert_packet.py` | 6.3 | Builds the expert-review packet in the scratchpad. Never writes into the repository. |
| `run_remaining.sh` | 2–4 | Runs the analysis steps in order; each is skipped if its output exists. |

## The duplicate rule, and the three traps in it

`near_duplicates.py` implements the published rule: 32x32 greyscale thumbnails,
bilinear resampling, RMS difference on the 0-255 scale, the distance between two
images taken as the **minimum over all 8 elements of the dihedral group**, and a
pair accepted below **6.0**. That threshold sits inside an empty band spanning
[3.92, 10.01), which is why the sets reproduce exactly despite small numerical
differences in the distances themselves.

Three things are easy to get wrong here, and all three have bitten this project:

1. **`Image.FLIP_LEFT_RIGHT == 0`.** A truthiness test on the PIL transpose
   constant silently skips the horizontal flip. The August sweep did exactly
   that. Horizontal flip turns out to be the single largest contributor — 150 of
   the 259 images qualify under it — so the bug is expensive and silent.
   `assert_transforms_distinct()` runs before any matching and fails loudly if
   any transform leaves a probe thumbnail unchanged, or if two transforms
   coincide.

2. **The identity subset is not "best transform == identity".** 124 test images
   fall below threshold under the identity transform, but for 61 of them some
   reflection scores lower still, so identity is the single best transform for
   only 63. Filtering the dihedral output on `matching_transform == identity`
   therefore yields 63, and understates the fixed-alignment set by half. The
   script runs a second, identity-only pass and records the result per row as
   `also_found_by_aligned_only`, which is the column the published S2 uses and
   the one that reproduces S1 exactly.

3. **PIL draft mode breaks reflected matching.** `draft()` asks libjpeg for a
   DCT-scaled decode at one pixel per 8x8 block. Where a dimension is not a
   multiple of 8 the encoder padded the final block, and that padding sits only
   on the right and bottom edges, so the thumbnail carries an asymmetric edge
   artifact that does not commute with reflection. These images are 612x408 and
   612 = 76*8 + 4. With draft on, 31 of the 259 pairs vanish and the mean
   absolute deviation from the published distances goes from 0.145 to 2.793; on
   one pair, rot180 scores 6.9408 with draft and 0.3903 without, the latter
   being exactly the published value. `USE_DRAFT = False`, deliberately, with
   the reasoning recorded at the call site. The spec describes the published
   rule as using draft mode; it demonstrably cannot have been in force, most
   likely because the original call sat after the image was already loaded,
   where `draft()` is a no-op.

## Reference sets

`results/reference/` holds the as-submitted supplementary material (S0-S5),
copied verbatim, with `PROVENANCE.md` recording where it came from. These are
the comparison target for the identity checks in Phase 0.4, not an output of
this revision. Nothing in that directory was regenerated.

## Conventions

- Every number carries its evaluator and its environment. Numbers produced by
  different evaluators or environments are never compared.
- `M` means mAP@0.5 or mAP@0.5:0.95. The two are analysed separately and never
  compared with each other.
- Seed 20260921 for every resampling procedure.
- Anything inferred rather than measured is labelled as inferred, at the point
  where it is reported.
