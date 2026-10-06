import numpy as np
from src.analysis.color import rgb_to_hsv_unwrapped, normalize_rgb
from src.analysis.rainbow import generate_reference_profile

def test_rgb_to_hsv_basic():
    """Test basic RGB to HSV conversion via rgb_to_hsv_unwrapped."""
    # White -> hue unwrapped is 0, saturation 0, value 1
    rgb = np.array([[[1.0, 1.0, 1.0]]])
    rgb01 = normalize_rgb(rgb.reshape(-1, 3))
    hue_unwrapped, saturation, value = rgb_to_hsv_unwrapped(rgb01)
    assert np.isclose(hue_unwrapped[0], 0.0)  # hue near 0
    assert np.isclose(saturation[0], 0.0)     # white has 0 saturation
    assert np.isclose(value[0], 1.0)

    # Red -> hue 0, saturation 1, value 1
    rgb = np.array([[[1.0, 0.0, 0.0]]])
    rgb01 = normalize_rgb(rgb.reshape(-1, 3))
    hue_unwrapped, saturation, value = rgb_to_hsv_unwrapped(rgb01)
    assert np.isclose(hue_unwrapped[0], 0.0)
    assert np.isclose(saturation[0], 1.0)
    assert np.isclose(value[0], 1.0)

def test_generate_reference_profile():
    """Test reference profile generation."""
    # Minimal config matching config.toml structure
    config = {
        "reference": {
            "hue_range": [0.0, 1.0],
            "default_saturation": 1.0,
        }
    }
    num_samples = 100
    reference = generate_reference_profile(num_samples, config)

    assert "hue" in reference
    assert "saturation" in reference
    assert len(reference["hue"]) == num_samples
    assert len(reference["saturation"]) == num_samples
    assert np.isclose(reference["hue"][0], 0.0)
    assert np.isclose(reference["hue"][-1], 1.0)
    assert np.allclose(reference["saturation"], 1.0)
