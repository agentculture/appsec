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
- **Lint / format** — the toolchain actually configured. The `.gitignore` indicates Python; common Python choices are `flake8`, `pylint`, `bandit`, `black`, `isort` — adopt only what this repo actually wires up.
- **Architecture** — the cross-file "big picture" once there are multiple modules. Skip until there is something non-obvious to describe.

## Workspace Context

The GitHub remote is `agentculture/appsec`. When opening PRs or posting comments here as an AI assistant, sign them so it's clear they're AI-authored — e.g. `- appsec (Claude)`.
