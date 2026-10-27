# AGENTS.md

Repository-local rules for `rainbower`.

Keep this file short and specific to this repo. Global behavior already lives in the higher-level agent instructions, so this file should only capture local constraints and conventions that are easy to forget.

> Just miscellaneous info for the AI agents working on the repo

## Scope

- Work inside `/Users/joshua/git/rainbower` unless explicitly asked otherwise.
- Prefer small, atomic edits over broad rewrites.
- Read `STATUS.md` before starting meaningful work and update it after a meaningful subtask.

## Environment

- Do **not** modify the system Python, Homebrew, shell profiles, or global package state.
- Use the project environment via **Pixi**.
- If a dependency is missing, add it through Pixi or ask before changing dependency files.

Examples:

```bash
pixi add <pkg>
pixi run <task>
pixi run python -c "..."
```

## Dependencies

- Keep runtime Python dependencies aligned across `pyproject.toml`, `pixi.toml`, and `requirements.txt` when deployment is affected.
- Treat `pyproject.toml` as the editable source of truth for runtime dependencies unless the repo says otherwise.
- `requirements.txt` is a generated deployment artifact kept for Streamlit Cloud compatibility.
- Do not add `uv.lock`, `Pipfile`, or `environment.yml` unless explicitly requested.
