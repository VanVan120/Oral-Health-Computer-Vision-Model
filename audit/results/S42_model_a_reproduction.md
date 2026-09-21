# Model A: running the deployed checkpoint (spec Phase 4.1, addition 1)

Raw numbers in `S36_model_a_reproduction.json`; per-image scores for all 544
images in `S37_model_a_per_image_scores.csv`.

## The question asked

Run `model_a.pth` — the checkpoint the application actually loads — on the
reproduced 109-image validation split, and compare with the notebook's stored
outputs. Report how `model_a.pth` relates to `model_a_best.pth`.

## The split reproduces exactly

`random_split` with `torch.manual_seed(42)` over the 544 pooled images gives
435 / 109. Two directory orders were tried, because `os.listdir` is not sorted:

| order | n_train | n_val | val names matching published S5 (of 96) |
|---|---|---|---|
| **sorted** | 435 | 109 | **96 / 96** |
| listdir | 435 | 109 | 22 / 96 |

Sorted order recovers every one of S5's 96 leaked validation images, so the
split is reproduced, not approximated. All figures below use it.

## `model_a.pth` IS the evaluated checkpoint — the earlier reading was wrong

An earlier note in this audit said the published metrics describe "a checkpoint
that no longer exists". That is **half right and materially misleading**, and it
is corrected here.

`model_a_best.pth` is genuinely absent as a *file*: not in the working tree, not
in any of the 62 commits across all refs, not in any git object, not in
`git lfs ls-files --all`. But its **weights** are what `model_a.pth` contains.
The notebook's own execution counts prove it:

| cell | exec count | what it does |
|---|---|---|
| 8 | 22 | trains; `torch.save(model.state_dict(), "model_a_best.pth")` on improvement |
| 9 | 23 | `model.load_state_dict(torch.load("model_a_best.pth"))`, then evaluates |
| 10 | 24 | `torch.save(model.state_dict(), "model_a.pth")` |

The counts are consecutive — 22, 23, 24 — so cell 10 ran in the same kernel
session immediately after cell 9. Cell 9 had already overwritten the in-memory
`model` with the best weights, so cell 10 did **not** save the final-epoch
model. It re-serialised the best checkpoint under a second name. The comment
`# 7. Export Model` and the message `✅ Final model saved to model_a.pth` are
both inaccurate descriptions of what that line does.

Cell 10's stored output also confirms the file existed at the time:
`✅ Best validation model saved to model_a_best.pth`.

**Consequence:** `model_a.pth` and `model_a_best.pth` are the same weights.
Table 3 is not evaluating an unrecoverable sibling. It is evaluating the
deployed model, and the deployed model's performance *is* measurable — below.

The empirical check agrees. Re-running `model_a.pth` deterministically
reproduces the stored confusion matrix on **both** splits exactly, which would
be a remarkable coincidence for a different checkpoint:

| split | stored (cell 9) | `model_a.pth` re-run | |
|---|---|---|---|
| validation, n=109 | TN 0, FP 4, FN 0, TP 105 | TN 0, FP 4, FN 0, TP 105 | **MATCH** |
| training, n=435 | TN 0, FP 14, FN 0, TP 421 | TN 0, FP 14, FN 0, TP 421 | **MATCH** |

## What does NOT reproduce, and why

| quantity | stored | `model_a.pth`, deterministic | match? |
|---|---|---|---|
| confusion matrix (both splits) | see above | see above | **YES, exact** |
| TVNT ROC-AUC, validation | **0.6476** | **0.8310** | no |
| TVNT ROC-AUC, training | 0.9333 | 0.9554 | no |
| Mitotic MAE | 0.1436 | 0.1352 | no |
| Mitotic R² | −0.0154 | +0.0719 | no |
| Mitotic exact match | 93.58% (102/109) | 93.58% | **YES, exact** |
| Mitotic within ±1 / ±2 | 99.08% / 100% | 99.08% / 100% | **YES, exact** |
| Nucleol MAE | 2.0272 | 1.7528 | no |
| Nucleol R² | 0.6887 | 0.7445 | no |
| Nucleol exact match | 12.84% | 18.35% | no |
| Hyperchrom MAE | 2.1767 | 2.0719 | no |
| Hyperchrom R² | 0.4834 | 0.4380 | no |
| Hyperchrom exact match | 25.69% | 26.61% | no |

