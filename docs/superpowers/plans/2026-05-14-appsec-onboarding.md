# appsec Onboarding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold `appsec` into a healthy AgentCulture sibling — package, CLI chassis with placeholder verbs, CI, lint configs, `culture.yaml`, and five vendored skills — in a single PR that closes issues #2–#7.

**Architecture:** Mirror the `afi-cli` sibling exemplar. A hatchling-built `appsec-cli` package exposes an `appsec` CLI: a real argparse chassis (`appsec/cli/`) with structured errors, a strict stdout/stderr split, and `--json` support, plus three honest placeholder verbs (`learn` / `explain` / `whoami`). Five canonical skills are copied verbatim from the local `../steward` checkout. CI runs pytest + coverage + flake8 + SonarCloud + a version-check, with bandit/pylint in a separate workflow and PyPI publishing via OIDC.

**Tech Stack:** Python ≥3.12, `uv`, hatchling, pytest + pytest-cov + pytest-xdist, flake8/black/isort/bandit/pylint, GitHub Actions, SonarCloud.

---

## Working context

- All work happens on branch `onboarding/sibling-scaffold` (already created; the design spec is already committed there). Do **not** create a worktree — the repo is near-empty and there is no parallel work.
- Reference exemplar: `../afi-cli/` (read freely for shape; never copy afi-specific content).
- Skill upstream: `../steward/.claude/skills/`.
- The design spec is at `docs/superpowers/specs/2026-05-14-appsec-onboarding-design.md`.
- One version bump for the whole PR: `0.1.0`.

## File structure

| File | Responsibility |
|------|----------------|
| `pyproject.toml` | Package metadata, `appsec` entry point, dev deps, tool configs. |
| `appsec/__init__.py` | `__version__` via `importlib.metadata`. |
| `appsec/__main__.py` | `python -m appsec` shim. |
| `appsec/cli/__init__.py` | argparse chassis: `main`, `_dispatch`, `_AppsecArgumentParser`, verb registration. |
| `appsec/cli/_errors.py` | `AppsecError` dataclass + exit-code constants. |
| `appsec/cli/_output.py` | `emit_result` / `emit_error` / `emit_diagnostic` — stdout/stderr split. |
| `appsec/cli/_commands/__init__.py` | Empty package marker for verb modules. |
| `appsec/cli/_commands/learn.py` | `appsec learn` placeholder verb. |
| `appsec/cli/_commands/explain.py` | `appsec explain` placeholder verb. |
| `appsec/cli/_commands/whoami.py` | `appsec whoami` placeholder verb. |
| `tests/__init__.py` | Test package marker. |
| `tests/test_package.py` | Package-level smoke test. |
| `tests/test_cli_errors.py` | `AppsecError` + exit-code tests. |
| `tests/test_cli_output.py` | Output-helper tests. |
| `tests/test_cli_chassis.py` | Chassis tests: `--version`, no-args help, unknown verb, `python -m`. |
| `tests/test_cli_stubs.py` | Per-verb stub tests (exit 0 + output + `--json`). |
| `culture.yaml` | Declares the `appsec` agent nick. |
| `CHANGELOG.md` | Keep-a-Changelog; `[0.1.0]` entry. |
| `.flake8`, `.markdownlint-cli2.yaml`, `.pre-commit-config.yaml` | Repo-local lint configs. |
| `sonar-project.properties` | SonarCloud project identity. |
| `.github/workflows/tests.yml` | pytest + coverage + flake8 + Sonar + version-check. |
| `.github/workflows/security-checks.yml` | bandit + pylint. |
| `.github/workflows/publish.yml` | TestPyPI on PR / PyPI on main via OIDC. |
| `.claude/skills.local.yaml.example` | Per-machine config template. |
| `.claude/skills/{cicd,communicate,run-tests,sonarclaude,version-bump}/` | Vendored skills. |
| `docs/skill-sources.md` | Vendored-skill provenance ledger. |
| `CLAUDE.md` | Refreshed with real build/run/test/lint commands. |

---

## Task 1: Package skeleton + pyproject.toml

**Files:**
- Create: `pyproject.toml`
- Create: `appsec/__init__.py`
- Create: `tests/__init__.py`
- Test: `tests/test_package.py`

- [ ] **Step 1: Write `pyproject.toml`**

```toml
[project]
name = "appsec-cli"
version = "0.1.0"
description = "appsec — an application-security agent (greenfield AgentCulture sibling)."
readme = "README.md"
license = "MIT"
requires-python = ">=3.12"
authors = [{name = "AgentCulture"}]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: MIT License",
    "Topic :: Software Development",
    "Intended Audience :: Developers",
]
dependencies = []

[project.urls]
Homepage = "https://github.com/agentculture/appsec"
Issues = "https://github.com/agentculture/appsec/issues"

[project.scripts]
appsec = "appsec.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["appsec"]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-xdist>=3.0",
    "pytest-cov>=4.1",
    "coverage>=7.2.0",
    "bandit>=1.7.5",
    "pylint>=2.17.0",
    "flake8>=6.1",
    "flake8-bandit>=4.1.1",
    "flake8-bugbear>=23.7.10",
    "black>=23.7.0",
    "isort>=5.12.0",
    "pre-commit>=3.5.0",
]

[tool.coverage.run]
source = ["appsec"]
omit = ["appsec/__pycache__/*"]

[tool.coverage.report]
fail_under = 70
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.",
    "if TYPE_CHECKING:",
]

[tool.isort]
profile = "black"
line_length = 100
known_first_party = ["appsec"]

[tool.black]
line-length = 100
target-version = ["py312"]

[tool.bandit]
exclude_dirs = ["tests"]
skips = ["B101"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra"
```

- [ ] **Step 2: Write `appsec/__init__.py`**

```python
"""appsec — an application-security agent (greenfield AgentCulture sibling)."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _v

try:
    __version__ = _v("appsec-cli")
except PackageNotFoundError:  # editable install without metadata
    __version__ = "0.0.0+local"

__all__ = ["__version__"]
```

- [ ] **Step 3: Create empty `tests/__init__.py`**

Create `tests/__init__.py` with no content (empty file — test package marker).

- [ ] **Step 4: Write the failing test `tests/test_package.py`**

```python
"""Package-level smoke test."""

from __future__ import annotations

import appsec


def test_version_is_a_nonempty_string() -> None:
    assert isinstance(appsec.__version__, str)
    assert appsec.__version__
```

- [ ] **Step 5: Sync the environment and run the test**

