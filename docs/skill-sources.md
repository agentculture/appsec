# Skill sources — vendored skill provenance

appsec vendors cross-sibling skills from `steward`, the AgentCulture skill
supplier. This follows the **cite, don't import** pattern: each skill is
copied into `.claude/skills/`, owned locally, and may diverge. Nothing
imports across repos at runtime.

This file is the upstream/downstream map. When upstream changes, re-sync
explicitly — these copies do not auto-update.

| Skill | Upstream | Vendored | Divergence |
|-------|----------|----------|------------|
| `cicd` | `steward` (`../steward/.claude/skills/cicd/`) | 2026-05-14 | Identifier-only: SKILL.md frontmatter `description` reframed for appsec. Body prose still references steward workflows (e.g. the `steward announce-skill-update` broadcast verb) — appsec is a skill *consumer*, not the supplier, so broadcast mode is not available here. |
| `communicate` | `steward` (`../steward/.claude/skills/communicate/`) | 2026-05-14 | Identifier-only: SKILL.md frontmatter `description` reframed for appsec. Body prose references steward as the supplier; the `steward announce-skill-update` broadcast verb is steward-cli-only and not available to appsec. |
| `run-tests` | `steward` (`../steward/.claude/skills/run-tests/`) | 2026-05-14 | None — portable verbatim. Coverage source resolves from `[tool.coverage.run]` in `pyproject.toml`. |
| `sonarclaude` | `steward` (`../steward/.claude/skills/sonarclaude/`) | 2026-05-14 | None — portable verbatim. Project key resolves from `$SONAR_PROJECT` / `--project`. |
| `version-bump` | `steward` (`../steward/.claude/skills/version-bump/`) | 2026-05-14 | None — pure Python, no per-repo customization. |

## Vendoring policy

- **Cite, don't import.** Skills are copied, not symlinked or installed as
  a dependency.
- **Re-sync explicitly.** When upstream changes, re-vendor from
  `../steward/.claude/skills/<name>/`.
- **Diverge intentionally.** Record any divergence in the table above and
  in the downstream `SKILL.md` frontmatter `description`.
