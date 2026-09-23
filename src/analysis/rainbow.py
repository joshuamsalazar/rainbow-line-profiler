import numpy as np

def generate_reference_profile(length, config):
    start, end = config["reference"]["hue_range"]
    hue = np.linspace(start, end, length)
    saturation = np.full(length, config["reference"]["default_saturation"])
    return {"hue": hue, "saturation": saturation}

def compare_profiles(measured, reference):
    measured_hue = measured["hue"]
    measured_sat = measured["saturation"]

    hue_corr = np.corrcoef(measured_hue, reference["hue"])[0, 1] if len(measured_hue) > 1 else 0.0
    sat_diff = float(np.mean(np.abs(measured_sat - reference["saturation"])))
    monotonicity = float(np.mean(np.diff(measured_hue) >= 0)) if len(measured_hue) > 1 else 0.0
    overall = max(0.0, min(1.0, (max(hue_corr, 0.0) * 0.5) + ((1.0 - sat_diff) * 0.3) + (monotonicity * 0.2)))

    if overall > 0.75:
        label = "Profile is reasonably consistent with an idealized rainbow signal."
    elif overall > 0.45:
        label = "Profile shows some rainbow-like structure, but evidence is inconclusive."
    else:
        label = "Profile does not strongly match the current idealized rainbow reference."

    return {
        "hue_correlation": float(hue_corr),
        "saturation_difference": sat_diff,
        "monotonicity": monotonicity,
        "overall_score": overall,
        "label": label,
    }