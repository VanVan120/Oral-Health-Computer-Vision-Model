# The deployed request path, and the class-mapping defect (spec Phases 3.1, 3.2, 3.3)

Branch `revision-r1`. All line numbers are from this branch's working tree.
Every claim below was read from the source, and the numeric and dictionary
content was transcribed directly rather than summarised.

## 3.1 What happens between upload and the text the user sees

There is exactly one upload endpoint in the deployed application:
`POST /analyze`, handler `analyze_image` ([main.py:194-196](../../main.py#L194-L196)).
The browser calls it from `APIService.analyzeImage` with a `FormData` field
named `file`.

Three other `UploadFile`/upload endpoints exist in the tree — in
`ml_models/model_a/api.py`, `ml_models/model_b/api.py` and
`ml_models/model_triage/app.py` (a **Flask** app) — but `main.py` mounts only
the auth, appointment, habits and chat routers, so none of those three is
reachable in the deployed app. This matters for one reason: the standalone
Flask app emits a *different* user-visible "Unknown" string, so any screenshot
taken from it would not represent the deployed behaviour.

The chain, in order:

1. **Save.** The upload is written to `temp_uploads/<uuid4>.<ext>`. The
   extension is taken from the client-supplied filename. A `finally` block
   deletes the file (main.py:264-268).

2. **Route.** `triage_router.predict(filepath)` (main.py:210), a module-level
   singleton built at import.

3. **Dispatch** on the returned string (main.py:223-253):
   - `"Histopathological"` -> Model A;
   - `"Clinical"` -> Model B;
   - **anything else** -> `response_data["error"] = "The uploaded image does not
     appear to be a valid oral health image (Clinical or Histopathological).
     Please upload a relevant image."`

   The `else` branch catches `"Unknown"`, but it also catches the router's two
   error returns, `"Error: Image file not found."` and
   `f"Error during inference: {str(e)}"`, because `TriageRouter.predict` catches
   its own exceptions and returns them as strings
   ([triage_inference.py:106-107](../../ml_models/model_triage/triage_inference.py#L106-L107)).
   **An internal failure is therefore presented to the user as "not a valid oral
   health image".** A router that crashed on every image would be
   indistinguishable, from the outside, from one rejecting out-of-domain input.
   This bears directly on how the Phase 3.5 router numbers should be read.

4. **Detect.** For a clinical image, `model_b.predict(filepath)` ->
   `OralHygieneModel.predict` (inference_model.py:65).

5. **Present.** The JSON response is rendered by `static/js/ui/model_b_ui.js`.
   No generative model touches this response; Gemini is only involved in a
   separate, user-initiated `POST /api/get-suggestion`.

### The router's decision rule

`TriageRouter.predict(image_path, threshold=0.95)`. `main.py:210` passes no
threshold, so **0.95** is the deployed value. The comparison is

    if confidence.item() < threshold:
        return "Unknown"

so a confidence of exactly 0.95 is accepted. `confidence` is the maximum softmax
probability over the two classes; `self.classes = ['Clinical', 'Histopathological']`,
index 0 and index 1 respectively, ordered to match the alphabetical `ImageFolder`
order used in training.

**Three gates fire before the network runs at all**
(triage_inference.py:76-86), on the full-resolution RGB array:

| gate | condition | result |
|---|---|---|
| brightness floor | `np.mean(img) < 40` | `"Unknown"` |
| brightness ceiling | `np.mean(img) > 250` | `"Unknown"` |
| detail floor | `np.std(img) < 15` | `"Unknown"` |

These must be reported alongside the router's softmax threshold: an image can be
rejected without the ResNet ever seeing it, so "rejected by the router" is not
the same as "the classifier was unconfident".

Preprocessing is `Resize((224, 224))`, `ToTensor()`, and `Normalize` with the
ImageNet statistics `[0.485, 0.456, 0.406]` / `[0.229, 0.224, 0.225]`.

### SAHI or plain YOLO

Selected on a single resolution test (inference_model.py:88):

    if width < 640 or height < 640:   ->  plain YOLO
    else:                             ->  SAHI sliced inference

- **Plain path**: `standard_model.predict(image_path, conf=0.15, imgsz=640)`.
- **SAHI path**: `get_sliced_prediction(img_rgb, sahi_model, slice_height=512,
  slice_width=512, overlap_height_ratio=0.2, overlap_width_ratio=0.2)`, with the
  SAHI model built at `confidence_threshold=0.15`.

**The Roboflow export is 640x640, so every benchmark image takes the SAHI
branch.** A 640x640 image is sliced into 512x512 tiles at 0.2 overlap. Any
end-to-end number computed on this benchmark therefore describes the SAHI path,
not the plain path, and the plain path is exercised only by smaller uploads.
This is why the Phase 3.2(iii) test captures the class index *inside* the chain
rather than calling the raw model separately: a raw standard-model call would
compare the two inference branches instead of isolating the name mapping.

### Per-class thresholds and the "No Issues Detected" branch

Both live in `_process_detection` (inference_model.py:166-189), which is the
single helper *both* branches funnel every box through. The thresholds are keyed
by **display name**:

    'Ulcers': 0.75, 'Tooth Discoloration': 0.40, 'Caries': 0.35,
    'Hypodontia': 0.60, 'Calculus': 0.25, 'Gingivitis': 0.30

with `confidence_thresholds.get(class_name, 0.25)` as the fallback. The 0.15
floor applied at inference is not binding, since every per-class threshold is
at or above 0.25.

"No Issues Detected" is returned when `len(detections) == 0` after thresholding
(inference_model.py:127-141), with `hygiene_score: "High"`. Note that
`screening_result = "Normal"` at line 144 is immediately overwritten at line 145
by `if len(detections) > 0`, which is always true at that point — so `"Normal"`
is **unreachable dead code**.

### Replicating it offline

Yes. An offline driver needs no web server: construct `TriageRouter(path)` and
`OralHygieneModel(path)` directly, then call `router.predict(image_path)` and,
on `"Clinical"`, `model.predict(image_path)`. Both take a filesystem path and
return plain Python structures. `main.py` adds only the upload, the temp file,
the dispatch and the cleanup.

## 3.2 Regression test

`tests/test_class_mapping.py`. Assertions (i) and (ii) are implemented and pass;
(iii) is implemented and skips without the dataset. The equivalent check in
`verify_classes.py`, run under the pinned 8.3.231 environment, output saved to
`S11_verify_classes_output.txt`:

    0 of 6 classes are reported under the wrong name.
    Mapping is correct: every class index resolves to the condition the
    weights say it is, and the display map covers the registry exactly.

## 3.3 The pre-fix permutation

The pre-fix dictionary, read verbatim from commit `7210dea` ("latest changes",
2026-04-24 13:04:02 +0800), at `ml_models/model_b/inference_model.py:30-33`:

    self.class_names = {
        0: 'Caries', 1: 'Calculus', 2: 'Gingivitis',
        3: 'Tooth Discoloration', 4: 'Ulcers', 5: 'Hypodontia'
    }

The model's own registry, read from `best.pt` itself, is
`{0: calculus, 1: caries, 2: gingivitis, 3: hypodontia, 4: tooth_discolation,
5: ulcer}`. The resulting permutation:

| index | true class (weights) | displayed PRE-fix | displayed POST-fix | pre-fix correct? |
|---|---|---|---|---|
| 0 | calculus | **Caries** | Calculus | NO |
| 1 | caries | **Calculus** | Caries | NO |
| 2 | gingivitis | Gingivitis | Gingivitis | yes |
| 3 | hypodontia | **Tooth Discoloration** | Hypodontia | NO |
| 4 | tooth_discolation | **Ulcers** | Tooth Discoloration | NO |
| 5 | ulcer | **Hypodontia** | Ulcers | NO |

**Five of six classes were displayed under the wrong name.** Only gingivitis
landed correctly. As a permutation of display labels it is one transposition and
one 3-cycle: (Calculus Caries) and (Hypodontia -> Tooth Discoloration -> Ulcers
-> Hypodontia). The fixing commit `0b21474` ("Key display names on the model's
class registry, not on index", 2026-08-13 15:55:35 +0800) states the same
finding independently in its message.

### The defect was not only a relabelling — and this changes how 3.3 must be read

The per-class threshold dictionary is keyed by display name, and it is
**byte-identical** at `7210dea` (lines 140-147) and after the fix (lines
169-176). Because the *name* was wrong pre-fix, the *threshold lookup* was wrong
too: each detection was tested against some other class's threshold.

| true class | correct threshold | threshold actually applied pre-fix | effect |
|---|---|---|---|
| calculus | 0.25 | 0.35 (Caries) | stricter — detections lost |
| caries | 0.35 | 0.25 (Calculus) | looser — extra detections |
| gingivitis | 0.30 | 0.30 (Gingivitis) | unchanged |
| hypodontia | 0.60 | 0.40 (Tooth Discoloration) | looser — extra detections |
| tooth_discolation | 0.40 | 0.75 (Ulcers) | stricter — detections lost |
| ulcer | 0.75 | 0.60 (Hypodontia) | looser — extra detections |

So the historical application did not merely print the wrong word on the right
finding: **the set of findings reported also differed**, in both directions.

Spec 3.3(4) asks for the pre-fix dictionary to be applied to the class indices
captured in the current chain, which isolates the mapping and is the right
estimand for "how many displayed findings would have carried the wrong name".
But that quantity is a *lower bound* on the historical discrepancy, because it
holds the surviving detection set fixed at the post-fix thresholds. The
manuscript should say which of the two it is reporting. Quantifying the second
effect needs the test images and is not done here.

One further pre-fix difference: the lookup was
`self.class_names.get(cls_id, "Unknown")`, a silent fallback, whereas the fixed
code raises on an unknown class name. The fallback is unreachable for indices
0-5, so it changes nothing for these six classes, but it is why a renamed class
could previously pass through and silently receive the default 0.25 threshold.

## Two display defects found in passing (not in the spec)

1. **`screening_result` has no translation for "Issues Detected", and the user
   is shown the raw key.** The lookup key is built by stripping spaces from the
   backend string (`static/js/ui/model_b_ui.js:217`):

       const screeningResultKey = 'screeningResult' + data.screening_result.replace(/\s+/g, '');
       screenRes.textContent = t(screeningResultKey, data.screening_result);

   `static/js/language.js` defines `screeningResult`, `screeningResultNormal`,
   `screeningResultNoIssuesDetected` and `screeningResultRefertoDentist` in all
   four language blocks (en at 459/579/580/581, ms at 1075/1195/1196/1197, zh at
   1663/1783/1784/1785, ta at 2265/2385/2386/2387) — but there is no
   `screeningResultIssuesDetected` in any of them (grep count: 0).

   The second argument to `t` looks like a fallback but is not one for this
   case. `model_b_ui.js:185` defines
   `const t = (key, fallback) => window.AppLanguage ? window.AppLanguage.t(key) : fallback;`
   so the fallback applies only when `AppLanguage` is missing entirely, and
   `AppLanguage.t` is `return lang[key] || key` (language.js:2427-2429), which
   returns **the key** when the key is absent.

   So whenever the backend returns `"Issues Detected"` — at least one finding,
   with no ulcer and no caries among them — the heading the user sees is the
   literal string `screeningResultIssuesDetected`.

2. **`screening_result = "Normal"` is unreachable**, as described above.

Neither affects any metric in the manuscript. Both are user-visible and are
recorded here because they were found while tracing the path the manuscript
describes.
