# AGENTS.md

Repository-local rules for `rainbower`.

Keep this file short and specific to this repo. Global behavior already lives in the higher-level agent instructions, so this file should only capture local constraints and conventions that are easy to forget.

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

## Git and file safety

- Read-only inspection is always fine.
- Ask before destructive or history-changing actions.
- Ask before `git commit`, `git push`, branch switching, resets, rebases, merges, or deleting/moving files.
- Do not leave the repo on a different branch without explicitly saying so.

## Verification

- Verify important claims with commands or tests instead of assuming.
- If blocked by permissions, sandboxing, or missing tools, report it plainly.
- If something goes wrong, describe the real state and next safe step.

## Current workflow

- The current app is Streamlit-based, but notebook or Dash prototyping is allowed when requested.
- Reuse code from `src/analysis/` and related modules before introducing parallel implementations.
- Keep experimental prototypes minimal and easy to remove or promote later.

## Open repository issues

- Dependency flow should ideally be one-step: add through Pixi, then regenerate `requirements.txt`.
- Streamlit Cloud compatibility may require pinning Streamlit or replacing `streamlit-drawable-canvas`.
- The coexistence of `pixi.toml` and `pyproject.toml` should stay intentional and documented.
- If the build metadata names a package that does not exist, fix or remove that packaging declaration.
