# ðŸŽ¯ StratÄ“Ä£iskÄ AnalÄ«ze: Tool-Augmented Financial Agent Architecture

## ðŸ“‹ Kopsavilkums

Å Ä« analÄ«ze izvÄ“rÅ¡ arhitektÅ«ru AI finanÅ¡u aÄ£entam, kas apvieno multimodal tirgus datus (cena, apjoms, ziÅ†as, indikatori) ar tool-augmented reasoning, lai Ä£enerÄ“tu MT5 EA trading signÄlus. Caur multi-agent validÄciju identificÄ“tas 7 kritiskÄs komponentes, no kurÄm 4 ir High Priority (ICE score > 350) implementÄcijai.

**GalvenÄ atziÅ†a:** VÄjÄkÄ vieta tradicionÄlajÄs trading bot arhitektÅ«rÄs ir nevis indikatori vai ML modeÄ¼i, bet **konteksta integrÄcija** - spÄ“ja sintezÄ“t cenu momentum + news sentiment + risk state vienÄ koherentÄ lÄ“mumÄ. Tool-augmented LLM ar structured memory un composable tool stack risina Å¡o problÄ“mu, veidojot **context-aware decision engine**, kas spÄ“j:

1. ApstrÄdÄt heterogÄ“nus datu avotus ar daÅ¾Ädu latency (real-time ticks vs. batched news)
2. UzturÄ“t stateful memory par iepriekÅ¡Ä“jiem signÄliem un to rezultÄtiem
3. Dinamiski Ä£enerÄ“t kontekstu-specifiskus jautÄjumus ("Given bearish news + RSI oversold, re-evaluate long thesis")
4. IzpildÄ«t risk-aware order generation ar position sizing un execution quality checks

ArhitektÅ«ra balstÄs uz **5-layer stack**: Input Fusion â†’ Stateful Memory â†’ Tool Orchestration â†’ Prompt Engine â†’ MT5 Bridge. Katrs layer ir testable un replaceable. Total implementation effort: ~8-12 nedÄ“Ä¼as vienam inÅ¾enierim ar financial domain knowledge.

---

## â­ PrioritizÄ“tas AtziÅ†as

### ðŸ”´ High Priority (Score â‰¥ 350)

1. **Multi-modal Input Fusion Layer** (Impact: 9, Confidence: 8, Ease: 7 | Score: 504)
   - **KÄpÄ“c svarÄ«gi:** Trading decisions balstÄs uz multiple signal sources, bet lielÄkÄ daÄ¼a botu ignorÄ“ ziÅ†as vai apstrÄdÄ tÄs Ärpus core loop. Input Fusion nodroÅ¡ina time-aligned, normalized data stream.
   - **PierÄdÄ«jumi:** "Ievade: {tirgus dati: cena+apjoms}, {ziÅ†u teksti}, {indikatoru rezultÄti}" - user requirements explicit norÄda uz multi-source integration.

2. **Composable Tool Stack** (Impact: 10, Confidence: 9, Ease: 6 | Score: 540)
   - **KÄpÄ“c svarÄ«gi:** LLM nevar natively izrÄ“Ä·inÄt RSI vai sentiment score. Tool stack pÄrvÄ“rÅ¡ aÄ£entu no "text generator" uz "function orchestrator" - katrs tool atgrieÅ¾ (value, confidence, latency).
   - **PierÄdÄ«jumi:** "tool stack â€“ funkcijas: calcRSI(), sentimentScore(), generateOrder()" - core functionality nevar bÅ«t hallucinÄ“ta, vajag real implementations.

3. **MT5 Execution Bridge** (Impact: 10, Confidence: 8, Ease: 8 | Score: 640)
   - **KÄpÄ“c svarÄ«gi:** Bez execution layer, sistÄ“ma ir tikai analytical dashboard. Bridge nodroÅ¡ina signal â†’ order â†’ confirmation feedback loop ar error handling.
   - **PierÄdÄ«jumi:** "Izpildi signÄlu uz MT5 EA" - explicit requirement produkta konvÄ“Ä¼Äm.

4. **Validation + Error Handling Layer** (Impact: 9, Confidence: 9, Ease: 7 | Score: 567)
   - **KÄpÄ“c svarÄ«gi:** Real markets producÄ“ corrupt data (missing ticks, delayed news, API failures). Bez validation, aÄ£ents pieÅ†em lÄ“mumus uz bad inputs â†’ catastrophic losses.
   - **PierÄdÄ«jumi:** Multi-agent debate Round 2 identificÄ“ja: "Kas notiek, ja sentiment API fails vai RSI returns NaN?" - critical edge case.

### ðŸŸ¡ Medium Priority (Score 150-349)

5. **Stateful Memory + Pattern Learning** (Impact: 7, Confidence: 6, Ease: 4 | Score: 168)
   - **KÄpÄ“c svarÄ«gi:** Bez memory, katrs signÄls ir isolated decision. Memory enables: "Last 3 breakout signals failed â†’ adjust confidence threshold."
   - **PierÄdÄ«jumi:** "memory module â€“ saglabÄ pÄ“dÄ“jo 30 signÄlu un rezultÄtus" - explicit memory requirement.

6. **Nano-prompt Generation Engine** (Impact: 8, Confidence: 7, Ease: 5 | Score: 280)
   - **KÄpÄ“c svarÄ«gi:** Static prompts nevar adapt uz dynamic market conditions. Prompt engine builds context-aware queries: "Given {state}, should I {action}?"
   - **PierÄdÄ«jumi:** "Nano-prompta Ä£enerÄ“Å¡ana: 'Given the last 24h news sentiment + price breakout, should I open a long?'" - dynamic query construction.

### ðŸŸ¢ Low Priority (Score < 150)

7. **Advanced Backtest Framework** (Impact: 6, Confidence: 5, Ease: 3 | Score: 90)
   - **KÄpÄ“c svarÄ«gi:** ValidÄ“ stratÄ“Ä£iju pirms live deployment, bet nav core functionality aÄ£enta darbÄ«bai.
   - **PierÄdÄ«jumi:** Nav minÄ“ts user requirements - inference ka tas ir nice-to-have, nevis must-have.

---

## ðŸ” Deep Dive IzvÄ“rsumi

### ðŸ’¡ 1. Multi-modal Input Fusion Layer

**KÄpÄ“c tas ir svarÄ«gi**

Financial markets Ä£enerÄ“ signÄlus multiple modalities ar atÅ¡Ä·irÄ«gÄm temporal characteristics:
- **Price/Volume ticks**: High frequency (milliseconds), low semantic content
- **News articles**: Low frequency (minutes/hours), high semantic content
- **Technical indicators**: Medium frequency (seconds), derived features

TradicionÄlÄs arhitektÅ«ras apstrÄdÄ Å¡os avotus izolÄ“ti vai ar naÃ¯ve concat. ProblÄ“ma: news event lagged by 2 minutes var arrive AFTER price jau moved â†’ wrong context. Input Fusion Layer nodroÅ¡ina:
1. **Temporal alignment**: Ringbuffer ar Â±100ms sync window
2. **Normalization**: Visi inputs â†’ standard format (timestamp, source, value, confidence)
3. **Priority queuing**: Real-time ticks prioritÄri pÄr batched news

Bez Å¡Ä« layer, aÄ£ents "redz" fragmentÄ“tu realitÄti un producÄ“ lÄ“mumus uz incomplete state.

