"""
verify_classes.py — run from the repo root.

Checks that the condition each class index actually means, according to the
trained weights, is the condition the deployment layer shows the user.

The deployment layer no longer keeps its own index -> condition table: it reads
the registry off the weights and passes each name through a display-label map
keyed by that same name. This script imports that real map rather than holding a
copy of it, so the two cannot drift apart.

    python verify_classes.py

Set MODEL_B_WEIGHTS to check a checkpoint stored outside the repo.
"""

import importlib.util
import os
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent
INFERENCE_MODULE = REPO_ROOT / "ml_models" / "model_b" / "inference_model.py"
WEIGHTS = pathlib.Path(
    os.environ.get("MODEL_B_WEIGHTS", REPO_ROOT / "ml_models/model_b/models/best.pt")
)

# Places where the display label deliberately differs from the name baked into
# the weights. Anything not listed here must match, or it is drift.
DECLARED_SPELLING_FIXES = {
    # The training dataset ships this class misspelled. Users see it corrected.
    "tooth_discolation": "Tooth Discoloration",
}


def _canonical(text):
    """Reduce a name to a form that ignores case, separators and plurals."""
    return text.strip().lower().replace("_", " ").rstrip("s")


def _load_deployment_layer():
    """Import inference_model.py by path (it is not an importable package)."""
    spec = importlib.util.spec_from_file_location(
        "model_b_inference_verify", INFERENCE_MODULE
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if not WEIGHTS.exists():
    sys.exit(f"Weights not found at {WEIGHTS}")

if WEIGHTS.read_bytes()[:40].startswith(b"version https://git-lfs"):
    sys.exit(
        f"{WEIGHTS} is a Git LFS pointer, not the weights themselves.\n"
        "Run 'git lfs install && git lfs pull' first."
    )

from ultralytics import YOLO  # noqa: E402  (imported after the cheap path checks)

deployment = _load_deployment_layer()
DISPLAY_NAMES = deployment.DISPLAY_NAMES

TRUE = YOLO(str(WEIGHTS)).names
# Exactly what OralHygieneModel.__init__ builds, from the same code path.
DEPLOYED = {index: deployment.display_name(name) for index, name in TRUE.items()}

print("\nMODEL'S OWN CLASS REGISTRY")
for i in sorted(TRUE):
    print(f"  {i}: {TRUE[i]}")

print("\nDISPLAY LABEL THE DEPLOYMENT LAYER DERIVES")
for i in sorted(DEPLOYED):
    print(f"  {i}: {DEPLOYED[i]}")

print("\nWHAT THE USER ACTUALLY SEES")
print(f"  {'detected':<24} {'displayed':<24} ok?")
print("  " + "-" * 62)

wrong = 0
for i in sorted(TRUE):
    actual = TRUE[i]
    shown = DEPLOYED[i]

    if actual in DECLARED_SPELLING_FIXES:
        ok = shown == DECLARED_SPELLING_FIXES[actual]
        verdict = "OK (declared spelling fix)" if ok else "<-- WRONG"
    else:
        ok = _canonical(actual) == _canonical(shown)
        verdict = "OK" if ok else "<-- WRONG"

    if not ok:
        wrong += 1
    print(f"  {actual:<24} {shown:<24} {verdict}")

print(f"\n  {wrong} of {len(TRUE)} classes are reported under the wrong name.")

# A label map that has drifted out of step with the weights is the failure this
# script exists to catch, so an incomplete or stale map is also a failure.
missing = sorted(set(TRUE.values()) - set(DISPLAY_NAMES))
unused = sorted(set(DISPLAY_NAMES) - set(TRUE.values()))
if missing:
    print(f"  Model classes with no display label: {missing}")
if unused:
    print(f"  Display labels for classes the model does not have: {unused}")

if wrong or missing or unused:
    print("\nThe display map in ml_models/model_b/inference_model.py no longer")
    print("matches the weights. Update DISPLAY_NAMES, and record any intentional")
    print("spelling change in DECLARED_SPELLING_FIXES above.")
    sys.exit(1)

print("\nMapping is correct: every class index resolves to the condition the")
print("weights say it is, and the display map covers the registry exactly.")
