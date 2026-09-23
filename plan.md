# Rainbow Line Profiler Plan

## Goal
- Build a small scientific Streamlit app.
- User uploads an image or uses a local demo image.
- User draws one straight line.
- App samples pixels on that line.
- App plots RGB and HSV signals.
- App compares them with an idealized rainbow reference.

## Main decisions
- Streamlit app.
- Pixi is the source of truth for environment and tasks.
- Single-line only.
- Local demo image stored in repo.
- Scientific tone, not playful.
- ML is future work only.

## Folder shape
```text
app.py
pixi.toml
pixi.lock
pyproject.toml
config.toml
README.md
assets/demo/
src/
  config.py
  pipeline.py
  domain/models.py
  analysis/
    sampling.py
    color.py
    rainbow.py
  ui/
    canvas.py
    plots.py
tests/
  test_color.py
  test_pipeline.py
  test_plots.py
  test_app_smoke.py
.github/workflows/ci.yml
```

## Responsibilities
- `app.py`: Streamlit entrypoint and page layout.
- `src/pipeline.py`: main end-to-end flow; this is the central orchestration layer.
- `src/domain/models.py`: small dataclasses for line, profile, and result objects.
- `src/analysis/`: pure math and signal logic.
- `src/ui/`: canvas parsing and plot rendering.
- `src/config.py`: load and lightly validate config.

## Pipeline flow
1. Load config.
2. Load uploaded image or local demo image.
3. Read one line from canvas.
4. Sample RGB values along the line.
5. Convert to HSV and unwrap hue.
6. Generate reference rainbow profile.
7. Compare measured vs reference.
8. Render plots and score.

## Minimal tests
- `test_color.py`: RGB normalization and HSV conversion.
- `test_pipeline.py`: simple end-to-end analysis on synthetic data.
- `test_plots.py`: figure creation smoke test.
- `test_app_smoke.py`: app starts without crashing.

## CI minimum
- Install with Pixi.
- Run lint.
- Run tests.
- Run one smoke check for plots/app.

## Work order
1. Create repo skeleton.
2. Set up Pixi.
3. Add local demo image.
4. Build `app.py` shell.
5. Build `pipeline.py`.
6. Add analysis modules.
7. Add plot modules.
8. Add tests and CI.
9. Deploy to Streamlit Community Cloud.

## Future placeholders
- Better scoring.
- Better scientific validation.
- Optional ML model.
- More UI controls.

