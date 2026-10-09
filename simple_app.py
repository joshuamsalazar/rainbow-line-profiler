from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from src.config import load_config
from streamlit_drawable_canvas import st_canvas


CANVAS_WIDTH = 500
CANVAS_HEIGHT = 400
ROOT = Path(__file__).resolve().parent


def line_endpoints(line_object):
    """Convert Fabric.js line coordinates to absolute canvas coordinates."""
    values = [line_object.get(name) for name in ("x1", "y1", "x2", "y2")]
    if any(value is None for value in values):
        return None

    left = line_object.get("left", 0)
    top = line_object.get("top", 0)
    x1, y1, x2, y2 = values
    return np.array([left + x1, top + y1]), np.array([left + x2, top + y2])


def latest_line(canvas_result):
    objects = (canvas_result.json_data or {}).get("objects", [])
    return line_endpoints(objects[-1]) if objects else None


def image_coordinates(endpoints, image_size):
    scale = np.array(
        [image_size[0] / CANVAS_WIDTH, image_size[1] / CANVAS_HEIGHT]
    )
    return endpoints[0] * scale, endpoints[1] * scale


def rgb_profile(endpoints, image):
    start, end = image_coordinates(endpoints, image.size)
    length = float(np.linalg.norm(end - start))
    count = max(int(np.ceil(length)) + 1, 2)

    points = np.linspace(start, end, count)
    x = np.clip(np.rint(points[:, 0]).astype(int), 0, image.width - 1)
    y = np.clip(np.rint(points[:, 1]).astype(int), 0, image.height - 1)
    rgb = np.asarray(image)[y, x, :3]

    profile = pd.DataFrame(
        {
            "Line length (image px)": np.linspace(0, length, count),
            "Red": rgb[:, 0],
            "Green": rgb[:, 1],
            "Blue": rgb[:, 2],
        }
    ).set_index("Line length (image px)")
    return profile, start, end, length


def simulated_rainbow_profile(num_points=500):
    """Build the normalized RGB profile from the analytical rainbow model."""
    position = np.linspace(0, 1, num_points)
    sky = 1 / (1 + np.exp(-12 * (position - 0.55)))

    base_red = 0.20 + 0.25 * sky
    base_green = 0.40 + 0.20 * sky
    base_blue = 0.70 + 0.15 * sky

    def gaussian(mean, amplitude, standard_deviation):
        return amplitude * np.exp(
            -((position - mean) ** 2) / (2 * standard_deviation**2)
        )

    profile = pd.DataFrame(
        {
            "Perpendicular position": position,
            "Red": base_red + gaussian(0.38, 0.40, 0.06),
            "Green": base_green + gaussian(0.48, 0.30, 0.07),
            "Blue": base_blue + gaussian(0.56, 0.15, 0.08),
        }
    )
    return profile.set_index("Perpendicular position").clip(0, 1)


st.set_page_config(layout="wide")
st.title("Simple Canvas")

config = load_config()
demo_path = ROOT / config.get("demo", {}).get("path", "assets/demo.png")
background = Image.open(demo_path).convert("RGB") if demo_path.exists() else None

canvas_col, plots_col = st.columns(2)

with canvas_col:
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="#000000",
        background_color="#f5f5f5",
        background_image=background,
        height=CANVAS_HEIGHT,
        width=CANVAS_WIDTH,
        drawing_mode="line",
        update_streamlit=True,
        key="canvas",
    )

    endpoints = latest_line(canvas_result)
    if background is not None and endpoints is not None:
        _, image_start, image_end, image_length = rgb_profile(endpoints, background)
        st.caption(f"Line length: {image_length:.1f} image pixels")
        st.caption(
            f"Initial image coordinate: ({image_start[0]:.1f}, {image_start[1]:.1f})"
        )
        st.caption(
            f"Final image coordinate: ({image_end[0]:.1f}, {image_end[1]:.1f})"
        )

with plots_col:
    plot_tab, plot_2_tab, plot_3_tab = st.tabs(
        ["Plot 1: RGB profile", "Plot 2", "Plot 3"]
    )
    with plot_tab:
        st.subheader("Color profile along the line")
        if background is None:
            st.info("Load a background image to analyze the line.")
        elif endpoints is None:
            st.info("Draw a line on the canvas.")
        else:
            profile, _, _, _ = rgb_profile(endpoints, background)
            st.line_chart(
                profile,
                y=["Red", "Green", "Blue"],
                color=["#e63946", "#2a9d8f", "#457b9d"],
                alt="Red, green, and blue pixel values along the drawn line",
            )
    with plot_2_tab:
        st.subheader("Simulated rainbow profile")
        st.caption("Analytical model: sky background plus localized RGB rainbow peaks")
        st.line_chart(
            simulated_rainbow_profile(),
            y=["Red", "Green", "Blue"],
            color=["#e63946", "#2a9d8f", "#457b9d"],
            alt="Simulated normalized red, green, and blue channels across a rainbow",
        )
        st.caption(
            "Position 0 is outside the arc; position 1 is toward the bright inner-sky plateau."
        )

    with plot_3_tab:
        st.info("Plot 3 will be added here.")
