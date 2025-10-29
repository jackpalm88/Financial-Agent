"""Test configuration helpers for src-layout imports."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent / "src"
if _ROOT.exists():
    sys.path.insert(0, str(_ROOT))


def pytest_ignore_collect(collection_path: Path, config):
    """Skip TA-heavy tests unless extras are installed."""
    path_str = str(collection_path)
    if "technical_analysis" in path_str:
        try:
            import pandas_ta  # type: ignore # noqa: F401
        except ModuleNotFoundError:
            return True
    return False
