# Phase 2: what the 259 duplicated test images actually do

Raw numbers: `S29_contamination_stats.json` (2.2–2.4), `S30_control_deltas.csv`
(30,000 control deltas), `S31_memorisation.json` (2.6), `S32_secondary.json`
(2.5, 2.7), `S25_clusters.json` (2.1), `S38`/`S40` (2.8).

All detector figures on this page come from the Phase 1 cached evaluator,
ultralytics 8.3.231, CPU, FP32, batch 1 — one evaluator, one environment.

## 2.1 Clusters

1,445 connected components over the 1,500 test images: 1,394 singletons, 47 of
size 2, 4 of size 3. 214 components contain at least one D image, 1,231 contain
none. 104 edges come from a shared training twin and 59 from test–test
duplicates. The component, not the image, is the resampling unit in 2.3.

## 2.2 Headline

| set | images | instances | P | R | mAP@0.5 | mAP@0.5:0.95 |
|---|---|---|---|---|---|---|
| All | 1500 | 9688 | 0.74542 | 0.73123 | 0.77094 | 0.40094 |
| ND | 1241 | 7413 | 0.75397 | 0.72675 | 0.77194 | 0.40205 |
| D | 259 | 2275 | 0.56268 | 0.75338 | 0.66023 | 0.31508 |

D carries **2,275** instances = 9,688 − 7,413, matching the published
supplementary S4 figure `contam_instances_orient259 = 2275` exactly.

## 2.3 Removal effect — the headline result of this audit

**Δ (ND − All) mAP@0.5 = +0.000997**, cluster bootstrap 95% CI
**[−0.01249, +0.01418]**
**Δ (ND − All) mAP@0.5:0.95 = +0.001111**, 95% CI **[−0.00738, +0.00957]**

10,000 resamples over the 1,445 clusters (214 containing D, 1,231 not).

Removing every duplicated image *raises* mAP@0.5 by one part in a thousand, and
the interval comfortably spans zero. **The contamination does not measurably
inflate the headline metric.**

## 2.4 Randomization — and the power the study actually had

259 images are removed at random and the same Δ recomputed, 10,000 times.
Stratified draws match D on dominant class × instance-count bin; unstratified
draws ignore both.

| design | metric | control mean | SD | 2.5–97.5% | observed Δ | rank | p (2-sided) | MDE |
|---|---|---|---|---|---|---|---|---|
| stratified | mAP@0.5 | −0.002413 | 0.003911 | [−0.00994, +0.00529] | +0.000997 | 80.7 | **0.390** | 0.01095 |
| stratified | mAP@0.5:0.95 | +0.000329 | 0.002501 | [−0.00457, +0.00527] | +0.001111 | 62.5 | **0.751** | 0.00700 |
| unstratified | mAP@0.5 | −0.000339 | 0.003321 | [−0.00678, +0.00612] | +0.000997 | 65.8 | **0.688** | 0.00930 |
| unstratified | mAP@0.5:0.95 | −0.000099 | 0.002523 | [−0.00508, +0.00487] | +0.001111 | 68.8 | **0.620** | 0.00707 |

Removing *these* 259 images is statistically indistinguishable from removing
*any* 259. Nothing about D's identity matters to the headline metric.

**The MDE is the number the revision should quote.** This design could only
have detected an effect of about **0.011 mAP@0.5** or **0.007 mAP@0.5:0.95**.
An inflation smaller than that is not ruled out — it is simply beyond what
1,500 test images can resolve. "No detectable effect" is the claim; "no effect"
is not.

### Balance

| quantity | D | control mean (stratified) |
|---|---|---|
| images | 259 | 259 |
| instances removed | 2275 | 2139.5 |
| mean instances / image | 8.78 | 8.26 |
| calculus / caries / gingivitis | 455 / 251 / 597 | 365.1 / 226.3 / 501.1 |
| hypodontia / tooth_discolation / ulcer | 144 / 825 / **3** | 139.1 / 908.0 / **0.0** |

