# appsec onboarding — AgentCulture sibling scaffold

**Date:** 2026-05-14
**Status:** Approved (design)
**Closes:** agentculture/appsec issues #2, #3, #4, #5, #6, #7

## Problem

`appsec` is a brand-new AgentCulture sibling repo. Today it contains only
`CLAUDE.md`, `LICENSE`, `README.md`, `.gitignore`, and
`.claude/settings.local.json` — no package, no build config, no CI, no
`culture.yaml`, no vendored skills.

Six GitHub issues define the onboarding work:

- **#2** — the onboarding contract: the 12 required sibling artifacts, the
  quality pipeline (CI workflows + SonarCloud gate), and the inherited
  conventions (signatures, per-machine config, portability).
- **#3–#7** — vendor five canonical skills from `steward`: `cicd`,
  `communicate`, `run-tests`, `sonarclaude`, `version-bump`.

Issues #3–#7 are written as "re-sync your *stale* vendored copy", but
`appsec` has nothing yet — for this repo they are a clean first-time
vendoring, and every `git rm <old-name>` / stale-reference-sweep step in
those issues is a no-op.

## Scope

**In scope:** the onboarding *infrastructure* only — make `appsec` a
"healthy sibling" per `steward`'s `docs/sibling-pattern.md`.

**Out of scope:** the actual `appsec` application-security agent product.
The `learn` / `explain` / `whoami` CLI verbs ship as honest placeholder
stubs; designing what the agent *does* is a separate later effort.

## Decisions (locked during brainstorming)

| Decision | Choice |
|----------|--------|
| Scope | Onboarding infrastructure only; agent product deferred. |
| CLI verb depth | Bare placeholder stubs — each verb prints one honest "not yet implemented; appsec is greenfield" line and exits 0. |
| `publish.yml` | Commit the workflow now; PyPI Trusted-Publishing registration is a manual step the maintainer does separately. The workflow runs red until then — expected, not a regression. |
| PR strategy | One PR for everything: full scaffold + all 5 vendored skills + provenance ledger. One version bump (`0.1.0`). Closes all 6 issues. |
| Scaffold model | Mirror `afi-cli` — the named "afi-cli pattern" exemplar in `sibling-pattern.md`, the most minimal sibling, a pure CLI tool, and its CI already carries the "no `pyproject.toml` on main yet" first-PR carve-out. |
| Known gaps | Collected into a single GitHub tracking issue (see "Gaps tracking issue" below), opened early in implementation so the scaffold PR references it. |

## Architecture

### Target repo layout

```
appsec/
├── pyproject.toml            # name="appsec-cli", CLI entry "appsec", hatchling, py>=3.12, zero runtime deps
├── CHANGELOG.md              # Keep-a-Changelog; [0.1.0] entry
├── culture.yaml              # agents: [{suffix: appsec, backend: claude}]
├── sonar-project.properties  # projectKey=agentculture_appsec, org=agentculture
├── .flake8                   # vendored from afi-cli
├── .markdownlint-cli2.yaml   # vendored from afi-cli
├── .pre-commit-config.yaml   # vendored from afi-cli
├── appsec/                   # the package
│   ├── __init__.py           # __version__ via importlib.metadata, "0.0.0+local" fallback
│   ├── __main__.py           # python -m appsec
│   └── cli/
│       ├── __init__.py       # argparse dispatch, structured-error routing, --json hint
│       ├── _errors.py        # AppsecError + exit-code policy
│       ├── _output.py        # stdout/stderr split helpers
│       └── _commands/
│           ├── __init__.py
│           ├── learn.py      # placeholder stub
│           ├── explain.py    # placeholder stub
│           └── whoami.py     # placeholder stub
├── tests/
│   ├── __init__.py
│   └── test_cli_stubs.py     # per-verb exit-0 + output assertions, --json shape, --version
├── .github/workflows/
│   ├── tests.yml             # pytest + coverage + Sonar + flake8 + version-check
│   ├── security-checks.yml   # bandit + pylint
│   └── publish.yml           # TestPyPI on PR, PyPI on main, OIDC Trusted Publishing
├── docs/
│   ├── skill-sources.md      # provenance ledger for the 5 vendored skills
│   └── superpowers/specs/    # this spec
└── .claude/
    ├── settings.local.json        # (already present)
    ├── skills.local.yaml.example  # documents culture_server_yaml + sibling_projects keys
    └── skills/
        ├── cicd/             # vendored from ../steward
        ├── communicate/      # vendored from ../steward
        ├── run-tests/        # vendored from ../steward
        ├── sonarclaude/      # vendored from ../steward
        └── version-bump/     # vendored from ../steward
```