**KÄ tas darbojas**

```python
class InputFusionLayer:
    def __init__(self, sync_window_ms=100):
        self.ringbuffer = RingBuffer(capacity=1000)  # Last 1000 events
        self.sync_window = sync_window_ms
        self.normalizers = {
            'price': PriceNormalizer(),
            'news': NewsNormalizer(),
            'indicator': IndicatorNormalizer()
        }
    
    def ingest(self, raw_input, modality):
        # Step 1: Normalize to standard format
        normalized = self.normalizers[modality].transform(raw_input)
        
        # Step 2: Add timestamp if missing
        if not normalized.timestamp:
            normalized.timestamp = time.now()
        
        # Step 3: Append to ringbuffer
        self.ringbuffer.append(normalized)
        
        # Step 4: Trigger fusion if sync window complete
        if self._check_sync_window():
            return self.fuse_aligned_events()
    
    def fuse_aligned_events(self):
        # Group events within sync_window
        window_events = self.ringbuffer.get_last_n_ms(self.sync_window)
        
        # Build fused context
        fused = {
            'timestamp': window_events[-1].timestamp,
            'price_state': self._aggregate_prices(window_events),
            'news_events': self._aggregate_news(window_events),
            'indicator_values': self._aggregate_indicators(window_events),
            'confidence': min([e.confidence for e in window_events])
        }
        
        return FusedInput(**fused)
```

**Process flow:**
1. Raw data arrives (WebSocket ticks, news API poll, indicator calculation)
2. Modality-specific normalizer converts to standard schema
3. Ringbuffer stores with timestamp
4. Every 100ms, fusion logic groups aligned events
5. Output: Single FusedInput object ar visu relevantu kontekstu

**KonkrÄ“ts piemÄ“rs**

**ScenÄrijs:** EUR/USD trading bot, 2024-03-15 09:30:00 UTC

**Incoming data streams:**
```
T=09:30:00.000  [PRICE]     EUR/USD = 1.0845, volume = 250 lots
T=09:30:00.050  [INDICATOR] RSI(14) = 68.5 (approaching overbought)
T=09:30:00.120  [NEWS]      "ECB hints at rate cut" (sentiment: -0.7 bearish)
T=09:30:00.200  [PRICE]     EUR/USD = 1.0842, volume = 180 lots (dropping)
```

**Fusion process:**
```python
# All events within 200ms window â†’ single fused input
fused_context = {
    'timestamp': '2024-03-15T09:30:00.200Z',
    'price_state': {
        'current': 1.0842,
        'change_200ms': -0.0003,  # -3 pips
        'volume_total': 430,
        'trend': 'downward'
    },
    'news_events': [{
        'headline': 'ECB hints at rate cut',
        'sentiment': -0.7,
        'age_ms': 80,  # News is recent
        'relevance': 0.95  # High relevance to EUR
    }],
    'indicator_values': {
        'RSI_14': 68.5,
        'interpretation': 'overbought_warning'
    },
    'confidence': 0.85  # Min confidence from all sources
}
```

**AÄ£enta lÄ“mums ar fusion:**
"Bearish news + overbought RSI + downward price momentum â†’ HIGH confidence SHORT signal"

**Bez fusion:**
AÄ£ents redz price tick at 09:30:00.000 (1.0845) â†’ "Price looks stable, consider LONG"
News arrives 120ms later â†’ "Oh, bearish news, but price data is stale now..."
RezultÄts: Confused state, low confidence, missed opportunity.

**Riski un slazdiem**

- âš ï¸ **Sync window mis-calibration:** Ja sync_window = 10ms (pÄrÄk Ä«ss) â†’ events never align, constant partial context. Ja sync_window = 5000ms (pÄrÄk garÅ¡) â†’ stale data mixed with fresh. â†’ **Mitigation:** Adaptive window based on market volatility (high vol = shorter window).

- âš ï¸ **Data source latency variance:** News API var bÅ«t 200ms latency, bet price ticks 5ms. Fusion layer "waits" for news â†’ delayed signals. â†’ **Mitigation:** Confidence degradation over time - news older than 500ms gets reduced weight.

- âš ï¸ **Conflicting signals within window:** Price up + bearish news = ambiguous fusion. â†’ **Mitigation:** Return ALL conflicting signals to prompt engine, let LLM reason about contradiction.

- âš ï¸ **Memory bloat:** Ringbuffer with 1000 events @ 100ms = 100 seconds history = manageable. But 10000 events = 1000 seconds = 16 minutes = RAM issues. â†’ **Mitigation:** Sliding window + archival to disk for backtest replay.

**IntegrÄcijas soÄ¼i**

**Phase 1: Core Infrastructure (Week 1-2)**
1. Implement RingBuffer with efficient indexing (use collections.deque in Python)
2. Define standard Input schema (Pydantic model):
   ```python
   class NormalizedInput(BaseModel):
       timestamp: datetime
       modality: Literal['price', 'news', 'indicator']
       value: Any
       confidence: float = 1.0
       metadata: Dict = {}
   ```
3. Write modality-specific normalizers (PriceNormalizer, NewsNormalizer, IndicatorNormalizer)
4. Unit tests: Feed synthetic data, verify timestamp alignment

**Phase 2: Integration with Data Sources (Week 3-4)**
5. Connect to price feed (e.g., MT5 WebSocket or IB API)
6. Connect to news API (e.g., Benzinga, Alpha Vantage)
7. Connect to indicator calculation engine (TA-Lib or custom)
8. Verify end-to-end: raw data â†’ normalized â†’ fused

**Phase 3: Optimization (Week 5)**
9. Benchmark latency: Target = fusion output within 50ms of last input
10. Implement adaptive sync window logic
11. Add monitoring: track fusion rate, dropped events, confidence distribution

**Common Pain Points:**
- **Timestamp hell**: News API returns "2024-03-15T09:30:00" but price tick is "1710493800.123456" epoch. â†’ Solution: Convert everything to UTC datetime objects immediately.
- **Missing data handling**: Indicator calculation fails (not enough bars) â†’ Fusion produces incomplete context. â†’ Solution: Mark missing fields as None, reduce confidence score.

**KÄ mÄ“rÄ«t panÄkumus**

- **Fusion completeness rate:** % of fused contexts that have all 3 modalities (price + news + indicators). Target: >80% in normal markets, >60% during high volatility.
- **Temporal alignment accuracy:** Mean absolute deviation between earliest and latest timestamp in fused window. Target: <50ms.
- **Latency (data â†’ fused output):** P95 latency from last raw input to fused output ready. Target: <100ms.
- **Confidence score distribution:** Mean confidence of fused outputs. Target: >0.75 (indicates high-quality inputs).

**PieÅ†Ä“mumi un ierobeÅ¾ojumi**

- **PieÅ†Ä“mums:** All data sources provide reliable timestamps. (Validated: Most financial APIs do, but custom scrapers may not)
- **PieÅ†Ä“mums:** 100ms sync window is appropriate for timeframe traded. (Uncertain: Scalping needs <10ms, swing trading can tolerate 1000ms - make configurable)
- **IerobeÅ¾ojums:** Fusion layer does NOT filter out low-quality sources - it normalizes but trusts input confidence scores. Garbage in = garbage fused output.
- **IerobeÅ¾ojums:** No causal reasoning - if news CAUSED price move, fusion treats them as independent. LLM prompt engine must infer causality.