**The cause is the evaluation pipeline, not the weights.** Cell 6 builds the
dataset with the *training* transform and never reassigns it:

```python
train_transform = transforms.Compose([
    Resize((224,224)), RandomHorizontalFlip(), RandomVerticalFlip(),
    RandomRotation(15), ColorJitter(0.1,0.1,0.1), ToTensor(), Normalize(...)])
val_transform   = transforms.Compose([Resize((224,224)), ToTensor(), Normalize(...)])

full_dataset = OSCCRealDataset(IMG_DIR, CSV_FILE, transform=train_transform)
# Note: For proper validation, we should use val_transform     <-- author's own comment
```

`random_split` returns `Subset` views of that one object, so the validation
loader inherits `train_transform`. `val_transform` is defined and never used.
`model.eval()` and `torch.no_grad()` switch BatchNorm and dropout to inference
mode but do nothing to the input pipeline.

So **every stored validation number is one draw from a random augmentation
distribution** — random flips, a ±15° rotation and a colour jitter applied to
each validation image at evaluation time. Re-running the *augmented* path five
times with `model_a.pth` gives validation AUCs of:

    0.7667,  0.7881,  0.6524,  0.7690,  0.6048

The published **0.6476 lies inside this spread**. It is a sample, not a
property of the model. The deterministic value — the one that describes the
deployed model — is **0.8310**.

The pattern across the table is exactly what shared weights under a different
input transform predict: decisions thresholded at 0.5 are robust (both
confusion matrices identical), counts that round to small integers near zero are
robust (mitotic exact-match identical), and continuous quantities (MAE, R², AUC)
and larger counts (nucleol, hyperchrom) move.

## Deployed-model metrics, computed with `model_a.pth`

Per the instruction, these are treated as the deployed model's metrics.
Validation split, n = 109, deterministic transform:

| quantity | value | 95% interval |
|---|---|---|
| sensitivity | 1.0000 | Clopper–Pearson [0.9655, 1.0000] |
| specificity | 0.0000 | Clopper–Pearson [0.0000, 0.6024] |
| balanced accuracy | 0.5000 | — |
| accuracy | 0.9633 | = the base rate, exactly |
| base rate positive | 0.9633 | — |
| ROC-AUC | 0.8310 | bootstrap [0.6571, 0.9714], 10,000 resamples |
| AP, positive as target | 0.9924 | — |
| AP, negative as target | 0.1872 | — |
| MCC | **undefined** | 0/0; sklearn returns 0.0 by convention |

Training split, n = 435: sens 1.0000 [0.9913, 1.0000], spec 0.0000
[0.0000, 0.2316], bal acc 0.5000, AUC 0.9554 [0.9046, 0.9919], AP+ 0.9984,
AP− 0.6817, base rate 0.9678.

**The classifier still predicts "Abnormal" for every image in both splits.**
That conclusion is unchanged and is unaffected by the checkpoint question: FN =
0 and TN = 0 throughout. An AUC of 0.83 with specificity 0.00 is not a
contradiction — the scores do carry some ranking information, but every score
sits above the 0.5 decision threshold, so no image is ever called normal. A
ranking metric and a fixed-threshold metric are answering different questions,
and only the second describes what the deployed system does.

## Source-level structure and the unleaked subset

- 544 images from **228** distinct source photographs.
- Validation: 109 images from **94** distinct sources — 15 images are augmented
  copies of a source already in the validation set.
- 96 of the 109 have a source that also appears in training (the published S5).
- **Unleaked subset: 13 images.** All 13 are TVNT-positive, so specificity,
  balanced accuracy, ROC-AUC and MCC are all undefined on it; sensitivity is
  1.0000 [0.7529, 1.0000]. The subset cannot settle the question it was meant
  to settle, and that is a property of the split, not of this analysis.

## What this means for the manuscript

1. Table 3's AUC of 0.6476 should not be reported as a model property. It is
   one draw from a stochastic evaluation. Either report the deterministic
   0.8310 [0.6571, 0.9714], or report the augmented distribution as a
   distribution — not a single figure.
2. The deployed checkpoint is measurable and has been measured. The earlier
   "checkpoint that no longer exists" framing should not go into the revision.
3. The degeneracy finding stands and is the substantive one: specificity 0.0000
   on 4 validation negatives and 14 training negatives, accuracy equal to the
   base rate, MCC undefined.
