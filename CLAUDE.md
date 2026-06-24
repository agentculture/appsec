# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

`appsec` is an AgentCulture sibling repo. The onboarding scaffold is in place
(package, CLI chassis, CI, vendored skills); the actual application-security
agent — what it analyzes, its real command surface, its architecture — has
**not** been designed yet. The `learn` / `explain` / `whoami` verbs are honest
placeholder stubs. Known gaps and deferred work are tracked in the repo's
onboarding gaps issue.

## Build / Install

```bash
uv sync                       # install the package + dev dependencies
```

## Run

```bash
uv run appsec --version       # or: uv run python -m appsec
uv run appsec learn           # placeholder verbs: learn / explain / whoami
```

## Test

```bash
uv run pytest -n auto         # full suite
uv run pytest tests/test_cli_chassis.py::test_no_args_prints_help_and_returns_zero -v   # single test (example node id)
```

## Lint / Format

```bash
uv run flake8 --config=.flake8 appsec/ tests/
uv run black appsec/ tests/
uv run isort appsec/ tests/
markdownlint-cli2 "**/*.md"
```

Bandit and pylint run in CI (`.github/workflows/security-checks.yml`).

## Architecture

- `appsec/cli/__init__.py` — the argparse CLI chassis: structured error
  routing (`_AppsecArgumentParser`), `--json` hint detection, and
  `_dispatch` (invokes the verb handler, translating `AppsecError` and bare
  exceptions to structured exit codes). `main()` is the entry point, exposed
  as the `appsec` console script and via `python -m appsec`.
- `appsec/cli/_errors.py` — `AppsecError` and the exit-code policy.
- `appsec/cli/_output.py` — strict stdout/stderr split helpers.
- `appsec/cli/_commands/` — one module per verb, each exposing `register()`.
  All three verbs are currently greenfield stubs.

## Version Management

Every PR bumps the version in `pyproject.toml` (CI's `version-check` job
blocks merge if it matches `main`) and prepends a `CHANGELOG.md` entry
(convention — not CI-enforced). The vendored `version-bump` skill does both.

## Vendored Skills

`.claude/skills/` holds skills vendored from `guildmaster` (cite, don't
import) — the AgentCulture skill supplier, post the 2026-05-24 steward→guildmaster
cutover. Provenance and divergence (including devague-origin re-broadcasts) are
tracked in `docs/skill-sources.md`. Re-sync from
`../guildmaster/.claude/skills/<name>/`.

## Workspace Context

The GitHub remote is `agentculture/appsec`. When opening PRs or posting comments here as an AI assistant, sign them so it's clear they're AI-authored — e.g. `- appsec (Claude)`.

## Conventions and workflow

**Memory discipline — recall before, remember after.** This repo keeps its
eidetic memory **in-repo and public**: records resolve to
`<repo-root>/.eidetic/memory` — committed, and shared with the team and mesh
peers (the `claude` and `colleague` backends both read the same
`appsec` scope), so memory travels with the repo, not a private
home-dir store. Make it a per-task habit:

- **`/recall` before you start.** Search the store for the area you're about
  to touch — prior decisions, gotchas, "have we done this before?" — so you
  build on what's already known instead of re-deriving it. Do this before
  non-trivial tasks, not just when asked.
- **`/remember` when something worth keeping surfaces.** A non-obvious
  decision and its rationale, a constraint, a fix and *why* it was needed, a
  gotcha that cost time, a fact the next session would otherwise re-learn.
  Capture it as it happens, not at the end when it's faded.

A plain `/remember` lands the note in `./.eidetic/memory` in this repo — no
flag needed (the wrappers here default to `--visibility public`; in-repo
routing needs `eidetic >= 0.10.0`, older CLIs keep records in `$HOME`). Keep
something out of the committed store only by passing `--visibility private`
(routes to `$HOME/.eidetic/memory`, never committed); `/recall` reads both
stores and merges. Don't store what the repo already records (code structure,
git history, what's already in this file or `CHANGELOG.md`) — store what you'd
have to re-derive. These are the `recall`/`remember` skills (`.claude/skills/`),
backed by the `eidetic` store.