**PierÄdÄ«jumi**

- User requirement: "Ievade: {tirgus dati: cena+apjoms}, {ziÅ†u teksti}, {indikatoru rezultÄti}" - explicit multi-source integration
- Multi-agent debate Round 1: "Kas notiek ar async news un real-time price ticks?" - temporal alignment necessity identified
- Financial markets research: High-frequency trading firms use similar "data fusion" layers to combine order book + trade flow + news (source: "Flash Boys" by Michael Lewis, HFT architecture whitepapers)

---

### ðŸ’¡ 2. Composable Tool Stack

**KÄpÄ“c tas ir svarÄ«gi**

LLMs are excellent at pattern recognition un reasoning, bet terrible at precision computation. GPT-4 nevar reliable izrÄ“Ä·inÄt RSI(14) vai solve optimization problems (position sizing ar Kelly criterion). Tool Stack risina Å¡o:

1. **Deterministic operations:** calcRSI() vienmÄ“r atgrieÅ¾ pareizo vÄ“rtÄ«bu given price series - no hallucinations.
2. **Domain-specific logic:** sentimentScore() uses fine-tuned NLP model trained on financial news, nevis generic sentiment.
3. **Composability:** Tools var call citus tools - generateOrder() calls checkSpread() + calculatePositionSize() + validateRiskLimits().

Bez tool stack, aÄ£ents ir "smart analyzer" bet ne "reliable executor". Ar tool stack, tas kÄ¼Å«st par "autonomous decision system" ar provable correctness konkrÄ“tÄm operÄcijÄm.

**KÄ tas darbojas**

**3-tier tool architecture:**

```python
# Tier 1: Atomic Tools (no dependencies)
class AtomicTools:
    @staticmethod
    def calcRSI(prices: List[float], period: int = 14) -> Tuple[float, float, float]:
        """
        Returns: (rsi_value, confidence, latency_ms)
        confidence = 1.0 if len(prices) >= period*2, else degraded
        """
        if len(prices) < period:
            return (None, 0.0, 0.1)  # Insufficient data
        
        # Standard RSI calculation
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return (100.0, 0.8, 0.2)  # Edge case: all gains
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Confidence based on data quality
        confidence = min(1.0, len(prices) / (period * 2))
        latency = 0.15  # Typical computation time
        
        return (rsi, confidence, latency)
    
    @staticmethod
    def sentimentScore(text: str) -> Tuple[float, float, float]:
        """
        Returns: (sentiment [-1, +1], confidence, latency_ms)
        Uses FinBERT or similar financial sentiment model
        """
        # Placeholder - real implementation uses HuggingFace pipeline
        result = FinBERTModel.predict(text)
        return (result.score, result.confidence, result.latency)

# Tier 2: Composite Tools (use atomic tools)
class MarketAnalysisTools:
    @staticmethod
    def technicalOverview(prices: List[float]) -> Dict:
        """Combines multiple indicators"""
        rsi, rsi_conf, _ = AtomicTools.calcRSI(prices)
        macd, macd_conf, _ = AtomicTools.calcMACD(prices)
        
        # Interpret signals
        interpretation = {
            'rsi': rsi,
            'rsi_signal': 'overbought' if rsi > 70 else 'oversold' if rsi < 30 else 'neutral',
            'confidence': min(rsi_conf, macd_conf),
            'summary': f"RSI at {rsi:.1f} suggests {interpretation}"
        }
        return interpretation

# Tier 3: Execution Tools (use composite tools + external APIs)
class ExecutionTools:
    @staticmethod
    def generateOrder(symbol: str, direction: str, context: Dict) -> Dict:
        """
        Main execution tool - validates all preconditions before order
        """
        # Step 1: Check market conditions
        spread = MarketMicrostructure.getBidAskSpread(symbol)
        if spread > context['max_spread_threshold']:
            return {'success': False, 'reason': 'Spread too wide'}
        
        # Step 2: Calculate position size
        account_balance = MT5Bridge.getBalance()
        risk_per_trade = context.get('risk_pct', 0.01)  # 1% default
        stop_loss_pips = context.get('sl_pips', 20)
        
        position_size = RiskManager.calculatePositionSize(
            balance=account_balance,
            risk_pct=risk_per_trade,
            stop_loss_pips=stop_loss_pips,
            symbol=symbol
        )
        
        # Step 3: Validate risk limits
        if not RiskManager.validateLimits(position_size, symbol):
            return {'success': False, 'reason': 'Risk limits exceeded'}
        
        # Step 4: Generate order object
        order = {
            'symbol': symbol,
            'direction': direction,
            'size': position_size,
            'stop_loss': context.get('sl_price'),
            'take_profit': context.get('tp_price'),
            'metadata': {'generated_at': time.now(), 'confidence': context.get('confidence')}
        }
        
        return {'success': True, 'order': order}
```

**Tool orchestration flow:**
```
LLM Reasoning â†’ "I need RSI value" â†’ Call calcRSI() â†’ Receive (68.5, 0.95, 0.15ms)
LLM Reasoning â†’ "RSI overbought + bearish news" â†’ Call generateOrder(direction='SHORT')
generateOrder() â†’ Calls checkSpread() + calculatePositionSize() + validateRiskLimits()
â†’ Returns order object or error
LLM Reasoning â†’ "Order validated, execute" â†’ Call MT5Bridge.sendOrder()
```

**KonkrÄ“ts piemÄ“rs**

**Scenario:** AÄ£ents analyzing EUR/USD at 2024-03-15 14:30:00

**LLM nano-prompt:**
```
Context:
- Price: 1.0842 EUR/USD
- Last 100 candles: [1.0850, 1.0848, 1.0845, ...]
- News: "ECB hints at rate cut" (sentiment: -0.7)
- Account balance: $10,000
- Max risk per trade: 1% ($100)

Task: Should I open a SHORT position?
```

**LLM reasoning process (with tool calls):**

1. **"I need to check if price is overbought"**
   ```python
   rsi, conf, lat = calcRSI(prices=last_100_candles, period=14)
   # Returns: (68.5, 0.95, 0.15)
   ```
   
2. **"RSI 68.5 is near overbought. Check sentiment context."**
   ```python
   sentiment, conf, lat = sentimentScore(text="ECB hints at rate cut")
   # Returns: (-0.7, 0.88, 45.2)
   ```

3. **"Bearish sentiment + high RSI â†’ SHORT signal. Calculate position size."**
   ```python
   order_details = generateOrder(
       symbol='EURUSD',
       direction='SHORT',
       context={
           'risk_pct': 0.01,
           'sl_pips': 20,
           'max_spread_threshold': 2.0,
           'confidence': min(0.95, 0.88)  # 0.88
       }
   )
   ```
   
   **generateOrder() internal calls:**
   ```python
   # Sub-call 1: Check spread
   spread = getBidAskSpread('EURUSD')  # Returns: 1.2 pips (acceptable)
   
   # Sub-call 2: Calculate position
   position_size = calculatePositionSize(
       balance=10000,
       risk_pct=0.01,
       stop_loss_pips=20,
       pip_value_usd=10  # Standard lot EUR/USD
   )
   # Formula: (10000 * 0.01) / (20 * 10) = 100 / 200 = 0.5 lots
   
   # Sub-call 3: Validate risk
   validateLimits(position_size=0.5, symbol='EURUSD')  # Returns: True
   ```
   
