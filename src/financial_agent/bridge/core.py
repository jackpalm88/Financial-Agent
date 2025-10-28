"""Compatibility layer for legacy imports.

The bridge module originally exposed its public API through a top-level
``core`` module.  Several examples and tests in this repository still rely on
``from core import ...``.  To maintain backwards compatibility and to ensure
those imports keep working, we re-export the bridge package's public
interfaces from this module.
"""

try:  # pragma: no cover - exercised when imported as package module
    from . import (
        MT5ExecutionBridge,
        AsyncExecutionEngine,
        MockAdapter,
        RealMT5Adapter,
        Signal,
        OrderDirection,
        ExecutionResult,
        ExecutionStatus,
        BaseExecutionAdapter,
        ErrorCode,
        OrderRequest,
        OrderResult,
        SymbolInfo,
        AccountInfo,
        PositionInfo,
    )
except ImportError:  # pragma: no cover - legacy top-level import path
    from financial_agent.bridge import (
        MT5ExecutionBridge,
        AsyncExecutionEngine,
        MockAdapter,
        RealMT5Adapter,
        Signal,
        OrderDirection,
        ExecutionResult,
        ExecutionStatus,
        BaseExecutionAdapter,
        ErrorCode,
        OrderRequest,
        OrderResult,
        SymbolInfo,
        AccountInfo,
        PositionInfo,
    )

__all__ = [
    'MT5ExecutionBridge',
    'AsyncExecutionEngine',
    'MockAdapter',
    'RealMT5Adapter',
    'Signal',
    'OrderDirection',
    'ExecutionResult',
    'ExecutionStatus',
    'BaseExecutionAdapter',
    'ErrorCode',
    'OrderRequest',
    'OrderResult',
    'SymbolInfo',
    'AccountInfo',
    'PositionInfo',
]
