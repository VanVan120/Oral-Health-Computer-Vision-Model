# Model A, the histopathology classifier (spec Phase 4)

This file has two parts. The first was written before the data arrived and
verifies the notebook's stored outputs from the stored 2×2 table alone. The
second, after the heading "Reproduction with the deployed checkpoint", is the
full reproduction against the real images and supersedes the "Blocked" list
below.

## 4.1(3) Verification against the stored outputs — all MATCH

Read verbatim from `ml_models/model_a/Model_A_Training_Master.ipynb`, cell 9
stored stdout.

| quantity | spec expected | stored | verdict |
|---|---|---|---|
| confusion matrix, validation | TN 0, FP 4, FN 0, TP 105 | TN 0, FP 4, FN 0, TP 105 | **MATCH** |
| AUC, validation | 0.6476 | 0.6476 | **MATCH** |
| split sizes | 435 / 109 | 435 / 109 | **MATCH** |

The stored matrices, verbatim:

    TVNT (Abnormality Detection) - Validation Set        TVNT - Training Set
                       Predicted                                    Predicted
                     Normal  Abnormal                             Normal  Abnormal
    Actual Normal         0        4                 Actual Normal     0        14
    Actual Abnormal       0      105                 Actual Abnormal   0       421

The class totals reconcile with the corpus: 4 + 14 = **18** negatives and
105 + 421 = **526** positives, and cells 2 and 6 both store
`TVNT: Normal=18, Abnormal=526` over the 544 pooled images.

## The finding that matters: the classifier is degenerate

**`FN = 0` and `TN = 0` in both splits. The model predicts "Abnormal" for every
single image it is given.** It has learned the constant function.

Everything else follows arithmetically:

| statistic | validation (n=109) | training (n=435) |
|---|---|---|
| sensitivity | 1.0000, CP 95% [0.9655, 1.0000] | 1.0000, CP 95% [0.9913, 1.0000] |
| **specificity** | **0.0000**, CP 95% [0.0000, 0.6024] | **0.0000**, CP 95% [0.0000, 0.2316] |
| balanced accuracy | **0.5000** | **0.5000** |
| accuracy | 0.9633 (105/109) | 0.9678 (421/435) |
| base rate (positive) | **0.9633** | **0.9678** |
| MCC | **undefined** (0/0) | **undefined** (0/0) |
| stored ROC-AUC | 0.6476 | 0.9333 |

Computed by `audit/scripts/model_a_classifier_metrics.py`, output in
`S20_model_a_classifier_metrics.json`. Clopper–Pearson intervals are exact Beta
quantiles, not normal approximations — with four negatives a Wald interval on
specificity would be the degenerate [0, 0], which is not a defensible claim.

Three things to state plainly in the revision:

1. **Accuracy equals the base rate, exactly, in both splits.** 0.9633 is not a
   measure of skill here; it is what any constant "Abnormal" predictor scores on
   a corpus that is 96.33% positive. Reporting accuracy alone would misrepresent
   the model.

2. **Balanced accuracy is 0.5000 — chance.** Sensitivity of 1.0000 is not
   evidence of a sensitive detector; it is the arithmetic consequence of never
   predicting the negative class.

3. **MCC is undefined, not zero.** The denominator
   `sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN))` has the factor `TN+FN = 0`, so the
   quantity is 0/0. `sklearn.matthews_corrcoef` returns 0.0 by convention, and
   that convention should be named rather than the 0.0 reported as a result.

The one number not fixed by the degenerate predictions is the ROC-AUC, 0.6476,
since it ranks continuous scores rather than thresholded labels. It is computed
against **four** negative images. Its confidence interval will be very wide, and
it could not be computed from the stored outputs, because the per-image scores
are not stored. It is computed from a rerun below.

Note also the training/validation AUC gap, 0.9333 against 0.6476, on a split
where 88.1% of validation images have an augmented sibling in training. The gap
is in the direction of memorisation despite that overlap, which makes the
validation figure the more generous of the two, not the more conservative.

## 4.1(6) The 13 validation images with no training sibling

96 of the 109 validation images have a sibling in training
(`S5_histopathology_leaked_validation.csv`, 96 rows, 81 distinct sources), so 13
do not. Recomputing the classifier metrics on those 13 is descriptive only —
and, given that the model predicts "Abnormal" for everything, it can only return
sensitivity 1.0 and specificity 0.0 or NaN on whatever subset is chosen. The
reproduction below identifies the 13 and confirms something stronger: all 13 are
TVNT positive, so the subset contains no negative class at all.

## 4.3 The R² convention — answered

`sklearn.metrics.r2_score`, imported at cell 9 line 5 and called at line 151 as

    r2 = r2_score(targets, preds_clipped)

guarded by `if np.var(targets) > 0` with `r2 = None` otherwise. Predictions are
clipped at zero first (`preds_clipped = np.maximum(preds, 0)`, line 137) because
the targets are counts.

