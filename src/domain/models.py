from dataclasses import dataclass
import numpy as np

@dataclass
class LineSelection:
    start: tuple[float, float]
    end: tuple[float, float]

@dataclass
class AnalysisResult:
    distance: np.ndarray
    rgb: np.ndarray
    hue: np.ndarray
    saturation: np.ndarray
    value: np.ndarray
    reference: dict
    comparison: dict