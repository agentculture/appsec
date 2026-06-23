# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/). This project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-06-23

### Added

- **Vendored the `remember` + `recall` memory skills from eidetic-cli**
  (cite-don't-import) — the write/read halves of eidetic's shared
  `~/.eidetic/memory` surface, so this agent (Claude and its colleague backend)
  can persist facts across sessions and recall them later, sharing one store.
  `remember` drives `eidetic remember` (idempotent upsert of one JSON record or
  an NDJSON batch on stdin, dedup by id + content hash); `recall` drives
  `eidetic recall` with four search modes — exact / approximate / keyword /
  hybrid — each hit carrying text, full provenance metadata, a relevance score,
  and a freshness signal. The `.sh` wrappers are byte-verbatim from eidetic-cli
  (their first-party origin); each `SKILL.md` is localized only in the
  illustrative `--scope <nick>` examples (Provenance keeps "First-party to
  eidetic-cli"). Both default to this agent's PRIVATE scope, reading the suffix
  from `culture.yaml`. Runtime dep: the `eidetic` CLI on PATH (else a local
  eidetic-cli checkout with `uv`). Propagated by rollout-cli's `eidetic-memory`
  recipe.

## [0.2.0] - 2026-05-25

### Added

- Six new vendored skills from `guildmaster` 0.5.1 (cite-don't-import): `agent-config`, `doc-test-alignment`, and `pypi-maintainer` (guildmaster-origin), plus the devague-origin trio `think`, `spec-to-plan`, and `assign-to-workforce` (re-broadcast via guildmaster). Completes the canonical skill kit per [#12](https://github.com/agentculture/appsec/issues/12).

### Changed

- Resynced the five existing vendored skills (`cicd`, `communicate`, `run-tests`, `sonarclaude`, `version-bump`) from `guildmaster` 0.5.1 and re-pointed their provenance from `steward` to `guildmaster` (the 2026-05-24 steward→guildmaster supplier cutover). `cicd` and `communicate` keep appsec's identity reframing; `communicate` gains the new `skill-new-brief.md` broadcast template.
- Re-applied appsec's two local script patches after the resync: `cicd/scripts/pr-status.sh` (`--repo "$REPO"` passthrough) and `version-bump/scripts/bump.py` (`idx != -1` insertion guard). Re-filed upstream against guildmaster — [guildmaster#19](https://github.com/agentculture/guildmaster/issues/19) and [guildmaster#18](https://github.com/agentculture/guildmaster/issues/18) — superseding the stale steward#34 references.
- Re-pointed `docs/skill-sources.md`, `CLAUDE.md`, and the `.claude/skills.local.yaml.example` sibling example from `steward` to `guildmaster` as the AgentCulture skill supplier.

## [0.1.0] - 2026-05-14

### Added

- AgentCulture sibling scaffold: the `appsec` package (hatchling,
  Python >=3.12, zero runtime deps) with the afi-cli CLI chassis —
  structured errors, a strict stdout/stderr split, and `--json` support.
- Placeholder agent-first verbs `learn` / `explain` / `whoami` — honest
  "not yet implemented; appsec is greenfield" stubs.
- CI workflows: `tests.yml` (pytest + coverage + flake8 + SonarCloud +
  version-check), `security-checks.yml` (bandit + pylint), `publish.yml`
  (TestPyPI on PR, PyPI on main, via OIDC Trusted Publishing).
- `culture.yaml` declaring the `appsec` agent nick.
- Vendored skills from steward: `cicd`, `communicate`, `run-tests`,
  `sonarclaude`, `version-bump`. Provenance tracked in
  `docs/skill-sources.md`.
- Repo-local lint configs: `.flake8`, `.markdownlint-cli2.yaml`,
  `.pre-commit-config.yaml`; `sonar-project.properties`; the
  `.claude/skills.local.yaml.example` per-machine config template.

Resolves #2, #3, #4, #5, #6, #7.
