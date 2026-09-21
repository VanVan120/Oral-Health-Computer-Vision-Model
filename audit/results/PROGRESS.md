# Revision R1 progress log

Append-only. Resume from the last entry if the session dies.

## Phase 0.0 — plan commit (DONE)

- Branch `revision-r1` created from `main` @ 5b815bb8e7f873f6e11771c55af12c3e7598d506.
- `ANALYSIS_PLAN_R1.md` = Appendix A of revision-analysis-spec.md, verbatim
  (spec lines 392-473, byte-identical, verified by diff).
- Commit: 12f3199e0669565b35fe663e3b9bc6fe993cc3a7
- ISO timestamp (author == committer): 2026-09-21T21:25:17+08:00
- Pushed to origin/revision-r1: YES

## Phase 0.2 — weights (DONE, PASS)

- git-lfs 3.8.0 installed via brew; `git lfs install --local`; `git lfs pull` OK
  (no bandwidth-quota failure). All three weight files were LFS pointers before
  the pull.
- SHA-256, and each equals its committed LFS pointer oid:
  - best.pt            4de8714f0f2b52a70564cc1be55058262564ced400cd8a7d5815192477aad0cc
  - model_a.pth        b469110a551aa4bb93189b05a424fa28239dc4f710983e779b41acf7a19a2d3f
  - triage_router.pth  59cb5a8d8445927a92b0fd0d502fc56b650a16c1a9be94246bc2d2115088f5e2
- best.pt starts 4de8714f and ends 7aad0cc as the spec requires: MATCH. No STOP.

## Phase 0.3 / 0.4 — datasets and duplicate lists (BLOCKED, partial)

**Evidence folder: FOUND.** Not on the Desktop as the spec expected, but at
`~/Documents/SEGP Journal/Supplementary-Material.zip`. Copied verbatim to
`audit/results/reference/` with `PROVENANCE.md`. Contains S0-S5. So the spec's
"if you cannot find it, ask" does not trigger.

Verified against the published S0 README, all exact:
- S1 = 124 rows / 124 unique test images
- S2 = 259 rows / 259 unique test images
- S2 best-transform tally hflip 85, vflip 74, identity 63, rot180 37 = 259
- S1 is a subset of S2, and S1 == the 124 S2 rows with
  also_found_by_aligned_only = yes
- S1 != the 63 S2 rows with matching_transform = identity  <-- see below
- S4 per-class test instances sum to exactly 9,688
- Class order, confirmed independently by S4 and by the committed
  BoxF1_curve.png legend: 0 calculus, 1 caries, 2 gingivitis, 3 hypodontia,
  4 tooth_discolation, 5 ulcer

**Correction to spec check 0.4.3.** The spec says D's "identity-only subset must
equal S1 (124)". Filtering S2 on matching_transform == identity gives 63, not
124, because for 61 of the 124 images that fall below threshold under identity,
some reflection scores lower still. The S0 README states the correct filter
explicitly. `audit/scripts/near_duplicates.py` now runs two passes -- full
dihedral and identity-only -- and reports both, so the 124 and the 259 are both
recoverable and directly diffable against S1 and S2.

**BLOCKED at 0.3.** The August scratchpad
`/private/tmp/claude-501/-Users-dev1-Desktop-Oral/c5e9d423-.../scratchpad/` no
longer exists (the whole per-project temp directory is gone). No Roboflow export
exists anywhere on this machine -- searched for data.yaml, README.roboflow.txt
and README.dataset.txt across $HOME, /private/tmp and /Volumes: zero hits.
So the datasets must be re-downloaded, which needs ROBOFLOW_API_KEY, which is
**unset**. Ground rule 5 says STOP. `audit/scripts/download_datasets.py` is
written and ready; it reads the key from the environment only and never prints it.

## Phase 5.4 — lineage (PARTIAL, blocked)

universe.roboflow.com returns HTTP 403 to non-browser clients and
api.roboflow.com needs the key, so the fork/source question is unresolved. See
`audit/results/S8_lineage_partial.md`. Search-index evidence is consistent with
reference 8 (tesisdientes/oral-diseases-5ctay-rqpxs) having 4 classes and ~4.2k
images, versus 6 classes and 10,000 in the project actually used.

## Phases 0.1, 0.2, 3.1, 3.2, 4.1(3), 4.3, 5.1, 5.2, 5.5, 5.6 — DONE

See SUMMARY_R1.md for every number. Files S8-S21 in this directory.

- 0.1 both venvs built and recorded; three environment hazards found, two fixed
  (thread-count pinning, per-venv YOLO_CONFIG_DIR).
- 0.2 weights fetched and verified; best.pt MATCHES. `git lfs fetch --all`
  succeeded, so both superseded checkpoints were read too.
- 3.1 request path traced in full. 3.2 test added; 39 passed, 6 skipped.
- 3.3 pre-fix permutation recovered verbatim; five of six classes wrong.
- 4.1(3) stored outputs verified: confusion matrix and AUC both MATCH.
  4.1(4) computed analytically from the 2x2 table.
- 4.3 R2 convention answered. 5.1/5.2/5.3 provenance; warm start identified.
- 5.5 all four independence questions answered. 5.6 chronology built.

## BLOCKED — waiting on the human

Two things are needed, in a terminal, never in a chat window:

    export ROBOFLOW_API_KEY=...

then re-run `bash audit/run_all.sh`. That unblocks Phases 0.3, 0.4, 1, 2,
3.2(iii), 3.3, 3.4, 3.5, 4.1(1)-(2), 4.2, 5.3's overlap measurement and 5.4.

