# PENDINGS

Ideas to improve later. Quick fixes come first; these make them systematic.

## Single source of truth for dependencies

- Source of truth: `[project.dependencies]` in `pyproject.toml` (Pixi reads it as PyPI deps).
- `requirements.txt` is a generated artifact, kept only because Streamlit Cloud needs it.
  Without it, Cloud falls back to parsing `pyproject.toml` as Poetry and fails.
- Idea: one routine to add a dependency and regenerate everything in one step:
  1. `pixi add --pypi <pkg>` (updates `pyproject.toml` and `pixi.lock`)
  2. `uv pip compile pyproject.toml -o requirements.txt`
  3. Wrap steps 1-2 as a Pixi task (e.g. `pixi run add-dep <pkg>`) so nobody edits both lists by hand.
- Optional: pre-push check that `requirements.txt` matches `pyproject.toml`.
- Do not commit `uv.lock`, `Pipfile` or `environment.yml`; Streamlit Cloud prefers them over `requirements.txt`.

## Streamlit Cloud

- Check `streamlit-drawable-canvas` compatibility with the Streamlit version Cloud installs (1.65 seen).
  The package is old; consider pinning Streamlit or using a maintained fork.
- `pixi.toml` and `pyproject.toml` both exist; decide on one Pixi manifest.
- `pyproject.toml` declares package `rainbower` but no such folder exists; fix or drop the build section.
