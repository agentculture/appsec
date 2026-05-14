"""Package-level smoke test."""

from __future__ import annotations

import appsec


def test_version_is_a_nonempty_string() -> None:
    assert isinstance(appsec.__version__, str)
    assert appsec.__version__
