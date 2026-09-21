# Revision R1 summary

**This revision is incomplete.** Everything that depends on the image data is
blocked: the Roboflow datasets are not on this machine and `ROBOFLOW_API_KEY` is
unset, which ground rule 5 makes a STOP. Everything that does not depend on the
data was completed, and several of those results are substantive.

To unblock, in a terminal (not in a chat window):

    export ROBOFLOW_API_KEY=...
    bash audit/run_all.sh

Each number below is tagged with the file it comes from. Numbers produced by
different evaluators or environments are never compared, and mAP@0.5 is never
set beside mAP@0.5:0.95.

```
PLAN        12f3199e0669565b35fe663e3b9bc6fe993cc3a7
            2026-09-21T21:25:17+08:00
            pushed: YES (origin/revision-r1)
            ANALYSIS_PLAN_R1.md == Appendix A verbatim, byte-identical (diff-verified)

ENV         both venvs: Python 3.12.13, macOS 26.6.2 arm64, Apple M5, 10 CPUs,
            torch 2.7.1, torchvision 0.22.1, sahi 0.11.15, numpy 2.5.3,
            scipy 1.18.1, pandas 3.0.6, scikit-learn 1.9.1, pillow 12.3.0,
            cv2 5.0.0 (headless), matplotlib 3.11.2; CUDA False, MPS True
            (unused), default dtype float32
            venv 1: ultralytics 8.3.231   venv 2: ultralytics 8.4.118
            torch.get_num_threads() = 4  -- PINNED, see below
            locks differ in 3 lines only: ultralytics, nvidia-ml-py (8.4.118
            only, inert on a Mac), pip (8.3.231 only)
            [audit/env/lock-ul8.3.231.txt, lock-ul8.4.118.txt,
             env-ul8.3.231.json, env-ul8.4.118.json, ENVIRONMENT_NOTES.md]
            NOTE the pinned torch installed cleanly; no substitution needed.
            NOTE sahi is pinned in requirements.txt as ">=0.11.15", a floor and
            not an exact pin; 0.11.15 was installed.

WEIGHTS     best.pt            4de8714f0f2b52a70564cc1be55058262564ced400cd8a7d5815192477aad0cc
            model_a.pth        b469110a551aa4bb93189b05a424fa28239dc4f710983e779b41acf7a19a2d3f
            triage_router.pth  59cb5a8d8445927a92b0fd0d502fc56b650a16c1a9be94246bc2d2115088f5e2
            best.pt starts 4de8714f and ends 7aad0cc: MATCH. No STOP.
            All three equal their committed LFS pointer oids.
            git lfs pull and git lfs fetch --all both succeeded; no quota block.
            [audit/env/weight-sha256.txt, audit/results/S12_checkpoint_provenance.md]

IDENTITY    Model B 7000/1500/1500, 9688 inst -- NOT CHECKED (no data)
            Model A 474/44/26 -- NOT CHECKED (no data)
            D == S2 (259), identity subset == S1 (124) -- NOT REGENERATED (no data)
            The reference sets themselves were found and verified internally:
              S2 = 259 rows / 259 unique test images
              S1 = 124 rows / 124 unique test images; S1 is a subset of S2
              S2 best-transform tally hflip 85, vflip 74, identity 63, rot180 37 = 259
              S4 per-class test instances sum to exactly 9,688
            [audit/results/reference/PROVENANCE.md]

            CORRECTION TO SPEC CHECK 0.4.3. "Identity-only subset" must mean the
            images below threshold UNDER identity (124), not the images whose
            BEST transform is identity (63). Verified: S1 equals the S2 rows
            flagged also_found_by_aligned_only = yes (124) and does NOT equal
            the matching_transform = identity rows (63). The published S0 README
            states this. near_duplicates.py runs both passes.

EXACTNESS   NOT RUN -- Phase 1 needs the test images.
BATCH       NOT RUN -- Phase 1.3 needs the test images.
CLUSTERS    NOT RUN -- Phase 2.1 needs the test images.
HEADLINE    NOT RUN -- Phase 2.2 needs the test images.
REMOVAL     NOT RUN -- Phase 2.3 needs the test images.
RANDOM      NOT RUN -- Phase 2.4 needs the test images.
CONTRASTS   NOT RUN. The deployed thresholds are recovered (see E2E below).
            t_global: the committed BoxF1_curve.png legend records
            "all classes 0.73 at 0.285" for the original run. Its split,
            ultralytics version and batch size are NOT recorded anywhere in the
            repository, so this is a PRIOR to check against, not the value spec
            2.5 asks for. [audit/results/S9_stored_run_artifacts.md]
MEMORISE    NOT RUN -- Phase 2.6 needs the test and training images.
VALID       NOT RUN -- Phase 2.7 needs the validation images.
PHOTOMETRIC NOT RUN -- Phase 2.8 needs the images.
VERSION     NOT RUN -- Phase 2.9 needs the test images. Both venvs are built and
            ready, and the version-isolation hazard is fixed (see below).

E2E         REQUEST PATH: traced in full. [audit/results/S13_request_path_and_mapping.md]
            One reachable upload endpoint, POST /analyze (main.py:194). Router
            first at softmax 0.95, compared as "< threshold rejects", so exactly
            0.95 is accepted. THREE gates fire before the network: mean
            brightness < 40, > 250, or std < 15 -> "Unknown". The router returns
            its own exceptions as strings, and main.py collapses every string
            that is not Clinical/Histopathological into one user message, so an
            internal failure is indistinguishable from an out-of-domain
            rejection.
            SAHI whenever width AND height >= 640; slices 512x512 at 0.2
            overlap. The Roboflow export is 640x640, so EVERY benchmark image
            takes the SAHI path. SAHI count, once run: expected 1500/1500.
            Deployed per-class thresholds, keyed by display name:
              Ulcers 0.75, Tooth Discoloration 0.40, Caries 0.35,
              Hypodontia 0.60, Calculus 0.25, Gingivitis 0.30; default 0.25
            "No Issues Detected" when len(detections) == 0 after thresholding.
            screening_result "Normal" is unreachable dead code.

            PYTEST: 39 passed, 6 skipped. [audit/results/S18_pytest_output.txt]
            tests/test_class_mapping.py implements (i), (ii) and (iii); the 6
            skips are (iii), which needs the images. verify_classes.py under the
            pinned env: "0 of 6 classes are reported under the wrong name."
            [audit/results/S11_verify_classes_output.txt]

            AGREEMENT POST-FIX: NOT RUN over the 1,500 images (needs data), but
            verified exhaustively over all six classes synthetically and against
            the weights' own registry.

            PRE-FIX PERMUTATION, from commit 7210dea verbatim:
              self.class_names = {
                  0: 'Caries', 1: 'Calculus', 2: 'Gingivitis',
                  3: 'Tooth Discoloration', 4: 'Ulcers', 5: 'Hypodontia'
              }
            against the weights' registry {0: calculus, 1: caries,
            2: gingivitis, 3: hypodontia, 4: tooth_discolation, 5: ulcer}:

              idx  true class          displayed PRE-fix        correct?
              0    calculus            Caries                   NO
              1    caries              Calculus                 NO
              2    gingivitis          Gingivitis               yes
              3    hypodontia          Tooth Discoloration      NO
              4    tooth_discolation   Ulcers                   NO
              5    ulcer               Hypodontia               NO

            FIVE OF SIX classes wrong; one transposition and one 3-cycle.
            Counts of affected findings/images: NOT RUN (needs the images).

            IMPORTANT QUALIFICATION. The threshold table is keyed by display
            name and is byte-identical before and after the fix, so a wrong name
            also meant a wrong THRESHOLD: calculus was tested at 0.35 not 0.25
            and tooth_discolation at 0.75 not 0.40 (stricter, detections lost),
            while caries, hypodontia and ulcer were tested more loosely. The
            historical app did not merely mislabel findings -- the SET of
            findings differed too. Applying the old dictionary to indices
            captured in the current chain, as spec 3.3(4) asks, isolates the
            mapping and is therefore a LOWER BOUND on the historical
            discrepancy. The manuscript must say which it reports.

IMAGE-LEVEL NOT RUN -- Phase 3.4 needs the 1,500 test images.
            Not estimable from this benchmark regardless, and to be stated as
            such: patient-level sensitivity, specificity in healthy mouths,
            predictive values at population prevalence, referral burden. There
            are no healthy images in the split.

ROUTER      CLASSES: ResNet-18, fc (2, 512), classes ['Clinical',
            'Histopathological'] = index 0, 1, fixed by a hard-coded list in
            triage_inference.py. The checkpoint stores NO class names, so
            nothing would detect a mismatch -- structurally the same hazard as
            the Model B defect, currently unguarded.
            TRAINING DATA: ./dataset, assembled by hand, split 0.8 with seed 42
            into ./dataset_final. NEITHER IS IN THE REPOSITORY AT ANY COMMIT.
            Stored training log: 20 epochs, "Best val Acc: 1.000000" -- a
            training-time number on its own split, which says nothing about
            out-of-distribution behaviour.
            RESULTS BY SET [Wilson CIs]: NOT RUN (needs all three sets).
            OVERLAP KNOWN: **UNKNOWN**, and it cannot be determined from the
            records that exist. The risk is real and must be stated with any
            future router numbers: the obvious way to populate that folder is
            from the same two Roboflow datasets, which would make the Phase 3.5
            evaluation an evaluation on its own training data.
            [audit/results/S19_router.md]

MODEL A     SPLIT REPRODUCED: not re-run (needs images), but the notebook's
            stored outputs confirm 435/109 and the pooling 474+44+26 = 544.
            CONFUSION MATRIX, validation (n=109): TN 0, FP 4, FN 0, TP 105
              -- MATCHES the spec's expectation exactly.
            CONFUSION MATRIX, training (n=435):   TN 0, FP 14, FN 0, TP 421
            ROC-AUC: validation 0.6476 -- MATCHES. Training 0.9333.
            TVNT corpus distribution: Normal=18, Abnormal=526 (sums to 544).

            THE CLASSIFIER IS DEGENERATE. FN = 0 and TN = 0 in BOTH splits: the
            model predicts "Abnormal" for every image. Therefore:
              sensitivity  1.0000  CP 95% [0.9655, 1.0000]   (validation)
              specificity  0.0000  CP 95% [0.0000, 0.6024]   (validation)
              bal accuracy 0.5000                            (chance)
              accuracy     0.9633 == the base rate, exactly
              base rate    0.9633 positive
              MCC          UNDEFINED (0/0; TN+FN = 0). sklearn returns 0.0 by
                           convention -- that is a convention, not a result.
              training:    sens 1.0000 [0.9913, 1.0000], spec 0.0000
                           [0.0000, 0.2316], bal acc 0.5000, base rate 0.9678
            [audit/results/S20_model_a_classifier_metrics.json, S21_model_a_findings.md]

            AP pos / AP neg / ROC-AUC bootstrap CI: NOT COMPUTABLE -- the
            per-image scores are not stored. Needs the images.
            SOURCE-LEVEL COUNTS: blocked (needs the images).
            13-UNLEAKED SUBSET: 109 - 96 = 13 confirmed from S5. Not evaluated;
            given constant predictions it can only return sens 1.0, spec 0 or NaN.

            THE REPORTED METRICS DESCRIBE A CHECKPOINT THAT NO LONGER EXISTS.
            The evaluation cell loads model_a_best.pth (stored output confirms
            the branch was taken); cell 10 saves the final-epoch model as
            model_a.pth; the application loads model_a.pth. model_a_best.pth is
            absent from the working tree, from every commit across all refs,
            from every git object, and from git lfs ls-files --all. So Table 3
            and the confusion matrix describe a sibling checkpoint, they are not
            reproducible, and the deployed model's performance is unmeasured.
            When 4.1(2) is finally run it should be EXPECTED to disagree with
            the stored outputs; that disagreement is the finding.

SOURCES     NOT RUN -- Phase 4.2 needs the 544 images.
            The filename convention is confirmed from committed samples and the
            published CSVs: OSCC_400x_<n>_jpg.rf.<32 hex>.jpg, source = the stem
            before ".rf.". The 18 TVNT negatives are confirmed to exist
            (Normal=18) but their source names need the images.
            Rahman et al. thumbnail match: NOT ATTEMPTED.

R2          FUNCTION: sklearn.metrics.r2_score(targets, preds_clipped), cell 9
            line 151, guarded by np.var(targets) > 0, predictions clipped at 0.
            REFERENCE MEAN: the mean of the y_true passed in, i.e. the
            evaluation set's own mean. So a validation R2 and a training R2 are
            referenced to different means and are not comparable.
            Stored: validation Mitotic Figures R2 = -0.0154, i.e. worse than
            predicting that set's own mean.

PROVENANCE  best.pt metadata [audit/results/S10_best_pt_metadata.json]:
              date 2025-12-12T16:33:59.554724, version 8.3.231
              names {0 calculus, 1 caries, 2 gingivitis, 3 hypodontia,
                     4 tooth_discolation, 5 ulcer}
              architecture nc 6, depth 0.67, width 0.75 (YOLOv8m)
              train_args: model 'Backend Development/Model B/models/best.pt',
                data '/home/hfyic3/Backend Development/Model B/oral-diseases-1/data.yaml',
                epochs 200, patience 20, batch 100, seed 0, deterministic True,
                pretrained True, device '0', workers 16, imgsz 640, rect False,
                project 'oral_cancer_screening', name 'yolov8m_evolved_final'.
                save_dir is NOT present in train_args.
              train_metrics (VALIDATION split, GPU, batch 100, 8.3.231):
                mAP50 0.75956, mAP50-95 0.38766, P 0.73058, R 0.73320,
                fitness 0.38766 -- these are NOT test-split figures and must not
                be set beside the abstract's or Table 1's numbers.
              train_results holds 48 epochs, not 200: with patience 20 the run
              stopped early. Do not describe it as a 200-epoch run.
              The checkpoint's own `version` is 8.3.231, so the revision's pin
              is the TRAINING-TIME version, not an arbitrary choice.

            WEIGHT HISTORY [audit/results/S15_weight_history_and_warm_start.md]:
              Model B/models/best.pt  f7e56f7 2025-12-07 16:48:02  added
                                      oid eec5aba9...97946, 52,022,866 bytes
              Model B/models/best.pt  122e026 2025-12-12 17:05:14  modified
                                      oid 4de8714f...7aad0cc, 52,035,922 bytes
              -> ml_models/...        065dbd4 2026-03-30 22:52:43  rename R100
              Model A/model_a.pth     f7e56f7 2025-12-07 16:48:02  added
                                      oid b7393a56...f19a1, 107,372,550 bytes
              Model A/model_a.pth     48e1c4e 2026-02-05 20:55:51  modified
                                      oid b469110a...9a2d3f, 55,240,265 bytes
              Model Triage/...pth     f7e56f7 2025-12-07 16:48:02  added, never changed
              27 LFS objects in total; both superseded checkpoints were fetched
              and read directly.

            WARM START IDENTIFIED: **YES**. oid eec5aba9, dated 2025-12-06.
              names: IDENTICAL to the released checkpoint.
              train_args.data: 'oral-diseases-1/data.yaml' -- THE SAME dataset
              directory as the released run. So training exposure spans at least
              two runs, 50 epochs then 48, not the 48 of the final run.
              ITS data: it was itself warm-started from a third 'best.pt' that
              is NOT in the repository. Origin NOT RECOVERABLE. That is the end
              of the provenance trail.
              OVERLAP WITH TEST: NOT MEASURED (needs the data). Note data.yaml
              was never committed, so it cannot even be proved the two runs used
              the same partition, only the same directory name.

            CLASS ORDER vs THE OLD DICTIONARY: does NOT match. No checkpoint in
            this repository's history has EVER had the old dictionary's order.
            The dictionary was introduced in the FIRST commit f7e56f7 -- the
            same commit that added the warm start it already failed to match --
            and survived until 0b21474 removed it, about EIGHT MONTHS later. It
            was never a stale copy of a once-valid order; it was wrong when
            written.

LINEAGE     BLOCKED. universe.roboflow.com returns HTTP 403 to non-browser
            clients and api.roboflow.com needs the key, so neither route is
            available. [audit/results/S8_lineage_partial.md]
            Search-index evidence only, labelled as such: reference 8
            (tesisdientes/oral-diseases-5ctay-rqpxs) has 4 classes (calculos,
            caries, gingivitis, ulcera), ~4.2k images, CC BY 4.0 -- consistent
            with the revision's claim that it does not describe the six-class,
            10,000-image project actually used. REF 8/9 CORRECT: NOT ESTABLISHED.
            The shared slug stems (oral-diseases-5ctay-*, oral-cancer-1mnve-*)
            are consistent with a fork but are a naming inference only and must
            be confirmed against the project metadata before print.

INDEPENDENCE [audit/results/S17_unit_of_independence.md]
            1. Patient IDs?            **NO**. No dataset image carries a
               subject identifier; the schema has User/Appointment/
               DailyHabitLog/GenAIFeedback and stores no image or study. The
               patient_id at core/models.py:16 is the appointment foreign key to
               an app user and never touches an image -- a grep alone would give
               a false positive here.
            2. Source-photograph IDs?  **YES**. The filename stem before ".rf.",
               materialised as test_source/train_source in S1 and S2 and
               source_prefix in S5, and implemented in near_duplicates.py.
            3. Episode or visit info?  **NO**.
            4. Upstream augmentation?  **YES**, with multiplicities: of S5's 96
               rows, 66 sources have 3 copies in the pool and 30 have 2,
               spanning 81 distinct sources, all originating in Roboflow's train
               partition.
            Consequence: the source photograph is the available unit of
            independence and the analyses should cluster on it; patient-level
            clustering is impossible. Because the stem catches only augmented
            copies of one file, and not one lesion photographed twice, every
            contamination count built on it is a LOWER BOUND.

CHRONOLOGY  62 commits across all refs [audit/results/S16_chronology_all_commits.txt].
            54 by "Your Name <youremail@example.com>", an unconfigured identity;
            8 by VanVan120. Range 2025-12-07 16:48:02 to the current tip.
            Key commits: f7e56f7 2025-12-07 first commit (introduces the wrong
            dictionary AND the warm start); 122e026 2025-12-12 the released
            checkpoint; 48e1c4e 2026-02-05 Model A replaced; 5c2dc35 2026-03-01
            the 12 runs/detect/val figures; 065dbd4 2026-03-30 restructure;
            7210dea 2026-04-24 carries the pre-fix dictionary; 0b21474
            2026-08-13 15:55:35 the fix; 5b815bb 2026-08-13 16:02:51 as-submitted.
            SURVIVING AUGUST FILES: the August scratchpad is GONE. The submitted
            supplementary survives at ~/Documents/SEGP Journal/
            Supplementary-Material.zip (members dated 2026-08-13 10:19, i.e.
            BEFORE the 15:55 fix, consistent with the manuscript's sequence),
            alongside the submission .docx, its PDF preview and Figure_1.tif.

PACKAGING   audit/ tree: README.md, env/ (2 locks, 2 env records, weight
            hashes, ENVIRONMENT_NOTES.md), scripts/ (6), results/ (this file,
            PROGRESS.md, S8-S21, reference/ with S0-S5 + PROVENANCE.md),
            run_all.sh.
            run_all.sh TESTED: syntax-checked only (bash -n). It cannot be run
            end to end without the key, and it is written to STOP with an
            explicit message at that point.
            Commits and tag: see the hand-off section below.
```

