"""Allow running appsec as ``python -m appsec``."""

import sys

from appsec.cli import main

if __name__ == "__main__":
    sys.exit(main())
