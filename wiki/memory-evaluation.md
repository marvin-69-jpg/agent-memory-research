---
aliases: [memory evaluation, memory benchmark, 記憶評估, evaluation paradox]
first_seen: 2026-04-14
last_updated: 2026-04-15
tags: [benchmark, memory]
---

# Memory Evaluation

Agent memory 的評估方法論 — 從 passive recall 到 agentic tasks，以及為什麼評估本身可能是不可能的。

## Current Understanding

### Evaluation Paradox（Chrys Bader）

> 驗證記憶系統需要 ground truth，但真實對話記憶跨月/年的 ground truth 超過任何 context window，也超過任何人能標註的範圍。任何用來評估完整歷史的 judge 都有跟被評估系統一樣的 context 限制。

→ 所有新方案都是「不同的 trade-offs 包裝成 solution」，沒人能證明自己的方法 works

### Benchmark 演進

| Benchmark | 層級 | 測什麼 | 限制 |
|---|---|---|---|
| [[locomo\|LoCoMo]] | Passive recall | 長對話理解、QA、摘要 | 只測 recall，不測決策 |
| **MemBench** (Tan 2025) | Multi-session | 多 session + 明確 forgetting | — |
| **MemoryAgentBench** (Hu 2025) | Agentic tasks | 記憶影響 action | ICLR 2026，四核能力 |
| [[memory-arena\|MemoryArena]] (He 2026) | Cross-session | 跨 session 一致性 + cost-effectiveness | LoCoMo 滿分的模型在這裡 40-60% |
| **ScreenshotVQA** (MIRIX 2025) | Multimodal | 從螢幕截圖建構記憶 + QA | 首個多模態記憶 benchmark |
| **M3-Bench** (ByteDance 2025) | Multimodal agentic | 高層認知（person understanding, cross-modal reasoning） | 首個 embodied agent 多模態記憶 benchmark |

### Key Findings from Survey

1. **"Long context is not memory"** — 超長 context window 模型在需要 selective retrieval 的任務上仍輸給專用 memory 系統
2. RAG 有幫助但距 human-level 仍有顯著差距（relevance & freshness）
3. **Selective forgetting** 嚴重被低估 — 幾乎沒有系統被明確評估
4. **Cross-session coherence** 是未解決的重大挑戰
5. Cost-effectiveness 評估普遍缺席

### Helix Benchmark — Procedural Memory Evaluation

[[helix|Helix]] 提供了 procedural memory 的具體 benchmark：50 個 agentic payment 錯誤場景，跨 4 個平台（x402/Coinbase、Tempo、Monad、Privy）。測量維度：

| 指標 | Without Helix | With Helix (warm) |
|---|---|---|
| LLM calls | 54 | 0 |
| Inference cost | $0.49 | $0.00 |
| Repair latency | 2,140ms | 1.1ms |

這是目前看到**最具體的 memory ROI 數據** — 直接量化了「記住修復策略」vs「每次重新診斷」的成本差異。回應了 cost-effectiveness 評估普遍缺席的問題。

### Four-Layer Metric Stack（Pengfei Du）

1. **Task effectiveness** — 任務完成品質
2. **Memory quality** — 準確性、freshness
3. **Efficiency** — token、latency、storage 成本
4. **Governance** — 隱私、deletion、合規

## Key Sources

- **2026-04-12** — Chrys Bader: evaluation paradox。Source: [[raw/chrysb-long-term-memory-unsolved]]
- **2026-04-14** — Helix: procedural memory benchmark，50 場景跨 4 平台，量化 memory ROI。Source: [[raw/nicholas-helix-self-healing-agents]]
- **2026-03-08** — Pengfei Du: benchmark 演進 + four-layer metric stack。Source: [[raw/pengfei-du-memory-survey-2026]]

## Related

[[locomo]] [[memory-arena]] [[agent-memory]] [[chrysb]] [[memory-staleness]] [[memory-failure-modes]] [[helix]] [[gene-map]] [[memgpt]] [[open-questions]] [[multimodal-memory]] [[mirix]]