`r2_score` is referenced to **the mean of the `y_true` passed in**, i.e. the
evaluation set's own mean. So an R² computed on the 109-image validation split
and one computed on the 435-image training split have different reference means
and different target variances, and are not comparable with each other. The
manuscript should say which set each R² is referenced to.

One stored value worth surfacing: on the validation set, Mitotic Figures has
**R² = −0.0154**. A negative R² means the model predicts that target worse than
its own evaluation-set mean would.

## The three regression heads

The weights confirm four heads: `head_tvnt` (1664 → 256 → 2) plus
`head_mitotic`, `head_nucleol` and `head_hyperchrom` (each 1664 → 128 → 1). The
notebook's `CLASS_NAMES` names them `{0: 'Mitotic Figures', 1: 'Multiple
Nucleol', 2: 'Nuclear Hyperchromatism'}`. These are what Table 3's MAE,
exact-match and R² columns describe; TVNT is the only classification target.

## What was blocked at the time of writing — now all done except one

4.1(1) the split, 4.1(2) the inference, the ROC-AUC bootstrap CI, both average
precisions, the source-level counts and 4.1(6) are all completed below. Only
4.2(4), the Rahman et al. thumbnail match, was **not attempted**.

## The stored metrics describe a checkpoint that no longer exists

This is independent of the missing data, and it is the most consequential thing
in this section.

The notebook's **evaluation** cell does not evaluate the model it saves for
deployment. Cell 9, lines 242-244:

    if os.path.exists("model_a_best.pth"):
        model.load_state_dict(torch.load("model_a_best.pth", map_location=DEVICE))
        print("✅ Loaded best model (model_a_best.pth) for evaluation\n")

and the stored output of that cell confirms the branch was taken:
`✅ Loaded best model (model_a_best.pth) for evaluation`. So the confusion
matrix, the 0.6476 AUC, and every Table 3 regression figure were computed on
**`model_a_best.pth`**, the lowest-validation-loss checkpoint saved at cell 8
line 95.

Cell 10 then saves a *different* file — `save_path = "model_a.pth"`, the
final-epoch model — and its stored output says so explicitly:

    ✅ Final model saved to model_a.pth
    ✅ Best validation model saved to model_a_best.pth
    📝 Note: Use 'model_a_best.pth' for inference (best validation performance)

The application loads `model_a.pth` (`main.py:119`, and
`ml_models/model_a/inference_model.py:88` defaults to the same name).

**And `model_a_best.pth` is not preserved anywhere.** Searched: the working
tree, every commit across all refs, every object in the object database, and
`git lfs ls-files --all`. Zero hits in all four.

Three consequences, all of which the revision has to state:

1. **The reported histopathology metrics do not describe the deployed model.**
   They describe a sibling checkpoint from the same run, selected on validation
   loss.
2. **They are not reproducible**, because the weights they were computed on no
   longer exist. Re-running the notebook's evaluation against `model_a.pth`
   would produce different numbers, and there is no way to recover the original
   ones.
3. The direction of the difference is not knowable without the missing file.
   Since `model_a_best.pth` was chosen for lowest validation loss on a split
   where 88.1% of validation images have a training sibling, the selection
   itself was made on contaminated data — so the reported figures are, if
   anything, the more favourable of the two.

Spec 4.1(2) asks to re-run `model_a.pth` inference on the validation split and
verify it against the stored outputs. When the images become available, that
comparison should be expected to **fail**, and the failure is the finding, not a
bug in the reproduction.

---

# Reproduction with the deployed checkpoint (added after the data arrived)

Run by `audit/scripts/model_a_reproduce.py`; full output in
`S36_model_a_reproduction.json`, per-image scores in
`S37_model_a_per_image_scores.csv`.

## The split reproduces exactly

`int(0.8 * 544) = 435` train, 109 validation, via
`random_split(..., generator=torch.Generator().manual_seed(42))`.

The pooled row order matters, because `random_split` permutes indices: cell 2
builds the record list with `os.listdir`, which is filesystem-ordered. Both
orderings were tried and scored against the 96 validation filenames the
published S5 records:

| pooling order | train / val | validation names matching S5 |
|---|---|---|
| **sorted** | 435 / 109 | **96 / 96** |
| raw `os.listdir` | 435 / 109 | 22 / 96 |

So the original run enumerated in sorted order, and the reproduced validation
split is **the same 109 images**. That also quantifies the hazard: had the
filesystem returned a different order, three-quarters of the validation set
would have differed, with the same code and the same seed.

Corpus check: TVNT Normal = 18, Abnormal = 526, exactly as stored.

## What reproduces, and what does not

Running **`model_a.pth`** — the deployed checkpoint — on that split, with
`val_transform` (deterministic):

| quantity | published (`model_a_best.pth`) | reproduced (`model_a.pth`) | verdict |
|---|---|---|---|
| confusion matrix | TN 0, FP 4, FN 0, TP 105 | **TN 0, FP 4, FN 0, TP 105** | **MATCH** |
| accuracy | 0.9633 | 0.9633 | MATCH |
| sensitivity | 1.0000 | 1.0000 | MATCH |
| **ROC-AUC** | **0.6476** | **0.8310** | **DOES NOT MATCH** |

