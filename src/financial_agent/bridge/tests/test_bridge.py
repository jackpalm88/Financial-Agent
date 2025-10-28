"""
Unit Tests for MT5 Bridge Hybrid
Tests using MockAdapter - no MT5 connection required
"""

import pytest
import pytest_asyncio
import asyncio
from datetime import datetime

from financial_agent.bridge import (
    MT5ExecutionBridge,
    AsyncExecutionEngine,
    MockAdapter,
    Signal,
    OrderDirection,
    ExecutionStatus,
    ErrorCode
)


# ========== FIXTURES ==========

@pytest.fixture
def mock_adapter():
    """Create mock adapter with high success rate"""
    adapter = MockAdapter(
        success_rate=1.0,  # 100% for deterministic tests
        latency_ms=10.0,
        slippage_pips=0.5
    )
    return adapter


@pytest_asyncio.fixture
async def connected_adapter(mock_adapter):
    """Create and connect mock adapter"""
    await mock_adapter.connect()
    yield mock_adapter
    await mock_adapter.disconnect()


@pytest.fixture
def bridge(connected_adapter):
    """Create bridge with connected mock adapter"""
    return MT5ExecutionBridge(
        adapter=connected_adapter,
        max_spread_points=30,
        deviation=10,
        magic=123456
    )


# ========== SIGNAL TESTS ==========

def test_signal_creation():
    """Test signal creation with valid data"""
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        confidence=0.85
    )
    
    assert signal.symbol == 'EURUSD'
    assert signal.direction == OrderDirection.LONG
    assert signal.size == 0.1
    assert signal.confidence == 0.85
    assert 'generated_at' in signal.metadata


# ========== VALIDATION TESTS ==========

@pytest.mark.asyncio
async def test_validate_signal_success(bridge):
    """Test successful signal validation"""
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        confidence=0.85
    )
    
    valid, msg = await bridge.validate_signal(signal)
    assert valid is True
    assert msg == "Signal valid"


@pytest.mark.asyncio
async def test_validate_signal_confidence_out_of_range(bridge):
    """Test validation fails for invalid confidence"""
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        confidence=1.5  # Invalid
    )
    
    valid, msg = await bridge.validate_signal(signal)
    assert valid is False
    assert "out of range" in msg.lower()


@pytest.mark.asyncio
async def test_validate_signal_invalid_size(bridge):
    """Test validation fails for invalid size"""
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.0,  # Invalid
        confidence=0.85
    )
    
    valid, msg = await bridge.validate_signal(signal)
    assert valid is False
    assert "invalid" in msg.lower()


@pytest.mark.asyncio
async def test_validate_signal_unknown_symbol(bridge):
    """Test validation fails for unknown symbol"""
    signal = Signal(
        symbol='INVALID',
        direction=OrderDirection.LONG,
        size=0.1,
        confidence=0.85
    )
    
    valid, msg = await bridge.validate_signal(signal)
    assert valid is False
    assert "not found" in msg.lower()


@pytest.mark.asyncio
async def test_validate_signal_spread_too_wide(bridge, connected_adapter):
    """Test validation fails when spread too wide"""
    # Set wide spread
    connected_adapter.set_price('EURUSD', 1.08000, 1.09000)  # 100 pip spread
    
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        confidence=0.85
    )
    
    valid, msg = await bridge.validate_signal(signal)
    assert valid is False
    assert "spread" in msg.lower()


# ========== EXECUTION TESTS ==========

@pytest.mark.asyncio
async def test_execute_order_success(bridge):
    """Test successful order execution"""
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        confidence=0.85
    )
    
    signal_id = bridge.receive_signal(signal)
    result = await bridge.execute_order(signal_id, signal)
    
    assert result.success is True
    assert result.status == ExecutionStatus.SUCCESS
    assert result.order_id is not None
    assert result.fill_price is not None
    assert result.execution_time_ms > 0


@pytest.mark.asyncio
async def test_execute_order_with_sl_tp(bridge):
    """Test order execution with stop loss and take profit"""
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        stop_loss=1.08300,
        take_profit=1.08700,
        confidence=0.85
    )
    
    signal_id = bridge.receive_signal(signal)
    result = await bridge.execute_order(signal_id, signal)
    
    assert result.success is True
    assert result.order_id is not None


@pytest.mark.asyncio
async def test_execute_order_failure(bridge, connected_adapter):
    """Test order execution failure"""
    # Set low success rate
    connected_adapter.set_success_rate(0.0)  # Force failure
    
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        confidence=0.85
    )
    
    signal_id = bridge.receive_signal(signal)
    result = await bridge.execute_order(signal_id, signal)
    
    assert result.success is False
    assert result.status == ExecutionStatus.FAILED
    assert result.error_code is not None
    assert result.error_message is not None


@pytest.mark.asyncio
async def test_slippage_calculation(bridge):
    """Test slippage calculation"""
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        confidence=0.85
    )
    
    signal_id = bridge.receive_signal(signal)
    result = await bridge.execute_order(signal_id, signal)
    
    assert result.success is True
    assert result.slippage_pips is not None
    assert result.slippage_pips >= 0


# ========== CALLBACK TESTS ==========

