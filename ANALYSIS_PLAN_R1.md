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

(none)
