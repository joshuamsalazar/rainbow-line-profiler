# Rainbow Line Profiler

Small scientific Streamlit app to inspect whether a line across an image is consistent with a rainbow-like color signal.

## Architecture

- `app.py` is the Streamlit entrypoint.
- `src/pipeline.py` contains the main end-to-end analysis flow.
- Keep business logic out of `app.py`.
- Keep signal logic in `src/analysis/`.
- Keep rendering helpers in `src/ui/`.

## Environment

Pixi is the source of truth for environment management and tasks.

## Main commands

```bash
pixi run run-app
pixi run test
pixi run lint
```

## Testing

- Unit tests for color conversion and profile generation (`tests/`)
- Pipeline integration test
- Smoke test for app startup

## Deployment

Deploy to Streamlit Community Cloud using `streamlit.yaml` configuration (future).

## Future improvements

- [ ] Better scoring metrics
- [ ] More sophisticated scientific validation
- [ ] Optional ML model for enhanced analysis
- [ ] Advanced UI controls (e.g., multi-line analysis)
- [ ] Enhanced demo image with varied conditions
- [ ] Real-time feedback during line drawing
- [ ] Export functionality for analysis results
