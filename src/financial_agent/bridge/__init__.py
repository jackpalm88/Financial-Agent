"""
MT5 Bridge Hybrid v2.0 - Core Module

Production-ready execution bridge with Adapter Pattern.
Swap execution providers (MT5, IBKR, Binance, etc.) without changing bridge code.
"""

# Adapter Base (Interface + Error Codes)
from .adapter_base import (
    BaseExecutionAdapter,
    ErrorCode,
    SymbolInfo,
    OrderRequest,
    OrderResult,
    AccountInfo,
    PositionInfo
)

# Concrete Adapters
from .adapter_mock import MockAdapter

# RealMT5Adapter is optional (requires MetaTrader5 package)
try:
    from .adapter_mt5 import RealMT5Adapter
    _HAS_MT5 = True
except ImportError:
    RealMT5Adapter = None
    _HAS_MT5 = False

# Bridge
from .bridge import (
    MT5ExecutionBridge,
    Signal,
    OrderDirection,
    ExecutionResult,
    ExecutionStatus,
)

# The asynchronous execution engine lives in ``bridge`` alongside the core
# implementation.  Import it lazily so that importing ``financial_agent.bridge``
# doesn't immediately construct any event loops or pull in optional
# dependencies.  This mirrors the pattern recommended in the incident report
# and keeps the public API stable.
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - type-checking only
    from .bridge import AsyncExecutionEngine

# Version
__version__ = '2.0.0'

# Export all public APIs
__all__ = [
    # Adapters
    'BaseExecutionAdapter',
    'MockAdapter',
    'RealMT5Adapter',
    
    # Bridge
    'MT5ExecutionBridge',
    'AsyncExecutionEngine',

    # Data Structures
    'Signal',
    'OrderDirection',
    'OrderRequest',
    'OrderResult',
    'SymbolInfo',
    'AccountInfo',
    'PositionInfo',
    'ExecutionResult',
    'ExecutionStatus',
    
    # Error Handling
    'ErrorCode',
    
    # Version
    '__version__'
]


def __getattr__(name):
    """Provide lazy access to heavy bridge helpers.

    The ``AsyncExecutionEngine`` is only needed by consumers that want the
    background execution helper.  Keeping its import here prevents unnecessary
    initialization during test discovery while still satisfying
    ``from financial_agent.bridge import AsyncExecutionEngine``.
    """

    if name == 'AsyncExecutionEngine':
        from .bridge import AsyncExecutionEngine as _AsyncExecutionEngine

        return _AsyncExecutionEngine
    raise AttributeError(name)


def __dir__():
    return sorted(__all__)
