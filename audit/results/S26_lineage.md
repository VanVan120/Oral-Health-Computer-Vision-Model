# Dataset lineage (spec Phase 5.4) — resolved from the Roboflow API

Raw payload: `S22_dataset_download_and_lineage.json`. Fetched 2026-09-21 with
the key from the environment; the key is not recorded anywhere in the output.

## `segp-fcn6m/oral-diseases-5ctay-h9oye` (Model B, detection)

| field | value |
|---|---|
| name / type | `oral-diseases`, object-detection |
| images | 10,000 (0 unannotated) |
| licence | **CC BY 4.0**, public |
| classes (instances) | calculus 9,172 · caries 11,868 · gingivitis 10,254 · hypodontia 2,382 · tooth_discolation 26,636 · ulcer 3,558 |
| project created | 2024-08-03 |
| versions | **1** — `2025-12-06 1:56pm`, 10,000 images, splits 7000 / 1500 / 1500 |
| preprocessing | auto-orient (EXIF stripping) only |
| **augmentation** | **none** |

The README states it outright: *"No image augmentation techniques were
applied."*

**This is a substantive finding, not bookkeeping.** Model B's near-duplicates
are therefore **not** a Roboflow artifact. Roboflow applied no augmentation to
this project, so the 259 test images with a training near-duplicate — including
the 150 that match only under a horizontal flip and the 75 under a 180° rotation
— were already duplicated, in those orientations, **in the source images as
uploaded**. The contamination was imported with the data, not introduced by the
platform.

That also rules out the most natural benign explanation for the reflected
duplicates, and it means the duplication cannot be undone by regenerating the
dataset version.

Note the single version, dated **2025-12-06 1:56pm**. The warm-start checkpoint
`eec5aba9` is dated 2025-12-06T15:51:39 and the released checkpoint
2025-12-12T16:33:59, so both post-date the only version of this dataset. The
`oral-diseases-1` directory named in both `train_args.data` values is consistent
with this version-1 export.

## `segp-fcn6m/oral-cancer-1mnve-n5yij` (Model A, histopathology)

| field | value |
|---|---|
| name / type | `Oral Cancer`, **object-detection** |
| project-level images | **228** |
| licence | **CC BY 4.0**, public |
| classes (instances) | Mitotic Figures 26 · Multiple Nucleol 1,091 · Nuclear Hyperchromatism 831 |
| versions | 2 — v1 `2026-02-03 9:16pm`, v2 `2026-02-03 9:34pm`; both 544 images, splits 474 / 44 / 26 |
| preprocessing | auto-orient, resize 512×512 (stretch), auto-contrast via adaptive equalisation |
| **augmentation** | **3 versions of each source image**: 50% horizontal flip, 50% vertical flip, equal-probability 90° rotation (none / cw / ccw / 180°), random crop 0–20% |

Three consequences.

1. **The project holds 228 source images; the export holds 544.** The difference
   is Roboflow augmentation, which creates three versions of each *training*
   source image. So the 544 are not 544 independent fields of tissue.

2. **This is the authoritative answer to the upstream-augmentation question**
   (Phase 5.5, Q4): the augmentation is declared, with its exact operations.
   Combined with the notebook's re-split, it is the mechanism behind the 96 of
   109 validation images that have a training sibling.

3. **The dataset is an object-detection project with three nuclear-feature
   classes and no tumour/non-tumour class.** The TVNT label the manuscript
   reports does not exist in the data; it is derived by the notebook as
   `tvnt = 1 if counts['has_objects'] else 0` — "this image has at least one
   annotated box". See `S27_model_a_reproduction.md`.

Versions 1 and 2 have identical image counts, splits, preprocessing and
augmentation, and were generated 18 minutes apart. Nothing distinguishes them
in the metadata.

## Reference 8 and reference 9 — NOT ESTABLISHED

The manuscript cites `tesisdientes/oral-diseases-5ctay-rqpxs` (ref 8) and
`oral-cancer-zui33/oral-cancer-1mnve` (ref 9).

The API returns **no fork or source field** for either `segp-fcn6m` project. The
full key list it exposes is

    annotation, augmentation, classes, colors, created, icon, id, images,
    license, multilabel, name, preprocessing, public, splits, type,
    unannotated, updated, versions

with no `forkedFrom`, `source`, `parent` or `universe` entry. `README.dataset.txt`
says only *"Provided by a Roboflow user"* for both. `universe.roboflow.com`
returns HTTP 403 to non-browser clients.

**So the fork relationship can be neither confirmed nor refuted from any source
available here.** What can be stated is the comparison the revision needs:

| | classes | images |
|---|---|---|
| ref 8, `tesisdientes/oral-diseases-5ctay-rqpxs` | 4 (calculos, caries, gingivitis, ulcera) — search-index evidence, **INFERRED** | ~4,162 |
| actually used, `segp-fcn6m/oral-diseases-5ctay-h9oye` | **6** (calculus, caries, gingivitis, hypodontia, tooth_discolation, ulcer) — API, **MEASURED** | **10,000** |

Reference 8 as printed therefore does not describe the dataset used: different
class count, different class list, different image count. That much is solid and
is enough to correct the citation to the project actually used, with its own
Universe URL and CC BY 4.0 licence.

The shared slug stems (`oral-diseases-5ctay-*`, `oral-cancer-1mnve-*`) remain
consistent with a fork, but that is a naming-pattern inference and must not be
printed as established provenance. Recommended wording for the revision: cite
`segp-fcn6m/oral-diseases-5ctay-h9oye` v1 and
`segp-fcn6m/oral-cancer-1mnve-n5yij` v2 directly, state the licence, and say
that the upstream origin of these Roboflow projects is not recorded by the
platform.