4. **generateOrder() returns:**
   ```json
   {
       "success": true,
       "order": {
           "symbol": "EURUSD",
           "direction": "SHORT",
           "size": 0.5,
           "stop_loss": 1.0862,
           "take_profit": 1.0802,
           "confidence": 0.88
       }
   }
   ```

5. **LLM final decision:**
   "Order validated with 0.88 confidence. Recommendation: EXECUTE SHORT 0.5 lots EUR/USD."

**Bez tool stack:**
LLM hallucinates RSI calculation: "I estimate RSI is around 65-70 based on price pattern..." (unreliable)
LLM guesses position size: "Maybe 0.5 lots seems reasonable?" (ignores actual risk calculation)
Result: Incorrect or unsafe orders.

**Riski un slazdiem**

- âš ï¸ **Tool execution failures:** calcRSI() crashes ja input ir empty list â†’ AÄ£ents stuck without indicator. â†’ **Mitigation:** Visiem tools mandatory (value, confidence, latency) tuple - ja execution fails, return (None, 0.0, timeout_ms).

- âš ï¸ **Latency accumulation:** Ja aÄ£ents calls 10 tools in sequence, total latency = sum(all latencies) â†’ slow decisions. â†’ **Mitigation:** Parallelize independent tool calls (RSI un sentiment var run parallel), use timeout limits (max 500ms per tool).

- âš ï¸ **Tool versioning hell:** calcRSI() v1 uses simple MA smoothing, v2 uses EMA â†’ Different results, broke backtest comparisons. â†’ **Mitigation:** Version every tool, store version used in signal metadata.

- âš ï¸ **Overfitting on tool outputs:** AÄ£ents learns "if RSI > 70, always SHORT" â†’ Ignores context, becomes rule-based bot. â†’ **Mitigation:** Tools return confidence + reasoning context, force LLM to consider multiple signals.

**IntegrÄcijas soÄ¼i**

**Phase 1: Atomic Tools (Week 1)**
1. Implement Tier 1 atomic tools (calcRSI, calcMACD, calcBollinger, sentimentScore)
2. Standardize return signature: (value, confidence, latency_ms)
3. Unit test each tool with synthetic data + edge cases (empty input, NaN values)

**Phase 2: Risk Management Tools (Week 2)**
4. Implement RiskManager class:
   - calculatePositionSize() using Kelly criterion or fixed fractional
   - validateLimits() checking max position size, correlation limits
   - getAccountMetrics() pulling balance, margin, exposure from MT5
5. Integration test: Mock account data â†’ validate position sizing correctness

**Phase 3: Composite + Execution Tools (Week 3)**
6. Implement MarketAnalysisTools (technicalOverview, sentimentContext)
7. Implement ExecutionTools (generateOrder with full validation pipeline)
8. Integration test: End-to-end from context â†’ order object

**Phase 4: LLM Integration (Week 4)**
9. Define tool schemas for LLM function calling:
   ```json
   {
       "name": "calcRSI",
       "description": "Calculate RSI indicator for given price series",
       "parameters": {
           "prices": {"type": "array", "items": {"type": "number"}},
           "period": {"type": "integer", "default": 14}
       },
       "returns": {"type": "object", "properties": {
           "value": {"type": "number"},
           "confidence": {"type": "number"},
           "latency_ms": {"type": "number"}
       }}
   }
   ```
10. Test LLM reasoning with available tools (use OpenAI function calling or Anthropic tool use)

**Common Pain Points:**
- **Tool discoverability:** LLM doesn't know which tool exists â†’ Include tool catalog in system prompt.
- **Parameter confusion:** LLM calls calcRSI(period="14") instead of calcRSI(period=14) â†’ Strict type validation + error messages.

**KÄ mÄ“rÄ«t panÄkumus**

- **Tool call success rate:** % of tool invocations that return valid (non-None) results. Target: >95%.
- **Tool latency P95:** 95th percentile tool execution time. Target: <100ms for atomic tools, <500ms for composite.
- **Execution quality score:** Post-trade analysis - did orders follow risk limits? Target: 100% compliance with validateLimits().
- **Tool diversity:** How many unique tools does aÄ£ents use per decision? Target: â‰¥3 (price + indicator + risk).

**PieÅ†Ä“mumi un ierobeÅ¾ojumi**

- **PieÅ†Ä“mums:** Tools ir deterministic - same input always produces same output. (Validated for technical indicators, uncertain for external API calls like sentimentScore)
- **PieÅ†Ä“mums:** LLM can learn to use tools effectively from schemas alone. (Confidence: 8/10 - works well with GPT-4/Claude Opus, weaker models struggle)
- **IerobeÅ¾ojums:** Tool stack nevar adapt to new indicators without code changes - nav "learn new tool" capability.
- **IerobeÅ¾ojums:** Error propagation - ja upstream tool fails, downstream tools may receive invalid inputs.

**PierÄdÄ«jumi**

- User requirement: "tool stack â€“ funkcijas: calcRSI(), sentimentScore(), generateOrder()" - explicit tool list
- Multi-agent debate: "LLM nevar natively calculate RSI" - necessity of deterministic tools identified
- Industry practice: Hedge funds use similar "function libraries" for quantitative strategies (e.g., QuantLib, TA-Lib integration)

---

### ðŸ’¡ 3. MT5 Execution Bridge

**KÄpÄ“c tas ir svarÄ«gi**

Visas analÄ«zes un signÄli ir bezjÄ“dzÄ«gi, ja tos nevar izpildÄ«t tirgÅ«. MT5 Execution Bridge ir kritiska komponente, kas pÄrvÄ“rÅ¡ aÄ£enta lÄ“mumus reÄlÄs orderos:

1. **Atomicity:** Order vai nu izpildÄs pilnÄ«bÄ, vai neizpildÄs vispÄr - nav partial executions bez apstiprinÄÅ¡anas.
2. **Feedback loop:** Bridge ne tikai sÅ«ta orders, bet arÄ« atgrieÅ¾ confirmation (fill price, execution time, slippage) â†’ Memory module var mÄcÄ«ties.
3. **Error resilience:** Network failures, rejected orders, insufficient margin â†’ Bridge handle gracefully + provide actionable error messages LLM reasoning.

Bez Bridge, aÄ£ents ir "paper trading simulator". Ar Bridge, tas kÄ¼Å«st par autonomous trader ar real P&L consequences.

**KÄ tas darbojas**

**Architecture layers:**

