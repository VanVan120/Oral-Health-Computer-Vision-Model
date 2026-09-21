# Dataset identity and duplicate regeneration (spec Phases 0.3, 0.4)

Both pinned versions were downloaded fresh on 2026-09-21 from the Roboflow REST
API, with the version number in the URL so "latest" can never be resolved by
accident and no version is generated.

## 0.3 Identity — ALL MATCH, no STOP

| check | expected | measured | verdict |
|---|---|---|---|
| Model B train / valid / test images | 7000 / 1500 / 1500 | 7000 / 1500 / 1500 | **MATCH** |
| Model B test instances | 9,688 | **9,688** | **MATCH** |
| Model B background (empty label) images | 0 | **0** | **MATCH** |
| Model A total images | 544 (474 / 44 / 26) | 544 (474 / 44 / 26) | **MATCH** |
| `data.yaml`, `README.roboflow.txt`, `README.dataset.txt` | present, both datasets | present | **MATCH** |

Per-class test instances, against the published supplementary S4:

| class | index | regenerated | published S4 |
|---|---|---|---|
| calculus | 0 | 1465 | 1465 |
| caries | 1 | 1694 | 1694 |
| gingivitis | 2 | 1544 | 1544 |
| hypodontia | 3 | 334 | 334 |
| tooth_discolation | 4 | 4153 | 4153 |
| ulcer | 5 | 498 | 498 |
| **total** | | **9688** | **9688** |

Every cell matches. `data.yaml` confirms `nc: 6` with the names in that order,
workspace `segp-fcn6m`, project `oral-diseases-5ctay-h9oye`, version 1,
licence CC BY 4.0.

### A counting trap worth recording

The first instance count came out as 8,189, not 9,688 — apparently a 1,499
shortfall and a STOP. It was an artifact of the *counting*, not the data:

    cat test/labels/*.txt | grep -c .        ->  8189   (wrong)

The label files carry no trailing newline, so `cat` joins the last line of each
file to the first line of the next, losing exactly one line per file boundary:
1500 files − 1 = 1499. Counting per file instead gives 9,688. The shortfall
being almost exactly the file count is the tell.

This is recorded because it is the same class of error the audit exists to find,
and because it would have produced a false STOP and a false "the dataset has
changed" claim.

### Model A: TVNT is derived, not annotated

`model_a/data.yaml` declares **three detection classes** — `Mitotic Figures`,
`Multiple Nucleol`, `Nuclear Hyperchromatism` — and no tumour/non-tumour class.
So the TVNT label the manuscript reports is **derived** from those annotations
by the notebook, not supplied by the dataset. This bears directly on R1.8.

## 0.4 Duplicate regeneration — EXACT, no STOP

| set | regenerated | published | set equality |
|---|---|---|---|
| D (full dihedral group) | 259 | S2, 259 | **EQUAL** (symmetric difference 0) |
| identity-only subset | 124 | S1, 124 | **EQUAL** (symmetric difference 0) |

D = 259, ND = 1500 − 259 = **1241**.

Per-transform yields, counting every transform that puts an image below
threshold (an image can qualify under more than one, so these exceed the union):

| transform | regenerated | published S0 README |
|---|---|---|
| identity | 124 | 124 |
| hflip | 150 | 150 |
| vflip | 145 | 144 |
| rot180 | 75 | 75 |
| rot90, rot270, transpose, transverse | 0 | 0 |
| **union** | **259** | **259** |

The single-image difference in the vflip yield does not affect the union or
either reported set. It is one image whose vflip distance sits within ~0.1 of
6.0 while some other transform already places it below threshold. The
best-scoring-transform tally differs likewise (regenerated hflip 80, vflip 77,
identity 59, rot180 43; published 85 / 74 / 63 / 37) because that tally is an
argmin over near-ties and shifts under distance differences far too small to
move set membership. The published S0 README already warns that this tally "is
not comparable" to the per-transform yields.

Both assertions the spec actually gates on — set equality with S2 and with S1 —
hold exactly.

## The finding: PIL draft mode silently breaks reflected matching

The first regeneration returned **228**, not 259: a strict subset of S2, missing
31 pairs, all of them reflected or rotated (hflip 11, rot180 11, vflip 9). Their
published distances were 0.39–2.70, i.e. essentially identical images, not
borderline cases — so this was not numerical drift.

The cause is `Image.draft()`. It asks libjpeg for a DCT-scaled decode, one
output pixel per 8×8 block at scale 1/8. Where a dimension is not a multiple of
8, the encoder padded the final block, and that padding sits only on the right
and bottom edges. The decoded thumbnail therefore carries an **asymmetric edge
artifact**, and an asymmetric artifact does not commute with reflection: for a
pair related by a flip, drafting both and then flipping one compares a padded
edge against a real edge.

These images are **612 × 408**, and 612 = 76·8 + 4 — the width has a partial
block. Measured on the first missing pair, `calculus-598` versus `calculus-742`
under rot180:

| | RMS |
|---|---|
| draft ON | **6.9408** — above the 6.0 threshold, pair missed |
| draft OFF | **0.3903** — exactly the published S2 distance |

Across the whole published S2, enabling draft moves the mean absolute deviation
from the published distances from 0.145 to 2.793. Identity pairs are barely
affected, which is why the 124 came out right either way and the defect hid.

`audit/scripts/near_duplicates.py` therefore sets `USE_DRAFT = False`, with the
reasoning recorded at the call site.

### What this means for the spec's description of the rule

The spec describes the published rule as "32 × 32 greyscale thumbnails (PIL
draft mode, then bilinear resampling)". Draft mode demonstrably cannot have been
in force when the published numbers were produced — with it, 31 of the 259 pairs
do not exist. The most likely explanation is that the August code called
`draft()` at a point where it had no effect: `draft()` is a no-op once the image
data has been loaded, so a call placed after any operation that triggers a load
silently does nothing. The description was then written from reading the code
rather than from its effect.

The pre-registered plan (`ANALYSIS_PLAN_R1.md` §1) does not mention draft — it
specifies "32 × 32 greyscale thumbnails, RMS < 6.0, minimum over the dihedral
group of order 8". Disabling draft is therefore faithful to the plan. It is
recorded under DEVIATIONS as D4 anyway, because the spec named it and the
difference is material.

## Residual numerical difference, and why it does not matter here

Even with draft off, the regenerated distances do not reproduce the published
ones to floating-point exactness: mean absolute deviation 0.145 over S2's 259
pairs, 0.060 over S1's 124. A grid search over resample filter (NEAREST, BOX,
BILINEAR, HAMMING, BICUBIC, LANCZOS), greyscale-before-versus-after-resize, and
draft on/off found no combination that reproduces them bit-exactly; BILINEAR
with greyscale first is the closest.

This does not threaten either reported set, and the published evidence says why:
the S0 README records that the 6.0 threshold "sits inside an empty band spanning
[3.92, 10.01)". No pair's minimum distance lands within 2 units of the
threshold, so a perturbation of order 0.1 cannot move any image across it — and
indeed both sets reproduce with zero symmetric difference.

The residual is most likely a libjpeg-turbo or Pillow version difference between
August 2026 and the pinned environment here (Pillow 12.3.0). It is reported
rather than explained away, and it is the reason the identity checks are stated
as set equality rather than as distance equality.
