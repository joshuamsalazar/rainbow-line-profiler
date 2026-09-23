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