### Component 1 — the package & CLI chassis

`appsec/__init__.py` and `appsec/__main__.py` are near-verbatim adaptations
of afi-cli's (substitute `afi-cli` → `appsec-cli`, `afi` → `appsec`).
`__version__` resolves via `importlib.metadata.version("appsec-cli")` with
a `"0.0.0+local"` fallback for editable installs without metadata.

`cli/__init__.py`, `cli/_errors.py`, `cli/_output.py` are **real working
code**, not stubs — `sibling-pattern.md` artifact #3 requires these files
and they are the chassis every future verb plugs into. Adapted from
afi-cli:

- `cli/_errors.py` — `AppsecError` dataclass `{code, message, remediation}`
  plus the exit-code policy constants (`EXIT_SUCCESS=0`,
  `EXIT_USER_ERROR=1`, `EXIT_ENV_ERROR=2`).
- `cli/_output.py` — `emit_result` / `emit_error` / `emit_diagnostic`,
  enforcing the strict "results to stdout, diagnostics + errors to stderr"
  split, with a JSON mode.
- `cli/__init__.py` — `_AppsecArgumentParser` subclass routes argparse
  errors through `emit_error`; `main()` builds the parser, registers the
  three verb subparsers, dispatches, and wraps any non-`AppsecError`
  exception so no traceback leaks. `appsec` with no args prints help and
  exits 0; `appsec --version` works via the chassis.

### Component 2 — the three placeholder verbs

Each of `cli/_commands/{learn,explain,whoami}.py` exposes a `register(sub)`
that adds its subparser (with `--json`) and a handler that prints one
honest line and returns 0:

- `appsec learn` → `appsec — application-security agent. Not yet
  implemented; appsec is a greenfield AgentCulture sibling. See CLAUDE.md.`
- `appsec explain` → `appsec explain — not yet implemented; appsec is
  greenfield. See CLAUDE.md.`
- `appsec whoami` → `appsec — not yet implemented; appsec is greenfield.
  See CLAUDE.md.`

With `--json`, each emits a small structured payload (e.g.
`{"tool": "appsec", "status": "greenfield", "verb": "<verb>"}`) so the
`--json` contract holds even for stubs.

### Component 3 — tests

`tests/test_cli_stubs.py` — one test per verb asserting exit 0 and the
expected line in stdout, plus a `--json` shape test and a `--version`
test. Exercises the chassis + all three stubs, satisfying the
"no untested verb ships" gate and keeping coverage meaningful.

### Component 4 — config & lint files

- `pyproject.toml` — `name = "appsec-cli"`, `version = "0.1.0"`,
  `requires-python = ">=3.12"`, hatchling build, `[project.scripts]`
  `appsec = "appsec.cli:main"`, empty runtime `dependencies`, dev group
  (pytest + pytest-xdist + pytest-cov + coverage + bandit + pylint +
  flake8 + flake8-bandit + flake8-bugbear + black + isort + pre-commit —
  the flake8 plugins are required by the vendored `.flake8`'s
  `extend-select = B`), `[tool.coverage.run] source = ["appsec"]`, plus
  `[tool.black]`, `[tool.isort]`, `[tool.bandit]`, `[tool.pytest.ini_options]`
  — adapted from afi-cli.
- `culture.yaml` — `agents: [{suffix: appsec, backend: claude}]`. The
  `suffix` resolves the signing nick `appsec` for `agtag`-backed signatures.
- `CHANGELOG.md` — Keep-a-Changelog skeleton with a `## [0.1.0] - 2026-05-14`
  entry describing the onboarding scaffold.
