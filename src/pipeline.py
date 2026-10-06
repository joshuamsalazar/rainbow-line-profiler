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
    # Initialize session state
    if 'canvas_key' not in st.session_state:
        st.session_state.canvas_key = 0
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None

    st.write("DEBUG: running pipeline module")
    # Get image and line
    image, line = get_image_and_line_selection(config)

    # Display stored analysis result if available
    if st.session_state.analysis_result is not None:
        result = st.session_state.analysis_result
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

    # Buttons for Start and Reset
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Analysis"):
            if image is None:
                st.info("Upload an image or use the local demo image.")
            elif line is None:
                st.warning("Draw a single line across the suspected rainbow region.")
            else:
                st.write("DEBUG: running analysis, line=", line)
                result = analyze_image(image, line, config)
                st.session_state.analysis_result = result
                st.rerun()
    with col2:
        if st.button("Reset"):
            st.session_state.canvas_key += 1
            st.session_state.analysis_result = None
            st.rerun()

    # If there's no analysis result yet, show prompts
    if st.session_state.analysis_result is None:
        if image is None:
            st.info("Upload an image or use the local demo image.")
        if line is None:
            st.warning("Draw a single line across the suspected rainbow region.")

if __name__ == "__main__":
    demo_path = Path("assets/demo/Ring-billed_gull_and_a_rainbow_(52910).jpg")
    if demo_path.exists():
        print("Pipeline module ready.")
    else:
        print("Pipeline module ready, demo image missing.")
