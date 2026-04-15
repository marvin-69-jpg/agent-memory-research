---
aliases: [SYNAPSE, synapse, spreading activation memory]
first_seen: 2026-04-15
last_updated: 2026-04-15
tags: [product, memory, retrieval]
---

# SYNAPSE

受認知科學啟發的 agent memory 架構 — 用 spreading activation 取代 vector similarity 做記憶檢索。University of Georgia 團隊開發。

## Current Understanding

- **核心創新**：記憶檢索 = 圖上的 energy propagation（Collins & Loftus 1975 spreading activation theory），不是 semantic similarity search
- **Unified Episodic-Semantic Graph**：
  - Episodic nodes（每個互動 turn）+ Semantic nodes（每 5 turns LLM 抽取）
  - 三種邊：Temporal（時序）、Abstraction（episodic ↔ semantic 雙向）、Association（semantic 之間）
- **四個認知動力學機制**：
  1. Spreading activation — energy 沿邊傳播
  2. Fan effect — 出度越大越 dilute（防 hub 壟斷）
  3. Lateral inhibition — 高激活抑制低激活（注意力選擇）
  4. Temporal decay — Ebbinghaus exponential decay
- **Triple-Signal Hybrid Retrieval**：semantic similarity + activation score + PageRank，三信號融合
- **Uncertainty-Aware Rejection**：activation energy 太低 → 拒絕回答，防幻覺。Adversarial F1 96.6
- **LoCoMo SOTA**：F1 40.5（+7.2 vs A-Mem），Multi-hop +8.7
- **效率驚人**：95% token reduction、11x cost reduction、4x latency reduction
- **Ablation 證明每個機制都必要**：
  - 移除 fan effect → multi-hop 大幅下降
  - 移除 lateral inhibition → adversarial robustness 崩潰
  - 移除 temporal decay → temporal F1 50.1 → 14.2
- **對 causally grounded retrieval 的意義**：spreading activation 通過結構傳播做檢索，是 open question #7 的第一個具體解法
- **局限**：cold start（初期圖稀疏）、cognitive tunneling（lateral inhibition 過度抑制弱連結）、目前只支援文字

## Key Sources

- **2026-01-06** — Hanqi Jiang, Junhao Chen et al., University of Georgia: SYNAPSE paper (arxiv 2601.02744)。Source: [[raw/synapse-spreading-activation-memory]]

## Related

[[neuroscience-memory]] [[graph-memory]] [[hybrid-search]] [[locomo]] [[memory-staleness]] [[memory-evaluation]] [[agent-memory]] [[memory-failure-modes]] [[mem0]] [[agemem]] [[open-questions]]
