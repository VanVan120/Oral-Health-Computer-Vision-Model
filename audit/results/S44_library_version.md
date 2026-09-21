# Phase 2.9: the ultralytics version effect, and where it comes from

Raw numbers in `S33_version_8.4.118.json`. Both versions run the same torch
2.7.1, the same CPU, FP32, and the same cached-evaluator replay.

## The effect reproduces the spec's expectation exactly

Full test split, batch 16:

| metric | 8.3.231 | 8.4.118 | version effect | spec expected |
|---|---|---|---|---|
| mAP@0.5 | 0.770997 | 0.766830 | **−0.004167** | 0.7710 → 0.7668 ✓ |
| mAP@0.5:0.95 | 0.401032 | 0.389203 | **−0.011828** | 0.4010 → 0.3892 ✓ |
| P | 0.7452059011127984 | 0.7452059011127984 | **0.000000** | — |
| R | 0.7283569800360402 | 0.7283569800360402 | **0.000000** | — |

Batch 1, the pinned evaluator:

| set | metric | 8.3.231 | 8.4.118 | version effect |
|---|---|---|---|---|
| full | mAP@0.5 | 0.770945 | 0.766750 | −0.004195 |
| full | mAP@0.5:0.95 | 0.400938 | 0.389135 | −0.011804 |
| ND | mAP@0.5 | 0.771942 | 0.767119 | −0.004823 |
| ND | mAP@0.5:0.95 | 0.402050 | 0.389903 | −0.012147 |

P and R are identical to all 16 significant figures in every case; only the AP
integrals move. Each effect is reported per metric, and mAP@0.5 is never set
beside mAP@0.5:0.95.

Removal effect under 8.4.118: Δ mAP@0.5 = +0.000369, Δ mAP@0.5:0.95 = +0.000768
— same sign, same order, same conclusion as under 8.3.231.

## 2.9(3) The decomposition, settled by direct comparison

The optional step asks whether the change comes from the predictions or from the
metric code. It does not need a code diff: the cached evaluator stores the exact
arrays the validator hands its metric accumulator, so the two versions can be
compared at that interface.

Over all 1,500 images and **61,159 predictions**:

| cached array | max abs difference |
|---|---|
| `tp` (n_pred × 10 IoU levels) | **0.0** |
| `conf` | **0.0** |
| `pred_cls` | **0.0** |
| `target_cls` | **0.0** |
| `target_img` | **0.0** |

Identical key sets, identical shapes, identical prediction counts (61,159 in
both). **The predictions, NMS and letterboxing are bit-identical. The entire
version effect is in the metric code.** That also explains P and R matching
exactly: both are read off the same curves at the max-F1 point.

## The exact change, and its direction

`ultralytics/utils/metrics.py`, `compute_ap`, is the only relevant difference:

```python
# 8.3.231
mrec = np.concatenate(([0.0], recall, [1.0]))
mpre = np.concatenate(([1.0], precision, [0.0]))

# 8.4.118
mrec = np.concatenate(([0.0], recall, [recall[-1] if len(recall) else 1.0], [1.0]))
mpre = np.concatenate(([1.0], precision, [0.0], [0.0]))
```

Both then take the precision envelope and integrate with 101-point COCO
interpolation.

Let `r_max` be the highest recall the model actually reaches. Under **8.3.231**
the curve runs straight from `(r_max, p)` to `(1.0, 0)`, so `np.interp` credits a
**linear ramp of precision across recall the model never achieved**. Under
**8.4.118** an extra point at `(r_max, 0)` is inserted first, so precision drops
to zero at `r_max` and the region beyond it contributes nothing.

**8.3.231 therefore overestimates AP, and 8.4.118 corrects it.** The correction
is a fix, not a regression, and the newer figures are the more defensible ones.

The mechanism predicts the relative sizes, which is a useful check: the spurious
region has width `1 − r_max`, so the effect must be larger where recall is
lower. At IoU 0.5:0.95 recall is much lower than at IoU 0.5, and indeed the
effect is **2.8× larger** on mAP@0.5:0.95 (−0.0118) than on mAP@0.5 (−0.0042).

## Why this matters more than the contamination effect

The version effect on mAP@0.5 is **−0.0042**. The effect of removing all 259
duplicated test images is **+0.0010** (Phase 2.3).

**Changing the ultralytics version moves the headline metric about four times as
much as removing every contaminated image, and about 2.8 standard deviations
further on mAP@0.5:0.95.** A reader comparing a Table 2 number (8.3.231) with a
Table 1 number (8.4.118) is reading a library-version artefact, not a result.

This is exactly the inconsistency raised as R1.3: the abstract's 0.7626/0.7670
and Table 1's 0.76682/0.76683 came from 8.4.118, while Table 2 came from
8.3.231. The revision's decision to pin one environment for every headline
number is the right fix, and this phase quantifies what was at stake: 0.0042 on
mAP@0.5 and 0.0118 on mAP@0.5:0.95, with predictions provably unchanged.

**Recommendation.** State the ultralytics version beside every detection metric,
and prefer 8.4.118's values, since its `compute_ap` is the corrected one. Note
that the checkpoint's own `version` field records 8.3.231 — that is the
*training-time* library, and it carries no implication about which version
should be used to evaluate.
