from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]

def load_config() -> dict:
    with open(ROOT / "config.toml", "rb") as f:
        config = tomllib.load(f)

    if config["app"]["default_line_width"] <= 0:
        raise ValueError("default_line_width must be > 0")
    if len(config["reference"]["hue_range"]) != 2:
        raise ValueError("reference.hue_range must contain exactly two values")

    return config