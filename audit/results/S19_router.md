# The domain router (spec Phase 3.5, part 1)

Part 2 — evaluating the router on the three sets — is blocked: it needs the
Model B test split, the 544 Model A images, and COCO128. Only COCO128 is
obtainable without the Roboflow key. What follows is everything the code and the
weights establish.

## Architecture and classes

`ml_models/model_triage/triage_inference.py`:

- `models.resnet18(pretrained=False)` with `fc` replaced by
  `nn.Linear(num_ftrs, 2)`. Confirmed against the weights: `triage_router.pth`
  is a bare state dict of 122 tensors whose `fc.weight` is `(2, 512)`.
- `self.classes = ['Clinical', 'Histopathological']` — index 0 and index 1.
  The source comment justifies the order: *"Classes must match the alphabetical
  order of ImageFolder used during training"*.

That justification checks out. `train_triage_robust.py:32` sets
`self.classes = sorted(os.listdir(root_dir))`, so the index order is
alphabetical, giving Clinical = 0 and Histopathological = 1. Note that
`1_prepare_triage_split.py:9` declares
`CLASSES = ["Histopathological", "Clinical"]` in the opposite order, but that
list only drives directory creation and does not set the index order, so it is
not a defect.

**The weights store no class names.** Which index means what is fixed by a
hard-coded list in the inference module, not by the checkpoint. There is no
mechanism that would detect a mismatch — this is structurally the same hazard as
the Model B defect, and it is currently unguarded.

## Preprocessing

`Resize((224, 224))`, `ToTensor()`, `Normalize([0.485, 0.456, 0.406],
[0.229, 0.224, 0.225])` — ImageNet statistics.

## The deployed decision rule

Threshold **0.95**, confirmed: `main.py:210` calls `triage_router.predict(filepath)`
with no threshold argument, and the signature default is
`def predict(self, image_path, threshold=0.95)`. The comparison is

    if confidence.item() < threshold:
        return "Unknown"

so exactly 0.95 is accepted. `confidence` is the max softmax probability over
the two classes.

**"Unknown" is not a class.** It is a threshold decision on a 2-class softmax,
which matters for how the Phase 3.5 proportions are described.

### Three gates fire before the network

`triage_inference.py:76-86`, on the full-resolution RGB array, before any
tensor is built:

| gate | condition | result |
|---|---|---|
| brightness floor | `np.mean(img_np) < 40` | `"Unknown"` |
| brightness ceiling | `np.mean(img_np) > 250` | `"Unknown"` |
| detail floor | `np.std(img_np) < 15` | `"Unknown"` |

Any COCO128 rejection rate will mix these gates with genuine classifier
uncertainty, and the two must be reported separately or the number is
uninterpretable. The evaluation script for Phase 3.5 should record which of the
four exit paths each image took.

### Errors are indistinguishable from rejections

`TriageRouter.predict` catches its own exceptions and returns
`f"Error during inference: {str(e)}"` as a string; a missing file returns
`"Error: Image file not found."`. `main.py`'s `else` branch treats every string
that is not `"Clinical"` or `"Histopathological"` identically, showing the user
"The uploaded image does not appear to be a valid oral health image". So a
router failing on every image would look, from the outside, exactly like a
router correctly rejecting out-of-domain input.

## Training data — and why overlap is UNKNOWN

The training data is **not in the repository and is not recoverable**.

- `1_prepare_triage_split.py:7-8`: `SOURCE_ROOT = Path("./dataset")`,
  `DEST_ROOT = Path("./dataset_final")`. It splits `./dataset/<class>/` into an
  ImageFolder tree at `SPLIT_RATIO = 0.8`, `SEED = 42`.
- Line 20 confirms `./dataset` is assembled by hand: *"Please create it and add
  your '{CLASSES[0]}' and '{CLASSES[1]}' folders."*
- `train_triage_robust.py:15`: `DATA_DIR = './dataset_final'`. ResNet-18, SGD
  `lr=0.001`, `momentum=0.9`, `StepLR(step_size=7, gamma=0.1)`, 25 epochs.

Neither `./dataset` nor `./dataset_final` is committed at any point in history,
and nothing records which images were put into them.

**So the answer to spec 3.5(4) is UNKNOWN**, and it should be reported with that
word. It cannot be strengthened from the records that exist.

One lead was considered and rejected. Model A's notebook writes its converted
corpus to a directory also named `dataset`
(`Model_A_Training_Master.ipynb` cell 2, `OUTPUT_DATASET_PATH = "dataset"`),
which superficially matches the triage script's `./dataset`. But the structures
differ: Model A's contains `images/` and `labels.csv`, whereas the triage
script expects `dataset/Clinical/` and `dataset/Histopathological/` class
folders. This is a name collision, **not** evidence that the router trained on
Model A's corpus. It is recorded so the same false lead is not followed again.

That said, the prior is not neutral. The obvious way to populate a folder of
clinical and histopathology images, in this project, is from the same two
Roboflow datasets the models use. If so, the router's evaluation on the Model B
test split and the 544 Model A images would be an evaluation on its own training
data. **This is a real risk to the Phase 3.5 numbers and must be stated
alongside them**, precisely because it cannot be ruled out.

## A second entry point with different behaviour

`ml_models/model_triage/app.py` is a standalone **Flask** app constructing
`TriageRouter()` with no `model_path`, so it falls back to the bare relative
default `'triage_router.pth'`. It is not mounted by `main.py` and is not part of
the deployed chain, but it emits a different user-visible string for the
rejected case. Any screenshot or demo taken from it would not represent the
deployed behaviour.

## Stored training outputs

`2_train_triage.ipynb` carries five stored stream outputs only — four stdout and
one stderr. There is no confusion matrix, no sklearn import, no classification
report and no stored figure: `grep -c 'confusion\|sklearn\|classification_report'`
over the notebook returns **0**, and no output is of type `display_data` or
`execute_result`.

What is stored is a 20-epoch train/val log (`Epoch 0/19` … `Epoch 19/19`) ending:

    train Loss: 0.0033 Acc: 1.0000
    val   Loss: 0.0014 Acc: 1.0000
    Training complete in 6m 6s
    Best val Acc: 1.000000

**The router reports 100% accuracy on its own validation split.** Two things
follow. First, this is a training-time number on a split drawn from the same
hand-assembled `./dataset`, so it says nothing about the three sets Phase 3.5
asks about and cannot stand in for the missing evaluation. Second, a perfect
score is unsurprising for a task as visually separable as clinical photographs
versus stained histopathology slides, and it therefore carries no information
about the behaviour that actually matters in deployment: what the router does
with out-of-distribution input. That is exactly what the COCO128 arm of Phase
3.5 is for, and it has not been run.
