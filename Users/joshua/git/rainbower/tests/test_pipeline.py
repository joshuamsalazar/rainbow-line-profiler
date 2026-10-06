import numpy as np
from PIL import Image
from src.domain.models import LineSelection
from src.pipeline import analyze_image

def test_pipeline_synthetic():
    """Test analyze_image with a synthetic rainbow image."""
    # Create a simple synthetic horizontal gradient image
    width, height = 100, 50
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    for x in range(width):
        img_array[:, x] = [int(255 * (x/width)), int(255 * (1 - x/width)), 128]

    image = Image.fromarray(img_array)
    image.save("tests/synthetic_rainbow.png")

    # Minimal config matching pipeline needs
    config = {
        "app": {"default_line_width": 2},
        "reference": {"hue_range": [0.0, 1.0], "default_saturation": 1.0},
        "plots": {"rgb_colors": ["red", "green", "blue"], "hue_color": "purple", "sat_color": "orange"},
    }

    line = LineSelection(start=(10, 25), end=(90, 25))
    result = analyze_image(image, line, config)
    assert result.rgb.shape[0] > 0
    assert result.comparison["overall_score"] >= 0.0
    assert result.comparison["overall_score"] <= 1.0
