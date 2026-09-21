"""Record the exact evaluation environment (spec Phase 0.1).

Run once per venv with that venv's python. Writes a JSON block to stdout; the
caller tees it into audit/env/. Everything here is descriptive: nothing is
imported that the evaluation itself does not already import.
"""
import json
import platform
import subprocess
import sys


def _safe(fn, default="unavailable"):
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001 - we want the reason in the record
        return f"{default}: {exc}"


def main() -> None:
    info = {
        "python_version": sys.version,
        "python_version_tuple": list(sys.version_info[:3]),
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "macos": _safe(lambda: platform.mac_ver()[0]),
        "cpu_model": _safe(
            lambda: subprocess.check_output(
                ["sysctl", "-n", "machdep.cpu.brand_string"], text=True
            ).strip()
        ),
        "cpu_count": _safe(lambda: int(subprocess.check_output(["sysctl", "-n", "hw.ncpu"], text=True))),
    }

    try:
        import torch

        info["torch"] = torch.__version__
        info["torch_num_threads"] = torch.get_num_threads()
        info["torch_num_interop_threads"] = torch.get_num_interop_threads()
        info["cuda_available"] = torch.cuda.is_available()
        info["mps_available"] = _safe(lambda: torch.backends.mps.is_available())
        info["default_dtype"] = str(torch.get_default_dtype())
    except Exception as exc:  # noqa: BLE001
        info["torch"] = f"unavailable: {exc}"

    for mod in ("torchvision", "ultralytics", "sahi", "numpy", "scipy", "pandas", "sklearn", "PIL", "cv2", "matplotlib"):
        try:
            m = __import__(mod)
            info[mod] = getattr(m, "__version__", "no __version__")
        except Exception as exc:  # noqa: BLE001
            info[mod] = f"unavailable: {exc}"

    print(json.dumps(info, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