Stratification balances image counts exactly and instance counts approximately.
It cannot balance ulcer: D contains only 3 ulcer instances and the controls
average 0.0, because ulcer is nowhere near dominant in any stratum D draws from.
Ulcer contrasts are therefore not interpretable and are excluded from 2.5.

**22 strata; 2 could not be filled from their own bin and were widened**, which
is reported rather than silently merged:

- `caries | ≥16 instances`: D needs 4, ND has **0** → widened to `caries | 8-15`
- `caries | 1 instance`: D needs 26, ND has 25 → widened to `caries | 2-3`

That ND contains *no* caries-dominant image with ≥16 instances while D contains
four is itself a composition difference worth noting: the duplicated images are
not a random sample of the split.

## 2.5 Per-class contrasts, D vs ND

`t_global` = **0.2823**, from the max of the smoothed mean F1 curve on the full
split. The committed `BoxF1_curve.png` legend records 0.285 for the original
run — close, but that run's split, version and batch size are unrecorded, so the
agreement is a sanity check, not a reproduction.

Five eligible classes (ulcer excluded, above). ΔAP = D − ND:

| class | AP50 D | AP50 ND | ΔAP50 | ΔAP50-95 |
|---|---|---|---|---|
| calculus | 0.6253 | 0.6481 | −0.0228 | −0.0048 |
| caries | 0.7514 | 0.8385 | −0.0871 | −0.0572 |
| gingivitis | 0.5646 | 0.5495 | +0.0151 | +0.0124 |
| hypodontia | 0.7992 | 0.7462 | +0.0530 | +0.0494 |
| tooth_discolation | 0.8121 | 0.8909 | −0.0788 | −0.0908 |

Recall and precision deltas at both thresholds, with cluster-bootstrap 95% CIs
(2,000 resamples):

| class | ΔR at t_global | ΔR at deployed | ΔP at t_global | ΔP at deployed |
|---|---|---|---|---|
| calculus (0.25) | +0.025 [−0.057, +0.110] | +0.023 [−0.064, +0.104] | −0.055 [−0.132, +0.024] | −0.054 [−0.132, +0.022] |
| caries (0.35) | −0.039 [−0.118, +0.038] | −0.069 [−0.152, +0.011] | −0.057 [−0.155, +0.032] | −0.053 [−0.149, +0.041] |
| gingivitis (0.30) | +0.074 [−0.021, +0.171] | +0.070 [−0.025, +0.161] | −0.032 [−0.128, +0.058] | −0.031 [−0.124, +0.062] |
| hypodontia (0.60) | +0.026 [−0.090, +0.142] | +0.003 [−0.144, +0.150] | +0.010 [−0.108, +0.126] | +0.018 [−0.093, +0.124] |
| tooth_discolation (0.40) | −0.049 [−0.104, +0.001] | **−0.067 [−0.130, −0.008]** | **−0.071 [−0.129, −0.012]** | **−0.062 [−0.126, −0.007]** |

**Nine of ten recall intervals include zero, and the only class that clears zero
does so in the wrong direction**: on tooth_discolation the model is *worse* on
the duplicated images than on the clean ones.

This is the opposite of what memorisation predicts, and it is the single most
important qualitative result in Phase 2. D is not a set the model has an
advantage on. Section 2.6 explains why.

## 2.6 Memorisation diagnostics

**(a) M by split** — train / validation / test, same evaluator:

| split | images | instances | P | R | mAP@0.5 | mAP@0.5:0.95 |
|---|---|---|---|---|---|---|
| train | 7000 | 44786 | 0.87238 | 0.88620 | 0.93416 | 0.61313 |
| valid | 1500 | 9396 | 0.73178 | 0.73121 | 0.75769 | 0.38737 |
| test | 1500 | 9688 | 0.74542 | 0.73123 | 0.77094 | 0.40094 |

The train–test gap is large (mAP@0.5 0.934 vs 0.771) — an ordinary overfitting
gap, and notably *not* a contamination signal, since validation and test agree
closely with each other.

**(b) Twin concordance** — 259 duplicate pairs, box matching at normalised IoU:

