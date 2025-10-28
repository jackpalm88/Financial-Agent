"""Public entry-point for the MT5 execution bridge."""

from __future__ import annotations

from typing import TYPE_CHECKING

__version__ = "2.0.0"

__all__ = [
    "MT5ExecutionBridge",
    "AsyncExecutionEngine",
    "MockAdapter",
    "RealMT5Adapter",
    "Signal",
    "OrderDirection",
    "ExecutionResult",
    "ExecutionStatus",
    "BaseExecutionAdapter",
    "ErrorCode",
    "OrderRequest",
    "OrderResult",
    "SymbolInfo",
    "AccountInfo",
    "PositionInfo",
    "__version__",
]

if TYPE_CHECKING:  # pragma: no cover - import heavy modules only for type checkers
    from .adapter_base import (
        AccountInfo,
        BaseExecutionAdapter,
        ErrorCode,
        OrderRequest,
        OrderResult,
        PositionInfo,
        SymbolInfo,
    )
    from .adapter_mock import MockAdapter
    from .adapter_mt5 import RealMT5Adapter
    from .bridge import (
        AsyncExecutionEngine,
        ExecutionResult,
        ExecutionStatus,
        MT5ExecutionBridge,
        OrderDirection,
        Signal,
    )


def __getattr__(name: str):
    """Lazily expose bridge symbols to avoid importing optional dependencies."""

    if name in {
        "MT5ExecutionBridge",
        "Signal",
        "OrderDirection",
        "ExecutionResult",
        "ExecutionStatus",
        "AsyncExecutionEngine",
    }:
        from . import bridge as _bridge

        return getattr(_bridge, name)

    if name in {
        "BaseExecutionAdapter",
        "ErrorCode",
        "OrderRequest",
        "OrderResult",
        "SymbolInfo",
        "AccountInfo",
        "PositionInfo",
    }:
        from . import adapter_base as _adapter_base

        return getattr(_adapter_base, name)

    if name == "MockAdapter":
        from .adapter_mock import MockAdapter

        return MockAdapter

    if name == "RealMT5Adapter":
        try:
            from .adapter_mt5 import RealMT5Adapter
        except ImportError as exc:  # pragma: no cover - depends on optional package
            raise AttributeError(name) from exc

        return RealMT5Adapter

    if name == "__version__":
        return __version__

    raise AttributeError(name)


def __dir__() -> list[str]:
    return sorted(__all__)