Run: `uv sync && uv run pytest tests/test_package.py -v`
Expected: `uv sync` creates `.venv` + `uv.lock` and installs `appsec-cli` editably; the test PASSES (`__version__` resolves to `0.1.0`).

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml uv.lock appsec/__init__.py tests/__init__.py tests/test_package.py
git commit -m "Add appsec-cli package skeleton and pyproject.toml"
```

---

## Task 2: CLI error types

**Files:**
- Create: `appsec/cli/__init__.py` (empty for now — package marker; filled in Task 4)
- Create: `appsec/cli/_errors.py`
- Test: `tests/test_cli_errors.py`

- [ ] **Step 1: Create empty `appsec/cli/__init__.py`**

Create `appsec/cli/__init__.py` with no content for now. Task 4 replaces it with the chassis.

- [ ] **Step 2: Write the failing test `tests/test_cli_errors.py`**

```python
"""Tests for AppsecError and the exit-code policy."""

from __future__ import annotations

from appsec.cli._errors import (
    EXIT_ENV_ERROR,
    EXIT_SUCCESS,
    EXIT_USER_ERROR,
    AppsecError,
)


def test_exit_code_constants() -> None:
    assert EXIT_SUCCESS == 0
    assert EXIT_USER_ERROR == 1
    assert EXIT_ENV_ERROR == 2


def test_appsec_error_is_an_exception() -> None:
    err = AppsecError(code=1, message="bad input", remediation="try --help")
    assert isinstance(err, Exception)
    assert str(err) == "bad input"


def test_appsec_error_to_dict() -> None:
    err = AppsecError(code=2, message="missing tool", remediation="install it")
    assert err.to_dict() == {
        "code": 2,
        "message": "missing tool",
        "remediation": "install it",
    }


def test_remediation_defaults_to_empty() -> None:
    err = AppsecError(code=1, message="x")
    assert err.remediation == ""
```

- [ ] **Step 3: Run test to verify it fails**

Run: `uv run pytest tests/test_cli_errors.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'appsec.cli._errors'`.

- [ ] **Step 4: Write `appsec/cli/_errors.py`**

```python
"""AppsecError and exit-code policy.

Every failure inside appsec raises :class:`AppsecError`. The top-level
``main()`` catches it, formats via :mod:`appsec.cli._output`, and exits with
:attr:`AppsecError.code`. This centralises the exit-code policy and guarantees
no Python traceback leaks to stderr.
"""

from __future__ import annotations

from dataclasses import dataclass

# Exit-code policy:
#   0  = success
#   1  = user-input error (bad flag, missing required arg, unknown path)
#   2  = environment / setup error (tool not installed, file unreadable)
#   3+ = reserved for future categorisation
EXIT_SUCCESS = 0
EXIT_USER_ERROR = 1
EXIT_ENV_ERROR = 2


@dataclass
class AppsecError(Exception):
    """Structured error raised within appsec; carries a remediation hint."""

    code: int
    message: str
    remediation: str = ""

    def __post_init__(self) -> None:
        super().__init__(self.message)

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
            "remediation": self.remediation,
        }
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/test_cli_errors.py -v`
Expected: PASS (4 tests).

- [ ] **Step 6: Commit**

```bash
git add appsec/cli/__init__.py appsec/cli/_errors.py tests/test_cli_errors.py
git commit -m "Add AppsecError type and exit-code policy"
```

---

## Task 3: CLI output helpers

**Files:**
- Create: `appsec/cli/_output.py`
- Test: `tests/test_cli_output.py`

- [ ] **Step 1: Write the failing test `tests/test_cli_output.py`**

```python
"""Tests for the stdout/stderr output helpers."""

from __future__ import annotations

import io
import json

from appsec.cli._errors import AppsecError
from appsec.cli._output import emit_diagnostic, emit_error, emit_result


def test_emit_result_text_adds_trailing_newline() -> None:
    buf = io.StringIO()
    emit_result("hello", json_mode=False, stream=buf)
    assert buf.getvalue() == "hello\n"


def test_emit_result_json() -> None:
    buf = io.StringIO()
    emit_result({"a": 1}, json_mode=True, stream=buf)
    assert json.loads(buf.getvalue()) == {"a": 1}


def test_emit_error_text_with_remediation() -> None:
    buf = io.StringIO()
    emit_error(
        AppsecError(code=1, message="bad", remediation="fix it"),
        json_mode=False,
        stream=buf,
    )
    assert buf.getvalue() == "error: bad\nhint: fix it\n"


def test_emit_error_text_without_remediation() -> None:
    buf = io.StringIO()
    emit_error(AppsecError(code=1, message="bad"), json_mode=False, stream=buf)
    assert buf.getvalue() == "error: bad\n"


def test_emit_error_json() -> None:
    buf = io.StringIO()
    emit_error(
        AppsecError(code=2, message="bad", remediation="fix"),
        json_mode=True,
        stream=buf,
    )
    assert json.loads(buf.getvalue()) == {
        "code": 2,
        "message": "bad",
        "remediation": "fix",
    }


def test_emit_diagnostic_adds_newline() -> None:
    buf = io.StringIO()
    emit_diagnostic("working", stream=buf)
    assert buf.getvalue() == "working\n"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cli_output.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'appsec.cli._output'`.

- [ ] **Step 3: Write `appsec/cli/_output.py`**

```python
"""stdout / stderr helpers with a strict split.

Rule: **results go to stdout, diagnostics and errors go to stderr.** Agents
parsing appsec output can rely on this invariant. JSON mode routes structured
payloads to the same streams — it never mixes them.
"""

from __future__ import annotations

import json
import sys
from typing import Any, TextIO

from appsec.cli._errors import AppsecError


def emit_result(data: Any, *, json_mode: bool, stream: TextIO | None = None) -> None:
    """Write a command result to stdout (text or JSON), newline-terminated."""
    s = stream if stream is not None else sys.stdout
    if json_mode:
        json.dump(data, s, ensure_ascii=False)
        s.write("\n")
        return
    text = data if isinstance(data, str) else str(data)
    s.write(text)
    if not text.endswith("\n"):
        s.write("\n")


def emit_error(err: AppsecError, *, json_mode: bool, stream: TextIO | None = None) -> None:
    """Write an :class:`AppsecError` to stderr (text or JSON)."""
    s = stream if stream is not None else sys.stderr
    if json_mode:
        json.dump(err.to_dict(), s, ensure_ascii=False)
        s.write("\n")
        return
    s.write(f"error: {err.message}\n")
    if err.remediation:
        s.write(f"hint: {err.remediation}\n")


def emit_diagnostic(message: str, *, stream: TextIO | None = None) -> None:
    """Write a human diagnostic (progress, summary) to stderr."""
    s = stream if stream is not None else sys.stderr
    s.write(message if message.endswith("\n") else message + "\n")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_cli_output.py -v`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git add appsec/cli/_output.py tests/test_cli_output.py
git commit -m "Add stdout/stderr output helpers"
```

---

## Task 4: CLI chassis + `python -m appsec`