- `.flake8`, `.markdownlint-cli2.yaml`, `.pre-commit-config.yaml` — vendored
  from afi-cli (drop afi-specific `exclude` / `per-file-ignores` paths that
  don't apply).
- `sonar-project.properties` — `sonar.projectKey=agentculture_appsec`,
  `sonar.organization=agentculture`, `sonar.sources=appsec`,
  `sonar.tests=tests`, coverage report path `coverage.xml`.

### Component 5 — CI workflows

All three vendored from afi-cli with `afi` → `appsec` substitutions.

- **`tests.yml`** (PR + push to main): a `test` job
  (`uv sync` → `uv run pytest -n auto --cov=appsec --cov-report=xml:coverage.xml`
  → SonarCloud scan gated on `SONAR_TOKEN_PRESENT` → `flake8` step) and a
  PR-only `version-check` job. The version-check's
  `if [ -z "$MAIN_VERSION" ]` branch auto-passes when `main` has no
  `pyproject.toml` — exactly the first-PR situation, so CI goes green
  without a chicken-and-egg fight. A `flake8` step is added to the `test`
  job so issue #2's literal "pytest + flake8 + bandit" wording is satisfied.
- **`security-checks.yml`** (PR + push + weekly cron): `bandit -r appsec/`
  and `pylint appsec/`, both `continue-on-error`, results uploaded as
  artifacts.
- **`publish.yml`** (PR/push touching `pyproject.toml` or `appsec/**`): a
  `test-publish` job (TestPyPI via OIDC on same-repo PRs, version suffixed
  `.dev<run_number>`, skipped on fork PRs) and a `publish` job (PyPI via
  OIDC on push to main). Uses `environment: testpypi` / `environment: pypi`
  and `id-token: write`.

### Component 6 — vendored skills & provenance ledger

Copy five skill directories from the local `../steward` checkout into
`.claude/skills/`:

| Skill | Scripts | Adaptation |
|-------|---------|------------|
| `cicd` | `_resolve-nick.sh`, `portability-lint.sh`, `pr-reply.sh`, `pr-status.sh`, `workflow.sh` | Nick resolves from `culture.yaml` — no hard-coded literal. SKILL.md prose: swap "steward" → "appsec" only where it names the *consumer*, never where it cites steward as upstream. |
| `communicate` | `fetch-issues.sh`, `mesh-message.sh`, `post-comment.sh`, `post-issue.sh` + `templates/` | Backed by `agtag` — signature resolves from `culture.yaml` (`suffix: appsec`). No literal to edit. |
| `run-tests` | `test.sh` | Coverage source resolves from `[tool.coverage.run]` in `pyproject.toml` — portable as-is. |
| `sonarclaude` | `sonar.sh` | Project key resolves from `$SONAR_PROJECT` / `--project` — nothing hard-coded. |
| `version-bump` | `bump.py` | Pure Python, no per-repo customization. |

All `scripts/*.sh` get `chmod +x`. Each `SKILL.md` frontmatter `name` must
equal its directory name (the `skills-convention` invariant).

`docs/skill-sources.md` — new provenance ledger, a table modeled on
steward's own, listing each of the five skills with upstream
`../steward/.claude/skills/<name>/`. Makes future re-syncs unambiguous and
satisfies the "if you keep a docs/skill-sources.md" acceptance line in
issues #3–#7.

`.claude/skills.local.yaml.example` — a committed, documented template
covering the `culture_server_yaml` and `sibling_projects` keys (the
steward-prescribed version, not afi-cli's empty file). The git-ignored
`.claude/skills.local.yaml` holds the real values; `.gitignore` is updated
to exclude it.

### Component 7 — CLAUDE.md refresh

`appsec/CLAUDE.md` currently carries greenfield placeholders ("no source
code… exists yet"). Once the scaffold lands, replace those with the real
build / run / test / lint commands and a short architecture note.

## Build sequence

Single branch, single PR. Each step is verified before the next.

0. **Open the gaps tracking issue** (see below) so the scaffold PR can
   reference it.
1. **Scaffold the package** — `pyproject.toml`, `appsec/` package
   (`__init__`, `__main__`, `cli/` chassis + 3 stub verbs), `tests/`.
   Verify: `uv sync && uv run pytest` green; `uv run python -m appsec
   --version` works; each verb exits 0.
2. **Config & lint files** — `culture.yaml`, `CHANGELOG.md`, `.flake8`,
   `.markdownlint-cli2.yaml`, `.pre-commit-config.yaml`,
   `sonar-project.properties`. Verify: `uv run flake8 appsec/` and
   `markdownlint-cli2` clean.
3. **CI workflows** — `tests.yml`, `security-checks.yml`, `publish.yml`.
4. **Vendor 5 skills** — `cp -R` from `../steward`, `chmod +x`, adapt
   SKILL.md consumer-prose, write `docs/skill-sources.md` and
   `.claude/skills/skills.local.yaml.example`. Verify: each `SKILL.md`
   frontmatter `name` matches its directory.
5. **Refresh `CLAUDE.md`** — replace greenfield placeholders with real
   commands.
6. **Verify as a sibling** — run `steward doctor` (self scope) and
   `bash .claude/skills/cicd/scripts/portability-lint.sh`; fix anything
   flagged in-PR.
7. **Open the PR** — via `agex pr` / the vendored `cicd` skill so the
   signature is auto-applied. Body: summary, `Closes #2 … #7`, and a
   pointer to the gaps tracking issue. One version bump: `0.1.0`.

Commit grouping: ~5 commits along the step 1–5 boundaries (scaffold /
config / CI / skills / CLAUDE.md) so the PR is reviewable.

## Gaps tracking issue

A single GitHub issue on `agentculture/appsec`, opened at build step 0,
collecting every known gap and divergence so future content work has one
reference point to fill against. Contents:

1. **PyPI Trusted Publishing not configured.** `publish.yml` runs red
   until the maintainer registers `appsec-cli` on PyPI + TestPyPI,
   configures the OIDC publisher for `agentculture/appsec`, and creates
   the `pypi` / `testpypi` GitHub environments.
2. **SonarCloud project registration.** Confirm the `agentculture_appsec`
   project exists on sonarcloud.io and the SonarCloud GitHub App is
   installed on the repo. The scan step is gated on `SONAR_TOKEN_PRESENT`
   so CI won't break if absent, but the quality gate won't report until
   the project is registered.
3. **CLI verbs are placeholder stubs.** `learn` / `explain` / `whoami`
   print "not yet implemented" lines. Real implementations come when the
   `appsec` agent product is designed.
4. **The `appsec` agent product is undefined.** README says "An appsec
   agent"; the actual application-security capability — what it analyzes,
   its real CLI surface, its architecture — has not been designed.
5. **Security-tooling layout diverges from issue #2's literal text.**
   Issue #2 says "pytest + flake8 + bandit" in `tests.yml`; this scaffold
   follows the afi-cli exemplar — `flake8` in `tests.yml`, `bandit` +
   `pylint` in `security-checks.yml`. A deliberate divergence, recorded
   here.

The issue is opened with the `cicd` / `communicate` skill so the
`- appsec (Claude)` signature is auto-applied.

## Acceptance criteria

From issue #2 plus #3–#7, the scaffold is done when:

- `steward doctor` (self scope) reports zero `portability` and
  `skills-convention` violations against the repo.
- `bash .claude/skills/cicd/scripts/portability-lint.sh` passes.
- `uv run pytest` is green; `uv run flake8 appsec/` is clean.
- `culture.yaml` declares `backend` + `suffix` for the `appsec` agent.
- All five vendored skill directories (`cicd`, `communicate`,
  `run-tests`, `sonarclaude`, `version-bump`) have a `SKILL.md` whose
  frontmatter `name` matches the directory name, plus a sibling
  `scripts/` directory; `scripts/*.sh` are executable.
- `docs/skill-sources.md` lists all five skills with their
  `../steward/...` upstreams.
- `CHANGELOG.md` has the `[0.1.0]` entry; `pyproject.toml` version is
  `0.1.0`; CI `version-check` is green (auto-passes — no `pyproject.toml`
  on `main`).
- The PR closes #2–#7 and references the gaps tracking issue.

### Known not-green at merge (tracked in the gaps issue, not blockers)

- `publish.yml` runs red until PyPI Trusted Publishing is configured.
- SonarCloud quality gate does not report until the project is
  registered.

## References

- `steward/docs/sibling-pattern.md` — the 12 required artifacts and the
  `steward doctor` invariants.
- `steward/docs/skill-sources.md` — canonical upstream for each skill.
- `afi-cli/` — the scaffold exemplar (`pyproject.toml`, `afi/` package,
  `.github/workflows/`, lint configs).
- agentculture/appsec issues #2–#7.
