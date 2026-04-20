---
aliases: [LOCOMO, LOCOMO benchmark, Long-term Conversational Memory, LoCoMo-Noise]
first_seen: 2026-04-13
last_updated: 2026-04-21
tags: [benchmark, memory]
---

# LOCOMO

第一個專門為 long-term conversational memory 設計的標準化 benchmark。讓不同 memory 架構第一次能在同一個評估集上公平比較。

## Current Understanding

- **設計目的**：測試跨多 session 的記憶回憶與理解能力，包含不同難度等級和問題類型
- **之前的問題**：memory quality 大多是自報或用不可重現的 ad hoc task 評估。LOCOMO 解決了測量問題
- **四維評估框架**：
  1. BLEU Score — token 層級的回應與真值相似度
  2. F1 Score — response token 的 precision/recall harmonic mean
  3. LLM Score — LLM judge 判斷的二元事實正確性（0 或 1）
  4. Token Consumption — 產出最終答案所需的 total tokens
  5. Latency — search 和 response generation 的牆鐘時間
- **多維評估的意義**：防止在單一軸上優化而犧牲其他。高 accuracy 但 26,000 tokens/query 不 production-viable，低 latency 但差 recall 也沒用
- **已跑過的 10 種方法**：LoCoMo baseline、ReadAgent、MemoryBank、MemGPT、A-Mem、LangMem、RAG、Full-context、OpenAI Memory、Zep
- **Open problem**：LOCOMO 測的是 general long-term recall，不能反映 application-specific quality。Medical assistant 和 coding assistant 對「正確的記憶行為」定義不同

## Key Sources

- **2026-04-01** — Mem0 報告中詳細介紹 LOCOMO 的評估框架和 10 種方法的 benchmark 結果。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]

- **後續批評**：DAIR.AI 指出 LOCOMO 有根本局限 — 在 LOCOMO 上接近飽和的模型在 real agentic scenarios 表現很差。Memory 不只是 retrieval，是「在正確時機應用正確 context 做出好決策」→ [[memory-arena|MemoryArena]] 試圖補這個缺口
- **Survey 定位**（Pengfei Du 2026）：LOCOMO 被歸類為 "passive recall" 層級的 benchmark。Survey 提出更完整的四層 metric stack（task effectiveness / memory quality / efficiency / governance）→ [[memory-evaluation]]
- **原始論文**：Snap Research + UNC Chapel Hill，ACL 2024。300 turns / 9K tokens / 35 sessions。arxiv 2402.17753

### Extension: LoCoMo-Noise（D-MEM 2026）

[[d-mem]] 提出 LoCoMo-Noise：原 LoCoMo 假設每 turn 都有意義，跟真實對話不符。LoCoMo-Noise 用 GPT-4o-mini 注入三類 noise（phatic fillers 40% / status updates 30% / tangent 30%），noise ratio ρ=0.75。

這暴露了一個原 benchmark 看不到的失敗模式：**append-and-evolve-all 系統（[[a-mem]]）的 token cost 在 noisy 環境會爆炸**（1.64M vs D-Mem 的 319K）。LoCoMo-Noise 把 token efficiency 從 nice-to-have 升級成 必要 metric。

### 近期 LOCOMO 成績（2026-04-21 補充）

| 系統 | 指標 | 分數 |
|------|------|------|
| APEX-MEM（GPT5）| overall accuracy | 88.88% |
| MIRIX | overall accuracy | 85.38% |
| TA-Mem | temporal F1 | 55.95（所有系統最高）|
| MemR3（疊在基礎 retriever 上）| 提升幅度 | +7.29% |

TA-Mem 在時序問題特別強，MemR3 是 plug-in 方式提升任何基礎系統。

## Related

[[mem0]] [[memgpt]] [[agent-memory]] [[compounding-memory]] [[memory-arena]] [[memory-evaluation]] [[agemem]] [[mirix]] [[multimodal-memory]] [[neuroscience-memory]] [[synapse]] [[a-mem]] [[d-mem]] [[fluxmem]] [[memwright]] [[mstar]] [[gam]] [[memu]] [[xmemory]] [[stitch]] [[deltamem]] [[memory-r1]] [[ta-mem]] [[memr3]] [[apex-mem]]