## UNFINISHED, and why

Blocked on `ROBOFLOW_API_KEY` (ground rule 5 STOP) — the datasets are not on
this machine and the August scratchpad no longer exists:

- **Phase 0.3** dataset identity checks; **0.4** regenerating D and ND
- **Phase 1** entirely — the cached evaluator, the 1e-9 exactness gate, batch
  sensitivity, the extra caches
- **Phase 2** entirely — clusters, headline table, removal effect, randomization,
  per-class contrasts, memorisation diagnostics, validation contamination,
  the photometric tier, the library-version comparison
- **Phase 3.2(iii)**, **3.3**, **3.4**, **3.5** part 2–3
- **Phase 4.1(1)–(2)**, the ROC-AUC CI and average precisions, source-level
  counts, **4.2**
- **Phase 5.3** overlap measurement, **5.4** lineage
- **Phase 6.3** the expert-review packet (needs the images)

Not attempted: the Rahman et al. thumbnail match (4.2 optional); the
version-effect decomposition (2.9(3), explicitly optional and last).

No analysis was run and then hidden. Nothing above is inferred unless it says
so.

## UNEXPECTED

Things found that the spec did not anticipate. Ordered by how much they matter.

1. **Model A's reported metrics describe a checkpoint that no longer exists.**
   The evaluation cell loads `model_a_best.pth`; the app and this manuscript use
   `model_a.pth`; `model_a_best.pth` is absent from the tree, from all 62
   commits, from every git object and from LFS. Table 3 is therefore not
   reproducible, and the deployed model's performance has never been measured.

