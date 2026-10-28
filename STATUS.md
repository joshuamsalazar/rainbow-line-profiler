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
- Updated the notebook’s simulated-profile plotting cell to read position from the DataFrame index, leaving only the three RGB columns in the plotted data.

## Log
- Updated default line coordinates in `src/simple_app.py`:
  - `DEFAULT_IMAGE_START` → (741.4, 201.4)
  - `DEFAULT_IMAGE_END` → (464.4, -21.5)
  - Round-trip verified through canvas↔image coordinate scaling matches exactly.
- Fixed replotting issue: `initial_drawing` is now built directly from `DEFAULT_IMAGE_START`/`DEFAULT_IMAGE_END` instead of session-state sliders, so the canvas always starts with the default line. User draws still update `endpoints` and the sliders, but no longer overwrite the initial drawing (Option B behavior).
- Fixed `ModuleNotFoundError: No module named 'src'` for Streamlit Cloud deployment: added `sys.path` insert of repo root before `from src.config import load_config`, and moved `ROOT` definition above the import. `simple_app.py` now runs both via `streamlit run src/simple_app.py` and as an imported module.

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
- Added `sample_screen_app.png` image to `README.md` under "Online testing".
- Added new notebook cell to `notebooks/line_profiler_minimal.ipynb` that plots the simulated rainbow profile using Plotly (following cell 20 structure), placed after the `simulated_rainbow_profile` import cell.
- Updated the simulated-profile plot to use `profile.index.to_numpy()` for position, matching the RGB-only `(n, 3)` profile returned by `simulated_rainbow_profile`.
- Updated the notebook comparison plot with dotted simulated curves, solid measured curves, and sliders for simulated-position shift and intensity scale.
- Kept the Pixi `notebook` task simple by opening the prototype notebook directly in JupyterLab.
- Fixed duplicate plot rendering in the interactive notebook cell by returning the Plotly figure instead of calling `fig.show()` inside `widgets.interact`.
- Removed the duplicate slider cell from the notebook and cleared saved outputs; only one interactive profile plot remains.

## Technical Notes
- Architecture follows original `plan.md` with skeleton alignment
- All core dependencies included for scientific analysis
- Modular structure with clear separation of concerns
- Ready for rapid iteration and testing