@pytest.mark.asyncio
async def test_confirmation_callback(bridge):
    """Test confirmation callback is triggered"""
    callback_called = False
    callback_result = None
    
    def test_callback(result):
        nonlocal callback_called, callback_result
        callback_called = True
        callback_result = result
    
    bridge.register_confirmation_callback(test_callback)
    
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        confidence=0.85
    )
    
    signal_id = bridge.receive_signal(signal)
    await bridge.execute_order(signal_id, signal)
    
    assert callback_called is True
    assert callback_result is not None
    assert callback_result.success is True


# ========== STATISTICS TESTS ==========

@pytest.mark.asyncio
async def test_execution_statistics(bridge):
    """Test execution statistics calculation"""
    # Execute multiple orders
    signals = [
        Signal(symbol='EURUSD', direction=OrderDirection.LONG, size=0.1, confidence=0.85),
        Signal(symbol='GBPUSD', direction=OrderDirection.SHORT, size=0.1, confidence=0.78),
        Signal(symbol='USDJPY', direction=OrderDirection.LONG, size=0.1, confidence=0.92),
    ]
    
    for signal in signals:
        signal_id = bridge.receive_signal(signal)
        await bridge.execute_order(signal_id, signal)
    
    stats = bridge.get_execution_statistics()
    
    assert stats['total_executions'] == 3
    assert stats['successful_executions'] == 3
    assert stats['failed_executions'] == 0
    assert stats['success_rate'] == 100.0
    assert stats['avg_execution_time_ms'] > 0


@pytest.mark.asyncio
async def test_statistics_with_failures(bridge, connected_adapter):
    """Test statistics with mixed success/failure"""
    # Set 50% success rate
    connected_adapter.set_success_rate(0.5)
    
    # Execute multiple orders
    for i in range(10):
        signal = Signal(
            symbol='EURUSD',
            direction=OrderDirection.LONG,
            size=0.1,
            confidence=0.85
        )
        signal_id = bridge.receive_signal(signal)
        await bridge.execute_order(signal_id, signal)
    
    stats = bridge.get_execution_statistics()
    
    assert stats['total_executions'] == 10
    assert stats['successful_executions'] > 0
    assert stats['failed_executions'] > 0
    assert 30 <= stats['success_rate'] <= 70  # Around 50% with variance


# ========== ASYNC ENGINE TESTS ==========

@pytest.mark.asyncio
async def test_async_engine_start_stop(bridge):
    """Test async engine start and stop"""
    engine = AsyncExecutionEngine(bridge)
    
    await engine.start()
    assert engine.is_running is True
    
    await engine.stop()
    assert engine.is_running is False


@pytest.mark.asyncio
async def test_async_engine_processes_queue(bridge):
    """Test async engine processes queued orders"""
    engine = AsyncExecutionEngine(bridge)
    await engine.start()
    
    # Queue signals
    for i in range(3):
        signal = Signal(
            symbol='EURUSD',
            direction=OrderDirection.LONG,
            size=0.1,
            confidence=0.85
        )
        bridge.receive_signal(signal)
    
    # Wait for processing
    await asyncio.sleep(0.5)
    
    # Check execution history
    assert len(bridge.execution_history) >= 3
    
    await engine.stop()


# ========== ACCOUNT INFO TESTS ==========

@pytest.mark.asyncio
async def test_get_account_info(bridge):
    """Test getting account information"""
    account = await bridge.get_account_info()
    
    assert account is not None
    assert account.balance > 0
    assert account.equity > 0


@pytest.mark.asyncio
async def test_get_open_positions(bridge):
    """Test getting open positions"""
    # Create position
    signal = Signal(
        symbol='EURUSD',
        direction=OrderDirection.LONG,
        size=0.1,
        confidence=0.85
    )
    
    signal_id = bridge.receive_signal(signal)
    result = await bridge.execute_order(signal_id, signal)
    
    assert result.success is True
    
    # Get positions
    positions = await bridge.get_open_positions('EURUSD')
    
    assert len(positions) > 0
    assert positions[0]['symbol'] == 'EURUSD'
    assert positions[0]['type'] == 'LONG'


# ========== ADAPTER TESTS ==========

@pytest.mark.asyncio
async def test_mock_adapter_connect():
    """Test mock adapter connection"""
    adapter = MockAdapter()
    
    connected = await adapter.connect()
    assert connected is True
    assert adapter.is_connected() is True
    
    await adapter.disconnect()
    assert adapter.is_connected() is False


@pytest.mark.asyncio
async def test_mock_adapter_symbol_info():
    """Test getting symbol info from mock"""
    adapter = MockAdapter()
    await adapter.connect()
    
    info = await adapter.symbol_info('EURUSD')
    
    assert info is not None
    assert info.symbol == 'EURUSD'
    assert info.digits == 5
    assert info.is_tradeable() is True
    
    await adapter.disconnect()


@pytest.mark.asyncio
async def test_mock_adapter_current_price():
    """Test getting current price from mock"""
    adapter = MockAdapter()
    await adapter.connect()
    
    prices = await adapter.current_price('EURUSD')
    
    assert prices is not None
    bid, ask = prices
    assert bid > 0
    assert ask > bid  # Ask should be higher than bid
    
    await adapter.disconnect()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
