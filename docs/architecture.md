# Financial Agent - System Architecture

## Overview

Financial Agent is a **tool-augmented, multi-modal trading system** that uses LLM orchestration to combine market data, news, and technical indicators into validated trading signals.

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AI Trading Agent                      │
│              (LLM Orchestration Layer)                   │
└────────────────────┬────────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
┌─────────┐    ┌─────────┐    ┌─────────┐
│  Input  │    │  Tool   │    │ Memory  │
│  Fusion │    │  Stack  │    │ Module  │
└────┬────┘    └────┬────┘    └────┬────┘
     │              │              │
     └──────────────┼──────────────┘
                    │
                    ▼
         ┌──────────────────┐
         │  Prompt Engine   │
         │  (Orchestration) │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │   MT5 Bridge     │
         │  (Execution)     │
         └──────────────────┘
                  │
                  ▼
         ┌──────────────────┐
         │  MetaTrader 5    │
         └──────────────────┘
```

---

## 📦 Component Details

### 1. Input Fusion Layer

**Purpose:** Process heterogeneous data streams with different latencies

**Key Features:**
- Temporal alignment (±100ms sync window)
- Normalization pipeline (standard format)
- Priority queuing (real-time > batched)
- RingBuffer storage (last 1000 events)

**Data Sources:**
- Price/Volume ticks (WebSocket, <1ms latency)
- News articles (REST API, 1-5min latency)
- Technical indicators (computed, 10-100ms)

**Output:** `FusedInput` object with aligned context

---

### 2. Tool Stack

**Purpose:** Atomic, testable functions for market analysis

**Tool Categories:**
1. **Technical Indicators**
   - `calcRSI(symbol, period)` → (value, confidence)
   - `calcMACD(symbol, fast, slow)` → (macd, signal, histogram)
   - `calcBollingerBands(symbol, period, std)` → (upper, middle, lower)

2. **Sentiment Analysis**
   - `sentimentScore(text)` → (score: -1.0 to 1.0, confidence)
   - `extractEntities(text)` → List[Entity]

3. **Risk Management**
   - `validateRisk(position, account)` → (valid: bool, reason)
   - `calculatePositionSize(signal, account)` → float
   - `checkCorrelation(symbol1, symbol2)` → float

**Tool Interface:**
```python
class BaseTool(ABC):
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    def timeout_ms(self) -> int:
        return 5000  # Default 5s timeout
```

---

### 3. Memory Module

**Purpose:** Learn from past signals and outcomes

**Storage:**
- Last 30 signals + results (SQLite or Redis)
- Pattern database (successful setups)
- Confidence calibration data

**Functions:**
- `store_signal(signal, result)` → None
- `get_similar_signals(signal, n=5)` → List[Signal]
- `calibrate_confidence(signal)` → float

---

### 4. Prompt Engine

**Purpose:** Generate context-aware queries for LLM

**Nano-Prompt Template:**
```
Given:
- Price: EUR/USD = {price} ({change_24h})
- RSI(14) = {rsi} ({state})
- News: {headline} (sentiment: {sentiment})
- Memory: Last 3 {direction} signals → {win_rate}% success

Should I {action}? Provide reasoning + confidence (0-1).
```

**Dynamic Context Building:**
1. Extract relevant tools from signal
2. Query memory for similar past cases
3. Build compact context (<500 tokens)
4. Generate prompt with clear structure

---

### 5. MT5 Execution Bridge

**Purpose:** Execute validated signals on MetaTrader 5

**Architecture:** Adapter Pattern
- `BaseExecutionAdapter` (interface)
- `MockAdapter` (testing, no MT5)
- `RealMT5Adapter` (production)

**Features:**
- 3-layer validation (Input → Rules → Pre-flight)
- Async execution engine
- Statistics tracking (success rate, latency, slippage)
- Callback system (for memory feedback)

**Status:** ✅ **Complete** (see [Bridge README](../src/financial_agent/bridge/README.md))

---

### 6. Validation Layer

**Purpose:** Prevent bad trades from reaching execution

**3-Stage Validation:**

1. **Input Validation**
   - Price in reasonable range
   - Timestamp not stale (< 5s old)
   - Indicators not NaN/None

2. **Business Logic**
   - Signal confidence > threshold (e.g., 0.70)
   - Spread within acceptable range
   - No conflicting positions

3. **Execution Pre-flight**
   - Sufficient margin for order
   - Stop loss/take profit valid distances
   - Account not in freeze mode

**Rejection Handling:**
- Log reason for rejection
- Update memory with "rejected signal"
- Alert monitoring if rejection rate > 50%

---

## 🔄 Data Flow

### Signal Generation Flow

```
1. [Market Event] → Input Fusion
   ├─ Price tick arrives
   ├─ News article processed
   └─ Indicators computed

2. [Fused Context] → Prompt Engine
   ├─ Build nano-prompt
   └─ Query LLM

3. [LLM Response] → Tool Stack
   ├─ Execute calcRSI()
   ├─ Execute sentimentScore()
   └─ Aggregate results

4. [Tools Output] → Memory
   ├─ Query similar past signals
   └─ Calibrate confidence

5. [Enriched Signal] → Validation
   ├─ Input validation
   ├─ Business rules
   └─ Pre-flight checks

6. [Validated Signal] → MT5 Bridge
   ├─ adapter.place_order()
   └─ Confirmation callback

7. [Execution Result] → Memory
   └─ Store for future learning
```

---

## 🎯 Design Principles

### 1. Modularity
Each component is independently testable and replaceable.

### 2. Adapter Pattern
External dependencies (MT5, APIs) wrapped in adapters for easy mocking.

### 3. Fail-Fast Validation
Catch errors early (input validation) rather than late (execution failure).

### 4. Observable System
Every component emits metrics and logs for monitoring.

### 5. Token Efficiency
Nano-prompts (<500 tokens) to minimize LLM costs.

---

## 📊 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **E2E Latency** | <200ms | Time from event → order |
| **Tool Execution** | <50ms per tool | Individual tool benchmarks |
| **Validation** | <20ms total | All 3 stages combined |
| **Memory Lookup** | <10ms | Pattern retrieval |
| **Input Fusion** | <30ms | Multi-modal sync |

---

## 🔒 Security & Risk Management

### API Key Management
- Store credentials in `.env` file (never commit)
- Use environment variables in production
- Rotate keys regularly

### Position Limits
- Max position size: 2% of account
- Max daily loss: 5% of account
- Max concurrent orders: 5

### Monitoring
- Alert on high rejection rate (>50%)
- Alert on execution failures (>5%)
- Daily performance reports

---

## 🚀 Deployment Architecture

### Development
```
Laptop → MockAdapter → Local logs
```

### Production
```
VPS/Cloud → RealMT5Adapter → MT5 Terminal
    ↓
Prometheus (metrics) → Grafana (dashboard)
    ↓
Alerting (email/SMS)
```

---

## 📚 References

- [INoT Implementation Plan](IMPLEMENTATION_PLAN.md)
- [Bridge Implementation Details](bridge_implementation.md)
- [Development Guide](development.md)
