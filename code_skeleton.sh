#!/usr/bin/env bash
set -euo pipefail

PROJECT_NAME="${1:-rainbow-line-profiler}"
ROOT="${PWD}/${PROJECT_NAME}"

mkdir -p \
  "$ROOT/.github/workflows" \
  "$ROOT/.streamlit" \
  "$ROOT/assets/demo" \
  "$ROOT/src/domain" \
  "$ROOT/src/analysis" \
  "$ROOT/src/ui" \
  "$ROOT/tests"

cat > "$ROOT/.gitignore" <<'GITIGNORE'
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
.pixi/
.DS_Store
streamlit.log
GITIGNORE

cat > "$ROOT/pixi.toml" <<'PIXI'
[project]
name = "rainbow-line-profiler"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-arm64", "osx-64", "win-64"]

[dependencies]
python = "3.12.*"
pip = "*"
streamlit = "*"
numpy = "*"
pillow = "*"
plotly = "*"
scikit-image = "*"
requests = "*"
pytest = "*"
ruff = "*"

[pypi-dependencies]
streamlit-drawable-canvas = "*"

[tasks]
run-app = "streamlit run app.py"
test = "pytest"
lint = "ruff check ."
format = "ruff format ."
smoke = "python -m src.pipeline"
PIXI

cat > "$ROOT/pyproject.toml" <<'PYPROJECT'
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "rainbow-line-profiler"
version = "0.1.0"
description = "Scientific single-line rainbow profiler"
requires-python = ">=3.12,<3.13"

[tool.setuptools]
package-dir = {"" = "."}

[tool.setuptools.packages.find]
where = ["src"]
PYPROJECT

cat > "$ROOT/config.toml" <<'CONFIG'
[app]
title = "Rainbow Line Profiler"
default_line_width = 5
use_local_demo = true

[demo]
path = "assets/demo/rainbow_wikimedia.jpg"
label = "Local rainbow demo image"

[reference]
enabled = true
hue_range = [0.0, 0.75]
default_saturation = 0.6

[plots]
rgb_colors = ["red", "green", "blue"]
hue_color = "black"
sat_color = "magenta"
CONFIG

cat > "$ROOT/README.md" <<'README'
# Rainbow Line Profiler

Small scientific Streamlit app to inspect whether a line across an image is consistent with a rainbow-like color signal.

## Architecture

- `app.py` is the Streamlit entrypoint.
- `src/pipeline.py` contains the main end-to-end analysis flow.
- Keep business logic out of `app.py`.
- Keep signal logic in `src/analysis/`.
- Keep rendering helpers in `src/ui/`.

## Environment

Pixi is the source of truth for environment management and tasks.

## Main commands

```bash
pixi run run-app
pixi run test
pixi run lint
```
README

cat > "$ROOT/app.py" <<'APP'
import streamlit as st
from src.config import load_config
from src.pipeline import run_app_pipeline


def main():
    config = load_config()
    st.set_page_config(page_title=config["app"]["title"], layout="wide")
    st.title(config["app"]["title"])
    st.caption("Scientific single-line image profiler for rainbow analysis.")
    run_app_pipeline(config)


if __name__ == "__main__":
    main()
APP

cat > "$ROOT/src/config.py" <<'CFG'
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def load_config() -> dict:
    with open(ROOT / "config.toml", "rb") as f:
        config = tomllib.load(f)

    if config["app"]["default_line_width"] <= 0:
        raise ValueError("default_line_width must be > 0")
    if len(config["reference"]["hue_range"]) != 2:
        raise ValueError("reference.hue_range must contain exactly two values")

    return config
CFG

cat > "$ROOT/src/pipeline.py" <<'PIPE'
from pathlib import Path
import numpy as np
import streamlit as st
from PIL import Image

from src.analysis.sampling import sample_line_rgb, compute_distances
from src.analysis.color import normalize_rgb, rgb_to_hsv_unwrapped
from src.analysis.rainbow import generate_reference_profile, compare_profiles
from src.domain.models import AnalysisResult, LineSelection
from src.ui.canvas import get_image_and_line_selection
from src.ui.plots import build_color_strip, build_hsv_plot, build_rgb_plot


def analyze_image(image, line, config):
    rgb = np.asarray(image)
    src = (line.start[1], line.start[0])
    dst = (line.end[1], line.end[0])

    sampled_rgb = sample_line_rgb(rgb, src=src, dst=dst, linewidth=config["app"]["default_line_width"])
    distance = compute_distances(src, dst, len(sampled_rgb))
    rgb01 = normalize_rgb(sampled_rgb)
    hue_unwrapped, saturation, value = rgb_to_hsv_unwrapped(rgb01)
    reference = generate_reference_profile(len(sampled_rgb), config)
    comparison = compare_profiles(
        measured={"hue": hue_unwrapped, "saturation": saturation},
        reference=reference,
    )

    return AnalysisResult(
        distance=distance,
        rgb=rgb01,
        hue=hue_unwrapped,
        saturation=saturation,
        value=value,
        reference=reference,
        comparison=comparison,
    )


