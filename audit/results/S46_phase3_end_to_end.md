# Phase 3: the deployed path, end to end over the 1,500 test images

Raw numbers in `S34_end_to_end_test.json` (per-image records included),
`S35_router_eval.json`, `S45_image_level_wilson.json`.

Everything here runs the repository's **own** modules — `inference_model.py` and
`triage_inference.py` are imported and called, not reimplemented — so the
thresholds, the gates, the SAHI decision and the name mapping are the deployed
ones.

## 3.3(1) SAHI never fires. The benchmark does not exercise the sliced path

`sahi_path_counts`: **standard 1500, sahi 0.**

The condition in `inference_model.py` is `if width < 640 or height < 640:` →
standard, else SAHI with 512×512 slices at 0.2 overlap. Measured over the test
split:

| quantity | value |
|---|---|
| images with width ≥ 640 **and** height ≥ 640 | **0 / 1500** |
| distinct image sizes | 338 |
| width range | 123 – 644 |
| height range | **33 – 612** |
| most common size | 612×408 (359 images) |

Height never reaches 640, so the SAHI branch is unreachable on this data.

**This corrects an earlier note in this audit** (`S13`), which said the Roboflow
export was 640×640 and therefore every benchmark image would take the SAHI path.
It is not 640×640: the export preserved the original dimensions, which are mostly
small web-sized photographs.

The consequence is substantive. **SAHI is a headline feature of the deployed
system and no reported number tests it.** A phone photograph — the intended
input — is far larger than 640×640 and would take a code path that the entire
evaluation leaves untouched. Anything the manuscript claims about tiled
inference for "tiny details" is unevidenced.

## 3.3(2) Post-fix agreement

11,831 detections were mapped. Agreement between the captured class index and
the displayed label is **100%**, and it is 100% *by construction*: after commit
0b21474 the display name is derived from the checkpoint's own `names` registry
rather than from a hard-coded dictionary, so a permutation of the kind that
existed before is no longer representable. This is verified rather than assumed,
and `tests/test_class_mapping.py` locks it (39 passed, 6 skipped).

## 3.3(3) The pre-fix path — primary result, full 7210dea simulation

Per deviation **D2**, the primary result simulates the whole historical path:
the old dictionary *and* the per-class thresholds looked up by the wrong display
name. The mapping-only estimand pre-specified in the plan is retained as
secondary.

| | **FULL path (primary)** | mapping only (secondary) |
|---|---|---|
| displayed findings, total | 1,994 | 2,106 |
| displayed findings under a wrong name | **1,464** | 1,582 |
| share wrong | **73.4%** | 75.1% |
| images with any wrong name | **1,302 / 1,500 (86.8%)** | 1,309 / 1,500 |
| images where *every* displayed name was wrong | **1,074 / 1,500 (71.6%)** | 1,011 / 1,500 |

(A "finding" is a distinct display name on one image, not a box.)

The two differ because the wrong threshold changes which detections survive at
all — the full path reports *fewer* findings (1,994 vs 2,106), since the two
stricter mis-lookups (calculus judged at 0.35, tooth_discolation at 0.75) remove
more than the three looser ones add.

**Roughly seven of every ten images shown to a user in that period carried only
incorrect condition names.**

### The permutation, measured

Box-level counts of true class → displayed name under the pre-fix path:

| index | true class (weights) | displayed pre-fix | detections | correct? |
|---|---|---|---|---|
| 0 | calculus | Caries | 1,162 | **NO** |
| 1 | caries | Calculus | 1,792 | **NO** |
| 2 | gingivitis | Gingivitis | 1,178 | yes |
| 3 | hypodontia | Tooth Discoloration | 301 | **NO** |
| 4 | tooth_discolation | Ulcers | 1,962 | **NO** |
| 5 | ulcer | Hypodontia | 413 | **NO** |

Each true class maps to exactly one display name, so the defect is a clean
permutation — one transposition (0↔1) and one 3-cycle (3→4→5→3) — and five of
six classes are wrong. Gingivitis is correct only because index 2 happens to be
a fixed point.

## 3.3(4) / 3.5 The three image-quality gates

Per deviation **D3**, gate rejections are counted separately from softmax
rejections, because an image rejected for being too dark was never classified.

| set | n | `gate_brightness_low` (<40) | `gate_brightness_high` (>250) | `gate_low_detail` (std<15) | softmax < 0.95 |
|---|---|---|---|---|---|
| Model B test | 1500 | **3** | 0 | 0 | **341** |
| Model A histopathology | 544 | **0** | 0 | 0 | **134** |
| COCO128 (out of domain) | 128 | **3** | 0 | 0 | **114** |

The gates are nearly inert: 6 rejections across 2,172 images, all from the
dark-image check, and neither the over-bright nor the low-detail gate ever
fires. **The router's behaviour is essentially entirely the softmax threshold.**

## 3.5 Router at its deployed threshold of 0.95