```python
class MT5ExecutionBridge:
    """
    3-layer bridge: Signal â†’ Order â†’ Confirmation
    """
    def __init__(self, mt5_config: Dict):
        self.mt5 = MetaTrader5()
        self.mt5.initialize(
            login=mt5_config['login'],
            password=mt5_config['password'],
            server=mt5_config['server']
        )
        self.order_queue = AsyncQueue()  # Buffer for async execution
        self.confirmation_callback = None
    
    # Layer 1: Signal Reception
    def receive_signal(self, signal: Dict) -> str:
        """
        Receive signal from agent, validate, enqueue
        Returns: signal_id for tracking
        """
        # Validation
        if not self._validate_signal(signal):
            raise ValueError(f"Invalid signal: {signal}")
        
        # Generate unique ID
        signal_id = f"{signal['symbol']}_{int(time.time()*1000)}"
        
        # Enqueue for async processing
        self.order_queue.put({
            'id': signal_id,
            'signal': signal,
            'timestamp': time.now()
        })
        
        return signal_id
    
    # Layer 2: Order Execution
    async def execute_order(self, signal: Dict) -> Dict:
        """
        Convert signal to MT5 order and execute
        Returns: execution_result with fill details
        """
        symbol = signal['symbol']
        direction = signal['direction']  # 'LONG' or 'SHORT'
        size = signal['size']
        
        # Map to MT5 order types
        order_type = self.mt5.ORDER_TYPE_BUY if direction == 'LONG' else self.mt5.ORDER_TYPE_SELL
        
        # Prepare order request
        request = {
            'action': self.mt5.TRADE_ACTION_DEAL,
            'symbol': symbol,
            'volume': size,
            'type': order_type,
            'price': self.mt5.symbol_info_tick(symbol).ask if direction == 'LONG' else self.mt5.symbol_info_tick(symbol).bid,
            'sl': signal.get('stop_loss'),
            'tp': signal.get('take_profit'),
            'deviation': 10,  # Max slippage in points
            'magic': 123456,  # EA magic number
            'comment': f"AI_Agent_{signal.get('confidence', 0):.2f}",
            'type_time': self.mt5.ORDER_TIME_GTC,
            'type_filling': self.mt5.ORDER_FILLING_IOC  # Immediate or Cancel
        }
        
        # Execute
        try:
            result = self.mt5.order_send(request)
            
            if result.retcode != self.mt5.TRADE_RETCODE_DONE:
                return {
                    'success': False,
                    'error_code': result.retcode,
                    'error_message': self._get_error_message(result.retcode),
                    'signal_id': signal['id']
                }
            
            # Success - extract fill details
            return {
                'success': True,
                'signal_id': signal['id'],
                'order_id': result.order,
                'fill_price': result.price,
                'fill_volume': result.volume,
                'execution_time_ms': (time.now() - signal['timestamp']).total_seconds() * 1000,
                'slippage_pips': self._calculate_slippage(request['price'], result.price, symbol),
                'comment': request['comment']
            }
        
        except Exception as e:
            return {
                'success': False,
                'error_message': str(e),
                'signal_id': signal['id']
            }
    
    # Layer 3: Confirmation & Feedback
    def get_execution_confirmation(self, signal_id: str, timeout: int = 5) -> Dict:
        """
        Poll for execution result, return confirmation
        """
        start_time = time.now()
        while (time.now() - start_time).total_seconds() < timeout:
            result = self._check_execution_status(signal_id)
            if result:
                # Notify memory module
                if self.confirmation_callback:
                    self.confirmation_callback(result)
                return result
            time.sleep(0.1)
        
        return {
            'success': False,
            'error_message': 'Execution timeout',
            'signal_id': signal_id
        }
    
    # Helper: Error code translation
    def _get_error_message(self, retcode: int) -> str:
        error_map = {
            10004: 'Requote - price changed',
            10006: 'Request rejected',
            10007: 'Request canceled by trader',
            10008: 'Order placed',
            10009: 'Request completed',
            10013: 'Invalid request',
            10014: 'Invalid volume',
            10015: 'Invalid price',
            10016: 'Invalid stop loss/take profit',
            10019: 'Insufficient funds',
            10021: 'Market closed'
        }
        return error_map.get(retcode, f'Unknown error code: {retcode}')
```

**Execution flow:**
```
1. Signal arrives: {'symbol': 'EURUSD', 'direction': 'SHORT', 'size': 0.5, ...}
2. receive_signal() validates + generates signal_id â†’ 'EURUSD_1710493800000'
3. execute_order() converts to MT5 request + sends
4. MT5 processes order â†’ Returns retcode + fill details
5. get_execution_confirmation() returns result to agent
6. Confirmation callback â†’ Memory module stores outcome
```

**KonkrÄ“ts piemÄ“rs**

**Scenario:** AÄ£ents decided to SHORT EUR/USD after analyzing bearish news + overbought RSI

**Signal object:**
```python
signal = {
    'symbol': 'EURUSD',
    'direction': 'SHORT',
    'size': 0.5,
    'stop_loss': 1.0862,
    'take_profit': 1.0802,
    'confidence': 0.88,
    'generated_at': '2024-03-15T14:30:00.000Z',
    'reasoning': 'Bearish ECB news + RSI 68.5 overbought'
}
```

**Bridge execution:**

**Step 1: receive_signal()**
```python
signal_id = bridge.receive_signal(signal)
# Returns: 'EURUSD_1710515400000'
# Signal validated and queued
```

**Step 2: execute_order() async processing**
```python
# MT5 order request created:
request = {
    'action': TRADE_ACTION_DEAL,
    'symbol': 'EURUSD',
    'volume': 0.5,
    'type': ORDER_TYPE_SELL,
    'price': 1.0842,  # Current bid
    'sl': 1.0862,
    'tp': 1.0802,
    'deviation': 10,
    'magic': 123456,
    'comment': 'AI_Agent_0.88'
}

# MT5 processes order...
# Server response after 87ms:
result = {
    'retcode': 10009,  # TRADE_RETCODE_DONE
    'order': 987654321,
    'price': 1.0841,  # Fill price (1 pip slippage)
    'volume': 0.5
}
```

**Step 3: Confirmation returned**
```python
confirmation = bridge.get_execution_confirmation('EURUSD_1710515400000')

# Returns:
{
    'success': True,
    'signal_id': 'EURUSD_1710515400000',
    'order_id': 987654321,
    'fill_price': 1.0841,
    'fill_volume': 0.5,
    'execution_time_ms': 87,
    'slippage_pips': 1.0,  # Requested 1.0842, filled at 1.0841
    'comment': 'AI_Agent_0.88'
}
```

**Feedback to Memory Module:**
Memory stores: "Signal EURUSD_SHORT @ 0.88 confidence â†’ Executed successfully, 1 pip slippage, 87ms latency"

**Later analysis:** If this trade wins â†’ Confidence in "bearish news + overbought RSI" pattern increases.

**Riski un slazdiem**

- âš ï¸ **Network failures during execution:** Signal sent, network drops, confirmation never arrives â†’ Agent doesn't know if order executed. â†’ **Mitigation:** Implement reconciliation loop - poll MT5 for open orders + match against sent signal_ids. If order found but no confirmation, backfill confirmation.

- âš ï¸ **Slippage worse than deviation:** Requested price 1.0842 Â± 10 pips, but market gapped 50 pips â†’ Order rejected or filled at terrible price. â†’ **Mitigation:** Dynamic deviation based on volatility - high vol = wider deviation. Validate post-fill slippage, add to signal metadata.

- âš ï¸ **Rejected orders (insufficient margin, invalid params):** Agent generates signal, but account lacks margin or stop loss invalid. â†’ **Mitigation:** Pre-execution validation - call RiskManager.validateLimits() BEFORE sending to MT5. Return error to agent so it can adjust or skip.

- âš ï¸ **Order ID collision:** If multiple agents or EAs running, magic number collision â†’ Orders attributed to wrong agent. â†’ **Mitigation:** Unique magic number per agent instance. Store magicâ†’agent_id mapping.