**Files:**
- Modify: `appsec/cli/__init__.py` (replace the empty file with the chassis)
- Create: `appsec/cli/_commands/__init__.py` (empty)
- Create: `appsec/__main__.py`
- Test: `tests/test_cli_chassis.py`

- [ ] **Step 1: Create empty `appsec/cli/_commands/__init__.py`**

Create `appsec/cli/_commands/__init__.py` with no content (package marker).

- [ ] **Step 2: Write the failing test `tests/test_cli_chassis.py`**

```python
"""Tests for the appsec CLI chassis (verbs are registered in later tasks)."""

from __future__ import annotations

import subprocess
import sys

import pytest

from appsec import __version__
from appsec.cli import main


def test_version_flag_exits_zero_and_prints_version(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_no_args_prints_help_and_returns_zero(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main([])
    assert rc == 0
    assert "usage: appsec" in capsys.readouterr().out


def test_unknown_verb_routes_through_structured_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["definitely-not-a-verb"])
    assert exc.value.code == 1
    assert "error:" in capsys.readouterr().err


def test_python_dash_m_invocation() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "appsec", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert __version__ in result.stdout
```

- [ ] **Step 3: Run test to verify it fails**

Run: `uv run pytest tests/test_cli_chassis.py -v`
Expected: FAIL with `ImportError: cannot import name 'main' from 'appsec.cli'` (the file is currently empty).

- [ ] **Step 4: Write `appsec/cli/__init__.py` (replacing the empty file)**

```python
"""Unified CLI entry point for appsec.

Error-propagation contract: every handler raises
:class:`appsec.cli._errors.AppsecError` on failure; ``main()`` catches it via
:func:`_dispatch` and routes through :mod:`appsec.cli._output`. Unknown
exceptions are wrapped into an ``AppsecError`` so no Python traceback leaks.

Argparse errors (unknown verb, missing required arg) also route through the
structured format — :class:`_AppsecArgumentParser` overrides ``.error()``.
Whether errors render as text or JSON depends on whether ``--json`` appears in
the raw argv (:func:`main` sets ``_AppsecArgumentParser._json_hint`` before
``parse_args``).
"""

from __future__ import annotations

import argparse
import sys

from appsec import __version__
from appsec.cli._errors import EXIT_USER_ERROR, AppsecError
from appsec.cli._output import emit_error


class _AppsecArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that routes errors through :func:`emit_error`."""

    _json_hint: bool = False

    def error(self, message: str) -> None:  # type: ignore[override]
        err = AppsecError(
            code=EXIT_USER_ERROR,
            message=message,
            remediation=f"run '{self.prog} --help' to see valid arguments",
        )
        emit_error(err, json_mode=type(self)._json_hint)
        raise SystemExit(err.code)


def _argv_has_json(argv: list[str] | None) -> bool:
    tokens = argv if argv is not None else sys.argv[1:]
    return any(t == "--json" or t.startswith("--json=") for t in tokens)


def _build_parser() -> argparse.ArgumentParser:
    parser = _AppsecArgumentParser(
        prog="appsec",
        description="appsec — an application-security agent (greenfield).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    sub = parser.add_subparsers(dest="command", parser_class=_AppsecArgumentParser)

    # Verb registrations land here as each verb module is added (Tasks 5-7).

    return parser


def _dispatch(args: argparse.Namespace) -> int:
    """Invoke the registered handler and translate exceptions to exit codes.

    A handler may return ``None`` (treated as success, exit 0) or an ``int``
    used directly as the exit code. Failures MUST raise :class:`AppsecError`;
    any other exception is wrapped so no Python traceback leaks.
    """
    json_mode = bool(getattr(args, "json", False))
    try:
        rc = args.func(args)
    except AppsecError as err:
        emit_error(err, json_mode=json_mode)
        return err.code
    except Exception as err:  # noqa: BLE001 - last-resort; wrap and route cleanly
        wrapped = AppsecError(
            code=EXIT_USER_ERROR,
            message=f"unexpected: {err.__class__.__name__}: {err}",
            remediation="file a bug at https://github.com/agentculture/appsec/issues",
        )
        emit_error(wrapped, json_mode=json_mode)
        return wrapped.code
    return rc if rc is not None else 0


def main(argv: list[str] | None = None) -> int:
    _AppsecArgumentParser._json_hint = _argv_has_json(argv)
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    return _dispatch(args)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Write `appsec/__main__.py`**

```python
"""Allow running appsec as ``python -m appsec``."""

import sys

from appsec.cli import main

if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 6: Run test to verify it passes**

Run: `uv run pytest tests/test_cli_chassis.py -v`
Expected: PASS (4 tests).

- [ ] **Step 7: Commit**

```bash
git add appsec/cli/__init__.py appsec/cli/_commands/__init__.py appsec/__main__.py tests/test_cli_chassis.py
git commit -m "Add CLI chassis with structured error routing and python -m entry"
```

---

## Task 5: `learn` placeholder verb

**Files:**
- Create: `appsec/cli/_commands/learn.py`
- Modify: `appsec/cli/__init__.py` (register the verb in `_build_parser`)
- Test: `tests/test_cli_stubs.py`

- [ ] **Step 1: Write the failing test `tests/test_cli_stubs.py`**

```python
"""Tests for the placeholder CLI verbs (learn / explain / whoami).

appsec is greenfield — these verbs are honest stubs. The tests pin the
contract: each verb exits 0, prints a 'not yet implemented' signal, and
honours --json with a structured payload.
"""

from __future__ import annotations

import json

import pytest

from appsec.cli import main


def test_learn_exits_zero_and_signals_greenfield(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main(["learn"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "appsec" in out
    assert "not yet implemented" in out.lower()


def test_learn_json(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["learn", "--json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["tool"] == "appsec"
    assert payload["status"] == "greenfield"
    assert payload["verb"] == "learn"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cli_stubs.py -v`
Expected: FAIL — `main(["learn"])` triggers the chassis "invalid choice" error (exit 2 / SystemExit) because no `learn` verb is registered yet.

- [ ] **Step 3: Write `appsec/cli/_commands/learn.py`**

```python
"""``appsec learn`` — placeholder verb.

appsec is a greenfield AgentCulture sibling: the scaffold (package, CLI
chassis, CI, vendored skills) is in place but the application-security agent
itself is not implemented yet. This verb prints an honest status line so a
probing agent or human gets a clear signal rather than a misleading response.
"""

from __future__ import annotations

import argparse

from appsec import __version__
from appsec.cli._output import emit_result

_TEXT = (
    "appsec — application-security agent. Not yet implemented; appsec is a "
    "greenfield AgentCulture sibling. See CLAUDE.md."
)


def _json_payload() -> dict[str, object]:
    return {
        "tool": "appsec",
        "version": __version__,
        "status": "greenfield",
        "verb": "learn",
        "message": _TEXT,
    }


def cmd_learn(args: argparse.Namespace) -> int:
    json_mode = bool(getattr(args, "json", False))
    if json_mode:
        emit_result(_json_payload(), json_mode=True)
    else:
        emit_result(_TEXT, json_mode=False)
    return 0


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("learn", help="Print appsec's self-teaching status line.")
    p.add_argument("--json", action="store_true", help="Emit structured JSON.")
    p.set_defaults(func=cmd_learn)
```

