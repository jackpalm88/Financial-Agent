"""
MT5 Bridge Hybrid - Usage Examples
Demonstrates adapter pattern with Mock and Real MT5 adapters
"""

import asyncio
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import (
    MT5ExecutionBridge,
    AsyncExecutionEngine,
    MockAdapter,
    RealMT5Adapter,
    Signal,
    OrderDirection
)


def memory_callback(execution_result):
    """Example callback for Memory Module integration"""
    print(f"\nðŸ“Š Memory Callback:")
    print(f"   Signal: {execution_result.signal_id}")
    print(f"   Success: {execution_result.success}")
    
    if execution_result.success:
        print(f"   Fill Price: {execution_result.fill_price}")
        print(f"   Slippage: {execution_result.slippage_pips:.2f} pips")
        print(f"   Latency: {execution_result.execution_time_ms:.1f}ms")
    else:
        print(f"   Error: {execution_result.error_code.value if execution_result.error_code else 'Unknown'}")
        print(f"   Message: {execution_result.error_message}")


async def example_1_mock_adapter():
    """
    Example 1: Using MockAdapter for testing without MT5
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: MockAdapter (Testing Without MT5)")
    print("="*70)
    
    # Initialize mock adapter
    mock = MockAdapter(
        success_rate=0.95,  # 95% success rate
        latency_ms=50.0,    # 50ms average latency
        slippage_pips=1.0    # 1 pip average slippage
    )
    
    # Connect (instant for mock)
    if await mock.connect():
        print("âœ… Connected to MockAdapter")
    
    # Create bridge with mock adapter
    bridge = MT5ExecutionBridge(
        adapter=mock,
        max_spread_points=30,
        deviation=10,
        magic=20251027
    )
    
    # Register callback
    bridge.register_confirmation_callback(memory_callback)
    
    # Create signal
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        stop_loss=1.08300,
        take_profit=1.08700,
        confidence=0.88,
        reasoning="Mock test signal"
    )
    
    print(f"\nðŸ“¨ Executing signal: {signal.direction.value} {signal.size} {signal.symbol}")
    
    # Execute
    signal_id = bridge.receive_signal(signal)
    result = await bridge.execute_order(signal_id, signal)
    
    if result.success:
        print(f"\nâœ… Success! Order ID: {result.order_id}")
    else:
        print(f"\nâŒ Failed: {result.error_message}")
    
    # Show statistics
    stats = bridge.get_execution_statistics()
    print(f"\nðŸ“Š Statistics:")
    print(f"   Adapter: {stats['adapter']}")
    print(f"   Success Rate: {stats['success_rate']:.1f}%")
    print(f"   Avg Latency: {stats['avg_execution_time_ms']:.1f}ms")
    
    await mock.disconnect()


async def example_2_real_mt5_adapter():
    """
    Example 2: Using RealMT5Adapter with actual MT5 connection
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: RealMT5Adapter (Production)")
    print("="*70)
    
    # Load config
    config_path = 'config/config.json'
    if not os.path.exists(config_path):
        config_path = 'config/config.example.json'
        print(f"âš ï¸  Using example config (update with real credentials)")
    
    try:
        with open(config_path) as f:
            config = json.load(f)
    except FileNotFoundError:
        print("âŒ Config file not found. Skipping Real MT5 example.")
        return
    
    # Initialize real MT5 adapter
    mt5_adapter = RealMT5Adapter(config['mt5'])
    
    # Connect
    if not await mt5_adapter.connect():
        print("âŒ Failed to connect to MT5. Check credentials.")
        return
    
    print("âœ… Connected to MT5")
    
    # Show account info
    account = await mt5_adapter.account_info()
    if account:
        print(f"   Account: {account.account_id}")
        print(f"   Balance: ${account.balance:.2f}")
        print(f"   Equity: ${account.equity:.2f}")
    
    # Create bridge with MT5 adapter
    bridge = MT5ExecutionBridge(
        adapter=mt5_adapter,
        max_spread_points=30,
        deviation=10,
        magic=20251027
    )
    
    bridge.register_confirmation_callback(memory_callback)
    
    # Create small test signal (micro lot)
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.01,  # Micro lot
        confidence=0.85,
        reasoning="Real MT5 test signal"
    )
    
    print(f"\nðŸ“¨ Executing real signal: {signal.direction.value} {signal.size} {signal.symbol}")
    
    # Execute
    signal_id = bridge.receive_signal(signal)
    result = await bridge.execute_order(signal_id, signal)
    
    if result.success:
        print(f"\nâœ… Real order executed! Order ID: {result.order_id}")
        print(f"   Fill Price: {result.fill_price}")
        print(f"   Slippage: {result.slippage_pips:.2f} pips")
    else:
        print(f"\nâŒ Execution failed: {result.error_message}")
    
    # Show open positions
    positions = await bridge.get_open_positions('EURUSD')
    if positions:
        print(f"\nðŸ“ Open Position:")
        pos = positions[0]
        print(f"   Ticket: {pos['ticket']}")
        print(f"   Type: {pos['type']}")
        print(f"   Volume: {pos['volume']}")
        print(f"   P&L: ${pos['profit']:.2f}")
    
    await mt5_adapter.disconnect()


