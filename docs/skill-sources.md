# Skill sources — vendored skill provenance

appsec vendors cross-sibling skills from `guildmaster`, the AgentCulture skill
supplier. This follows the **cite, don't import** pattern: each skill is
copied into `.claude/skills/`, owned locally, and may diverge. Nothing
imports across repos at runtime.

This file is the upstream/downstream map. When upstream changes, re-sync
explicitly — these copies do not auto-update.

> **Provenance / cutover.** Upstream was reassigned from `steward` to
> `guildmaster` on 2026-05-24 (the steward→guildmaster broadcaster cutover).
> All rows below were re-pointed and resynced from **guildmaster 0.5.1** per
> [agentculture/appsec#12](https://github.com/agentculture/appsec/issues/12).
> guildmaster's canonical kit is itself a steward fork, so the vendored bodies
> still reference steward-specific constructs (`steward doctor`,
> `STEWARD_PR_AWAIT_WAIT`, `steward announce-skill-update`) as inherited
> upstream context.

## Canonical skills (upstream = guildmaster)

| Skill | Re-vendor from | Vendored | Runtime backing & notes |
|-------|----------------|----------|-------------------------|
| `cicd` | `guildmaster` (`../guildmaster/.claude/skills/cicd/`) | 2026-05-25 | **Runtime:** the core PR-lifecycle verbs (`lint` / `open` / `read` / `reply` / `delta`) are a thin delegate to `agex pr` from `agentculture/agex-cli` — `agex` must be installed (`uv tool install agex-cli`). The `await` combo verb has since landed natively in agex ([agex-cli#41](https://github.com/agentculture/agex-cli/issues/41), now closed); the remaining gate extras not yet native — SonarCloud hotspots, deploy-preview URL, unresolved-thread tally — are tracked upstream in [agex-cli#52](https://github.com/agentculture/agex-cli/issues/52). **Divergence:** (1) identifier-only — SKILL.md frontmatter `description` reframed for appsec; body prose (incl. the "guildmaster edition" H1, `steward doctor`, `STEWARD_PR_AWAIT_WAIT`) references upstream constructs as inherited context, not appsec-actionable. (2) Local script patch — `scripts/pr-status.sh` passes `--repo "$REPO"` to `gh pr view` / `gh pr checks` (upstream omits it; marked `# appsec-divergence:`). Filed upstream as [agentculture/guildmaster#19](https://github.com/agentculture/guildmaster/issues/19); drop the patch on next re-vendor. |
| `communicate` | `guildmaster` (`../guildmaster/.claude/skills/communicate/`) | 2026-05-25 | **Runtime:** the GitHub issue-I/O verbs (`post-issue` / `post-comment` / `fetch-issues`) are thin wrappers around `agtag` (>=0.1) — `agtag` must be installed. Signatures resolve from the local `culture.yaml` first-agent `suffix` (here: `appsec`), overridable via `agtag --as NICK`; mesh messages stay unsigned. **Divergence:** identifier-only — SKILL.md frontmatter `description` reframed for appsec (incl. the auto-sign `- appsec (Claude)`). Body prose references guildmaster as the supplier and the steward-cli-only `steward announce-skill-update` broadcast verb, neither of which is appsec-actionable — appsec is a consumer, it doesn't broadcast. |
| `run-tests` | `guildmaster` (`../guildmaster/.claude/skills/run-tests/`) | 2026-05-25 | None — portable verbatim. Coverage source resolves from `[tool.coverage.run]` in `pyproject.toml`. |
| `sonarclaude` | `guildmaster` (`../guildmaster/.claude/skills/sonarclaude/`) | 2026-05-25 | None — portable verbatim. Project key resolves from `$SONAR_PROJECT` / `--project`. (Upstream carries a `cmd_accept` transition-status bug tracked in [agentculture/guildmaster#18 §2](https://github.com/agentculture/guildmaster/issues/18); carried verbatim, not patched locally.) |
| `version-bump` | `guildmaster` (`../guildmaster/.claude/skills/version-bump/`) | 2026-05-25 | **Divergence:** local script patch — `scripts/bump.py` uses `idx != -1` (not upstream's `idx > 0`) so a `CHANGELOG.md` that starts directly with a `## [` entry (marker at index 0) is a valid insertion point (marked `# appsec-divergence:`). Flagged upstream on [agentculture/guildmaster#18](https://github.com/agentculture/guildmaster/issues/18) (the bump.py insertion-logic issue); drop the patch on next re-vendor. Otherwise pure Python, no per-repo customization. |
| `agent-config` | `guildmaster` (`../guildmaster/.claude/skills/agent-config/`) | 2026-05-25 | New 2026-05-25. Backs the `guild show` inventory view; read-only. Ships `data/backend-fingerprints.yaml`; suffix mode reads `.claude/skills.local.yaml`. None — verbatim. (Upstream carries a missing-config `awk` robustness bug tracked in [agentculture/guildmaster#18 §3](https://github.com/agentculture/guildmaster/issues/18); carried verbatim, not patched locally.) |
| `doc-test-alignment` | `guildmaster` (`../guildmaster/.claude/skills/doc-test-alignment/`) | 2026-05-25 | New 2026-05-25. **STUB** — `scripts/check.sh` exits with a not-yet-implemented notice today; the contract for what it will check lives in `SKILL.md`. None — verbatim. |
| `pypi-maintainer` | `guildmaster` (`../guildmaster/.claude/skills/pypi-maintainer/`) | 2026-05-25 | New 2026-05-25. Switches a package install between production PyPI, TestPyPI, and a local editable checkout via `uv`; the package name is passed as an argument (generic across siblings). None — verbatim. |

## Inbound workflow skills (origin = devague, re-broadcast via guildmaster)

These three originate in [`agentculture/devague`](https://github.com/agentculture/devague);
guildmaster pulls and re-broadcasts them. Cite guildmaster's copy, track devague
as the true upstream.

| Skill | Re-vendor from | Vendored | Runtime backing & notes |
|-------|----------------|----------|-------------------------|
| `think` | `guildmaster` (re-broadcast; origin `agentculture/devague`) | 2026-05-25 | New 2026-05-25. idea→spec; drives the deterministic `devague` CLI (must be installed to run). Inherits guildmaster's `type: command` frontmatter addition over the devague original (culture/agex `core.skill_loader` requires `type:`, and appsec declares an agent in `culture.yaml`, so it is load-bearing on the culture backend, harmless on claude-code). Verbatim from guildmaster — no appsec divergence. |
| `spec-to-plan` | `guildmaster` (re-broadcast; origin `agentculture/devague`) | 2026-05-25 | New 2026-05-25. spec→plan; drives the `devague plan` CLI group. Same inherited `type: command` note as `think`. Verbatim from guildmaster. |
| `assign-to-workforce` | `guildmaster` (re-broadcast; origin `agentculture/devague`) | 2026-05-25 | New 2026-05-25. plan→parallel implementation (fans out `devague plan waves` to worktree agents; operator-driven). Same inherited `type: command` note as `think`. Verbatim from guildmaster. |

## Vendoring policy

- **Cite, don't import.** Skills are copied, not symlinked or installed as
  a dependency.
- **Re-sync explicitly.** When upstream changes, re-vendor from
  `../guildmaster/.claude/skills/<name>/` (devague-origin skills too — guildmaster
  is the re-broadcast point).
- **Diverge intentionally.** Record any divergence in the tables above and
  in the downstream `SKILL.md` frontmatter `description`.
