# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

This repository is a **greenfield project**. As of the initial commit, it contains only `README.md`, `LICENSE`, and a Python `.gitignore` — no source code, dependencies, build configuration, or tests exist yet.

The stated intent (from `README.md`) is: **"An appsec agent"** — an application-security agent. Specifics (language beyond the Python `.gitignore` hint, frameworks, architecture, target surface) have not been chosen.

## When Extending This File

Once the project takes shape, replace the placeholders below with concrete information. Do not pad this file with generic best-practice advice — only document things a new Claude instance could not derive by reading the code itself.

- **Build / install** — record the exact command(s) once `pyproject.toml` / `requirements.txt` / equivalent exists.
- **Run** — entry point (`python -m …`, CLI name, daemon command).
- **Test** — full suite command and the form for running a single test.
- **Lint / format** — the toolchain actually configured (the workspace-level `~/git/CLAUDE.md` mentions `flake8`, `pylint`, `bandit`, `black`, `isort` as common defaults across sibling Python projects, but only adopt what this repo actually uses).
- **Architecture** — the cross-file "big picture" once there are multiple modules. Skip until there is something non-obvious to describe.

## Workspace Context

This repo lives under `/home/spark/git/` alongside other independent projects (see `/home/spark/git/CLAUDE.md`). The GitHub remote is `agentculture/appsec`, so this is an **AgentCulture org repo** — the cicd/PR-signing conventions from the global `~/.claude/CLAUDE.md` apply. There is no `culture.yaml` yet, so `_resolve-nick.sh` will fall back to the repo basename (`appsec`); signatures resolve to `- appsec (Claude)`. When the cicd skill's `pr-reply.sh` / `pr-batch.sh` author a post, let them append the signature automatically — don't sign manually. For posts those scripts don't author (manual `gh pr create --body …`, etc.), sign explicitly as `- appsec (Claude)`.