async def example_3_adapter_swap():
    """
    Example 3: Demonstrate adapter swap - start with Mock, switch to MT5
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Adapter Swap (Mock â†’ Real MT5)")
    print("="*70)
    
    # Start with MockAdapter
    print("\nðŸ”§ Phase 1: Testing with MockAdapter")
    mock = MockAdapter(success_rate=1.0, latency_ms=30.0, slippage_pips=0.5)
    await mock.connect()
    
    bridge_mock = MT5ExecutionBridge(adapter=mock)
    
    # Test 3 signals on mock
    test_signals = [
        Signal(symbol='EURUSD', direction=OrderDirection.LONG, size=0.1, confidence=0.85),
        Signal(symbol='GBPUSD', direction=OrderDirection.SHORT, size=0.1, confidence=0.78),
        Signal(symbol='USDJPY', direction=OrderDirection.LONG, size=0.1, confidence=0.92),
    ]
    
    for sig in test_signals:
        signal_id = bridge_mock.receive_signal(sig)
        result = await bridge_mock.execute_order(signal_id, sig)
        status = "âœ…" if result.success else "âŒ"
        print(f"   {status} {sig.symbol}: {result.fill_price if result.success else result.error_message}")
    
    stats_mock = bridge_mock.get_execution_statistics()
    print(f"\nðŸ“Š Mock Stats: {stats_mock['success_rate']:.0f}% success, "
          f"{stats_mock['avg_execution_time_ms']:.1f}ms avg")
    
    await mock.disconnect()
    
    # Switch to Real MT5 (if available)
    print("\nðŸ”§ Phase 2: Switching to RealMT5Adapter")
    
    config_path = 'config/config.json'
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
        
        mt5_adapter = RealMT5Adapter(config['mt5'])
        
        if await mt5_adapter.connect():
            print("âœ… Connected to Real MT5")
            
            bridge_mt5 = MT5ExecutionBridge(adapter=mt5_adapter)
            
            # Execute one real signal (micro lot)
            real_signal = Signal(
                symbol='EURUSD',
                direction=OrderDirection.LONG,
                size=0.01,
                confidence=0.85
            )
            
            signal_id = bridge_mt5.receive_signal(real_signal)
            result = await bridge_mt5.execute_order(signal_id, real_signal)
            
            status = "âœ…" if result.success else "âŒ"
            print(f"   {status} Real Execution: {result.fill_price if result.success else result.error_message}")
            
            await mt5_adapter.disconnect()
        else:
            print("âŒ Could not connect to MT5. Using mock results only.")
    else:
        print("âš ï¸  No MT5 config found. Demonstrating mock only.")
    
    print("\nâœ… Adapter swap complete - same bridge code, different backends!")


async def example_4_async_engine():
    """
    Example 4: Async execution engine with multiple signals
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Async Execution Engine (Background Processing)")
    print("="*70)
    
    # Use mock for demo
    mock = MockAdapter(success_rate=0.90, latency_ms=100.0)
    await mock.connect()
    
    bridge = MT5ExecutionBridge(adapter=mock)
    bridge.register_confirmation_callback(memory_callback)
    
    # Start async engine
    engine = AsyncExecutionEngine(bridge)
    await engine.start()
    
    print("\nðŸš€ Async engine started")
    print("ðŸ“¨ Queuing 5 signals...")
    
    # Queue multiple signals
    signals = [
        Signal(symbol='EURUSD', direction=OrderDirection.LONG, size=0.1, confidence=0.88),
        Signal(symbol='GBPUSD', direction=OrderDirection.SHORT, size=0.1, confidence=0.75),
        Signal(symbol='USDJPY', direction=OrderDirection.LONG, size=0.1, confidence=0.92),
        Signal(symbol='AUDUSD', direction=OrderDirection.SHORT, size=0.1, confidence=0.81),
        Signal(symbol='EURUSD', direction=OrderDirection.SHORT, size=0.1, confidence=0.79),
    ]
    
    for sig in signals:
        signal_id = bridge.receive_signal(sig)
        print(f"   Queued: {signal_id}")
    
    # Let engine process
    print("\nâ³ Processing signals (waiting 3 seconds)...")
    await asyncio.sleep(3)
    
    # Show results
    stats = bridge.get_execution_statistics()
    print(f"\nðŸ“Š Final Statistics:")
    print(f"   Total: {stats['total_executions']}")
    print(f"   Success: {stats['successful_executions']} ({stats['success_rate']:.1f}%)")
    print(f"   Failed: {stats['failed_executions']}")
    print(f"   Avg Latency: {stats['avg_execution_time_ms']:.1f}ms")
    print(f"   P95 Latency: {stats['p95_execution_time_ms']:.1f}ms")
    
    # Stop engine
    await engine.stop()
    await mock.disconnect()


async def main():
    """Run examples"""
    print("\n" + "="*70)
    print("MT5 BRIDGE HYBRID - ADAPTER PATTERN EXAMPLES")
    print("="*70)
    
    print("\nAvailable examples:")
    print("1. MockAdapter (instant testing)")
    print("2. RealMT5Adapter (production)")
    print("3. Adapter Swap (Mock â†’ MT5)")
    print("4. Async Engine (background processing)")
    print("all. Run all examples")
    
    choice = input("\nSelect example (1-4 or 'all'): ").strip()
    
    if choice == '1':
        await example_1_mock_adapter()
    elif choice == '2':
        await example_2_real_mt5_adapter()
    elif choice == '3':
        await example_3_adapter_swap()
    elif choice == '4':
        await example_4_async_engine()
    elif choice.lower() == 'all':
        await example_1_mock_adapter()
        await asyncio.sleep(1)
        await example_2_real_mt5_adapter()
        await asyncio.sleep(1)
        await example_3_adapter_swap()
        await asyncio.sleep(1)
        await example_4_async_engine()
    else:
        print(f"Invalid choice: {choice}")
        return
    
    print("\n" + "="*70)
    print("EXAMPLES COMPLETED")
    print("="*70 + "\n")


if __name__ == '__main__':
    asyncio.run(main())