The tag `v1.1-r1` has deliberately NOT been applied. It should mark the
completed revision, and this one is not complete; applying it now would label an
incomplete audit as the deliverable, and a pushed tag cannot be moved without
the history rewrite ground rule 1 forbids. Apply it after the blocked phases run.

---

# RESUMED 2026-09-21 ~22:20 with ROBOFLOW_API_KEY supplied

## Phase 0.3 — datasets (DONE, PASS)

Both pinned versions downloaded via the REST API with the version in the URL.
Model B 7000/1500/1500, **9,688** test instances, **0** background images;
per-class counts match published S4 exactly. Model A 474/44/26 = 544.
All six required files (data.yaml, README.roboflow.txt, README.dataset.txt)
present for both. No STOP. Details in `S23_dataset_identity_and_duplicates.md`.

Counting note: `cat labels/*.txt | grep -c .` undercounts by one line per file
(no trailing newlines), giving a spurious 8,189. Count per file.

## Phase 0.4 — duplicate regeneration (DONE, EXACT)

D == S2 as a set (259, symmetric difference 0); identity-only subset == S1
(124, symmetric difference 0). ND = 1241. No STOP.

Required disabling PIL draft mode, which breaks reflected matching through
asymmetric JPEG block padding on non-multiple-of-8 dimensions. See
`S23_dataset_identity_and_duplicates.md` and DEVIATIONS D4.

## Phase 2.1 — clusters (DONE)

1,445 components over 1,500 images: 1,394 singletons, 47 of size 2, 4 of size 3.
214 contain a D image, 1,231 do not. 104 edges from a shared training twin,
59 from test-test duplicates. `S25_clusters.json`.

## Phase 5.4 — lineage (DONE)

Resolved from the Roboflow API. Model B: 10,000 images, 6 classes, CC BY 4.0,
one version, **no augmentation** — so its near-duplicates were in the source
upload, not created by the platform. Model A: 228 source images expanded to 544
by declared augmentation (3 versions per image: flips, 90-degree rotations, crop
0-20%). Neither project exposes a fork/source field, so references 8 and 9
cannot be confirmed or refuted. `S26_lineage.md`.

## Still running at the time of writing

Phase 1.2 gate, then caches (valid, train), then Phases 2.2-2.9, 3.3-3.5, 4.1
via `audit/scripts/run_remaining.sh`.

## Phase 1 — cached evaluator (DONE, PASS)

Exactness gate **0.0 on all four sets** (full, ND, ctrl1, ctrl2), not merely
below 1e-9. The first attempt gave 6.158e-08 on ctrl2; cause found and fixed —
`rect=True` sorts the dataloader by aspect ratio (338 distinct image sizes) and
float32 cumsum in `ap_per_class` is order-sensitive, so the replay must use the
validator's own order, not filename order. Both numbers reported.
Batch-16 reproduces the spec's expected P/R/mAP figures exactly at the quoted
precision. The batch effect on mAP@0.5 is 0.00006 — about 44x too small to
explain the August 0.0025 discrepancy. Caches built for test, valid and all
7,000 training images (~11 min, so no sampling needed). `S24`, `S28`, `S41`.

## Phase 2 — contamination (DONE)

Removal effect **Δ mAP@0.5 = +0.000997 [-0.01249, +0.01418]**, Δ mAP@0.5:0.95 =
+0.001111 [-0.00738, +0.00957], 10,000 cluster bootstrap resamples over 1,445
clusters. Randomization p = 0.39-0.75; **MDE ~0.011 mAP@0.5**. Removing these
259 images is indistinguishable from removing any 259.

The substantive finding is elsewhere: only **57 of 259 (22.0%)** duplicate pairs
have identical label sets, and the same 224 photographs score mAP@0.5 0.882 with
their training labels against 0.660 with their test labels. The contamination is
an annotation-consistency problem, not a leaderboard-inflation problem.
`S29`, `S30`, `S31`, `S32`, `S43`.

Fixed en route: `plan_strata()` could emit a stratum with no donor pool
(`KeyError: '1|8-15'`). Rewritten to allocate greedily against a used-set, so
two strata can never draw the same image and a stratum is never emptied by an
earlier one; the 2 strata that genuinely lack donors are widened and **reported**
(`caries|>=16` needs 4, ND has 0; `caries|1` needs 26, ND has 25).

## Phase 4.1 — Model A (DONE) — and an earlier conclusion CORRECTED

`model_a.pth` reproduces the notebook's stored confusion matrix **exactly on
both splits**. It does not reproduce the AUC (0.8310 vs 0.6476) or the MAE/R²,
and the cause is the evaluation pipeline, not the weights: cell 6 builds the
dataset with `train_transform` and never reassigns it, so the validation loader
applies random flips, rotation and colour jitter at evaluation time
(`val_transform` is defined and never used — the author's own comment says so).
Five re-runs of the augmented path give AUC 0.6048-0.7881; the published 0.6476
is one draw from that spread.

**Correction.** The earlier note that the published metrics describe "a
checkpoint that no longer exists" is wrong. Notebook execution counts are
consecutive (cell 8 = 22 saves best, cell 9 = 23 loads best and evaluates,
cell 10 = 24 saves `model.state_dict()` as `model_a.pth`), so `model_a.pth` is a
re-serialisation of `model_a_best.pth`'s weights. The file is missing; the
weights are not. The deployed model IS measurable, and is measured in `S42`.

## Phase 6.3 — expert packet (DONE, prepared not sent)

`r1-scratch/work/expert_packet/`: A = 100 test images stratified by class
(seed 20260921), 715 box rows; B = all **18** TVNT negatives + 18 random
positives, renamed and shuffled, with the unblinding key kept separate. The 18
is an independent confirmation of the CSV's `Normal=18`. Never committed.