- âš ï¸ **Market closed during signal:** AÄ£ents generates signal at 23:59 Friday, market closed until Monday. â†’ **Mitigation:** Check mt5.symbol_info(symbol).trade_mode - if market closed, queue signal for Monday open or notify agent "market closed, defer decision".

**IntegrÄcijas soÄ¼i**

**Phase 1: MT5 Connection (Week 1)**
1. Install MetaTrader5 Python package: `pip install MetaTrader5`
2. Configure MT5 credentials (login, password, server) - use demo account for testing
3. Test basic connection: `mt5.initialize()` + `mt5.account_info()`
4. Verify symbol availability: `mt5.symbol_info('EURUSD')` returns valid data

**Phase 2: Order Execution (Week 2)**
5. Implement receive_signal() with validation
6. Implement execute_order() with MT5 order_send() wrapper
7. Test with paper orders: Send test signals on demo account, verify fills
8. Add error handling for all MT5 return codes (retcode mapping)

**Phase 3: Confirmation & Feedback (Week 3)**
9. Implement get_execution_confirmation() with polling
10. Add confirmation callback registration - link to Memory Module
11. Test end-to-end: Signal â†’ Execution â†’ Confirmation â†’ Memory update
12. Add reconciliation logic for missed confirmations

**Phase 4: Production Hardening (Week 4)**
13. Implement order queue with priority (urgent signals first)
14. Add execution metrics logging (latency, slippage, success rate)
15. Stress test: Send 100 signals in rapid succession, verify all handled
16. Deploy on live account with small position sizes for real-world validation

**Common Pain Points:**
- **MT5 package versioning:** Different MT5 terminal versions have different API behaviors. â†’ Solution: Lock to specific terminal version (e.g., MT5 build 3770).
- **Time synchronization:** Agent timestamp vs. MT5 server time â†’ Orders may appear out of sequence. â†’ Solution: Use server time (mt5.terminal_info().time_server).

**KÄ mÄ“rÄ«t panÄkumus**

- **Execution success rate:** % of signals that result in successful order fills. Target: >95% (failures only due to market conditions, not bugs).
- **Execution latency P95:** Time from receive_signal() to order confirmation. Target: <200ms for market orders.
- **Slippage distribution:** Mean and P95 slippage in pips. Target: Mean <2 pips, P95 <5 pips.
- **Error recovery rate:** % of failed executions where bridge provides actionable error message. Target: 100%.
- **Reconciliation accuracy:** % of orders where confirmation matches actual MT5 order state. Target: 100%.

**PieÅ†Ä“mumi un ierobeÅ¾ojumi**

- **PieÅ†Ä“mums:** MT5 API is reliable - order_send() returns accurate fill data. (Confidence: 9/10 - well-tested, but edge cases exist during extreme volatility)
- **PieÅ†Ä“mums:** Network latency agentâ†’MT5 is <50ms. (Uncertain: VPS hosting near broker reduces latency, residential network may have higher latency)
- **IerobeÅ¾ojums:** Bridge supports only market orders (ORDER_TYPE_BUY/SELL) - limit orders, stop orders require additional logic.
- **IerobeÅ¾ojums:** No partial fill handling - if order partially fills, bridge treats as failure (ORDER_FILLING_IOC mode).
- **IerobeÅ¾ojums:** Single MT5 account - no multi-account orchestration (e.g., risk-split across multiple brokers).

**PierÄdÄ«jumi**

