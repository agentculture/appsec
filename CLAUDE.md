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
uv run pytest tests/test_cli_chassis.py::test_no_args_prints_help_and_returns_zero -v   # single test
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
  routing (`_AppsecArgumentParser`), `--json` hint detection, and the
  `_dispatch` exception wrapper. `main()` is the entry point, exposed as the
  `appsec` console script and via `python -m appsec`.
- `appsec/cli/_errors.py` — `AppsecError` and the exit-code policy.
- `appsec/cli/_output.py` — strict stdout/stderr split helpers.
- `appsec/cli/_commands/` — one module per verb, each exposing `register()`.
  All three verbs are currently greenfield stubs.

## Version Management

Every PR bumps the version (`pyproject.toml` + `CHANGELOG.md`) — CI's
`version-check` job blocks merge if the version matches `main`. Use the
vendored `version-bump` skill.

## Vendored Skills

`.claude/skills/` holds skills vendored from `steward` (cite, don't import).
Provenance and divergence are tracked in `docs/skill-sources.md`. Re-sync
from `../steward/.claude/skills/<name>/`.

## Workspace Context

The GitHub remote is `agentculture/appsec`. When opening PRs or posting comments here as an AI assistant, sign them so it's clear they're AI-authored — e.g. `- appsec (Claude)`.
