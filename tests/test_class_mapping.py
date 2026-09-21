"""End-to-end regression test for the class index -> display name mapping.

This is the test that would have caught the defect described in the manuscript:
the deployment layer once carried its own index -> condition dictionary, which
drifted out of step with the class order baked into the weights, so findings
were shown to users under the wrong condition name.

The three assertions mirror the three ways that defect can come back:

  (i)   the display-label map no longer covers the weights' class registry
        exactly -- a stale key, a missing key, or a renamed class;
  (ii)  a detection of class index i is presented as some other class's name --
        the permutation bug itself, checked for every index through the real
        deployed code path;
  (iii) the whole deployed path, run on a real image the raw model fires on,
        disagrees with the raw model about which condition was found.

EXPECTED_MAPPING below is deliberately hard-coded rather than derived from
DISPLAY_NAMES. A test that builds its expectation out of the same dictionary it
is testing cannot fail. These values were read off the trained weights and
cross-checked against two independent artifacts committed with the original
work: the legend of runs/detect/val/BoxF1_curve.png, and the class_id/class_name
columns of the published supplementary S4. If the weights are ever retrained,
this table must be updated deliberately, by a human, and that is the point.

Tests that need the weights skip cleanly when the weights are absent, so the
suite still runs on a checkout that has not fetched git-lfs objects.

Environment variables:
  MODEL_B_WEIGHTS    override the checkpoint path
  MODEL_B_TEST_DIR   directory of test-split images, enabling assertion (iii)
"""

import importlib.util
import os
import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
INFERENCE_MODULE = REPO_ROOT / "ml_models" / "model_b" / "inference_model.py"
WEIGHTS = pathlib.Path(
    os.environ.get("MODEL_B_WEIGHTS", REPO_ROOT / "ml_models/model_b/models/best.pt")
)

# index -> (name baked into the weights, label the user is intended to see)
EXPECTED_MAPPING = {
    0: ("calculus", "Calculus"),
    1: ("caries", "Caries"),
    2: ("gingivitis", "Gingivitis"),
    3: ("hypodontia", "Hypodontia"),
    # The training data ships this class misspelled. Showing it corrected is a
    # declared display choice, not drift; see verify_classes.py.
    4: ("tooth_discolation", "Tooth Discoloration"),
    5: ("ulcer", "Ulcers"),
}

# Read from _process_detection. Keyed by display label, as the deployed code is.
DEPLOYED_THRESHOLDS = {
    "Ulcers": 0.75,
    "Tooth Discoloration": 0.40,
    "Caries": 0.35,
    "Hypodontia": 0.60,
    "Calculus": 0.25,
    "Gingivitis": 0.30,
}

LFS_POINTER_PREFIX = b"version https://git-lfs"


def _weights_reason():
    """Why the weights cannot be used, or None if they can."""
    if not WEIGHTS.exists():
        return f"weights not present at {WEIGHTS}"
    if WEIGHTS.read_bytes()[:40].startswith(LFS_POINTER_PREFIX):
        return f"{WEIGHTS} is a Git LFS pointer; run 'git lfs install && git lfs pull'"
    return None


requires_weights = pytest.mark.skipif(
    _weights_reason() is not None, reason=_weights_reason() or ""
)


