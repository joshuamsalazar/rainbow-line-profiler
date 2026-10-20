from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

from src.config import load_config

CANVAS_WIDTH = 500
CANVAS_HEIGHT = 400
DEFAULT_IMAGE_START = np.array([888.1, 340.2])
DEFAULT_IMAGE_END = np.array([611.1, 117.3])
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


def canvas_coordinates_from_image(image_start, image_end, image_size):
    scale = np.array([CANVAS_WIDTH / image_size[0], CANVAS_HEIGHT / image_size[1]])
    return image_start * scale, image_end * scale


def image_coordinates(endpoints, image_size):
    scale = np.array([image_size[0] / CANVAS_WIDTH, image_size[1] / CANVAS_HEIGHT])
    return endpoints[0] * scale, endpoints[1] * scale


def canvas_line_object(start, end):
    return {
        "type": "line",
        "version": "4.4.0",
        "originX": "left",
        "originY": "top",
        "left": float(start[0]),
        "top": float(start[1]),
        "x1": 0.0,
        "y1": 0.0,
        "x2": float(end[0] - start[0]),
        "y2": float(end[1] - start[1]),
        "stroke": "#000000",
        "strokeWidth": 3,
        "fill": "rgba(0,0,0,0)",
        "selectable": True,
        "evented": True,
    }


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
        return amplitude * np.exp(-((position - mean) ** 2) / (2 * standard_deviation**2))

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
st.title("Color Profiler")
st.caption(
    "Draw a path over the image, and see the generated vs. computed color profiles for rainbows. WIP: mobile support via sliders."
)

config = load_config()
demo_path = ROOT / config.get("demo", {}).get("path", "assets/demo.png")
background = Image.open(demo_path).convert("RGB") if demo_path.exists() else None

if background is not None:
    slider_start = st.session_state.get("slider_image_start", DEFAULT_IMAGE_START.copy())
    slider_end = st.session_state.get("slider_image_end", DEFAULT_IMAGE_END.copy())

    x1 = st.session_state.get("x1", float(slider_start[0]))
    y1 = st.session_state.get("y1", float(slider_start[1]))
    x2 = st.session_state.get("x2", float(slider_end[0]))
    y2 = st.session_state.get("y2", float(slider_end[1]))

    slider_image_start = np.array([x1, y1], dtype=float)
    slider_image_end = np.array([x2, y2], dtype=float)
    st.session_state["slider_image_start"] = slider_image_start
    st.session_state["slider_image_end"] = slider_image_end

    default_canvas_start, default_canvas_end = canvas_coordinates_from_image(
        slider_image_start, slider_image_end, background.size
    )
    initial_drawing = {
        "version": "4.4.0",
        "objects": [canvas_line_object(default_canvas_start, default_canvas_end)],
    }
else:
    slider_image_start = DEFAULT_IMAGE_START.copy()
    slider_image_end = DEFAULT_IMAGE_END.copy()
    initial_drawing = None

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
        initial_drawing=initial_drawing,
        update_streamlit=True,
        key="canvas",
    )

    endpoints = latest_line(canvas_result)
    if endpoints is None and background is not None:
        endpoints = default_canvas_start, default_canvas_end
    if background is not None and endpoints is not None:
        _, image_start, image_end, image_length = rgb_profile(endpoints, background)
        st.session_state["slider_image_start"] = image_start
        st.session_state["slider_image_end"] = image_end
        st.caption(f"Line length: {image_length:.1f} image pixels")
        st.caption(f"Initial image coordinate: ({image_start[0]:.1f}, {image_start[1]:.1f})")
        st.caption(f"Final image coordinate: ({image_end[0]:.1f}, {image_end[1]:.1f})")

with plots_col:
    plot_tab, plot_2_tab, plot_3_tab = st.tabs(["Plot 1: RGB profile", "Plot 2", "Plot 3"])
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
        st.info("Plot 3 will be added here. Someday :D")

    if background is not None:
        st.markdown("### Line coordinates")
        slider_col_1, slider_col_2 = st.columns(2)
        with slider_col_1:
            st.slider(
                "x1",
                min_value=0.0,
                max_value=float(background.width),
                value=float(st.session_state["slider_image_start"][0]),
                step=0.1,
                key="x1",
            )
            st.slider(
                "y1",
                min_value=0.0,
                max_value=float(background.height),
                value=float(st.session_state["slider_image_start"][1]),
                step=0.1,
                key="y1",
            )
        with slider_col_2:
            st.slider(
                "x2",
                min_value=0.0,
                max_value=float(background.width),
                value=float(st.session_state["slider_image_end"][0]),
                step=0.1,
                key="x2",
            )
            st.slider(
                "y2",
                min_value=0.0,
                max_value=float(background.height),
                value=float(st.session_state["slider_image_end"][1]),
                step=0.1,
                key="y2",
            )