2. **The histopathology classifier is degenerate**: TN = 0 and FN = 0 in both
   splits, so it predicts "Abnormal" for everything. Specificity 0.0000,
   balanced accuracy 0.5000, accuracy exactly equal to the base rate, MCC
   undefined. This bears directly on R1.8's question about the TVNT label.

3. **The wrong class dictionary was never right.** It entered in the very first
   commit, alongside a checkpoint whose class order it already failed to match,
   and no checkpoint in the repository's history has ever had its order.

4. **The pre-fix defect changed thresholds as well as names**, because the
   threshold table is keyed by display name. The set of reported findings
   differed, not just their labels, so the spec's mapping-isolated estimand is a
   lower bound.

5. **The warm start used the same dataset directory**, and was itself
   warm-started from a third checkpoint that no longer exists — so training
   exposure spans at least two runs and the provenance trail does not close.

6. **Importing ultralytics before torch silently drops CPU threads from 4 to 1**
   (`ultralytics/__init__.py` sets `OMP_NUM_THREADS=1` when unset). Threaded
   reductions are order-sensitive, and the Phase 1.2 gate compares to 1e-9, so
   this could have failed the gate for reasons unrelated to the evaluator, or
   passed on one machine and failed on another. Now pinned explicitly.

7. **The two venvs shared one global ultralytics `settings.json`** and rewrote
   each other's schema — mutable shared state in the middle of a comparison
   whose entire point is to isolate the library version. Each venv now has its
   own `YOLO_CONFIG_DIR`.