- [ ] **Step 4: Register the verb in `appsec/cli/__init__.py`**

In `_build_parser`, replace the line:

```python
    # Verb registrations land here as each verb module is added (Tasks 5-7).
```

with:

```python
    from appsec.cli._commands import learn as _learn_cmd

    _learn_cmd.register(sub)

    # Verb registrations land here as each verb module is added (Tasks 5-7).
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/test_cli_stubs.py -v`
Expected: PASS (2 tests).

- [ ] **Step 6: Commit**

```bash
git add appsec/cli/_commands/learn.py appsec/cli/__init__.py tests/test_cli_stubs.py
git commit -m "Add learn placeholder verb"
```

---

## Task 6: `explain` placeholder verb

**Files:**
- Create: `appsec/cli/_commands/explain.py`
- Modify: `appsec/cli/__init__.py` (register the verb)
- Modify: `tests/test_cli_stubs.py` (append tests)

- [ ] **Step 1: Append the failing tests to `tests/test_cli_stubs.py`**

Add these two functions at the end of `tests/test_cli_stubs.py`:

```python
def test_explain_exits_zero_and_signals_greenfield(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main(["explain"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "not yet implemented" in out.lower()


def test_explain_json(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["explain", "--json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["verb"] == "explain"
    assert payload["status"] == "greenfield"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cli_stubs.py -k explain -v`
Expected: FAIL — `explain` verb is not registered yet.

- [ ] **Step 3: Write `appsec/cli/_commands/explain.py`**

```python
"""``appsec explain`` — placeholder verb.

See :mod:`appsec.cli._commands.learn` for why the verbs are stubs. ``explain``
will eventually print docs for a given topic / command path; today it prints
an honest "not yet implemented" line.
"""

from __future__ import annotations

import argparse

from appsec import __version__
from appsec.cli._output import emit_result

_TEXT = "appsec explain — not yet implemented; appsec is greenfield. See CLAUDE.md."


def _json_payload() -> dict[str, object]:
    return {
        "tool": "appsec",
        "version": __version__,
        "status": "greenfield",
        "verb": "explain",
        "message": _TEXT,
    }


def cmd_explain(args: argparse.Namespace) -> int:
    json_mode = bool(getattr(args, "json", False))
    if json_mode:
        emit_result(_json_payload(), json_mode=True)
    else:
        emit_result(_TEXT, json_mode=False)
    return 0


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("explain", help="Explain an appsec topic or command (stub).")
    p.add_argument("--json", action="store_true", help="Emit structured JSON.")
    p.set_defaults(func=cmd_explain)
```

- [ ] **Step 4: Register the verb in `appsec/cli/__init__.py`**

In `_build_parser`, the block currently reads:

```python
    from appsec.cli._commands import learn as _learn_cmd

    _learn_cmd.register(sub)

    # Verb registrations land here as each verb module is added (Tasks 5-7).
```

Replace it with:

```python
    from appsec.cli._commands import explain as _explain_cmd
    from appsec.cli._commands import learn as _learn_cmd

    _learn_cmd.register(sub)
    _explain_cmd.register(sub)

    # Verb registrations land here as each verb module is added (Tasks 5-7).
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/test_cli_stubs.py -v`
Expected: PASS (4 tests).

- [ ] **Step 6: Commit**

```bash
git add appsec/cli/_commands/explain.py appsec/cli/__init__.py tests/test_cli_stubs.py
git commit -m "Add explain placeholder verb"
```

---

## Task 7: `whoami` placeholder verb

**Files:**
- Create: `appsec/cli/_commands/whoami.py`
- Modify: `appsec/cli/__init__.py` (register the verb)
- Modify: `tests/test_cli_stubs.py` (append tests)

- [ ] **Step 1: Append the failing tests to `tests/test_cli_stubs.py`**

Add these two functions at the end of `tests/test_cli_stubs.py`:

```python
def test_whoami_exits_zero_and_signals_greenfield(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = main(["whoami"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "not yet implemented" in out.lower()


def test_whoami_json(capsys: pytest.CaptureFixture[str]) -> None:
    rc = main(["whoami", "--json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["verb"] == "whoami"
    assert payload["status"] == "greenfield"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cli_stubs.py -k whoami -v`
Expected: FAIL — `whoami` verb is not registered yet.

- [ ] **Step 3: Write `appsec/cli/_commands/whoami.py`**

```python
"""``appsec whoami`` — placeholder verb.

See :mod:`appsec.cli._commands.learn` for why the verbs are stubs. ``whoami``
will eventually be the smallest identity / auth probe; today it prints an
honest "not yet implemented" line.
"""

from __future__ import annotations

import argparse

from appsec import __version__
from appsec.cli._output import emit_result

_TEXT = "appsec — not yet implemented; appsec is greenfield. See CLAUDE.md."


def _json_payload() -> dict[str, object]:
    return {
        "tool": "appsec",
        "version": __version__,
        "status": "greenfield",
        "verb": "whoami",
        "message": _TEXT,
    }


def cmd_whoami(args: argparse.Namespace) -> int:
    json_mode = bool(getattr(args, "json", False))
    if json_mode:
        emit_result(_json_payload(), json_mode=True)
    else:
        emit_result(_TEXT, json_mode=False)
    return 0


def register(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("whoami", help="Print appsec's identity probe (stub).")
    p.add_argument("--json", action="store_true", help="Emit structured JSON.")
    p.set_defaults(func=cmd_whoami)
```

- [ ] **Step 4: Register the verb in `appsec/cli/__init__.py`**

In `_build_parser`, the block currently reads:

```python
    from appsec.cli._commands import explain as _explain_cmd
    from appsec.cli._commands import learn as _learn_cmd

    _learn_cmd.register(sub)
    _explain_cmd.register(sub)

    # Verb registrations land here as each verb module is added (Tasks 5-7).
```

Replace it with:

```python
    from appsec.cli._commands import explain as _explain_cmd
    from appsec.cli._commands import learn as _learn_cmd
    from appsec.cli._commands import whoami as _whoami_cmd

    _learn_cmd.register(sub)
    _explain_cmd.register(sub)
    _whoami_cmd.register(sub)
```

- [ ] **Step 5: Run the full test suite with coverage**

Run: `uv run pytest -n auto --cov=appsec --cov-report=term -v`
Expected: PASS (all tests across 5 test files); coverage well above the `fail_under = 70` threshold.

- [ ] **Step 6: Commit**

