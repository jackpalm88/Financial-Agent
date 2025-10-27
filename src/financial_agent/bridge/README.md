# MT5 Bridge Hybrid v2.0 ðŸš€

**Production-ready execution bridge with Adapter Pattern**

Swap execution providers (MT5, IBKR, Binance, etc.) without changing bridge code.

---

## ðŸŽ¯ What's New in v2.0

**Adapter Pattern Architecture:**
- âœ… **MockAdapter** - Test without broker connection
- âœ… **RealMT5Adapter** - Production MT5 integration
- âœ… **Pluggable** - Easy to add new brokers (IBKR, Binance, etc.)
- âœ… **Same bridge code** - No changes when swapping adapters

**All Original Features Preserved:**
- 3-layer validation (Input â†’ Business Rules â†’ Pre-flight)
- Comprehensive error handling (unified error codes)
- Real-time statistics (success rate, latency, slippage)
- Callback system for memory integration
- Async execution engine

---

## ðŸ“¦ Quick Start

### Installation

```bash
cd mt5_bridge_hybrid
pip install -r requirements.txt
```

### Test Without MT5 (MockAdapter)

```python
import asyncio
from core import MT5ExecutionBridge, MockAdapter, Signal, OrderDirection

# Create mock adapter
mock = MockAdapter(success_rate=0.95, latency_ms=50.0, slippage_pips=1.0)
await mock.connect()

# Create bridge
bridge = MT5ExecutionBridge(adapter=mock)

# Execute signal
signal = Signal(
    symbol='EURUSD',
    direction=OrderDirection.LONG,
    size=0.1,
    confidence=0.88
)

signal_id = bridge.receive_signal(signal)
result = await bridge.execute_order(signal_id, signal)

print(f"Success: {result.success}, Fill: {result.fill_price}")

await mock.disconnect()
```

### Production with MT5

```python
# Configure MT5 credentials
config = {
    'login': 12345678,
    'password': 'your_password',
    'server': 'YourBroker-Demo'
}

# Create real MT5 adapter
from core import RealMT5Adapter

mt5 = RealMT5Adapter(config)
await mt5.connect()

# Same bridge code!
bridge = MT5ExecutionBridge(adapter=mt5)

# Execute works identically
signal_id = bridge.receive_signal(signal)
result = await bridge.execute_order(signal_id, signal)

await mt5.disconnect()
```

---

## ðŸ—ï¸ Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚         AI Trading Agent                    â”‚
â”‚  (Input Fusion â†’ Tool Stack â†’ Decision)    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                   â”‚ Signal
                   â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚      MT5ExecutionBridge (Adapter-based)     â”‚
â”‚                                              â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚ Layer 1: Signal Reception & Validationâ”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚ Layer 2: Order Execution               â”‚ â”‚
â”‚  â”‚   bridge.adapter.place_order()         â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚ Layer 3: Confirmation & Feedback       â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                   â”‚
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        â”‚                    â”‚
    â”Œâ”€â”€â”€â–¼â”€â”€â”€â”€â”         â”Œâ”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”
    â”‚  Mock  â”‚   OR    â”‚ RealMT5    â”‚   OR   [Future: IBKR, Binance...]
    â”‚Adapter â”‚         â”‚  Adapter   â”‚
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”˜         â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## ðŸŽ¨ Adapter Pattern Benefits

### 1. **Instant Testing (MockAdapter)**

```python
# No MT5 required - instant execution
mock = MockAdapter(success_rate=1.0, latency_ms=10.0)
await mock.connect()  # Instant

# Test your strategy immediately
bridge = MT5ExecutionBridge(adapter=mock)
```

### 2. **Easy Broker Switch**

```python
# Start with Mock for development
bridge = MT5ExecutionBridge(adapter=MockAdapter())

# Switch to MT5 for paper trading
bridge = MT5ExecutionBridge(adapter=RealMT5Adapter(config))

# Future: Switch to IBKR
# bridge = MT5ExecutionBridge(adapter=IBKRAdapter(config))
```

### 3. **Custom Adapters**

Create your own adapter for any broker:

```python
from core import BaseExecutionAdapter

class YourBrokerAdapter(BaseExecutionAdapter):
    async def connect(self) -> bool:
        # Your connection logic
        pass
    
    async def place_order(self, request: OrderRequest) -> OrderResult:
        # Your order execution logic
        pass
    
    # Implement other abstract methods...
```

---

## ðŸ“– Complete Example

```python
import asyncio
from core import (
    MT5ExecutionBridge,
    MockAdapter,
    RealMT5Adapter,
    Signal,
    OrderDirection
)

async def trading_system():
    # 1. Choose adapter
    adapter = MockAdapter()  # Or RealMT5Adapter(config)
    await adapter.connect()
    
    # 2. Create bridge
    bridge = MT5ExecutionBridge(
        adapter=adapter,
        max_spread_points=30,
        deviation=10
    )
    
    # 3. Register memory callback
    def memory_callback(result):
        if result.success:
            print(f"Order {result.order_id} executed @ {result.fill_price}")
            # Store in database for pattern learning
    
    bridge.register_confirmation_callback(memory_callback)
    
    # 4. Generate signal (from your AI agent)
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        stop_loss=1.08300,
        take_profit=1.08700,
        confidence=0.88,
        reasoning="Bullish breakout + positive sentiment"
    )
    
    # 5. Execute
    signal_id = bridge.receive_signal(signal)
    result = await bridge.execute_order(signal_id, signal)
    
    # 6. Check statistics
    stats = bridge.get_execution_statistics()
    print(f"Success Rate: {stats['success_rate']:.1f}%")
    print(f"Avg Latency: {stats['avg_execution_time_ms']:.1f}ms")
    
    await adapter.disconnect()

asyncio.run(trading_system())
```