The confusion matrix matching is not evidence that the checkpoints agree. Both
models predict "Abnormal" for every image, so the 2×2 table is fixed by the
class balance alone and cannot distinguish one checkpoint from another. The AUC
ranks continuous scores and does discriminate — and it differs by 0.18.

## Why the AUC differs: the evaluation itself was stochastic

`full_dataset` is constructed with `train_transform`, and `val_transform` is
defined but never used (it appears exactly twice in the notebook: at its
definition, and in the comment *"For proper validation, we should use
val_transform"*). The validation loader therefore wraps a Subset whose transform
applies `RandomHorizontalFlip`, `RandomVerticalFlip`, `RandomRotation(15)` and
`ColorJitter`, with no seed fixed at evaluation time.

Re-running the notebook's own pipeline five times on `model_a.pth`:

| run | confusion | accuracy | ROC-AUC |
|---|---|---|---|
| 1 | TN 0, FP 4, FN 0, TP 105 | 0.9633 | 0.7667 |
| 2 | TN 0, FP 4, FN 0, TP 105 | 0.9633 | 0.7881 |
| 3 | TN 0, FP 4, FN 0, TP 105 | 0.9633 | **0.6524** |
| 4 | TN 0, FP 4, FN 0, TP 105 | 0.9633 | 0.7690 |
| 5 | TN 0, FP 4, FN 0, TP 105 | 0.9633 | 0.6048 |

The AUC spans **0.605 to 0.788** across five draws of the same model on the same
images. The published 0.6476 sits inside that range, and run 3's 0.6524 is
within 0.005 of it.

**So the published AUC of 0.6476 is one draw from a random augmentation process,
not a property of the model.** It is not reproducible in principle, and the
difference from 0.8310 is attributable to the evaluation transform rather than
necessarily to the missing checkpoint. Two defects compound here: the metric was
computed on a checkpoint that no longer exists, *and* through a stochastic
pipeline. Neither can be recovered.

## Full classifier statistics for the deployed model (n = 109)

| statistic | value |
|---|---|
| sensitivity | 1.0000, CP 95% [0.9655, 1.0000] |
| **specificity** | **0.0000**, CP 95% [0.0000, 0.6024] |
| balanced accuracy | **0.5000** |
| accuracy | 0.9633 = the base rate exactly |
| base rate (positive) | 0.9633 |
| ROC-AUC | 0.8310, stratified bootstrap 95% **[0.6571, 0.9714]** |
| average precision, positive as target | 0.9924 |
| average precision, negative as target | **0.1872** |
| MCC | **undefined** (zero factor in the denominator; sklearn returns 0.0 by convention) |

The ROC-AUC interval spans 0.31 and reaches down towards chance, which is what
four negative images buys. Training-set figures for contrast: confusion
TN 0, FP 14, FN 0, TP 421, ROC-AUC 0.9554 [0.9046, 0.9919].

## The 13 validation images with no training sibling

All **13 are TVNT positive**. There is not a single negative among them, so
specificity and ROC-AUC are undefined on that subset (accuracy 1.0000 is
vacuous). Spec 4.1(6) asks for the classifier metrics there as a descriptive
check; the honest report is that the uncontaminated subset contains no negative
class at all and can support no discrimination estimate.

## Source-level counts

| | images | distinct sources |
|---|---|---|
| validation split | 109 | **94** |
| all pooled | 544 | **228** |

The 228 matches the Roboflow project's own `images: 228` exactly, independently
confirming that the 544 are three augmented versions of 228 source fields. At
source level the validation split is 94 units, not 109, and 96 of its 109 images
share a source with training.

## Regression heads, deployed checkpoint, deterministic (validation)

| target | MAE | RMSE | R² | exact match | within ±1 |
|---|---|---|---|---|---|
| mitotic | 0.1352 | 0.2831 | 0.0719 | 0.9358 | 0.9908 |
| nucleol | 1.7528 | 2.5191 | 0.7445 | 0.1835 | 0.5413 |
| hyperchrom | 2.0719 | 4.4330 | 0.4380 | 0.2661 | 0.6697 |

These do not match the stored values either — the notebook stores mitotic
MAE 0.1436 and R² −0.0154 on validation — for the same two reasons as the AUC.
Note R² here is referenced to this evaluation set's own mean.

## One further hazard found while loading the weights

`ml_models/model_a/inference_model.py:56` loads with **`strict=False`**. Each
head is `Linear → ReLU → Dropout → Linear`, so the final Linear sits at index 3.
An architecture that omits the Dropout puts it at index 2, and with
`strict=False` the mismatch loads silently, leaving the output layers randomly
initialised and every prediction meaningless — with no error. The shipped
architecture does match the checkpoint, so nothing is currently broken; the
reproduction script loads with `strict=True` so that any future drift is loud.