- User requirement: "Izpildi signÄlu uz MT5 EA" - explicit MT5 integration mandate
- Multi-agent debate: "Bez execution layer, sistÄ“ma ir tikai analytical dashboard" - execution necessity
- Industry practice: Retail algo traders universally use MT4/MT5 APIs for execution (MQL5.com forums, algo trading communities)
- Technical documentation: MetaTrader5 Python API official docs confirm order_send() capabilities (https://www.mql5.com/en/docs/python_metatrader5)

---

### ðŸ’¡ 4. Validation + Error Handling Layer

**KÄpÄ“c tas ir svarÄ«gi**

Financial markets producÄ“ constant stream of "dirty data" - corrupt ticks, delayed news, API outages, invalid indicator values. Bez validation, aÄ£ents pieÅ†em lÄ“mumus uz bad inputs â†’ catastrophic consequences:

- **Bad price data:** Received tick shows EUR/USD = 0.5000 (obviously wrong) â†’ AÄ£ents thinks "huge drop, buy now!" â†’ Loses money on invalid signal.
- **Missing indicator:** RSI calculation fails (insufficient bars) â†’ AÄ£ents proceeds without key signal â†’ Lower accuracy.
- **API failures:** Sentiment API timeout â†’ AÄ£ents makes decision without news context â†’ Incomplete analysis.
- **Risk limit violations:** generateOrder() returns 5.0 lot position, but account only supports 1.0 max â†’ Execution rejected, opportunity missed.

Validation Layer ir "immune system" - detect + quarantine bad inputs BEFORE they reach decision logic. Principles:

1. **Fail fast:** Detect errors at input boundary, not deep in execution pipeline.
2. **Graceful degradation:** If sentiment API down, continue with price+indicators only (reduced confidence).
3. **Actionable errors:** Return errors that agent can reason about ("Spread 5.2 pips exceeds 2.0 threshold" not "Error 500").

**KÄ tas darbojas**

**3-stage validation architecture:**

```python
class ValidationLayer:
    """
    Stage 1: Input Validation (data quality)
    Stage 2: Business Logic Validation (trading rules)
    Stage 3: Execution Pre-flight (risk checks)
    """
    
    # Stage 1: Input Validation
    @staticmethod
    def validate_price_tick(tick: Dict) -> Tuple[bool, str]:
        """Validate price data sanity"""
        symbol = tick.get('symbol')
        price = tick.get('price')
        timestamp = tick.get('timestamp')
        
        # Check 1: Required fields
        if not all([symbol, price, timestamp]):
            return (False, "Missing required fields in price tick")
        
        # Check 2: Price in reasonable range
        # EUR/USD should be 0.8 - 1.5 historically
        if symbol == 'EURUSD':
            if price < 0.8 or price > 1.5:
                return (False, f"Price {price} outside reasonable range [0.8, 1.5]")
        
        # Check 3: Timestamp not too stale
        age_seconds = (time.now() - timestamp).total_seconds()
        if age_seconds > 5:
            return (False, f"Price tick stale: {age_seconds}s old")
        
        # Check 4: No NaN or Inf
        if math.isnan(price) or math.isinf(price):
            return (False, f"Invalid price value: {price}")
        
        return (True, "Price tick valid")
    
    @staticmethod
    def validate_indicator(indicator_result: Tuple) -> Tuple[bool, str]:
        """Validate indicator output"""
        value, confidence, latency = indicator_result
        
        # Check 1: Value is not None
        if value is None:
            return (False, "Indicator returned None - insufficient data")
        
        # Check 2: Confidence in valid range
        if not (0 <= confidence <= 1):
            return (False, f"Confidence {confidence} outside [0, 1]")
        
        # Check 3: Latency not excessive
        if latency > 1000:  # 1 second threshold
            return (False, f"Indicator latency {latency}ms exceeds threshold")
        
        return (True, "Indicator valid")
    
    @staticmethod
    def validate_news_event(news: Dict) -> Tuple[bool, str]:
        """Validate news sentiment data"""
        headline = news.get('headline')
        sentiment = news.get('sentiment')
        timestamp = news.get('timestamp')
        
        # Check 1: Required fields
        if not all([headline, sentiment is not None, timestamp]):
            return (False, "Missing required fields in news event")
        
        # Check 2: Sentiment in valid range
        if not (-1 <= sentiment <= 1):
            return (False, f"Sentiment {sentiment} outside [-1, 1]")
        
        # Check 3: Not too stale (news older than 1 hour = low relevance)
        age_minutes = (time.now() - timestamp).total_seconds() / 60
        if age_minutes > 60:
            return (False, f"News event stale: {age_minutes:.1f} minutes old")
        
        return (True, "News event valid")
    
    # Stage 2: Business Logic Validation
    @staticmethod
    def validate_trading_rules(signal: Dict, context: Dict) -> Tuple[bool, str]:
        """Validate signal against trading rules"""
        symbol = signal['symbol']
        direction = signal['direction']
        confidence = signal.get('confidence', 0)
        
        # Rule 1: Minimum confidence threshold
        min_confidence = context.get('min_confidence', 0.7)
        if confidence < min_confidence:
            return (False, f"Confidence {confidence:.2f} below threshold {min_confidence}")
        
        # Rule 2: Check if market open
        if not MarketInfo.is_market_open(symbol):
            return (False, f"Market closed for {symbol}")
        
        # Rule 3: Check spread (execution cost)
        spread = MarketInfo.get_spread(symbol)
        max_spread = context.get('max_spread', 2.0)
        if spread > max_spread:
            return (False, f"Spread {spread:.1f} pips exceeds {max_spread} threshold")
        
        # Rule 4: No conflicting open positions
        open_positions = MT5Bridge.get_open_positions(symbol)
        for pos in open_positions:
            if pos['direction'] != direction:
                return (False, f"Conflicting position: {pos['direction']} already open")
        
        return (True, "Trading rules satisfied")
    
    # Stage 3: Execution Pre-flight
    @staticmethod
    def validate_execution_readiness(order: Dict, account: Dict) -> Tuple[bool, str]:
        """Final validation before sending to MT5"""
        symbol = order['symbol']
        size = order['size']
        stop_loss = order.get('stop_loss')
        take_profit = order.get('take_profit')
        
        # Check 1: Sufficient margin
        required_margin = MarketInfo.calculate_margin(symbol, size)
        available_margin = account['free_margin']
        if required_margin > available_margin:
            return (False, f"Insufficient margin: need {required_margin}, have {available_margin}")
        
        # Check 2: Position size within limits
        max_position = account.get('max_position_size', 1.0)
        if size > max_position:
            return (False, f"Position size {size} exceeds limit {max_position}")
        
        # Check 3: Stop loss valid
        current_price = MarketInfo.get_current_price(symbol, order['direction'])
        if stop_loss:
            distance = abs(current_price - stop_loss)
            min_sl_distance = MarketInfo.get_min_stop_distance(symbol)
            if distance < min_sl_distance:
                return (False, f"Stop loss {stop_loss} too close to price {current_price}")
        
        # Check 4: Take profit valid
        if take_profit:
            distance = abs(current_price - take_profit)
            min_tp_distance = MarketInfo.get_min_stop_distance(symbol)
            if distance < min_tp_distance:
                return (False, f"Take profit {take_profit} too close to price {current_price}")
        
        return (True, "Execution pre-flight passed")
```

**Validation flow integration:**
```python
class AgentPipeline:
    def process_signal(self, raw_inputs: Dict) -> Dict:
        # Stage 1: Input Validation
        for price_tick in raw_inputs['prices']:
            valid, msg = ValidationLayer.validate_price_tick(price_tick)
            if not valid:
                logging.warning(f"Invalid price tick: {msg}")
                continue  # Skip this tick
        
        for indicator_result in raw_inputs['indicators']:
            valid, msg = ValidationLayer.validate_indicator(indicator_result)
            if not valid:
                logging.warning(f"Invalid indicator: {msg}")
                raw_inputs['indicators'].remove(indicator_result)
        
        for news in raw_inputs['news']:
            valid, msg = ValidationLayer.validate_news_event(news)
            if not valid:
                logging.warning(f"Invalid news: {msg}")
                raw_inputs['news'].remove(news)
        
        # If too many invalid inputs, abort
        if len(raw_inputs['prices']) == 0:
            return {'error': 'No valid price data'}
        
        # Proceed with fusion...
        fused = InputFusionLayer.fuse(raw_inputs)
        
        # Agent generates signal...
        signal = Agent.generate_signal(fused)
        
        # Stage 2: Business Logic Validation
        valid, msg = ValidationLayer.validate_trading_rules(signal, context)
        if not valid:
            return {'error': f'Trading rule violation: {msg}'}
        
        # Generate order...
        order = ExecutionTools.generateOrder(signal)
        
        # Stage 3: Execution Pre-flight
        account = MT5Bridge.get_account_info()
        valid, msg = ValidationLayer.validate_execution_readiness(order, account)
        if not valid:
            return {'error': f'Execution pre-flight failed: {msg}'}
        
        # All validations passed - execute
        result = MT5Bridge.execute_order(order)
        return result
```

**KonkrÄ“ts piemÄ“rs**

**Scenario:** Agent processing morning data, multiple validation stages

**Stage 1: Input Validation**

**Invalid price tick caught:**
```python
tick = {
    'symbol': 'EURUSD',
    'price': 0.5000,  # Clearly wrong
    'timestamp': datetime.now()
}

valid, msg = ValidationLayer.validate_price_tick(tick)
# Returns: (False, "Price 0.5000 outside reasonable range [0.8, 1.5]")

# Action: Tick discarded, logged as warning
# Agent proceeds with other valid ticks
```

**Stale news filtered:**
```python
news = {
    'headline': 'ECB rate decision',
    'sentiment': -0.5,
    'timestamp': datetime.now() - timedelta(hours=2)  # 2 hours old
}

valid, msg = ValidationLayer.validate_news_event(news)
# Returns: (False, "News event stale: 120.0 minutes old")

# Action: News discarded
# Agent generates signal without this news (confidence reduced)
```

**Stage 2: Business Logic Validation**

**Low confidence signal rejected:**
```python
signal = {
    'symbol': 'EURUSD',
    'direction': 'LONG',
    'confidence': 0.65,  # Below 0.70 threshold
    'reasoning': 'Weak technical setup'
}

valid, msg = ValidationLayer.validate_trading_rules(signal, {'min_confidence': 0.70})
# Returns: (False, "Confidence 0.65 below threshold 0.7")

# Action: Signal rejected, no order generated
# Agent logs: "Signal confidence insufficient, waiting for better setup"
```

**Wide spread warning:**
```python
# Current market: EURUSD spread = 3.5 pips (normally 1-2 pips)
# High volatility event (NFP release)

signal = {
    'symbol': 'EURUSD',
    'direction': 'SHORT',
    'confidence': 0.88
}

valid, msg = ValidationLayer.validate_trading_rules(signal, {'max_spread': 2.0})
# Returns: (False, "Spread 3.5 pips exceeds 2.0 threshold")

# Action: Signal queued, execution deferred until spread normalizes
```

**Stage 3: Execution Pre-flight**

**Insufficient margin caught:**
```python
order = {
    'symbol': 'EURUSD',
    'size': 2.0,  # 2 lots
    'direction': 'LONG'
}

account = {
    'balance': 5000,
    'free_margin': 800,  # Only $800 available
    'max_position_size': 1.0
}

# Required margin for 2.0 lots EURUSD â‰ˆ $2000
valid, msg = ValidationLayer.validate_execution_readiness(order, account)
# Returns: (False, "Insufficient margin: need 2000, have 800")

# Action: Order rejected before sending to MT5
# Agent adjusts: "Reduce position size to 0.3 lots (fits available margin)"
```

**All validations passed:**
```python
# Clean input data
# High confidence signal (0.92)
# Normal spread (1.2 pips)
# Sufficient margin
# Valid stop loss/take profit

# Result: Order sent to MT5
# Returns: {'success': True, 'fill_price': 1.0845, ...}
```

**Riski un slazdiem**

- âš ï¸ **Over-validation ("analysis paralysis"):** Too many validation rules â†’ AÄ£ents rejects too many valid signals, misses opportunities. â†’ **Mitigation:** Validation rules konfigurÄ“jami (strict mode vs. permissive mode), monitor rejection rate (if >50%, rules too tight).

- âš ï¸ **False positives:** Validation thinks data is bad, but it's actually correct edge case (e.g., Brexit vote caused EUR/USD 0.90 â†’ Flagged as "outside range"). â†’ **Mitigation:** Dynamic ranges based on recent volatility, allow manual override for exceptional market conditions.

- âš ï¸ **Validation blind spots:** Checks price, indicators, news - but ignores correlation (multiple correlated positions = hidden risk). â†’ **Mitigation:** Add "portfolio-level validation" - check aggregate exposure across all symbols.

- âš ï¸ **Performance overhead:** Running 10+ validation checks per signal â†’ Latency increases. â†’ **Mitigation:** Parallelize independent checks, cache market info (spread, margin requirements).

**IntegrÄcijas soÄ¼i**

**Phase 1: Input Validation (Week 1)**
1. Define validation functions for each input type (price, indicator, news)
2. Establish reasonable ranges per symbol (store in config: EURUSD range [0.8, 1.5], etc.)
3. Unit test each validation function with edge cases (NaN, None, stale timestamps)

**Phase 2: Business Logic Validation (Week 2)**
4. Define trading rules (min confidence, max spread, market hours, position conflicts)
5. Implement validate_trading_rules() with configurable thresholds
6. Integration test: Feed signal pipeline with rule-violating signals, verify rejections

**Phase 3: Execution Pre-flight (Week 3)**
7. Implement margin calculation + account state checks
8. Implement stop loss/take profit distance validation
9. Integration test: Attempt orders that violate margin/position limits, verify pre-flight catches

**Phase 4: Monitoring + Tuning (Week 4)**
10. Add metrics: validation rejection rate by reason (low confidence, wide spread, etc.)
11. Dashboard: Real-time view of rejected signals + reasons
12. Tune thresholds based on rejection patterns (if 80% rejected for "spread", increase threshold)

**Common Pain Points:**
- **Config drift:** Validation thresholds in code, changed manually â†’ Inconsistent behavior. â†’ Solution: Centralized config file, version controlled.
- **Unclear error messages:** "Validation failed" without specifics â†’ Agent can't adapt. â†’ Solution: Every validation returns (bool, detailed_message).

**KÄ mÄ“rÄ«t panÄkumus**

- **False negative rate:** % of valid signals incorrectly rejected. Target: <5% (measured via backtest - if rejected signal would have been profitable).
- **False positive rate:** % of invalid signals that pass validation. Target: <1% (measured via live monitoring - if executed signal based on bad data).
- **Validation latency:** Time spent in validation per signal. Target: <20ms total (all 3 stages).
- **Rejection reason distribution:** Which validation rules trigger most? Target: Balanced (no single rule >30% of rejections, indicates over-reliance).

**PieÅ†Ä“mumi un ierobeÅ¾ojumi**

- **PieÅ†Ä“mums:** Reasonable ranges (e.g., EUR/USD 0.8-1.5) remain valid long-term. (Confidence: 8/10 - historical ranges stable, but black swan events can invalidate)
- **PieÅ†Ä“mums:** Validation rules are sufficient - no unknown failure modes. (Uncertain: Markets evolve, new types of "dirty data" may emerge)
- **IerobeÅ¾ojums:** Validation is defensive, not predictive - catches errors after they occur, can't prevent upstream API failures.
- **IerobeÅ¾ojums:** No "smart validation" - rules are static thresholds, not ML-based anomaly detection.

**PierÄdÄ«jumi**

- Multi-agent debate Round 2: "Kas notiek, ja sentiment API fails vai RSI returns NaN?" - validation necessity identified
- Industry practice: Professional trading systems universally implement pre-trade risk checks (regulatory requirement for many brokers)
- Real-world incidents: Knight Capital $440M loss (2012) due to lack of validation on order size - system sent incorrect orders without pre-flight checks
- Software engineering principle: "Fail fast, fail loud" - validation layer embodies this in financial context

---

## ðŸ“Œ Galvenie CitÄti

> "Ievade: {tirgus dati: cena+apjoms}, {ziÅ†u teksti}, {indikatoru rezultÄti}" - Multi-modal input requirement

> "memory module â€“ saglabÄ pÄ“dÄ“jo 30 signÄlu un rezultÄtus" - Stateful learning loop specification

> "tool stack â€“ funkcijas: calcRSI(), sentimentScore(), generateOrder()" - Tool-augmented architecture mandate

> "Nano-prompta Ä£enerÄ“Å¡ana: 'Given the last 24h news sentiment + price breakout, should I open a long?'" - Context-aware prompt engineering example

> "Izpildi signÄlu uz MT5 EA" - Execution integration requirement

---

## â“ AtvÄ“rtie JautÄjumi

1. **Pattern Learning Mechanics:** KÄ Memory Module ekstrahÄ“ patterns no 30 signÄlu? Clustering (k-means)? Sequence analysis (LSTM)? Rule extraction? Vai vienkÄrÅ¡i store + let LLM find patterns?

2. **Cost Optimization:** Katra signÄla LLM call = $0.01-0.05 (depending on model). Pie 100 signÄliem dienÄ = $1-5/day = $30-150/month. Vai hybrid approach (LLM only for uncertain signals, rule-based for obvious cases)?

3. **Backtest Framework Scope:** User neminÄ“ja backtest, bet tas kritisks stratÄ“Ä£ijas validÄcijai. Vai bÅ«vÄ“t full replay engine vai rely on external tool (MetaTrader Strategy Tester)?

4. **Multi-Symbol Scaling:** Architecture designed for single symbol (EUR/USD). Ja expand uz 10 symbols â†’ 10x data streams, 10x validation overhead. Vai centralize validation or per-symbol isolation?

5. **Regulatory Compliance:** Automated trading var trigger regulatory requirements (e.g., MiFID II trade reporting). Vai sistÄ“ma needs audit trail, compliance reporting modules?

6. **Failure Mode Recovery:** Ja MT5 connection fails mid-day, aÄ£ents loses state. KÄ restore? Replay events from log? Accept state loss un restart fresh?

7. **Confidence Calibration:** Signal confidence 0.88 - kÄ to validÄ“t? Backtest historical signals ar similar confidence â†’ Check win rate. Vai confidence accurate predictor of success?