```bash
git add appsec/cli/_commands/whoami.py appsec/cli/__init__.py tests/test_cli_stubs.py
git commit -m "Add whoami placeholder verb"
```

---

## Task 8: Config & lint files

**Files:**
- Create: `culture.yaml`
- Create: `CHANGELOG.md`
- Create: `.flake8`
- Create: `.markdownlint-cli2.yaml`
- Create: `.pre-commit-config.yaml`
- Create: `sonar-project.properties`
- Modify: `.gitignore` (append the skills.local carve-out)

- [ ] **Step 1: Write `culture.yaml`**

```yaml
agents:
- suffix: appsec
  backend: claude
```

- [ ] **Step 2: Write `CHANGELOG.md`**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/). This project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-14

### Added

- AgentCulture sibling scaffold: the `appsec-cli` package (hatchling,
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
```

- [ ] **Step 3: Write `.flake8`**

```ini
[flake8]
max-line-length = 100
extend-select = B
extend-ignore =
    # whitespace before ':' — conflicts with black
    E203,
    # line break before binary operator — conflicts with black
    W503
exclude =
    .venv,
    .git,
    __pycache__,
    dist,
    build
per-file-ignores =
    # Bandit S-rules are noisy in tests (assert, subprocess, etc.) — mute them.
    tests/*:S101,S404,S603
```

- [ ] **Step 4: Write `.markdownlint-cli2.yaml`**

```yaml
# markdownlint-cli2 config for appsec.
# markdownlint-cli2 stops walking at the git root, so a global
# markdownlint config in the user's home directory isn't picked up from
# inside the repo. Keep this file aligned with the global preset.

config:
  default: true
  # MD013: Line length — disabled. Prose lines wrap at the reader.
  MD013: false
  # MD060: Table pipe spacing — disabled (stylistic preference).
  MD060: false
  # MD024: Duplicate headings — allow under different parents so Keep a
  # Changelog entries can each have ### Added / ### Changed / ### Fixed.
  MD024:
    siblings_only: true

ignores:
  - "node_modules/**"
  - ".local/**"
  - ".venv/**"
  - ".claude/skills/**"
```

> Note: `.claude/skills/**` is ignored because the vendored SKILL.md files are cited verbatim from steward and are not first-party content to lint.

- [ ] **Step 5: Write `.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-ast
      - id: detect-private-key

  - repo: local
    hooks:
      - id: markdownlint-cli2
        name: markdownlint-cli2 (check)
        description: Lint markdown (no auto-fix).
        entry: markdownlint-cli2
        language: system
        types: [markdown]

      - id: flake8
        name: flake8
        entry: uv run flake8 --config=.flake8
        language: system
        types: [python]

      - id: isort
        name: isort
        entry: uv run isort
        language: system
        types: [python]

      - id: black
        name: black
        entry: uv run black
        language: system
        types: [python]
```

- [ ] **Step 6: Write `sonar-project.properties`**

```properties
# SonarCloud project identity. The project must be registered on
# sonarcloud.io under the agentculture organization, and the SonarCloud
# GitHub App installed on this repo, before the scan produces a quality gate.
sonar.projectKey=agentculture_appsec
sonar.organization=agentculture

# Source layout — package lives at the top level (no src/ wrapper).
sonar.sources=appsec
sonar.tests=tests

# Coverage report produced in CI by `uv run pytest --cov-report=xml:coverage.xml`.
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.version=3.12

sonar.exclusions=**/__pycache__/**,**/.venv/**,uv.lock
```

- [ ] **Step 7: Append the skills.local carve-out to `.gitignore`**

Append these lines to the end of `.gitignore`:

```gitignore

# AgentCulture per-machine skill config (the .example is committed)
.claude/skills.local.yaml
```

- [ ] **Step 8: Verify lint configs work**

Run: `uv run flake8 --config=.flake8 appsec/ tests/`
Expected: no output, exit 0.

Run: `uv run black --check appsec/ tests/ && uv run isort --check-only appsec/ tests/`
Expected: both report no changes needed (exit 0). If `black` or `isort` report changes, run them without `--check` / `--check-only`, re-run the full test suite (`uv run pytest -n auto`), and confirm green.

- [ ] **Step 9: Commit**

```bash
git add culture.yaml CHANGELOG.md .flake8 .markdownlint-cli2.yaml .pre-commit-config.yaml sonar-project.properties .gitignore
git commit -m "Add culture.yaml, CHANGELOG, lint configs and SonarCloud properties"
```

---

## Task 9: CI workflows

**Files:**
- Create: `.github/workflows/tests.yml`
- Create: `.github/workflows/security-checks.yml`
- Create: `.github/workflows/publish.yml`

- [ ] **Step 1: Write `.github/workflows/tests.yml`**

```yaml
name: Tests

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    # Promote a presence flag (not the secret) to job env so the SonarCloud
    # step can gate on it — secrets.* isn't allowed in `if:`.
    env:
      SONAR_TOKEN_PRESENT: ${{ secrets.SONAR_TOKEN != '' }}
    steps:
      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
        with:
          # Sonar needs full git history for accurate "new code" blame attribution.
          fetch-depth: 0

      - uses: astral-sh/setup-uv@38f3f104447c67c051c4a08e39b64a148898af3a # v4

      - run: uv python install 3.12

      - run: uv sync

      - run: uv run flake8 --config=.flake8 appsec/ tests/

      - run: uv run pytest -n auto --cov=appsec --cov-report=xml:coverage.xml --cov-report=term -v

      - name: SonarCloud Scan
        if: env.SONAR_TOKEN_PRESENT == 'true'
        uses: SonarSource/sonarqube-scan-action@fd88b7d7ccbaefd23d8f36f73b59db7a3d246602 # v6
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: https://sonarcloud.io

  version-check:
    # Only run on PR events. On push to main the comparison would always
    # fail (PR_VERSION == MAIN_VERSION) and there is no PR number.
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4
        with:
          fetch-depth: 0

      - run: git fetch origin main

      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5
        with:
          python-version: "3.12"

      - name: Check version bump
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          # AgentCulture rule: every PR bumps the version — even docs/config/CI.
          PR_VERSION=$(python3 -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")
          MAIN_VERSION=$(git show origin/main:pyproject.toml 2>/dev/null | python3 -c "import sys,tomllib; print(tomllib.loads(sys.stdin.read())['project']['version'])" 2>/dev/null || echo "")

          if [ -z "$MAIN_VERSION" ]; then
            echo "No pyproject.toml on main yet — skipping version check (initial scaffold)."
            exit 0
          fi

          if [ "$PR_VERSION" = "$MAIN_VERSION" ]; then
            MARKER="<!-- version-check -->"
            BODY="⚠️ **Version not bumped** — \`pyproject.toml\` still has \`$PR_VERSION\` (same as main). Bump before merging to avoid a failed PyPI publish.

          $MARKER"

            EXISTING=$(gh api repos/${{ github.repository }}/issues/${{ github.event.pull_request.number }}/comments \
              --jq '.[] | select(.body | contains("<!-- version-check -->")) | .id' | head -1)

            if [ -n "$EXISTING" ]; then
              gh api repos/${{ github.repository }}/issues/comments/$EXISTING \
                -X PATCH -f body="$BODY" > /dev/null
            else
              gh pr comment ${{ github.event.pull_request.number }} --body "$BODY" || true
            fi

            echo "::error::Version $PR_VERSION matches main. Bump before merging."
            exit 1
          else
            echo "Version bumped: $MAIN_VERSION -> $PR_VERSION"
          fi
```

- [ ] **Step 2: Write `.github/workflows/security-checks.yml`**

```yaml
name: Security Checks

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday at midnight
  workflow_dispatch:

jobs:
  security-scans:
    name: Security Scans
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4

      - uses: astral-sh/setup-uv@38f3f104447c67c051c4a08e39b64a148898af3a # v4

      - run: uv python install 3.12

      - run: uv sync

      - name: Run Bandit
        run: uv run bandit -r appsec/ -f json -o bandit-results.json -c pyproject.toml
        continue-on-error: true

      - name: Run Pylint
        run: uv run pylint appsec/ --output-format=json:pylint-results.json,text
        continue-on-error: true

      - name: Upload Security Results
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4
        with:
          name: security-results
          path: |
            bandit-results.json
            pylint-results.json
```

- [ ] **Step 3: Write `.github/workflows/publish.yml`**

```yaml
name: Publish to PyPI

on:
  push:
    branches: [main]
    paths:
      - "pyproject.toml"
      - "appsec/**"
  pull_request:
    branches: [main]
    paths:
      - "pyproject.toml"
      - "appsec/**"

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4

      - uses: astral-sh/setup-uv@38f3f104447c67c051c4a08e39b64a148898af3a # v4

      - run: uv python install 3.12

      - run: uv sync

      - run: uv run pytest -n auto -v

  test-publish:
    # Skip on fork PRs — no OIDC/environment context is available there.
    if: github.event_name == 'pull_request' && github.event.pull_request.head.repo.full_name == github.repository
    needs: test
    runs-on: ubuntu-latest
    environment: testpypi
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4

      - uses: astral-sh/setup-uv@38f3f104447c67c051c4a08e39b64a148898af3a # v4

      - run: uv python install 3.12

      - run: uv sync

      - name: Set dev version
        run: |
          BASE=$(uv run python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")
          DEV_VERSION="${BASE}.dev${{ github.run_number }}"
          sed -i "s/^version = .*/version = \"${DEV_VERSION}\"/" pyproject.toml
          echo "DEV_VERSION=${DEV_VERSION}" >> "$GITHUB_ENV"
          echo "Publishing ${DEV_VERSION} to TestPyPI"

      - name: Build and publish to TestPyPI
        run: |
          uv build
          uv publish --publish-url https://test.pypi.org/legacy/ --trusted-publishing always --check-url https://test.pypi.org/simple/

      - name: Print install commands
        if: always()
        run: |
          echo "::notice::Test with: uv tool install --index-url https://test.pypi.org/simple/ --index-strategy unsafe-best-match appsec-cli==${DEV_VERSION}"

  publish:
    if: github.event_name == 'push'
    needs: test
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4

      - uses: astral-sh/setup-uv@38f3f104447c67c051c4a08e39b64a148898af3a # v4

      - run: uv python install 3.12

      - run: uv sync

      - name: Build and publish to PyPI
        run: |
          uv build
          uv publish --trusted-publishing always --check-url https://pypi.org/simple/
```

- [ ] **Step 4: Sanity-check the YAML parses**

Run: `uv run python -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('.github/workflows/*.yml')]; print('workflows parse OK')"`
Expected: `workflows parse OK`.

