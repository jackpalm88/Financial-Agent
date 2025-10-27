# Financial Agent 🤖📈

**Tool-Augmented Multi-Modal Trading System with INoT Architecture**

Production-ready financial AI agent that combines market data (price, volume, news, indicators) with tool-augmented reasoning to generate validated MT5 trading signals.

---

## 🎯 Project Vision

Traditional trading bots fail at **context integration** - synthesizing price momentum + news sentiment + risk state into coherent decisions. This agent solves this with:

1. **Multi-modal Input Fusion** - Process heterogeneous data streams (real-time ticks vs batched news)
2. **Tool-Augmented Reasoning** - LLM orchestrates atomic functions (calcRSI, sentimentScore, generateOrder)
3. **Stateful Memory** - Learn from past signals and outcomes
4. **Risk-Aware Execution** - 3-layer validation before order placement

---

## 🏗️ Architecture (5-Layer Stack)

```
┌─────────────────────────────────────┐
│  Input Fusion Layer                 │  Multi-modal sync
│  (price + news + indicators)        │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Stateful Memory                    │  Pattern learning
│  (last 30 signals + outcomes)       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Tool Stack                         │  Composable functions
│  (RSI, MACD, sentiment, risk)       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  Prompt Engine                      │  Context-aware queries
│  (nano-prompt generation)           │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  MT5 Execution Bridge ✅            │  Signal → Order → Confirm
│  (Adapter Pattern: Mock + Real)    │
└─────────────────────────────────────┘
```

---

## 📦 Components Status

| Component | Priority | ICE Score | Status | Docs |
|-----------|----------|-----------|--------|------|
| **MT5 Bridge** | 🔴 High | 640 | ✅ Complete | [README](src/financial_agent/bridge/README.md) |
| **Tool Stack** | 🔴 High | 540 | 🚧 In Progress | [README](src/financial_agent/tools/README.md) |
| **Input Fusion** | 🔴 High | 504 | 📋 Planned | - |
| **Validation Layer** | 🔴 High | 567 | ⚠️ Partial (in Bridge) | - |
| **Memory Module** | 🟡 Medium | 168 | 📋 Planned | - |
| **Prompt Engine** | 🟡 Medium | 280 | 📋 Planned | - |
| **Backtest Framework** | 🟢 Low | 90 | 📋 Future | - |

**ICE Scoring:** Impact × Confidence × Ease (max 1000)

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd financial-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Run Example (No MT5 Required!)

```bash
# Test with MockAdapter - instant execution
python examples/bridge_example.py
# Select: 1 (MockAdapter)
```

### Run Tests

```bash
# Unit tests (fast)
pytest src/financial_agent/bridge/tests/ -v

# Integration tests (requires full setup)
pytest tests/integration/ -v

# With coverage
pytest --cov=src/financial_agent --cov-report=html
```

---

## 📖 Documentation

- **[Architecture](docs/architecture.md)** - System design & component interactions
- **[Implementation Plan](docs/IMPLEMENTATION_PLAN.md)** - INoT Deep Dive analysis
- **[Development Guide](docs/development.md)** - Contributing & coding standards
- **API Reference:**
  - [Bridge API](docs/api/bridge.md)
  - [Tools API](docs/api/tools.md) *(coming soon)*
  - [Fusion API](docs/api/fusion.md) *(coming soon)*

---

## 🛠️ Development

### Project Structure

```
financial-agent/
├── src/financial_agent/      # Main package
│   ├── bridge/                # ✅ MT5 execution (DONE)
│   ├── tools/                 # 🚧 Function toolkit (IN PROGRESS)
│   ├── fusion/                # 📋 Input processing
│   ├── memory/                # 📋 Pattern learning
│   ├── orchestration/         # 📋 Prompt engine
│   └── common/                # Shared utilities
├── tests/                     # Integration tests
├── examples/                  # Usage examples
├── configs/                   # Configuration templates
└── docs/                      # Documentation
```

### Adding New Components

1. Create module directory under `src/financial_agent/`
2. Follow adapter pattern (see Bridge example)
3. Add unit tests (`tests/` subfolder)
4. Document in module README.md
5. Update this main README with status

---

## 🎯 Roadmap

### Phase 1: Foundation ✅ (Weeks 1-2)
- [x] MT5 Bridge with Adapter Pattern
- [x] MockAdapter for instant testing
- [x] Comprehensive test suite
- [x] Git repository structure

### Phase 2: Tool Stack 🚧 (Weeks 3-4)
- [ ] BaseTool abstraction
- [ ] Technical indicators (RSI, MACD, Bollinger)
- [ ] Sentiment analysis tools
- [ ] Risk management functions
- [ ] Tool registry & dynamic loading

### Phase 3: Data Pipeline (Weeks 5-6)
- [ ] Input Fusion Layer (multi-modal sync)
- [ ] Normalization pipeline
- [ ] Temporal alignment (100ms window)
- [ ] Data quality validation

### Phase 4: Intelligence (Weeks 7-9)
- [ ] Memory Module (pattern storage)
- [ ] Confidence calibration
- [ ] Prompt Engine (nano-prompt generation)
- [ ] Context-aware orchestration

### Phase 5: Production (Weeks 10-12)
- [ ] End-to-end integration
- [ ] Performance optimization
- [ ] Monitoring & alerting
- [ ] Deployment automation

---

## 📊 Metrics & KPIs

| Metric | Target | Current |
|--------|--------|---------|
| **Test Coverage** | >85% | 85% (Bridge) |
| **Signal Latency** | <200ms | TBD |
| **Validation Reject Rate** | <5% false negatives | TBD |
| **Tool Execution Time** | <50ms per tool | TBD |
| **Memory Pattern Accuracy** | >80% recall | TBD |

---

## ⚠️ Disclaimer

**This is educational/research software.** Trading involves substantial risk of loss. Always:
- Test on demo accounts first
- Understand the risks
- Never invest more than you can afford to lose
- Comply with local financial regulations

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-tool`)
3. Write tests for new functionality
4. Ensure all tests pass (`pytest`)
5. Submit pull request

---

## 📞 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/financial-agent/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/financial-agent/discussions)
- **Documentation:** [Project Wiki](https://github.com/yourusername/financial-agent/wiki)

---

**Built with INoT Deep Dive Methodology** 🧠  
**Version:** 0.1.0-alpha  
**Status:** Active Development 🚧
