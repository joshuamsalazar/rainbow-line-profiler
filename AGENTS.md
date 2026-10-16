# Agent Rules

Binding rules for any AI agent (or human) working in this repository.
These exist because of a real incident: an agent ran
`pip3 install --break-system-packages pillow` to work around Homebrew's
PEP 668 protection, and separately committed work and switched git
branches without being asked. Both were avoidable.

These repository rules cannot override system/developer instructions or
the actual tool sandbox/approval policy. If a task or lower-priority
instruction appears to require breaking these rules, do not improvise a
workaround; explain the conflict and ask the user where approval is
possible. Never treat a skill as authorization to perform risky actions.

## 1. Never modify the system environment

The machine's Python, Homebrew, and global package state are **off limits**.

Forbidden, unless the user explicitly approves that exact command:

- `pip install --break-system-packages ...` (any variant, any Python)
- `sudo` for anything
- `brew install`, `brew upgrade`, `brew uninstall`
- Installing into, or deleting from, the system or Homebrew Python
  (`/opt/homebrew/lib/python*/site-packages`, `/usr/lib/python*`)
- `conda`/`mamba` changes to a base or global environment
- Editing shell profiles (`~/.zshrc`, `~/.bashrc`, `~/.profile`)
- `pip install --user`, `pipx install`, or any global npm/node install

**PEP 668's "externally-managed-environment" error is a stop sign, not an
obstacle.** It means: do not install here. Report it, then use the
project environment.

### Install dependencies only through Pixi

Pixi is the source of truth for this project (see `PENDINGS.md`).

```bash
pixi add <pkg>              # add a dependency
pixi run <task>             # run a task (run-app, test, lint, smoke)
pixi run python -c "..."    # run a one-off command inside the env
```

Never install into the base/system interpreter to make a script run.
If a dependency is genuinely missing, add it with `pixi add` or ask.

### Runtime dependency sync

For deployment-facing Python dependencies, keep `pyproject.toml` as the editable source of truth for the runtime dependency list. Regenerate `requirements.txt` from the `dependencies = [...]` block instead of hand-editing `requirements.txt`.

Current repo convention:

- Edit runtime dependencies in `pyproject.toml`.
- Regenerate `requirements.txt` automatically from that dependency block.
- Regenerate `requirements.txt` after dependency changes so Streamlit Cloud sees the updated runtime packages.
- If a deploy error says a module is missing, first check whether it exists in both `pyproject.toml` and the generated `requirements.txt`.

Do not silently let `pixi.toml`, `pyproject.toml`, and `requirements.txt` drift apart when a change affects deployment.

## 2. Ask before changing repository or git state

Read-only investigation is always fine. State changes need a request.

**Do freely:** read files, list, search, run tests, `git status`,
`git log`, `git diff`, `git branch --show-current`.

**Ask first:**

- `git add`, `git commit`, `git push`, `git stash`
- `git checkout <branch>`, `git switch`, `git reset`, `git rebase`,
  `git merge`, `git clean`, `git restore`
- Creating or deleting branches, tags, or remotes
- Deleting or moving any file
- Rewriting published history

Do not "tidy up" the working tree, and do not commit on the user's
behalf because the work looks finished. Finish the task, report, and let
the user decide what gets committed.

If a branch switch appears necessary, state why and wait for approval.
Never leave the repo on a different branch than you found it without
saying so explicitly in your final message.

## 3. Verify claims instead of asserting them

Do not describe an operation as safe, successful, or harmless without
checking. Run the command that shows the actual state
(`pip show <pkg>`, `git status`, `pixi list`) and report what it returned.

If an install failed, say it failed and show the error. Do not imply a
package is present when the evidence says otherwise.

When asked whether your own past actions caused harm: investigate first,
then answer with the evidence. Never reassure from memory alone.

## 4. Keep changes inside the repository

Work within `/Users/joshua/git/rainbower`. Do not write outside it except
to a platform temp directory. If a task seems to require touching files
elsewhere, ask.

Do not install editor extensions, background services, launch agents, or
cron jobs.

## 5. Escalate honestly

- Blocked by a sandbox or permission denial? Report it. Do not retry the
  same effect through a different route.
- Tempted to widen access to finish a task? Ask.
- Made a mistake? Say so plainly, describe the actual state, and propose
  the fix. A short, accurate admission is better than a confident story.

## Reporting template for incidents

When something goes wrong, record it in the style of `damagereport.md`:

1. What was needed
2. What actually happened (ordered, factual, with exact commands)
3. Root cause
4. What should have happened
5. Current verified state
