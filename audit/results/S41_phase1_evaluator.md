# The exact cached evaluator (spec Phase 1)

## 1.1 What is cached

`audit/scripts/cached_evaluator.py` subclasses ultralytics'
`DetectionValidator` and, for each image keyed by `batch["im_file"]`, records
**exactly the dict the validator hands to its metric accumulator** —
`tp` (n_pred × 10 IoU levels), `conf`, `pred_cls`, `target_cls`, `target_img` —
taken from `DetMetrics.stats` immediately after `super().update_metrics()`
appends it. Nothing about the matching is re-implemented: `_process_batch` and
`match_predictions` run untouched.

`evaluate(image_multiset)` builds a fresh `DetMetrics`, replays those same
entries through `update_stats`, and calls `DetMetrics.process` — which is the
call `get_stats` makes. It is a multiset, not a set, because the bootstrap draws
images with replacement and an image drawn twice must contribute twice.

Predicted and ground-truth boxes are also cached in **original-image
coordinates**, mapped with the validator's own `scale_preds` / `ops.scale_boxes`
so the transform matches what it would export.

Two implementation notes that matter:

- The cache is keyed in the validator's own iteration order, which is *not*
  filename order — see 1.2.
- The entry stores every key the installed version accumulates, plus `im_name`.
  8.4.118 does not keep `im_name` in `stats` but its `update_stats` requires it
  (for `Metric.update_image_metrics`), while 8.3.231 neither stores nor wants
  it. Passing the whole entry lets one evaluator serve both pinned versions,
  which Phase 2.9 needs.

## 1.2 Exactness gate — **PASSED**

`evaluate()` against a genuine `val(batch=1)` run, on every reported metric
including per-class P, R, AP50 and AP50-95:

| set | images | max abs diff | verdict |
|---|---|---|---|
| full split | 1500 | **0.0** | PASS |
| ND | 1241 | **0.0** | PASS |
| ctrl1 (seed 20260921) | 1241 | **0.0** | PASS |
| ctrl2 (seed 20260921) | 1241 | **0.0** | PASS |

Exact agreement, not agreement to 1e-9.

### The first attempt failed, and the cause is worth recording

The first run gave 0.0 on three sets and **6.158e-08** on ctrl2, on
`tooth_discolation/AP50_95` — above the 1e-9 gate. The spec is right to insist
the cause be found rather than tolerated.

The cause is concatenation order, not the evaluator. `val()` runs with
`rect=True`, which sorts the dataloader by aspect ratio; this split has **338
distinct image sizes**, so the validator's order differs from filename order.
`DetMetrics.process` concatenates the per-image arrays and `ap_per_class` takes
float32 cumulative sums over them, and a float32 cumsum is order-sensitive.
`tooth_discolation` is the most numerous class (4,153 instances), so it
accumulates the most.

Replaying the cached entries **in the validator's own order** removes the
difference entirely. Both are reported: for ctrl2, 6.158e-08 in filename order
and 0.0 in validator order. The effect is bounded by float32 precision and is
four orders of magnitude below the removal effect being measured (~1e-3), but
the gate is met exactly rather than argued around.

## 1.3 Batch sensitivity — and it does NOT explain the August discrepancy

Full test split, ultralytics 8.3.231, CPU, `rect=True`:

| metric | val(batch=16) | spec expected | val(batch=1) | batch16 − batch1 |
|---|---|---|---|---|
| P | 0.74521 | 0.7452 | 0.74542 | −0.00021 |
| R | 0.72836 | 0.7284 | 0.73123 | **−0.00287** |
| mAP@0.5 | 0.77100 | 0.7710 | 0.77094 | +0.00006 |
| mAP@0.5:0.95 | 0.40103 | 0.4010 | 0.40094 | +0.00009 |

**All four batch-16 values reproduce the spec's expected figures exactly at the
precision they are quoted.** No deviation to report.

The mechanism is real but small where it matters. In rect mode the dataloader
sorts by aspect ratio and pads every batch to its largest member, so batch
composition changes the letterbox padding each image receives. The split has 338
distinct image sizes, which is why the effect exists at all — and why batch 16
is much *slower* here than batch 1 (386.7 ms/image against ~76 ms), since small
images get padded up to the batch maximum.

It moves **recall** by 0.0029, which is the largest single effect, but moves
mAP@0.5 by only **0.00006**.

### Does it explain the August 0.0025 discrepancy? **NO.**

The August gap between the offline evaluator (0.7643) and `val()` (0.7668) was
0.0025 in mAP@0.5. The batch effect on mAP@0.5 measured here is 0.00006 —
**about 44 times too small**. Batch composition can be ruled out as the
explanation.

The remaining candidate is the one this phase was built to eliminate: the August
offline evaluator re-implemented the prediction-to-ground-truth matching instead
of reusing the validator's. That is precisely why the Phase 1 evaluator caches
the validator's own `tp`/`conf`/`pred_cls` arrays and replays them through
`DetMetrics.process`, and why the exactness gate is set at 1e-9 — a
re-implementation drifting by 0.0025 would fail that gate by five orders of
magnitude. The August number itself cannot be re-derived, because that
evaluator's code is not in the repository, so this is an inference about the
cause rather than a measurement of it, and is labelled as such.

## 1.4 Additional caches

Test (1,500), validation (1,500) and **all 7,000 training images**. The training
pass took about 11 minutes on CPU, far inside the spec's two-hour threshold, so
no sampling was needed: the training figures are over the complete split, not a
seeded sample of 2,000. The training twins of D are evaluated as a subset of the
training cache, so they need no separate pass.

## Headline evaluator output (batch 1, ultralytics 8.3.231, CPU, FP32)

| set | images | instances | P | R | mAP@0.5 | mAP@0.5:0.95 |
|---|---|---|---|---|---|---|
| All | 1500 | 9688 | 0.74542 | 0.73123 | 0.77094 | 0.40094 |
| ND | 1241 | 7413 | 0.75397 | 0.72675 | 0.77194 | 0.40205 |

D therefore carries **2,275** instances (9,688 − 7,413), which matches the
published supplementary S4 figure `contam_instances_orient259 = 2275` exactly —
an independent confirmation that the regenerated D is the published D.

Per class, full split:

| class | instances | images | P | R | AP@0.5 | AP@0.5:0.95 |
|---|---|---|---|---|---|---|
| calculus | 1465 | 342 | 0.6675 | 0.6007 | 0.6402 | 0.2811 |
| caries | 1694 | 536 | 0.7741 | 0.7922 | 0.8282 | 0.4361 |
| gingivitis | 1544 | 297 | 0.6288 | 0.5039 | 0.5537 | 0.2381 |
| hypodontia | 334 | 184 | 0.7067 | 0.7485 | 0.7684 | 0.3507 |
| tooth_discolation | 4153 | 610 | 0.7745 | 0.8304 | 0.8776 | 0.5718 |
| ulcer | 498 | 274 | 0.9208 | 0.9116 | 0.9575 | 0.5279 |

All revised detector figures come from this evaluator. The originally reported
values (batch 16, GPU) belong only in the reproducibility paragraph.
