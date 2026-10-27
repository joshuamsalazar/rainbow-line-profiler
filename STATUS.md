# Project Status: Rainbow Line Profiler

## Overview
Initial setup completed with skeleton alignment. Ready for rainbow demo image and testing.

## Completed Tasks
- ✅ Initialized Git repository (`git init`)
- ✅ Created directory structure (`src/`, `tests/`, `assets/demo/`, `.github/workflows/`)
- ✅ Set up Pixi with skeleton dependencies (scikit-image, plotly, streamlit-drawable-canvas)
- ✅ Simplified config.toml to match skeleton structure
- ✅ Updated `src/domain/models.py` to skeleton specifications (LineSelection, AnalysisResult)
- ✅ Refactored `src/analysis/sampling.py` to use scikit-image `profile_line`
- ✅ Refactored `src/analysis/color.py` to use scikit-image `rgb2hsv`
- ✅ Implemented correlation-based scoring in `src/analysis/rainbow.py`
- ✅ Updated `src/ui/canvas.py` to use streamlit-drawable-canvas
- ✅ Updated `src/ui/plots.py` to use Plotly
- ✅ Updated `src/pipeline.py` and `app.py` to wire new components
- ✅ Created CI workflow (`.github/workflows/ci.yml`)
- ✅ Updated README.md with architecture and future improvement notes
- ✅ Created package init files (`src/__init__.py`, `src/analysis/__init__.py`, `src/ui/__init__.py`)
- ✅ Commited all changes to git
- ✅ Resolved Pixi dependency pendings:
    - `pyproject.toml` `[project.dependencies]` is the single source of truth for runtime deps
    - `pixi.toml` mirrors `pyproject.toml` runtime deps (added `pandas`, dropped `requests`); dev tools (`pytest`, `ruff`, `jupyter`) stay in pixi only
    - `streamlit-drawable-canvas` kept as a pypi dep in `pixi.toml`
    - `requirements.txt` regenerated to match `pyproject.toml` (Streamlit Cloud artifact)
    - Added `pixi run add-dep <pkg>` task (`pixi add --pypi $1` + regenerate `requirements.txt`)
    - Fixed packaging: `[tool.setuptools.packages.find] include = ["src*"]` so `pyproject.toml` no longer declares a missing `rainbower` package
    - Removed redundant `[project.optional-dependencies] dev` block from `pyproject.toml`

## In Progress
- No tasks currently in progress

## Next Steps
- [ ] Add rainbow demo image to `assets/demo/`
- [x] Test the pipeline with demo image
  Evidence: Created minimal notebook prototype `notebooks/line_profiler_minimal.ipynb` for interactive manual testing with the demo image.
- [ ] Run CI to verify environment setup
- [ ] Fine-tune scoring and visualization if needed

## Log
- Notebook prototype created at `notebooks/line_profiler_minimal.ipynb`, reusing existing analysis modules and demo image.
- Fixed notebook `src` imports: removed fragile `sys.path` hack; `from src...` imports now resolve via editable install (`pip install -e .`, already configured via `[tool.setuptools.packages.find] include = ["src*"]`). Verified imports + demo image load.
- `simple_app.py` exposes `simulated_rainbow_profile(num_points=500)` and `rgb_profile(endpoints, image)`; importable in Jupyter as `from simple_app import simulated_rainbow_profile`.

## Technical Notes
- Architecture follows original `plan.md` with skeleton alignment
- All core dependencies included for scientific analysis
- Modular structure with clear separation of concerns
- Ready for rapid iteration and testing
