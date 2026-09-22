# Analysis plan, revision round 1 (R1)

Written 21 September 2026 and committed before any analysis listed here was run. The analyses of August 2026 and their outcomes were known when this plan was written. This plan pre-specifies the revision analyses only. Deviations are appended under DEVIATIONS in later commits; the text above that heading is not edited.

## 1. Fixed inputs

- Detector: the released checkpoint (best.pt under ml_models/model_b), SHA-256 beginning 4de8714f (full hash recorded at run time). No retraining.
- Data: Roboflow segp-fcn6m/oral-diseases-5ctay-h9oye version 1 (train 7,000, valid 1,500, test 1,500 images; 9,688 test instances). Histopathology: segp-fcn6m/oral-cancer-1mnve-n5yij version 2 (544 images).
- Duplicate set D: the 259 test images with a training near-duplicate under the published rule (32 × 32 greyscale thumbnails, RMS < 6.0, minimum over the dihedral group of order 8), reproducing Supplementary S2 exactly. ND: the other 1,241 test images.
- Environment for all headline figures: ultralytics 8.3.231, CPU, FP32, imgsz 640, conf 0.001, NMS IoU 0.7, max_det 300, batch 1.
- Evaluator: per-image match statistics cached from ultralytics' own validator; subset metrics computed with ultralytics' own metric function. It is used only after reproducing val(batch=1) to within 1e-9 on the full split, on ND and on two random subsets.
- M denotes mAP@0.5 or mAP@0.5:0.95. The two are always analysed separately and never compared with each other.
- Random seed 20260921 for every resampling procedure.

## 2. Primary analysis

Estimand: the removal effect Δ = M(ND) − M(All), for each M.

(a) Confidence interval. Cluster bootstrap with 10,000 resamples. Clusters are the connected components of the within-test duplicate graph (test–test pairs under the same rule, plus test images sharing a training near-duplicate). Resampling is stratified by whether a cluster contains any image of D. 95% percentile intervals.