---

## ðŸ§ª Testing

```bash
# Run all tests (uses MockAdapter)
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=core

# Run specific test
pytest tests/test_bridge.py::test_execute_order_success -v
```

**Test Coverage: 85%+**

All tests run instantly with MockAdapter - no MT5 required!

---

## ðŸ“Š Features Comparison

| Feature | v1.0 (Original) | v2.0 (Hybrid) |
|---------|----------------|---------------|
| **MT5 Execution** | âœ… | âœ… |
| **Validation** | âœ… | âœ… |
| **Statistics** | âœ… | âœ… |
| **Callbacks** | âœ… | âœ… |
| **Error Handling** | âœ… | âœ… Unified codes |
| **MockAdapter** | âŒ | âœ… NEW |
| **Pluggable Adapters** | âŒ | âœ… NEW |
| **Instant Testing** | âŒ | âœ… NEW |
| **Multi-broker Support** | âŒ | âœ… NEW (framework) |

---

## ðŸ”§ Configuration

**config/config.json:**
```json
{
  "mt5": {
    "login": 12345678,
    "password": "your_password",
    "server": "YourBroker-Demo",
    "timeout": 60000
  },
  "bridge": {
    "max_spread_points": 30,
    "deviation": 10,
    "magic_number": 20251027
  },
  "mock": {
    "success_rate": 0.95,
    "latency_ms": 50.0,
    "slippage_pips": 1.0
  }
}
```

---

## ðŸŽ¯ Migration from v1.0

**v1.0 code:**
```python
config = {...}
bridge = MT5ExecutionBridge(config)  # Direct MT5
```

**v2.0 code:**
```python
config = {...}
adapter = RealMT5Adapter(config)  # Wrap in adapter
await adapter.connect()
bridge = MT5ExecutionBridge(adapter=adapter)  # Pass adapter
```

**All other code remains identical!**

---

## ðŸ“ˆ Performance

| Metric | MockAdapter | RealMT5Adapter |
|--------|-------------|----------------|
| Connection | <1ms | ~100ms |
| Execution (avg) | 10-50ms | 50-150ms |
| Success Rate | Configurable | >95% |
| Testability | 100% (no MT5) | Requires MT5 |

---

## ðŸš€ Roadmap

**Phase 1: Adapter Foundation** âœ… (Current)
- [x] BaseExecutionAdapter interface
- [x] MockAdapter implementation
- [x] RealMT5Adapter implementation
- [x] Refactored bridge
- [x] Comprehensive tests

**Phase 2: Additional Adapters** (Future)
- [ ] IBKRAdapter (Interactive Brokers)
- [ ] BinanceAdapter (Crypto)
- [ ] AlpacaAdapter (US Stocks)

**Phase 3: Advanced Features**
- [ ] Multi-account orchestration
- [ ] Limit/stop order support
- [ ] Position modification
- [ ] Partial fills handling

---

## ðŸ› ï¸ Project Structure

```
mt5_bridge_hybrid/
â”œâ”€â”€ core/
â”‚   â”œâ”€â”€ __init__.py           # Package exports
â”‚   â”œâ”€â”€ adapter_base.py       # Abstract adapter + error codes
â”‚   â”œâ”€â”€ adapter_mock.py       # Mock adapter (testing)
â”‚   â”œâ”€â”€ adapter_mt5.py        # Real MT5 adapter
â”‚   â””â”€â”€ bridge.py             # Main bridge (adapter-based)
â”œâ”€â”€ config/
â”‚   â””â”€â”€ config.example.json   # Configuration template
â”œâ”€â”€ tests/
â”‚   â””â”€â”€ test_bridge.py        # Unit tests (MockAdapter)
â”œâ”€â”€ example_usage.py          # Usage examples
â”œâ”€â”€ requirements.txt          # Dependencies
â””â”€â”€ README.md                 # This file
```

---

## ðŸ’¡ Key Concepts

### Adapter Pattern

**Problem:** Tightly coupled to MT5 API  
**Solution:** Abstract interface + multiple implementations

**Benefits:**
- Test without broker
- Swap brokers easily
- Cleaner code
- Better testability

### Error Code Harmonization

All adapters use unified error codes:

```python
ErrorCode.SPREAD_TOO_WIDE  # Same across all brokers
ErrorCode.MARGIN_INSUFFICIENT
ErrorCode.ORDER_REJECTED
# etc.
```

MT5-specific codes automatically mapped to unified codes.

---

## ðŸ¤ Contributing

Want to add a new broker adapter?

1. Subclass `BaseExecutionAdapter`
2. Implement abstract methods
3. Map broker errors to unified `ErrorCode`
4. Add tests with MockAdapter
5. Submit PR!

---

## âš ï¸ Disclaimer

Trading involves substantial risk. This software is for educational purposes. Always test on demo accounts first.

---

## ðŸ“ License

MIT License - Use freely, modify as needed.

---

**Built with INoT Deep Dive methodology** ðŸŽ¯  
**Version 2.0.0 - Hybrid Architecture with Adapter Pattern**