8. **Two OpenCV distributions are installed at once** (`opencv-python` 4.7.0.72
   and `opencv-python-headless` 5.0.0.93). They ship the same `cv2` package, so
   one silently overwrites the other; headless 5.0.0 wins here. Nothing pins
   which.

9. **Spec check 0.4.3 as written would fail.** "Identity-only subset" has to
   mean below-threshold-under-identity (124), not best-transform-is-identity
   (63).

10. **The supplementary uses two different naming schemes.** `S0_README.txt`
    calls the files `modelB_124_aligned_pairs.csv` etc., and the spec follows
    the README, but the archive members are named `S1_…` through `S5_…`. Same
    files, and the S4 "ALL" row has 9 fields against a 10-field header.

11. **Two user-visible display defects**, neither affecting any metric: a result
    of "Issues Detected" has no i18n key in any of the four languages, so the
    user is shown the literal string `screeningResultIssuesDetected`; and
    `screening_result = "Normal"` is unreachable dead code.

12. **The router cannot be distinguished from a broken router** from the
    outside: it returns its own exceptions as strings and `main.py` collapses
    every unrecognised string into the same "not a valid oral health image"
    message. Its three pre-network gates also mean a rejection is not
    necessarily a low-confidence classification.

13. **The router's training data is unrecoverable and may overlap the
    evaluation sets.** `./dataset` was hand-assembled and never committed.
    Overlap is UNKNOWN and cannot be determined.

14. **`best.pt` records `batch: 100` and 48 of 200 epochs.** The run was not a
    200-epoch run, and AutoBatch was not used.
