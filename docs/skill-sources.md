# Skill sources — vendored skill provenance

appsec vendors cross-sibling skills from `steward`, the AgentCulture skill
supplier. This follows the **cite, don't import** pattern: each skill is
copied into `.claude/skills/`, owned locally, and may diverge. Nothing
imports across repos at runtime.

This file is the upstream/downstream map. When upstream changes, re-sync
explicitly — these copies do not auto-update.

| Skill | Re-vendor from | Vendored | Runtime backing & notes |
|-------|----------------|----------|-------------------------|
| `cicd` | `steward` (`../steward/.claude/skills/cicd/`) | 2026-05-14 | **Runtime:** as of steward 0.12.0 the core PR-lifecycle verbs (`lint` / `open` / `read` / `reply` / `delta`) are a thin delegate to `agex pr` from `agentculture/agex-cli` — `agex` must be installed (`uv tool install agex-cli`). Steward keeps two extensions on top — `status` (SonarCloud gate + hotspots + unresolved-thread tally) and `await` (`agex pr read --wait` + `status`, non-zero exit on Sonar ERROR / unresolved threads) — filed upstream as [agex-cli#41](https://github.com/agentculture/agex-cli/issues/41). **Divergence:** (1) identifier-only — SKILL.md frontmatter `description` reframed for appsec; body prose still references steward-specific constructs (e.g. `steward doctor`, the `STEWARD_PR_AWAIT_WAIT` env var), which are inherited context, not appsec-actionable. (2) Local script patch — `scripts/pr-status.sh` passes `--repo "$REPO"` to `gh pr view` / `gh pr checks` (upstream omits it; marked with `# appsec-divergence:`). Fix filed upstream as [agentculture/steward#34](https://github.com/agentculture/steward/issues/34); drop the patch on next re-vendor. |
| `communicate` | `steward` (`../steward/.claude/skills/communicate/`) | 2026-05-14 | **Runtime:** as of steward 0.11.0 the GitHub issue-I/O verbs (`post-issue` / `post-comment` / `fetch-issues`) are thin wrappers around `agtag` (>=0.1) — `agtag` must be installed. Signatures resolve from the local `culture.yaml` first-agent `suffix` (here: `appsec`), overridable via `agtag --as NICK`; mesh messages stay unsigned. **Divergence:** identifier-only — SKILL.md frontmatter `description` reframed for appsec. Body prose references steward as the supplier; the `steward announce-skill-update` broadcast verb is steward-cli-only and not available to appsec. |
| `run-tests` | `steward` (`../steward/.claude/skills/run-tests/`) | 2026-05-14 | None — portable verbatim. Coverage source resolves from `[tool.coverage.run]` in `pyproject.toml`. |
| `sonarclaude` | `steward` (`../steward/.claude/skills/sonarclaude/`) | 2026-05-14 | None — portable verbatim. Project key resolves from `$SONAR_PROJECT` / `--project`. |
| `version-bump` | `steward` (`../steward/.claude/skills/version-bump/`) | 2026-05-14 | **Divergence:** local script patch — `scripts/bump.py` uses `idx != -1` (not upstream's `idx > 0`) so a `CHANGELOG.md` that starts directly with a `## [` entry is a valid insertion point (marked with `# appsec-divergence:`). Fix filed upstream as [agentculture/steward#34](https://github.com/agentculture/steward/issues/34); drop the patch on next re-vendor. Otherwise pure Python, no per-repo customization. |

## Vendoring policy

- **Cite, don't import.** Skills are copied, not symlinked or installed as
  a dependency.
- **Re-sync explicitly.** When upstream changes, re-vendor from
  `../steward/.claude/skills/<name>/`.
- **Diverge intentionally.** Record any divergence in the table above and
  in the downstream `SKILL.md` frontmatter `description`.
