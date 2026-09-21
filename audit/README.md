# Revision R1 audit

Everything needed to regenerate the numbers in the revised manuscript, in the
order they must be run.

The pre-registered analysis plan is `ANALYSIS_PLAN_R1.md` at the repository
root. It was committed before any environment was built or any new metric was
computed. Deviations are appended under its `DEVIATIONS` heading; the text above
that heading is never edited.

## Status

This audit is **incomplete**. See `results/PROGRESS.md` for what ran and what
did not, and `results/SUMMARY_R1.md` for the report. The short version: the
dataset-dependent phases are blocked because the Roboflow datasets are not on
this machine and `ROBOFLOW_API_KEY` is unset.

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
| `build_env.sh` | 0.1 | Builds one pinned venv. Run twice, once per ultralytics version. |
| `record_env.py` | 0.1 | Records python, torch, ultralytics, sahi, macOS, CPU and `torch.get_num_threads()` for a venv. Run with that venv's python. |
| `download_datasets.py` | 0.3 | Fetches the two pinned Roboflow versions — `oral-diseases-5ctay-h9oye` v1 and `oral-cancer-1mnve-n5yij` v2 — in yolov8 format. Version numbers are in the URL, so "latest" can never be resolved by accident. |
| `near_duplicates.py` | 0.4 | Regenerates the test-vs-train near-duplicate set under the published rule and writes it in the supplementary's S2 column format. |

## The duplicate rule, and the two traps in it

`near_duplicates.py` implements the published rule: 32x32 greyscale thumbnails
built with PIL draft mode then bilinear resampling, RMS difference on the 0-255
scale, the distance between two images taken as the **minimum over all 8
elements of the dihedral group**, and a pair accepted below **6.0**. That
threshold sits inside an empty band spanning [3.92, 10.01).

Two things are easy to get wrong here, and both have bitten this project:

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
