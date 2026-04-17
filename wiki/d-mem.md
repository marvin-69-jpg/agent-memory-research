---
aliases: [D-MEM, dopamine-gated memory, RPE memory routing]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [product, memory, architecture]
---

# D-MEM

Dopamine-gated agentic memory（arxiv 2603.14597，UCSD/CMU）。直接針對 [[a-mem]] 的 O(N²) 寫入瓶頸：不是每個 utterance 都該觸發 memory evolution。用神經科學的 Reward Prediction Error 當 gate，把 80% 的對話 noise 直接 SKIP。

## Current Understanding

### 動機：A-Mem 的 scaling 問題

[[a-mem]] 的「append-and-evolve-all」設計把每個 input 都跑完整 evolution pipeline：
- 每次 utterance → 找 top-k neighbors → LLM 判斷是否更新每個鄰居 → 改 context/keywords/tags
- 結果：write-latency 是 O(N²)，token cost unbounded，conversational filler 污染 knowledge graph

D-MEM 的核心觀察：**人腦不是這樣**。Ventral Tegmental Area（VTA）的 dopamine 只在 prediction error 高時才觸發 consolidation —— 大部分 input 是 routine，不需要重組長期記憶。

### Agentic RPE 公式

```
RPE(x_t) = min(1.0, I(Utility(x_t) ≥ τ) · [Utility(x_t) × (Surprise(x_t) + β)])
```

兩個維度：
- **Surprise**：embedding 跟既有記憶的 max cosine distance，z-score normalize（解 anisotropy 問題）+ sigmoid。**不需要 LLM call**。
- **Utility**：輕量 LLM call 分三類 — Transient（phatic filler，utility=0）/ Short-term（days-weeks）/ Persistent（months+）

`I(·)` 是 hard utility threshold —— 沒有 utility 就算 surprise 再高也是 0（防 high-entropy noise 觸發 evolution）。`β=0.4` 是 utility safety net，讓 useful but expected inputs 仍能進 STM。

### 三層 Critic Router

| Tier | 觸發 | 行為 | 成本 |
|------|------|------|------|
| **SKIP** | RPE < 0.3 | bypass memory pipeline，存 raw 進 Shadow Buffer | O(0) |
| **CONSTRUCT_ONLY** | 0.3 ≤ RPE < 0.7 | 建 atomic note 進 STM buffer，**不做 graph evolution** | O(1) |
| **FULL_EVOLUTION** | RPE ≥ 0.7 | 完整 A-Mem pipeline：node 寫入 + linking + retroactive update | O(N) |

Cold-start 時前 N 次強制走 CONSTRUCT_ONLY（避免 sparse memory 上的 false-positive evolution）。

### Shadow Buffer：對抗 SKIP 的 risk

SKIP 的 raw text 存進 O(1) FIFO Shadow Buffer。當 knowledge graph retrieval 信心低時，fallback 到 buffer。這讓 D-MEM 對 adversarial queries（問被 skip 掉的 trivial 細節）仍有防禦。

### LoCoMo-Noise Benchmark

D-MEM 順手提出新 benchmark。原 [[locomo]] 假設每個 turn 都有意義 —— 不真實。LoCoMo-Noise 用 GPT-4o-mini 注入 phatic fillers (40%) / status updates (30%) / tangent remarks (30%)，noise ratio ρ=0.75。

這是 [[memory-evaluation]] 演進的一步：從 retrieval 評估到 noise-robust 評估。

### 結果（vs A-Mem on LoCoMo-Noise）

| Metric | A-Mem | D-Mem | 差異 |
|--------|-------|-------|------|
| API tokens | 1.64M | 319K | **−80.5%** |
| Multi-hop F1 | 0.365 | 0.412 | +12.9% |
| Single-hop F1 | 0.208 | 0.246 | +18.3% |
| Adversarial F1 | 0.388 | 0.412 | +6.2% |

**Routing pattern**：SKIP 53.9% real turns + 43.2% noise turns（real turns 包含很多 social acknowledgement，utility 接近 0）。FULL_EVOLUTION 僅在 high-utility & high-surprise quadrant 觸發，sparse activation。

無 noise 時 D-MEM Single-hop 反而落後 A-Mem（21.6% vs 44.7%）—— 因為 single-hop 的 target 通常是低 utility 事實，被 SKIP 掉。論文承認這是 principled trade-off，不是 bug。

### 與 [[reconsolidation]] 的關係

A-Mem 的 reconsolidation 是 **uniform write-triggered**（每次寫都更新鄰居）。D-MEM 是 **selective write-triggered**（只有 high-RPE 才更新）。這呼應神經科學的 prediction error gating —— 不是所有經驗都該 reconsolidate。

對 openab-bot 的啟示：目前 `memory.py reconsolidate` 是 manual 觸發。要不要學 D-MEM 加 RPE-style gate，避免每次 recall 都 LLM call？

### 與其他系統的位置

- [[a-mem]]: D-MEM 直接的前身與比較對象
- [[ssgm]]: 也處理 evolution governance，但 SSGM 從 safety angle，D-MEM 從 efficiency angle —— 互補
- [[memory-staleness]]: D-MEM 的 SKIP tier 直接避免 stale low-utility 累積
- [[neuroscience-memory]]: dopamine RPE 是新的生物學 motif，加在 hippocampal replay / spreading activation 之外

## Key Sources

- **2026-03-15** — D-MEM: Dopamine-Gated Agentic Memory via Reward Prediction Error Routing。Source: [[raw/song-d-mem]]

## Related

[[a-mem]] [[reconsolidation]] [[ssgm]] [[neuroscience-memory]] [[locomo]] [[memory-evaluation]] [[memory-staleness]] [[sleep-time-compute]] [[fluxmem]] [[agent-memory]] [[memory-failure-modes]] [[memory-worth]]