| set | n | routed correctly | "Unknown" | wrong domain |
|---|---|---|---|---|
| Model B test (expect Clinical) | 1500 | 1156 — **0.7707** [0.7487, 0.7912] | 344 — 0.2293 [0.2088, 0.2513] | **0** [0.0000, 0.0026] |
| Model A (expect Histopathological) | 544 | 410 — **0.7537** [0.7158, 0.7880] | 134 — 0.2463 [0.2120, 0.2842] | **0** [0.0000, 0.0070] |
| COCO128 (expect rejection) | 128 | 117 — **0.9141** [0.8527, 0.9513] | 117 | **11 — 0.0859** [0.0487, 0.1473] |

Wilson 95% intervals. Two clear findings:

1. **The router refuses about a quarter of the system's own in-domain images** —
   22.9% of the detector's benchmark split and 24.6% of the histopathology set.
   These are the exact images the system is built for.
2. **It never confuses the two clinical domains** (0 wrong-domain routes on
   either in-domain set), but it **accepts 8.6% of COCO128** — 10 photographs of
   ordinary objects routed to the oral detector and 1 to the histopathology
   model.

**Overlap with the router's training data: UNKNOWN.** `./dataset` was assembled
by hand and never committed at any commit. The stored training log reports
"Best val Acc: 1.000000" on its own split. Since the obvious way to build that
folder is from these same two Roboflow projects, this evaluation may be partly
an evaluation on training data, and that cannot be resolved from the records
that exist. Any router number in the manuscript must carry that caveat.

## 3.4 Image-level reporting, with and without the router

Per condition, over all 1,500 images, with Wilson 95% intervals. "Reported when
present" is the image-level sensitivity a user actually experiences.

**With the router (the deployed system):**

| condition | reported when present | reported when absent | no finding when present |
|---|---|---|---|
| Calculus | 280/342 = 0.8187 [0.7744, 0.8559] | 41/1158 = 0.0354 [0.0262, 0.0477] | 0.0673 [0.0452, 0.0989] |
| Caries | 391/536 = 0.7295 [0.6903, 0.7654] | 41/964 = 0.0425 [0.0315, 0.0572] | 0.1978 [0.1662, 0.2336] |
| Gingivitis | 213/297 = 0.7172 [0.6634, 0.7654] | 45/1203 = 0.0374 [0.0281, 0.0497] | 0.0808 [0.0549, 0.1174] |
| Hypodontia | 95/184 = 0.5163 [0.4445, 0.5874] | 1/1316 = 0.0008 [0.0001, 0.0043] | 0.3424 [0.2777, 0.4135] |
| Tooth Discoloration | 481/610 = 0.7885 [0.7544, 0.8191] | 74/890 = 0.0831 [0.0667, 0.1031] | 0.1246 [0.1007, 0.1532] |
| **Ulcers** | **100/274 = 0.3650 [0.3102, 0.4235]** | 0/1226 = 0.0000 [0.0000, 0.0031] | **0.6241 [0.5654, 0.6794]** |

**Without the router (detector alone):**

| condition | reported when present | reported when absent | no finding when present |
|---|---|---|---|
| Calculus | 293/342 = 0.8567 [0.8156, 0.8899] | 48/1158 = 0.0415 [0.0314, 0.0545] | 0.0058 [0.0016, 0.0211] |
| Caries | 489/536 = 0.9123 [0.8853, 0.9334] | 45/964 = 0.0467 [0.0351, 0.0619] | 0.0131 [0.0063, 0.0267] |
| Gingivitis | 233/297 = 0.7845 [0.7343, 0.8275] | 46/1203 = 0.0382 [0.0288, 0.0506] | 0.0000 [0.0000, 0.0128] |
| Hypodontia | 126/184 = 0.6848 [0.6145, 0.7476] | 2/1316 = 0.0015 [0.0004, 0.0055] | 0.1522 [0.1074, 0.2111] |
| Tooth Discoloration | 544/610 = 0.8918 [0.8647, 0.9140] | 84/890 = 0.0944 [0.0769, 0.1154] | 0.0066 [0.0026, 0.0167] |
| Ulcers | 196/274 = 0.7153 [0.6592, 0.7655] | 0/1226 = 0.0000 [0.0000, 0.0031] | 0.2664 [0.2176, 0.3217] |

**Overall "No Issues Detected" rate: 0.2687 [0.2468, 0.2917] with the router,
0.0740 [0.0618, 0.0884] without it.**

### What the router costs

| condition | Δ reported-when-present (with − without) |
|---|---|
| **Ulcers** | **−0.350** |
| Caries | −0.183 |
| Hypodontia | −0.169 |
| Tooth Discoloration | −0.103 |
| Gingivitis | −0.067 |
| Calculus | −0.038 |

The router removes a third of ulcer detections and roughly a fifth of caries
detections, and it more than triples the rate at which a user with a visible
condition is told "No Issues Detected" (7.4% → 26.9%). None of the detector
metrics in the manuscript include this, because they are computed on the
detector alone. **The mAP figures describe a component; the table above
describes the product.**

Ulcers are worst-hit for a compounding reason: its deployed threshold is the
highest of any class (0.75), so it loses detections at both stages.

## Not estimable from this benchmark, and to be stated as such

The split contains no healthy mouths and no patient identifiers, so none of the
following can be derived from it at any confidence: patient-level sensitivity,
specificity in healthy mouths, positive or negative predictive value at
population prevalence, and referral burden. "Reported when absent" above is
per-condition within images that all contain some other condition — it is not a
false-positive rate in a healthy population.