(b) Stratified randomization test. 10,000 control sets. Each removes 259 images drawn from ND without replacement, matched to D on stratum counts. Stratum = dominant class (the class with most instances in the image; ties go to the lower class index) × instance-count bin (1, 2–3, 4–7, 8–15, ≥16). Where ND has too few images in a stratum, that stratum is merged with the adjacent bin of the same dominant class, and the merge is reported. Two-sided p = (1 + #{controls with |Δc − median| ≥ |Δ − median|}) / (1 + 10,000). The percentile rank of Δ is also reported, with a balance table (instances removed, per-class instances removed, mean instances per image).

(c) Unstratified randomization test. As (b) without strata; this is the design of the original submission, run with 10,000 draws.

(d) Minimum detectable effect: (1.96 + 0.84) × SD of the stratified control distribution. This is the removal effect the design would detect with 80% power at two-sided α = 0.05.

Interpretation rule: no equivalence claim will be made, because no equivalence margin was specified before the original results were seen. Results are reported as a point estimate, a 95% CI and a randomization p-value, and are described in words no stronger than the interval supports.

## 3. Secondary analyses

These are estimation only: 95% CIs, no hypothesis tests. Intervals that exclude zero among many secondary contrasts are not interpreted individually.

3.1 Per-class contrasts between D and ND, for classes with at least 30 annotated instances in D. The metrics are:
- AP@0.5 and AP@0.5:0.95;
- instance recall and precision at t_global, the confidence at which ultralytics' smoothed mean-F1 curve peaks on the full split;
- instance recall and precision at the deployed per-class thresholds.
CIs come from the cluster bootstrap in 2(a).

3.2 Memorisation diagnostics:
- (a) M on training images (all, or a seeded random sample of 2,000), on the validation split and on the test split.
- (b) Annotation concordance between each image in D and its training near-duplicate, after the training boxes are mapped through the matching transform. The measures are box-level precision, recall and F1 at IoU ≥ 0.5, with and without class agreement, and the proportion of pairs with identical label sets.
- (c) For D, instance recall at t_global of the detector's predictions against two label sets: the image's own labels, and its training twin's mapped labels.
- (d) M on the training twins, against their own labels, versus M on D.

3.3 Validation-split contamination. For the released checkpoint, M and fitness (0.1·mAP@0.5 + 0.9·mAP@0.5:0.95), on the full validation split and on the validation split without its training near-duplicates.

3.4 User-facing, image-level metrics through the deployed inference path at the deployed thresholds, with and without the domain router. For each condition:
- the proportion of test images annotated with it in which the application reports it;
- the proportion of test images not annotated with it in which the application reports it (all such images carry other conditions);
- the proportion of images annotated with it for which the application reports no condition.
CIs come from the cluster bootstrap. Patient-level sensitivity, specificity in healthy mouths, predictive values at population prevalence and referral burden are not estimable from this benchmark, and will be stated as such.

3.5 End-to-end label mapping on all 1,500 test images. This is the agreement between the class index inside the deployed path and the displayed label, after correction and under the pre-correction dictionary (commit 7210dea).

3.6 Router outcomes at the deployed softmax threshold (0.95) on three sets: the detector test split, the histopathology images, and COCO128 as out-of-distribution input. Reported as proportions with Wilson 95% CIs.

3.7 Histopathology classifier on the reproduced validation split (n = 109), reported at image and source level:
- the confusion matrix;
- sensitivity and specificity with Clopper–Pearson 95% CIs;
- balanced accuracy;
- ROC-AUC with a CI from a 10,000-resample bootstrap stratified by class;
- average precision for each class;
- MCC;
- base rate.

3.8 Sensitivity analysis. If the photometric tier (322 images) verifies at full resolution against a random-pair null, analyses 2(a)–(c) are repeated with it as D.

3.9 Library version. Full-split and ND metrics under ultralytics 8.4.118, with the same torch and device. Version effects are reported separately for each metric.

## 4. Exploratory

These are labelled as exploratory wherever they are reported:
- the decomposition of the version effect into prediction changes and metric-code changes;
- any analysis not listed above.

## 5. Not done in this round

No retraining. The reproducibility of model development (the training environment, the AutoBatch size and the warm-start data) is documented as far as the records allow, but it is not reproduced.

## DEVIATIONS
**D1 — 2026-09-21. Definition of the identity-only duplicate set (S1).**

Section 1 defines D by the dihedral rule and refers to Supplementary S1 as the
identity-only subset. The phrase is ambiguous, and the two readings differ by
almost a factor of two. Filtering the dihedral result on "the best-scoring
transform is identity" yields **63** test images. Filtering on "the RMS under
the identity transform is below 6.0" yields **124**, which is the published S1
and the set the original analysis used.

The second reading is the operative one. It is what the published
`S0_README.txt` states — *"To recover the fixed-alignment set, filter on
also_found_by_aligned_only = yes (exactly 124 rows), not on matching_transform =
identity"* — and it was verified here: S1 equals the 124 S2 rows flagged
`also_found_by_aligned_only = yes` as a set, and does not equal the 63
best-transform-identity rows.

The cause is that 124 images fall below threshold under identity, but for 61 of
them some reflection scores lower still, so identity is the single best
transform for only 63. `audit/scripts/near_duplicates.py` therefore runs two
passes, full-dihedral and identity-only, and reports both.

No analysis changes: D is still the 259-image dihedral set, exactly as
pre-specified. This entry records the disambiguation so the 124/63 distinction
cannot be mistaken for a discrepancy later.

**D2 — 2026-09-21. Pre-correction end-to-end simulation: full path, not mapping
alone.**

Section 3.5 pre-specifies the end-to-end label-mapping analysis as the agreement
between the class index inside the deployed path and the displayed label, under
the pre-correction dictionary of commit 7210dea. Reading the code at that commit
showed the plan understates what the defect did.

The per-class confidence thresholds are keyed by **display name**, and that
table is byte-identical before and after the correction. Because the pre-fix
dictionary mapped each index to the wrong display name, the threshold lookup
resolved to the wrong class's threshold as well:

| true class | correct threshold | applied pre-fix | direction |
|---|---|---|---|
| calculus | 0.25 | 0.35 (Caries) | stricter |
| caries | 0.35 | 0.25 (Calculus) | looser |
| gingivitis | 0.30 | 0.30 | unchanged |
| hypodontia | 0.60 | 0.40 (Tooth Discoloration) | looser |
| tooth_discolation | 0.40 | 0.75 (Ulcers) | stricter |
| ulcer | 0.75 | 0.60 (Hypodontia) | looser |

So the historical application did not merely display a wrong label on a correct
finding: the set of findings that survived thresholding also differed, in both
directions. Applying the old dictionary to indices captured under the *current*
thresholds isolates the mapping, but is therefore a lower bound on the
historical discrepancy.

**Change.** The primary pre-correction result is now a simulation of the full
7210dea path — the old dictionary together with thresholds looked up by the
wrong display name. The mapping-only count pre-specified in 3.5 is retained and
reported as a secondary result. Both are labelled wherever they appear.

This is a change of estimand, made after reading the code and before the
analysis was run, and it is recorded here for that reason.

**D3 — 2026-09-21. Image-quality gates included in the replicated path.**

Section 3.4 and 3.6 describe the deployed inference path and the router's
softmax threshold. Reading `triage_inference.py` showed that three checks run
*before* the network: mean brightness below 40, mean brightness above 250, and
standard deviation below 15, each returning "Unknown" directly from the
full-resolution array.

A router rejection is therefore not necessarily a low-confidence
classification, and a proportion that mixes the two is uninterpretable. The
replicated path now records which of the four exit paths each image takes, and
the per-gate rejection counts are reported separately from the softmax
rejections, for the detector test split, the histopathology set and COCO128.

This adds reporting detail to a pre-specified analysis; it does not change the
estimand.

**D4 — 2026-09-21. PIL draft mode disabled when regenerating the duplicate
sets.**

Section 1's duplicate rule is defined on 32x32 greyscale thumbnails. The obvious
fast implementation asks PIL for a DCT-scaled decode (`Image.draft`), which
decodes a JPEG directly at a reduced size and is several times quicker.

Using it does not reproduce the published sets: the first regeneration returned
**228** pairs instead of 259. The cause is that `draft()` scales by whole DCT
blocks, and for a JPEG whose dimensions are not multiples of 8 the padding it
leaves is **not symmetric**. A reflected copy of an image therefore lands on a
slightly different pixel grid from the original, and the reflected matches — the
majority of D, since hflip and vflip account for 159 of the 259 pairs — score
far above threshold and are lost. One pair was traced end to end: RMS 6.9408
with draft mode against **0.3903** without, the latter being exactly the
published value for that pair.

`audit/scripts/near_duplicates.py` therefore sets `USE_DRAFT = False` and
decodes at full resolution before resizing. With that change D reproduces the
published S2 exactly (259, symmetric difference 0) and the identity-only pass
reproduces S1 exactly (124, symmetric difference 0).

This is an implementation correction, not a change of estimand. It is recorded
because the fast path is the natural thing to write and silently loses 12% of
the duplicate set.

**D5 — 2026-09-21. Stratum widening in the stratified randomization.**

Section 2.4(b) pre-specifies that where ND has too few images in a stratum, the
stratum is merged with the adjacent bin of the same dominant class and the merge
reported. Two cases in the data are not covered by that wording, and both occur:

1. **The adjacent bin can also be exhausted.** `caries | >=16 instances` needs 4
   controls and ND contains **zero** such images.
2. **Two strata can compete for the same donors.** A naive merge that moves a
   neighbour's images into one stratum can empty a bin that a second stratum
   still needs, and can hand the same image to two strata in one draw.

The implementation therefore allocates each control set greedily, scarcest
stratum first, against a **used-set**: a stratum draws from its own bin, then
from the adjacent bins of the same dominant class in order of distance, then
from ND at large, and every image drawn is removed from the pool for the rest of
that draw. Each control set is asserted to contain exactly 259 distinct images.

Both strata that required widening are reported rather than merged silently:

| stratum | controls needed | ND images available | widened to |
|---|---|---|---|
| `caries \| >=16` | 4 | **0** | `caries \| 8-15` |
| `caries \| 1` | 26 | 25 | `caries \| 2-3` |

That ND contains no caries-dominant image with 16 or more instances while D
contains four is itself a composition difference, and is reported as such: the
duplicated images are not a random sample of the split.

This is an implementation detail of a pre-specified analysis; the estimand, the
p-value formula and the MDE definition are unchanged.

**D6 — 2026-09-22. Per-class contrasts: resample count, and the point estimate.**

Section 2.5 inherits the 10,000-resample cluster bootstrap specified in 2.3(a).
The table published in the R1 summary was computed with **2,000**. Two
corrections, both applied by re-running:

1. The bootstrap is now run at the pre-registered **10,000** resamples.
2. The point estimate reported for each contrast is now the **observed** D-minus-ND
   difference. The earlier table reported the bootstrap **mean** in that column,
   which is a resampling artefact rather than an estimate of the quantity. The
   two differ by at most 0.0021 here, so no conclusion changes; the bias is
   reported per class alongside the corrected figures.

Percentile intervals are unchanged in definition (2.5th and 97.5th). No
estimand changes.

**D7 — 2026-09-22. The fitness formula in this plan is wrong for the pinned
ultralytics.**

Section 2.7 of this plan defines fitness as `0.1 * mAP@0.5 + 0.9 * mAP@0.5:0.95`.
That is an older ultralytics convention. The pinned version, **8.3.231**, defines
it in `DetMetrics.fitness` as

    w = [0.0, 0.0, 0.0, 1.0]   # weights for [P, R, mAP@0.5, mAP@0.5:0.95]

so **fitness is mAP@0.5:0.95 alone**. Confirmed two ways: against the installed
source, and against `best.pt`, whose stored `train_metrics.fitness` (0.38766) is
equal to its stored `metrics/mAP50-95(B)` (0.38766) to every digit.

Validation fitness is therefore reported as mAP@0.5:0.95. This changes the
reported delta from −0.00520 (under the plan's formula) to **−0.00473**. The
direction and the order of magnitude are unchanged.

This is an error in the pre-registered plan, corrected against the software the
plan itself pins, and recorded rather than silently fixed.

**D8 — 2026-09-22. Exploratory analyses in addendum R1b.**

The following were requested after the pre-registered analysis was complete and
are **not in this plan**. They are exploratory, and every number they produce is
labelled as such wherever it appears. None of them alters a pre-registered
estimand; they test whether pre-registered conclusions survive.

- **R1b item 1** — re-determining the duplicate transform at 256x256, the
  cross-tab against the thumbnail transform and against the published S2, the
  pixel-dimension and aspect-ratio checks, the recomputation of 2.6(b) under the
  full-resolution transform, and the within-rule oracle upper bound on box F1.
- **R1b item 2** — the five model-versus-label consistency contrasts, their
  stratification by whether the training augmentation could reach the twin's
  frame, and the interaction test. **Note that the stratification variable was
  chosen after seeing the per-transform breakdown**, which is why the interaction
  is reported with its full sensitivity analysis (threshold sweep, weighting,
  matching rule, balance controls) rather than as a single p-value.
- **R1b item 3** — visual inspection of 24 pairs.
- **R1b item 4** — decomposing the image-level "No Issues Detected" rate into
  router rejection versus accepted-with-no-finding. This is a *refinement* of the
  pre-registered 3.4 reporting, not a new estimand: the earlier figure was a sum
  of two events that mean opposite things to a user.
- **R1b item 8** — full-resolution verification of the validation pairs against
  a random-pair null.

Items 1, 2 and 3 were prompted by a question the plan does not ask: whether the
2.6(b) annotation-disagreement finding could be an artefact of a misregistered
frame. It is not, and the checks are reported whichever way they came out.