def run_app_pipeline(config):
    image, line = get_image_and_line_selection(config)
    if image is None:
        st.info("Upload an image or use the local demo image.")
        return
    if line is None:
        st.warning("Draw a single line across the suspected rainbow region.")
        return

    result = analyze_image(image, line, config)

    st.subheader("Profile strip")
    st.plotly_chart(build_color_strip(result.rgb), use_container_width=True)

    st.subheader("Measured signals")
    st.plotly_chart(build_rgb_plot(result.distance, result.rgb, config), use_container_width=True)
    st.plotly_chart(
        build_hsv_plot(result.distance, result.hue, result.saturation, result.reference, config),
        use_container_width=True,
    )

    st.subheader("Interpretation")
    st.metric("Rainbow consistency score", f"{result.comparison['overall_score']:.2f}")
    st.write(result.comparison["label"])


if __name__ == "__main__":
    demo_path = Path("assets/demo/rainbow_wikimedia.jpg")
    if demo_path.exists():
        print("Pipeline module ready.")
    else:
        print("Pipeline module ready, demo image missing.")
PIPE

cat > "$ROOT/src/domain/models.py" <<'MODELS'
from dataclasses import dataclass
import numpy as np


@dataclass
class LineSelection:
    start: tuple[float, float]
    end: tuple[float, float]


@dataclass
class AnalysisResult:
    distance: np.ndarray
    rgb: np.ndarray
    hue: np.ndarray
    saturation: np.ndarray
    value: np.ndarray
    reference: dict
    comparison: dict
MODELS

cat > "$ROOT/src/analysis/sampling.py" <<'SAMP'
import numpy as np
from skimage.measure import profile_line


def sample_line_rgb(rgb, src, dst, linewidth=5):
    channels = [
        profile_line(rgb[:, :, i], src, dst, linewidth=linewidth, order=1, mode="reflect")
        for i in range(3)
    ]
    return np.stack(channels, axis=1)


def compute_distances(src, dst, sample_count):
    total = np.hypot(dst[1] - src[1], dst[0] - src[0])
    return np.linspace(0, total, sample_count)
SAMP

cat > "$ROOT/src/analysis/color.py" <<'COLOR'
import numpy as np
from skimage.color import rgb2hsv


def normalize_rgb(sampled_rgb):
    return np.clip(sampled_rgb / 255.0, 0.0, 1.0)


def rgb_to_hsv_unwrapped(rgb01):
    hsv = rgb2hsv(rgb01.reshape(-1, 1, 3)).reshape(-1, 3)
    hue, saturation, value = hsv.T
    hue_unwrapped = np.unwrap(hue * 2 * np.pi) / (2 * np.pi)
    return hue_unwrapped, saturation, value
COLOR

cat > "$ROOT/src/analysis/rainbow.py" <<'RAIN'
import numpy as np


def generate_reference_profile(length, config):
    start, end = config["reference"]["hue_range"]
    hue = np.linspace(start, end, length)
    saturation = np.full(length, config["reference"]["default_saturation"])
    return {"hue": hue, "saturation": saturation}


def compare_profiles(measured, reference):
    measured_hue = measured["hue"]
    measured_sat = measured["saturation"]

    hue_corr = np.corrcoef(measured_hue, reference["hue"])[0, 1] if len(measured_hue) > 1 else 0.0
    sat_diff = float(np.mean(np.abs(measured_sat - reference["saturation"])))
    monotonicity = float(np.mean(np.diff(measured_hue) >= 0)) if len(measured_hue) > 1 else 0.0
    overall = max(0.0, min(1.0, (max(hue_corr, 0.0) * 0.5) + ((1.0 - sat_diff) * 0.3) + (monotonicity * 0.2)))

    if overall > 0.75:
        label = "Profile is reasonably consistent with an idealized rainbow signal."
    elif overall > 0.45:
        label = "Profile shows some rainbow-like structure, but evidence is inconclusive."
    else:
        label = "Profile does not strongly match the current idealized rainbow reference."

    return {
        "hue_correlation": float(hue_corr),
        "saturation_difference": sat_diff,
        "monotonicity": monotonicity,
        "overall_score": overall,
        "label": label,
    }
RAIN

cat > "$ROOT/src/ui/canvas.py" <<'CANVAS'
from pathlib import Path
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

from src.domain.models import LineSelection


def _load_local_demo(config):
    demo_path = Path(config["demo"]["path"])
    if demo_path.exists():
        return Image.open(demo_path).convert("RGB")
    return None


def _extract_latest_line(canvas_result):
    if not canvas_result or not canvas_result.json_data:
        return None
    objects = canvas_result.json_data.get("objects", [])
    lines = [obj for obj in objects if obj.get("type") == "line"]
    if not lines:
        return None
    line = lines[-1]
    return LineSelection(start=(line["x1"], line["y1"]), end=(line["x2"], line["y2"]))


def get_image_and_line_selection(config):
    use_demo = st.checkbox("Use local demo image", value=config["app"].get("use_local_demo", True))
    uploaded = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    image = None
    if use_demo:
        image = _load_local_demo(config)
    elif uploaded is not None:
        image = Image.open(uploaded).convert("RGB")

    if image is None:
        return None, None

    width, height = image.size
    canvas_result = st_canvas(
        background_image=image,
        stroke_width=config["app"]["default_line_width"],
        stroke_color="#ff0000",
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="line",
        key="line-canvas",
    )

    line = _extract_latest_line(canvas_result)
    return image, line
CANVAS

cat > "$ROOT/src/ui/plots.py" <<'PLOTS'
import numpy as np
import plotly.graph_objects as go


def build_color_strip(rgb01):
    strip = np.repeat(rgb01[np.newaxis, :, :], 24, axis
