import numpy as np
from src.analysis.color import rgb_to_hsv_unwrapped, normalize_rgb
from src.analysis.rainbow import generate_reference_profile

def test_rgb_to_hsv_basic():
    rgb = np.array([[[1.0, 1.0, 1.0]]])
    rgb01 = normalize_rgb(rgb.reshape(-1, 3))
    hue_unwrapped, saturation, value = rgb_to_hsv_unwrapped(rgb01)
    assert np.isclose(hue_unwrapped[0], 0.0)
    assert np.isclose(saturation[0], 0.0)
    assert np.isclose(value[0], 1.0)

    rgb = np.array([[[1.0, 0.0, 0.0]]])
    rgb01 = normalize_rgb(rgb.reshape(-1, 3))
    hue_unwrapped, saturation, value = rgb_to_hsv_unwrapped(rgb01)
    assert np.isclose(hue_unwrapped[0], 0.0)
    assert np.isclose(saturation[0], 1.0)
    assert np.isclose(value[0], 1.0)

def test_generate_reference_profile():
    config = {"reference": {"hue_range": [0.0, 1.0], "default_saturation": 1.0}}
    reference = generate_reference_profile(100, config)
    assert len(reference["hue"]) == 100
    assert np.isclose(reference["hue"][0], 0.0)
    assert np.isclose(reference["hue"][-1], 1.0)
