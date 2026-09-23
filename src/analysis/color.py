import numpy as np
from skimage.color import rgb2hsv

def normalize_rgb(sampled_rgb):
    return np.clip(sampled_rgb / 255.0, 0.0, 1.0)

def rgb_to_hsv_unwrapped(rgb01):
    hsv = rgb2hsv(rgb01.reshape(-1, 1, 3)).reshape(-1, 3)
    hue, saturation, value = hsv.T
    hue_unwrapped = np.unwrap(hue * 2 * np.pi) / (2 * np.pi)
    return hue_unwrapped, saturation, value