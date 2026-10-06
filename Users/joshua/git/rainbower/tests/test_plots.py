import numpy as np
from src.ui.plots import build_color_strip, build_rgb_plot, build_hsv_plot
from src.domain.models import AnalysisResult

def test_plot_creation():
    """Test that plot functions create plotly figures without crashing."""
    positions = np.linspace(0, 1, 50)
    rgb01 = np.random.rand(50, 3)
    hue = np.linspace(0, 1, 50)
    saturation = np.ones(50) * 0.8
    reference = {"hue": np.linspace(0, 1, 50), "saturation": np.ones(50)}
    config = {
        "plots": {"rgb_colors": ["red", "green", "blue"], "hue_color": "purple", "sat_color": "orange"}
    }

    # build_color_strip takes rgb01 array
    fig_strip = build_color_strip(rgb01)
    assert fig_strip is not None

    # build_rgb_plot takes distance and rgb
    fig_rgb = build_rgb_plot(positions, rgb01, config)
    assert fig_rgb is not None

    # build_hsv_plot takes distance, hue, saturation, reference, config
    fig_hsv = build_hsv_plot(positions, hue, saturation, reference, config)
    assert fig_hsv is not None
