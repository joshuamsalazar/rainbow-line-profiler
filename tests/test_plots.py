import numpy as np
from src.ui.plots import build_color_strip, build_rgb_plot, build_hsv_plot

def test_plot_creation():
    rgb01 = np.random.rand(50, 3)
    positions = np.linspace(0, 1, 50)
    hue = np.linspace(0, 1, 50)
    saturation = np.ones(50) * 0.8
    reference = {"hue": np.linspace(0, 1, 50), "saturation": np.ones(50)}
    config = {"plots": {"rgb_colors": ["red","green","blue"], "hue_color":"purple", "sat_color":"orange"}}
    assert build_color_strip(rgb01) is not None
    assert build_rgb_plot(positions, rgb01, config) is not None
    assert build_hsv_plot(positions, hue, saturation, reference, config) is not None