| | precision | recall | F1 |
|---|---|---|---|
| class-agnostic | 0.6857 | 0.6721 | 0.6788 |
| class-aware | 0.6686 | 0.6554 | 0.6619 |

2,275 boxes on the test side against 2,230 on the twin side. **Only 57 of 259
pairs (22.0%) have identical label sets**, and there are 38 box-level class
disagreements.

**This is the key finding of Phase 2.** These are the *same photograph* appearing
in both splits, and their annotations disagree about a fifth of the time — in
geometry and in class. Examples: a `calculus` box on the test side annotated
`caries` on the train side; `calculus` against `tooth_discolation`. Ulcer is
starkest: 3 boxes test-side, **0** twin-side.

A duplicated image whose twin carries a *different* label cannot help the model
— it trains the model toward the wrong answer for that test image. That is why
D underperforms ND.

**(c) Recall against own labels vs twin labels**, at t_global:

| subset | vs own labels | vs twin labels |
|---|---|---|
| all D (n=259) | 0.6844 | 0.6955 |
| differing-label subset (n=202) | 0.6717 | 0.6835 |

The model agrees *slightly better with the training twin's annotation than with
the test image's own annotation* — +0.011 on all D, +0.012 on the differing
subset. Small, but in the direction memorisation predicts: the model reproduces
what it was trained on rather than what the test set asks for. Because the two
label sets disagree, that costs it measured recall instead of gaining it.

**(d) M on the training twins vs M on D:**

| set | images | instances | P | R | mAP@0.5 | mAP@0.5:0.95 |
|---|---|---|---|---|---|---|
| training twins (own labels) | 224 | 1974 | 0.78921 | 0.83585 | 0.88202 | 0.54968 |
| D | 259 | 2275 | 0.56268 | 0.75338 | 0.66023 | 0.31508 |

The same 224 photographs score **0.882** with their training labels and
**0.660** with their test labels. The images are identical up to a dihedral
transform; only the annotations differ. The 0.22 mAP@0.5 gap is a measure of
**annotation inconsistency between the splits**, not of image difficulty.

## 2.7 Validation contamination

`S7_valid_train_pairs.csv`: **256** validation images match a training image
under the dihedral rule, **120** under identity alone — exactly the figures the
spec expected (256 / 120).

| validation set | images | instances | mAP@0.5 | mAP@0.5:0.95 | fitness |
|---|---|---|---|---|---|
| full | 1500 | 9396 | 0.75769 | 0.38737 | 0.42440 |
| de-duplicated | 1244 | 7179 | 0.74827 | 0.38264 | 0.41920 |
| Δ | | | **−0.00942** | **−0.00473** | **−0.00520** |

De-duplicating validation makes it *harder*, by about one part in a hundred —
the same order as the test-split effect and the same sign story. Model
selection used `fitness`; the difference of 0.0052 is far smaller than the gap
between adjacent epochs in the stored `train_results`, so no checkpoint choice
turns on it.

## 2.8 Photometric tier

Dropped, with reasons, in `S40_photometric_tier.md`. The substantive output is a
lower-bound statement: relaxing the rule by one invariance — global brightness
and contrast — raises the contaminated set from 259 to 422, a 63% increase, with
no gap in the distribution at any cut. Every duplicate count in this manuscript
is a lower bound.

## What Phase 2 supports, and what it does not

**Supported:**
- The test split contains 259 duplicated images (17.3%), and validation 256.
- Those images' annotations disagree with their training twins about 78% of the
  time, and the model tracks the training annotation more closely than the test
  one.
- The duplicate count is a lower bound; a mild relaxation gives 422.

**Not supported, and the revision should stop claiming it:**
- That the contamination inflates the headline detection metrics. Δ mAP@0.5 =
  +0.001 [−0.012, +0.014], p = 0.39–0.69, and removing these 259 images is
  indistinguishable from removing any 259.

**The honest framing** is that this benchmark cannot resolve an effect below
~0.011 mAP@0.5, and the measured effect is an order of magnitude smaller than
that. The finding worth reporting is the **annotation inconsistency**, which is
large, well-estimated, and independent of the power problem.
