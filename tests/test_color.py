import numpy as np
from src.analysis.color import rgb_to_hsv, generate_reference_rainbow

def test_rgb_to_hsv_basic():
    """Test basic RGB to HSV conversion."""
    # White
    rgb = np.array([[1.0, 1.0, 1.0]])
    hsv = rgb_to_hsv(rgb)
    assert np.allclose(hsv[0], [0.0, 0.0, 1.0])
    
    # Red
    rgb = np.array([[1.0, 0.0, 0.0]])
    hsv = rgb_to_hsv(rgb)
    assert np.isclose(hsv[0, 0], 0.0)  # Hue
    assert np.isclose(hsv[0, 1], 1.0)  # Saturation
    assert np.isclose(hsv[0, 2], 1.0)  # Value

def test_generate_reference_rainbow():
    """Test reference rainbow generation."""
    num_samples = 100
    positions, rgb, hsv = generate_reference_rainbow(num_samples)
    
    assert len(positions) == num_samples
    assert rgb.shape == (num_samples, 3)
    assert hsv.shape == (num_samples, 3)
    
    # Check hue goes from 0 to 1
    assert np.isclose(hsv[0, 0], 0.0)
    assert np.isclose(hsv[-1, 0], 1.0)
    
    # Check saturation and value are 1
    assert np.allclose(hsv[:, 1], 1.0)
    assert np.allclose(hsv[:, 2], 1.0)