> Note: `publish.yml` will run **red** in CI until PyPI Trusted Publishing is configured (a manual maintainer step). This is expected and is recorded in the gaps tracking issue (Task 13).

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/tests.yml .github/workflows/security-checks.yml .github/workflows/publish.yml
git commit -m "Add CI workflows: tests, security-checks, publish"
```

---

## Task 10: Vendor the five skills + per-machine config template

**Files:**
- Create: `.claude/skills/cicd/` (copied from `../steward`)
- Create: `.claude/skills/communicate/` (copied from `../steward`)
- Create: `.claude/skills/run-tests/` (copied from `../steward`)
- Create: `.claude/skills/sonarclaude/` (copied from `../steward`)
- Create: `.claude/skills/version-bump/` (copied from `../steward`)
- Create: `.claude/skills.local.yaml.example`
- Modify: `.claude/skills/cicd/SKILL.md` (frontmatter description only)
- Modify: `.claude/skills/communicate/SKILL.md` (frontmatter description only)

- [ ] **Step 1: Copy the five skill directories from the local steward checkout**

Run:

```bash
mkdir -p .claude/skills
for s in cicd communicate run-tests sonarclaude version-bump; do
  rm -rf ".claude/skills/$s"
  cp -R "../steward/.claude/skills/$s" .claude/skills/
done
# Drop any compiled-bytecode dirs that cp -R may have carried over.
find .claude/skills -type d -name '__pycache__' -exec rm -rf {} +
# Ensure scripts are executable.
find .claude/skills -type f -name '*.sh' -exec chmod +x {} +
chmod +x .claude/skills/version-bump/scripts/bump.py
```

- [ ] **Step 2: Verify the expected files landed**

Run:

```bash
find .claude/skills -type f | sort
```

Expected (exactly these files — no `__pycache__`, no extras):

```
.claude/skills/cicd/SKILL.md
.claude/skills/cicd/scripts/_resolve-nick.sh
.claude/skills/cicd/scripts/portability-lint.sh
.claude/skills/cicd/scripts/pr-reply.sh
.claude/skills/cicd/scripts/pr-status.sh
.claude/skills/cicd/scripts/workflow.sh
.claude/skills/communicate/SKILL.md
.claude/skills/communicate/scripts/fetch-issues.sh
.claude/skills/communicate/scripts/mesh-message.sh
.claude/skills/communicate/scripts/post-comment.sh
.claude/skills/communicate/scripts/post-issue.sh
.claude/skills/communicate/scripts/templates/skill-update-brief.md
.claude/skills/run-tests/SKILL.md
.claude/skills/run-tests/scripts/test.sh
.claude/skills/sonarclaude/SKILL.md
.claude/skills/sonarclaude/scripts/sonar.sh
.claude/skills/version-bump/SKILL.md
.claude/skills/version-bump/scripts/bump.py
```

If `find` shows extra or missing files, re-run Step 1.

- [ ] **Step 3: Verify each SKILL.md frontmatter `name` matches its directory**

Run:

```bash
for s in cicd communicate run-tests sonarclaude version-bump; do
  echo -n "$s: "; grep -m1 '^name:' ".claude/skills/$s/SKILL.md"
