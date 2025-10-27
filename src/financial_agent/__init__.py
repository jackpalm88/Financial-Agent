"""
Financial Agent - Tool-Augmented Multi-Modal Trading System

A production-ready AI agent that combines market data (price, volume, news, indicators)
with tool-augmented reasoning to generate validated MT5 trading signals.

Architecture:
    Input Fusion → Stateful Memory → Tool Stack → Prompt Engine → MT5 Bridge

Components:
    - bridge: MT5 execution with adapter pattern (✅ Complete)
    - tools: Composable function toolkit (🚧 In Progress)
    - fusion: Multi-modal input processing (📋 Planned)
    - memory: Pattern learning & feedback (📋 Planned)
    - orchestration: Context-aware prompts (📋 Planned)
    - common: Shared utilities

Example:
    >>> from financial_agent.bridge import MT5ExecutionBridge, MockAdapter
    >>> 
    >>> # Test without MT5
    >>> adapter = MockAdapter(success_rate=0.95)
    >>> await adapter.connect()
    >>> bridge = MT5ExecutionBridge(adapter=adapter)
    >>> 
    >>> # Execute signal
    >>> result = await bridge.execute_order(signal_id, signal)
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

# Component imports will be added as modules are completed
# from .bridge import MT5ExecutionBridge, MockAdapter, RealMT5Adapter
# from .tools import ToolRegistry, BaseTool
# from .fusion import InputFusionLayer
# from .memory import MemoryModule
# from .orchestration import PromptEngine

__all__ = [
    "__version__",
    "__author__",
    "__license__",
]
