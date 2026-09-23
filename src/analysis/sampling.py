import numpy as np
from skimage.measure import profile_line

def sample_line_rgb(rgb, src, dst, linewidth=5):
    channels = [
        profile_line(rgb[:, :, i], src, dst, linewidth=linewidth, order=1, mode="reflect")
        for i in range(3)
    ]
    return np.stack(channels, axis=1)

def compute_distances(src, dst, sample_count):
    total = np.hypot(dst[1] - src[1], dst[0] - src[0])
    return np.linspace(0, total, sample_count)