done
```

Expected: each line reads `<dir>: name: <dir>` (e.g. `cicd: name: cicd`). The `skills-convention` invariant requires this; the copied files already satisfy it — this step is a confirmation, not an edit.

- [ ] **Step 4: Adapt the `cicd/SKILL.md` frontmatter description**

Edit `.claude/skills/cicd/SKILL.md`. In the YAML frontmatter `description:` block, make exactly these substitutions (consumer-naming → `appsec`; upstream-history / provenance references → left unchanged):

- `Steward's CI/CD lane, layered on` → `appsec's CI/CD lane, layered on`
- `Use when: creating PRs in steward, handling` → `Use when: creating PRs in appsec, handling`

Then append this sentence to the end of the `description:` block text (before the closing of the frontmatter):

```
Vendored from steward; see docs/skill-sources.md for divergence notes.
```

Do **not** change `adds two steward extensions` or `Renamed from \`pr-review\` in steward 0.7.0; rebased on agex in 0.12.0.` — those cite steward as the upstream/author, not appsec as the consumer. Do **not** edit the SKILL.md body — it is the upstream skill cited verbatim; divergence is recorded in `docs/skill-sources.md` (Task 11).

- [ ] **Step 5: Adapt the `communicate/SKILL.md` frontmatter description**

Edit `.claude/skills/communicate/SKILL.md`. In the YAML frontmatter `description:` block, make exactly these substitutions:

- `Cross-repo + mesh communication from steward:` → `Cross-repo + mesh communication from appsec:`
- `the next step lives outside steward (a brief` → `the next step lives outside appsec (a brief`
- `Issue posts auto-sign with \`- steward (Claude)\`; mesh` → `Issue posts auto-sign with \`- appsec (Claude)\`; mesh`
- `Not for in-steward` → `Not for in-appsec`

Then append this sentence to the end of the `description:` block text:

```
Vendored from steward; see docs/skill-sources.md for divergence notes.
```

Do **not** change `Renamed from \`coordinate\` in steward 0.8.0; absorbed \`gh-issues\` in 0.9.1.` — that is upstream history. Do **not** edit the SKILL.md body.

> `run-tests`, `sonarclaude`, and `version-bump` SKILL.md frontmatter descriptions contain no consumer-naming references to "steward" — leave those three files verbatim.

- [ ] **Step 6: Write `.claude/skills.local.yaml.example`**

```yaml
# Per-machine config for appsec's vendored skills.
#
# Skills read .claude/skills.local.yaml (git-ignored) and fall back to this
# committed .example. Copy this file to .claude/skills.local.yaml and fill in
# real values for the local machine. No absolute user-home paths in the tracked
# .example — keep those in the git-ignored copy only.

# Path to the local Culture server manifest, used by skills that resolve
# Culture agent suffixes or mesh channels. Leave empty if appsec is not yet
# a registered mesh agent.
culture_server_yaml: ""

# Map of sibling-project names to their local checkout paths. Used by
# cross-repo skills (e.g. communicate, cicd delta) to locate siblings
# without hard-coded absolute paths. Relative paths are resolved from the
# repo root.
sibling_projects: {}
  # steward: ../steward
  # afi-cli: ../afi-cli
```

- [ ] **Step 7: Confirm portability of the vendored tree**

Run: `bash .claude/skills/cicd/scripts/portability-lint.sh`
Expected: exit 0 with no absolute user-home paths or per-user-dotfile findings. If it reports findings inside the freshly vendored files, stop and investigate — the upstream copy should already be clean; a finding likely means a stale copy. Re-run Step 1.

- [ ] **Step 8: Commit**

```bash
git add .claude/skills .claude/skills.local.yaml.example
git commit -m "Vendor cicd, communicate, run-tests, sonarclaude, version-bump skills from steward"
```

---

## Task 11: Skill provenance ledger

**Files:**
- Create: `docs/skill-sources.md`

- [ ] **Step 1: Write `docs/skill-sources.md`**

```markdown
# Skill sources — vendored skill provenance

appsec vendors cross-sibling skills from `steward`, the AgentCulture skill
supplier. This follows the **cite, don't import** pattern: each skill is
copied into `.claude/skills/`, owned locally, and may diverge. Nothing
imports across repos at runtime.

This file is the upstream/downstream map. When upstream changes, re-sync
explicitly — these copies do not auto-update.

| Skill | Upstream | Vendored | Divergence |
|-------|----------|----------|------------|
| `cicd` | `steward` (`../steward/.claude/skills/cicd/`) | 2026-05-14 | Identifier-only: SKILL.md frontmatter `description` reframed for appsec. Body prose still references steward-specific constructs (e.g. `steward doctor`, the `STEWARD_PR_AWAIT_WAIT` env var, the steward `status` / `await` gating extensions) — appsec is a skill *consumer*, so these are inherited context, not appsec-actionable calls. |
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
```

- [ ] **Step 2: Commit**

```bash
git add docs/skill-sources.md
git commit -m "Add skill-sources.md provenance ledger"
```

---

## Task 12: Refresh CLAUDE.md

**Files:**
- Modify: `CLAUDE.md` (replace the greenfield placeholder content)

- [ ] **Step 1: Replace the entire contents of `CLAUDE.md`**

Overwrite `CLAUDE.md` with:

````markdown
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

