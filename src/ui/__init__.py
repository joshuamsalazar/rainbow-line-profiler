# UI module imports
from .plots import build_color_strip, build_hsv_plot, build_rgb_plot


def get_image_and_line_selection(*args, **kwargs):
    from .canvas import get_image_and_line_selection as _get_image_and_line_selection

    return _get_image_and_line_selection(*args, **kwargs)


__all__ = [
    "build_color_strip",
    "build_hsv_plot",
    "build_rgb_plot",
    "get_image_and_line_selection",
]