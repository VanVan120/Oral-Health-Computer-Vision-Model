# Checkpoint provenance (spec Phases 0.2, 5.1, and inputs to 3.5 and 4.1)

All three checkpoints were fetched from git-lfs on 2026-09-21 and verified
against their committed LFS pointer oids. Read under the pinned environment
(ultralytics 8.3.231, torch 2.7.1, CPU).

## Detector — `ml_models/model_b/models/best.pt`

SHA-256 `4de8714f0f2b52a70564cc1be55058262564ced400cd8a7d5815192477aad0cc`
— starts `4de8714f`, ends `7aad0cc`, as the spec requires. **MATCH.**

Full metadata in `S10_best_pt_metadata.json`. The load needed
`weights_only=False`, because from torch 2.6 the default refuses a checkpoint
that pickles ultralytics' own classes. The file's hash is verified before it is
opened, so this is not an unpickle of unknown origin.

| field | value |
|---|---|
| `date` | 2025-12-12T16:33:59.554724 |
| `version` | **8.3.231** |
| `names` | 0 calculus, 1 caries, 2 gingivitis, 3 hypodontia, 4 tooth_discolation, 5 ulcer |
| architecture | DetectionModel, nc 6, depth 0.67, width 0.75 — YOLOv8m |
| `epoch` / `best_fitness` | -1 / None (optimizer stripped on save) |

The `version` field is worth stating plainly in the revision: the released
checkpoint was **written by ultralytics 8.3.231**, which is the version the
revision pins for all headline figures. The pin is therefore the training-time
version, not an arbitrary choice.

### `train_args` (provenance-critical subset)

| arg | value |
|---|---|
| `model` | `Backend Development/Model B/models/best.pt` |
| `data` | `/home/hfyic3/Backend Development/Model B/oral-diseases-1/data.yaml` |
| `epochs` | 200 (requested) |
| `patience` | 20 |
| `batch` | **100** (explicit, not AutoBatch) |
| `seed` | 0 |
| `deterministic` | True |
| `pretrained` | True |
| `device` | `'0'` (a single GPU) |
| `workers` | 16 |
| `imgsz` / `iou` / `max_det` | 640 / 0.7 / 300 |
| `rect` | False |
| `project` / `name` | `oral_cancer_screening` / `yolov8m_evolved_final` |
| `save_dir` | not present in `train_args` |

Three things follow directly.

1. **The warm start is a previous checkpoint of this same project, not a stock
   release.** `train_args.model` is `Backend Development/Model B/models/best.pt`
   — a relative path to a `best.pt` inside the project tree. Combined with
   `pretrained: True`, the released model is at least a second-generation
   checkpoint. What that earlier `best.pt` was trained on cannot be read from
   this file; it is the open question behind R1.2 and R2.9.

2. **Training ran on Linux under user `hfyic3`, on one GPU.** The `data` path is
   `/home/hfyic3/...`, and the dataset directory is `oral-diseases-1`, i.e. a
   Roboflow export of `oral-diseases` **version 1** — consistent with the pinned
   `oral-diseases-5ctay-h9oye` v1. The evaluation environment for this revision
   is macOS on CPU, which is a documented difference, not a silent one.

3. **`batch` was 100, and `epochs: 200` did not run to completion.**
   `train_results` holds **48** epochs, so with `patience: 20` training stopped
   early at epoch 48 and the best epoch was around 28. The manuscript should not
   describe this as a 200-epoch run.

### `train_metrics` stored in the checkpoint

    fitness              0.38766
    metrics/mAP50(B)     0.75956
    metrics/mAP50-95(B)  0.38766
    metrics/precision(B) 0.73058
    metrics/recall(B)    0.73320
    val/box_loss         1.78334
    val/cls_loss         1.34736
    val/dfl_loss         1.35858

**These are validation-split figures recorded at training time, on GPU, at batch
100, under ultralytics 8.3.231.** They are not test-split figures and must not
be set beside the abstract's 0.7626/0.7670 or Table 1's 0.76682/0.76683, which
are test-split numbers. Recorded here so the distinction is explicit.

## Histopathology classifier — `ml_models/model_a/model_a.pth`

SHA-256 `b469110a551aa4bb93189b05a424fa28239dc4f710983e779b41acf7a19a2d3f`.
A bare `OrderedDict` state dict, 1029 tensors, loadable with
`weights_only=True`. No class names, no training metadata, no optimizer state:
nothing about provenance is recoverable from the file itself.

- **Backbone**: DenseNet with dense blocks of 6/12/32/32 layers and 1664 output
  features, i.e. **DenseNet-169**.
- **Four heads**, so this is a multi-task model, not a single classifier:

  | head | shape | target |
  |---|---|---|
  | `head_tvnt` | 1664 -> 256 -> **2** | tumour vs non-tumour, 2-class |
  | `head_mitotic` | 1664 -> 128 -> **1** | scalar |
  | `head_nucleol` | 1664 -> 128 -> **1** | scalar |
  | `head_hyperchrom` | 1664 -> 128 -> **1** | scalar |

This answers spec 4.1.5 from the weights alone: besides TVNT there are three
scalar regression heads — mitotic figures, nucleoli, hyperchromatism — which are
what the MAE, exact-match and R^2 columns of manuscript Table 3 must refer to.
Whether the TVNT label itself is meaningful is Phase 4.2's question and needs
the images.

## Domain router — `ml_models/model_triage/triage_router.pth`

SHA-256 `59cb5a8d8445927a92b0fd0d502fc56b650a16c1a9be94246bc2d2115088f5e2`.
A bare state dict, 122 tensors, `weights_only=True`.

- `conv1`/`bn1`/`layer1..4` with 512 channels at `layer4` and two BasicBlocks per
  stage: **ResNet-18**.
- `fc.weight` is `(2, 512)`, so **two output classes**.

The checkpoint stores no class names, so which index means clinical and which
means histopathology can only come from the training code, not from the weights.
The deployed "Unknown" outcome is therefore a thresholding decision on a 2-class
softmax, not a third class.