`.claude/skills/` holds skills vendored from `steward` (cite, don't import).
Provenance and divergence are tracked in `docs/skill-sources.md`. Re-sync
from `../steward/.claude/skills/<name>/`.

## Workspace Context

The GitHub remote is `agentculture/appsec`. When opening PRs or posting comments here as an AI assistant, sign them so it's clear they're AI-authored — e.g. `- appsec (Claude)`.
````

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "Refresh CLAUDE.md with real build/run/test commands and architecture"
```

---

## Task 13: Final verification, gaps issue, and PR

**Files:** none created — verification, issue creation, and PR creation.

- [ ] **Step 1: Run the full verification sweep**

Run each command; all must pass before continuing:

```bash
uv sync
uv run pytest -n auto --cov=appsec --cov-report=term -v        # all tests pass, coverage >= 70%
uv run flake8 --config=.flake8 appsec/ tests/                  # no output
uv run black --check appsec/ tests/                            # no changes needed
uv run isort --check-only appsec/ tests/                       # no changes needed
uv run appsec --version                                        # prints "appsec 0.1.0"
uv run appsec learn && uv run appsec explain && uv run appsec whoami   # each exits 0
bash .claude/skills/cicd/scripts/portability-lint.sh           # exit 0, no findings
```

If any command fails, fix the cause, commit the fix with a clear message, and re-run the sweep.

- [ ] **Step 2: Run `steward doctor` against the repo**

Run:

```bash
APPSEC_DIR="$(pwd)"
(cd ../steward && uv run steward doctor "$APPSEC_DIR")
```

Expected: zero `portability` and zero `skills-convention` violations. If `steward doctor` reports violations, fix them in this repo, commit the fix, and re-run. (If the `steward` command is unavailable, note it and rely on Step 1's `portability-lint.sh` plus the Step 3 skill-name check as the substitute verification.)

- [ ] **Step 3: Confirm the skills-convention invariant by hand**

Run:

```bash
for s in cicd communicate run-tests sonarclaude version-bump; do
  test -f ".claude/skills/$s/SKILL.md" && test -d ".claude/skills/$s/scripts" \
    && grep -q "^name: $s$" ".claude/skills/$s/SKILL.md" \
    && echo "$s OK" || echo "$s FAIL"
done
```

Expected: five `OK` lines. Any `FAIL` must be fixed (and committed) before continuing.

- [ ] **Step 4: Write the gaps-issue body to a temp file**

Write the following to `/tmp/appsec-gaps-issue.md`:

```markdown
## Onboarding: known gaps and deferred work

The onboarding scaffold PR (closes #2–#7) makes `appsec` a healthy
AgentCulture sibling, but several items are deliberately deferred. This
issue is the single reference point — link future content work here.

### 1. PyPI Trusted Publishing not configured

`.github/workflows/publish.yml` is committed but runs **red** until a
maintainer:

- registers the `appsec-cli` project on PyPI and TestPyPI,
- configures the OIDC Trusted Publisher for `agentculture/appsec`,
- creates the `pypi` and `testpypi` GitHub environments.

Expected, not a regression — see the design spec.

### 2. SonarCloud project registration

Confirm the `agentculture_appsec` project exists on sonarcloud.io and the
SonarCloud GitHub App is installed on this repo. The CI scan step is gated
on `SONAR_TOKEN_PRESENT`, so CI does not break if the token/project is
absent — but the quality gate will not report until the project is
registered.

### 3. CLI verbs are placeholder stubs

`learn` / `explain` / `whoami` print honest "not yet implemented" lines.
Real implementations come when the `appsec` agent product is designed.

### 4. The `appsec` agent product is undefined

`README.md` says "An appsec agent"; the actual application-security
capability — what it analyzes, its real CLI surface, its architecture —
has not been designed.

### 5. Security-tooling layout diverges from issue #2's literal text

Issue #2 specifies "pytest + flake8 + bandit" in `tests.yml`. This
scaffold follows the `afi-cli` exemplar instead: `flake8` runs in
`tests.yml`, while `bandit` and `pylint` run in a separate
`security-checks.yml`. A deliberate divergence, recorded here.

- appsec (Claude)
```

- [ ] **Step 5: Create the gaps tracking issue**

Run:

```bash
gh issue create --repo agentculture/appsec \
  --title "Onboarding: known gaps and deferred work" \
  --body-file /tmp/appsec-gaps-issue.md
```

Capture the printed issue URL / number — call it `GAPS_ISSUE` (e.g. `#8`). It is used in the PR body in Step 7.

- [ ] **Step 6: Push the branch**

Run:

```bash
git push -u origin onboarding/sibling-scaffold
```

- [ ] **Step 7: Write the PR body and open the PR**

Write the following to `/tmp/appsec-pr-body.md` (replace `GAPS_ISSUE` with the actual issue number from Step 5):

```markdown
## Summary

Scaffolds `appsec` into a healthy AgentCulture sibling, mirroring the
`afi-cli` exemplar:

- `appsec-cli` package (hatchling, Python >=3.12, zero runtime deps) with a
  real CLI chassis — structured errors, strict stdout/stderr split, `--json`.
- Placeholder agent-first verbs `learn` / `explain` / `whoami` (honest
  "greenfield" stubs).
- CI: `tests.yml` (pytest + coverage + flake8 + SonarCloud + version-check),
  `security-checks.yml` (bandit + pylint), `publish.yml` (TestPyPI/PyPI via
  OIDC).
- `culture.yaml`, `CHANGELOG.md`, repo-local lint configs,
  `sonar-project.properties`, `.claude/skills.local.yaml.example`.
- Five skills vendored from `steward` — `cicd`, `communicate`, `run-tests`,
  `sonarclaude`, `version-bump` — with `docs/skill-sources.md` provenance.
- `CLAUDE.md` refreshed with real commands and architecture.

Closes #2, #3, #4, #5, #6, #7.

Known gaps and deferred work are tracked in GAPS_ISSUE — notably PyPI
Trusted Publishing is not yet configured, so `publish.yml` runs red until a
maintainer completes the one-time PyPI-side setup. This is expected.

## Test plan

- [ ] `uv run pytest -n auto` — full suite green, coverage >= 70%
- [ ] `uv run flake8 --config=.flake8 appsec/ tests/` — clean
- [ ] `uv run appsec --version` / `learn` / `explain` / `whoami` — each exits 0
- [ ] `bash .claude/skills/cicd/scripts/portability-lint.sh` — exit 0
- [ ] `steward doctor` — zero portability / skills-convention violations
- [ ] CI: `tests.yml` and `security-checks.yml` green; `publish.yml` red
      (expected — see GAPS_ISSUE)

- appsec (Claude)
```

Then run:

```bash
gh pr create --repo agentculture/appsec \
  --base main --head onboarding/sibling-scaffold \
  --title "Onboarding: AgentCulture sibling scaffold + 5 vendored skills" \
  --body-file /tmp/appsec-pr-body.md
```

- [ ] **Step 8: Report the PR URL**

Print the PR URL returned by `gh pr create` and the gaps issue URL from Step 5 so the user can review both.

---

## Self-review notes

- **Spec coverage:** Components 1–7 of the spec map to Tasks 1–12; the build sequence's "step 0 / gaps issue" and "open PR" map to Task 13. The `.claude/skills.local.yaml.example` path correction (under `.claude/`, not `.claude/skills/`) is reflected in Task 10.
- **First-PR version-check:** `tests.yml`'s `version-check` job auto-passes when `main` has no `pyproject.toml` — exactly this PR's situation.
- **Type/name consistency:** `AppsecError`, `_AppsecArgumentParser`, `emit_result` / `emit_error` / `emit_diagnostic`, `cmd_learn` / `cmd_explain` / `cmd_whoami`, and `register(sub)` are used consistently across Tasks 2–7. Each verb's `_json_payload()` returns `tool` / `version` / `status` / `verb` / `message`, matching the assertions in `tests/test_cli_stubs.py`.
- **Known not-green at merge:** `publish.yml` runs red until PyPI Trusted Publishing is configured — tracked in the gaps issue, called out in the PR body, not a blocker.
