# Environment notes (spec Phase 0.1)

Both venvs: Python 3.12.13, macOS 26.6.2 (arm64), Apple M5, 10 CPUs,
torch 2.7.1, torchvision 0.22.1, sahi 0.11.15, numpy 2.5.3, scipy 1.18.1,
pandas 3.0.6, scikit-learn 1.9.1, pillow 12.3.0, matplotlib 3.11.2.
CUDA unavailable; MPS available but unused — all headline figures are CPU.
Default dtype torch.float32.

- `audit/env/lock-ul8.3.231.txt`, `audit/env/env-ul8.3.231.json`
- `audit/env/lock-ul8.4.118.txt`, `audit/env/env-ul8.4.118.json`

The pinned torch installed cleanly, so no substitution was needed.

The two locks differ in exactly three lines: `ultralytics` itself,
`nvidia-ml-py==13.610.43` (a new transitive dependency of 8.4.118 — inert on a
Mac, there is no NVIDIA driver to query), and `pip`, which is present only in
the 8.3.231 venv because it was added there to capture the freeze. Nothing else
differs, which is what the Phase 2.9 version comparison requires.

## Three hazards found while building these, each of which can move a number

### 1. Importing ultralytics before torch changes the CPU thread count 4x

`ultralytics/__init__.py` lines 10-11:

    if not os.environ.get("OMP_NUM_THREADS"):
        os.environ["OMP_NUM_THREADS"] = "1"  # default for reduced CPU utilization during training

This runs at import time. torch reads `OMP_NUM_THREADS` when *it* is first
imported, so the result depends entirely on import order:

    import torch                      -> torch.get_num_threads() == 4
    import ultralytics; import torch  -> torch.get_num_threads() == 1
    import torch; import ultralytics  -> torch.get_num_threads() == 4

All three were measured in this venv. There is a third value in play:
`utils/torch_utils.py:223` calls `torch.set_num_threads(NUM_THREADS)` where
`NUM_THREADS = min(8, max(1, os.cpu_count() - 1))`, which is 8 on this machine.

Why it matters here, beyond a 4x difference in wall-clock: threaded reductions
sum in a nondeterministic order, so changing the thread count perturbs
floating-point results in the last few digits. The Phase 1.2 exactness gate
compares the cached evaluator against a real `val(batch=1)` run **to within
1e-9**. If the two run under different thread counts, that gate can fail for a
reason that has nothing to do with the evaluator being wrong — and, worse, it
could pass on one machine and fail on another.

**Mitigation, applied:** `OMP_NUM_THREADS` is set explicitly before any import,
so the value is fixed by the caller rather than by import order. It is recorded
with every result.

### 2. The two venvs share one global ultralytics settings file

Both write to `~/Library/Application Support/Ultralytics/settings.json`.
Observed in this session: 8.3.231 reset it to defaults, then 8.4.118 "updated
settings to the latest schema", which would then be what 8.3.231 next reads.
For a comparison whose entire point is to isolate the library version, letting
the two versions share mutable state is wrong.

**Mitigation, applied:** each venv gets its own `YOLO_CONFIG_DIR`.

### 3. Two OpenCV distributions are installed at once

    opencv-python==4.7.0.72
    opencv-python-headless==5.0.0.93

Both ship the same `cv2` package, so one silently overwrites the other. The
active one is headless 5.0.0 (verified: `cv2.__version__` is `5.0.0`). The
non-headless 4.7.0.72 arrives as a transitive dependency. The resolved version
is therefore an artifact of installation order and is not pinned by anything.
It is recorded here so the figure can be reproduced, and flagged because a
future rebuild could silently resolve the other way.