def _load_deployment_layer():
    """Import inference_model.py by path; it is not an importable package."""
    spec = importlib.util.spec_from_file_location(
        "model_b_inference_under_test", INFERENCE_MODULE
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def deployment():
    return _load_deployment_layer()


@pytest.fixture(scope="module")
def model_names():
    """The class registry as the weights themselves report it."""
    from ultralytics import YOLO

    return YOLO(str(WEIGHTS)).names


@pytest.fixture(scope="module")
def deployed_model(deployment):
    """A real OralHygieneModel, i.e. the object the API actually serves from."""
    return deployment.OralHygieneModel(str(WEIGHTS))


# --------------------------------------------------------------------------
# (i) the display-label map covers the weights' registry exactly
# --------------------------------------------------------------------------


@requires_weights
def test_display_name_keys_equal_model_registry(deployment, model_names):
    assert set(deployment.DISPLAY_NAMES) == set(model_names.values()), (
        "DISPLAY_NAMES keys must equal the class names in the weights exactly. "
        f"only in DISPLAY_NAMES: {sorted(set(deployment.DISPLAY_NAMES) - set(model_names.values()))}; "
        f"only in the weights: {sorted(set(model_names.values()) - set(deployment.DISPLAY_NAMES))}"
    )


@requires_weights
def test_weights_carry_the_expected_class_registry(model_names):
    """Pin the registry itself, so a swapped checkpoint fails loudly here."""
    actual = {i: n for i, n in sorted(model_names.items())}
    expected = {i: name for i, (name, _label) in EXPECTED_MAPPING.items()}
    assert actual == expected


# --------------------------------------------------------------------------
# (ii) every class index resolves to its intended label, through the real path
# --------------------------------------------------------------------------


@requires_weights
@pytest.mark.parametrize(
    ("index", "class_name", "expected_label"),
    [(i, n, l) for i, (n, l) in sorted(EXPECTED_MAPPING.items())],
)
def test_synthetic_detection_presents_intended_label(
    deployed_model, index, class_name, expected_label
):
    """A synthetic detection of index `index` must surface as `expected_label`.

    This drives _process_detection, the same helper both the standard and the
    SAHI branch funnel every box through, so it exercises the deployed index ->
    label step rather than a reimplementation of it.
    """
    detections, findings, counts = [], set(), {
        name: 0 for name in deployed_model.class_names.values()
    }

    deployed_model._process_detection(
        cls_id=index,
        conf=0.99,  # comfortably above every per-class threshold
        bbox=[10.0, 20.0, 110.0, 120.0],
        detections=detections,
        findings=findings,
        counts=counts,
    )

    assert len(detections) == 1, "a 0.99-confidence detection must survive thresholding"
    assert detections[0]["class"] == expected_label
    assert findings == {expected_label}
    assert counts[expected_label] == 1
    # Nothing else may be incremented: a permutation bug would light up a
    # different class here even when the label on this one happens to be right.
    assert [k for k, v in counts.items() if v] == [expected_label]


@requires_weights
@pytest.mark.parametrize(
    ("index", "class_name", "expected_label"),
    [(i, n, l) for i, (n, l) in sorted(EXPECTED_MAPPING.items())],
)
def test_detection_below_deployed_threshold_is_dropped(
    deployed_model, index, class_name, expected_label
):
    """The per-class threshold must bind to the class it is written for.

    If the index -> label step were permuted, a box would be tested against
    another class's threshold. Probing just below this class's own threshold
    catches that even when the emitted label looks plausible.
    """
    threshold = DEPLOYED_THRESHOLDS[expected_label]
    detections, findings, counts = [], set(), {
        name: 0 for name in deployed_model.class_names.values()
    }

    deployed_model._process_detection(
        cls_id=index,
        conf=threshold - 0.01,
        bbox=[10.0, 20.0, 110.0, 120.0],
        detections=detections,
        findings=findings,
        counts=counts,
    )

    assert detections == [], (
        f"a detection at {threshold - 0.01:.2f} is below {expected_label}'s "
        f"deployed threshold of {threshold} and must not be reported"
    )


@requires_weights
def test_deployed_thresholds_cover_every_class(deployed_model):
    """Guard the fallback: an unlisted class silently gets 0.25."""
    assert set(DEPLOYED_THRESHOLDS) == set(deployed_model.class_names.values())


# --------------------------------------------------------------------------
# (iii) a real image the raw model fires on is presented under the same name
# --------------------------------------------------------------------------


def _test_images():
    raw = os.environ.get("MODEL_B_TEST_DIR")
    if not raw:
        return []
    root = pathlib.Path(raw)
    if not root.is_dir():
        return []
    return sorted(
        p for p in root.rglob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )


# How many images to scan before giving up on the rarer classes. One pass, not
# one pass per class: a naive per-class search costs six full sweeps.
MAX_IMAGES_SCANNED = int(os.environ.get("MODEL_B_TEST_SCAN", "400"))


@pytest.fixture(scope="module")
def real_image_evidence(deployed_model):
    """First real image per class index, with the deployed output for it.

    The class index is captured *inside* the deployed chain, immediately before
    the name mapping, by wrapping _process_detection. That is what isolates the
    mapping: comparing against a separate raw-model call would instead be
    comparing the two inference branches, because these images are 640x640 and
    so always take the SAHI branch, whereas a raw standard-model call would not.
    """
    images = _test_images()
    if not images:
        return {}

    original = type(deployed_model)._process_detection
    captured = []

    def recording(self, cls_id, conf, bbox, detections, findings, counts):
        captured.append((int(cls_id), float(conf)))
        return original(self, cls_id, conf, bbox, detections, findings, counts)

    evidence = {}
    try:
        type(deployed_model)._process_detection = recording
        for path in images[:MAX_IMAGES_SCANNED]:
            captured.clear()
            out = deployed_model.predict(str(path))
            if "error" in out:
                continue
            for index, (_name, label) in EXPECTED_MAPPING.items():
                if index in evidence:
                    continue
                threshold = DEPLOYED_THRESHOLDS[label]
                if any(c == index and v >= threshold for c, v in captured):
                    evidence[index] = {
                        "path": path,
                        "output": out,
                        "captured": list(captured),
                    }
            if len(evidence) == len(EXPECTED_MAPPING):
                break
    finally:
        type(deployed_model)._process_detection = original

    return evidence


@requires_weights
@pytest.mark.parametrize(
    ("index", "class_name", "expected_label"),
    [(i, n, l) for i, (n, l) in sorted(EXPECTED_MAPPING.items())],
)
def test_real_image_presents_intended_label(
    real_image_evidence, index, class_name, expected_label
):
    """On a real image, a detection of index `index` is displayed as its label."""
    if not _test_images():
        pytest.skip("set MODEL_B_TEST_DIR to a directory of test-split images")

    found = real_image_evidence.get(index)
    if found is None:
        pytest.skip(
            f"no image among the first {MAX_IMAGES_SCANNED} scanned produced a "
            f"detection of class {index} ({class_name}) at or above "
            f"{DEPLOYED_THRESHOLDS[expected_label]}"
        )

    findings = found["output"]["findings"]
    assert expected_label in findings, (
        f"{found['path'].name}: the deployed chain detected class index {index} "
        f"({class_name}) above its threshold, but reported {sorted(findings)}"
    )

    # Every name shown must correspond to an index the chain actually captured,
    # which is the permutation check applied to real data rather than synthetic.
    expected_from_indices = {
        EXPECTED_MAPPING[c][1]
        for c, v in found["captured"]
        if v >= DEPLOYED_THRESHOLDS[EXPECTED_MAPPING[c][1]]
    }
    assert set(findings) == expected_from_indices, (
        f"{found['path'].name}: displayed {sorted(findings)} but the indices "
        f"captured before mapping imply {sorted(expected_from_indices)}"
    )
