# Project package imports
from .analysis import (
    compare_profiles,
    compute_distances,
    generate_reference_profile,
    normalize_rgb,
    rgb_to_hsv_unwrapped,
    sample_line_rgb,
)
from .config import load_config
from .domain.models import AnalysisResult, LineSelection


def analyze_image(*args, **kwargs):
    from .pipeline import analyze_image as _analyze_image

    return _analyze_image(*args, **kwargs)


def run_app_pipeline(*args, **kwargs):
    from .pipeline import run_app_pipeline as _run_app_pipeline

    return _run_app_pipeline(*args, **kwargs)


def build_color_strip(*args, **kwargs):
    from .ui import build_color_strip as _build_color_strip

    return _build_color_strip(*args, **kwargs)


def build_hsv_plot(*args, **kwargs):
    from .ui import build_hsv_plot as _build_hsv_plot

    return _build_hsv_plot(*args, **kwargs)


def build_rgb_plot(*args, **kwargs):
    from .ui import build_rgb_plot as _build_rgb_plot

    return _build_rgb_plot(*args, **kwargs)


def get_image_and_line_selection(*args, **kwargs):
    from .ui import get_image_and_line_selection as _get_image_and_line_selection

    return _get_image_and_line_selection(*args, **kwargs)


__all__ = [
    "AnalysisResult",
    "LineSelection",
    "analyze_image",
    "build_color_strip",
    "build_hsv_plot",
    "build_rgb_plot",
    "compare_profiles",
    "compute_distances",
    "generate_reference_profile",
    "get_image_and_line_selection",
    "load_config",
    "normalize_rgb",
    "rgb_to_hsv_unwrapped",
    "run_app_pipeline",
    "sample_line_rgb",
]