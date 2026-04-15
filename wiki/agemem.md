---
aliases: [AgeMem, unified agentic memory, RL memory management]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [product, memory, architecture]
---

# AgeMem

統一 long-term 和 short-term memory 管理的框架 — 用 RL 訓練 agent 自己學會何時 store / retrieve / summarize / forget，而非依賴 trigger-based rules。

## Current Understanding

- **核心論點**：memory 不是兩個獨立系統（long-term + short-term），是一個 cognitive process。目前的做法把它們分開處理（各自有 heuristics、controllers、optimization），AgeMem 統一它們
- **做法**：把 memory operations 變成 tool-based actions，整合進 agent 的 policy：
  - Long-term：ADD、UPDATE、DELETE
  - Short-term：RETRIEVE、SUMMARY、FILTER
  - Agent 透過 RL 學會何時呼叫哪個 operation
- **三階段 progressive RL**：
  1. 先學 long-term memory storage
  2. 再學 short-term context management
  3. 最後在完整 task 下協調兩者
- **Step-wise GRPO**（Group Relative Policy Optimization）：把跨階段的 dependencies 轉成 learnable signals
- **Benchmark 結果**（5 個 long-horizon benchmarks）：
  - Qwen2.5-7B：AgeMem 41.96 vs Mem0 37.14（+13%）
  - Qwen3-4B：54.31 vs 44.70（gap 更大）
  - Long-term memory alone：+10-14%
  - RL training：+6%
  - Full unified：+21.7% vs no-memory baseline
- **與 openab-bot 的對比**：我們目前完全是 trigger-based rules（CLAUDE.md 硬規則 + hooks）。AgeMem 的方向是讓 agent 自己學會 memory management，不需要人寫規則。這是我們 enforcement spectrum 的下一個可能層級
- **Paper**: arxiv.org/abs/2601.01885
- **Survey 定位**（Pengfei Du 2026）：AgeMem 被歸類為 "Policy-learned Memory Management" — 五大機制家族中最先進的。Control Policy 維度上屬於 "learned control"（vs heuristic / prompted）。Survey 指出此方向能發現 non-obvious strategies（如 preemptive summarization），但有訓練成本和 interpretability 疑慮

## Key Sources

- **2026-01-12** — Elvis (omarsar0) 的推文介紹 AgeMem（56.4K views）。Source: [[raw/elvis-agemem-unified-memory]]
- **2026-03-08** — Pengfei Du survey: AgeMem 歸類為 policy-learned management。Source: [[raw/pengfei-du-memory-survey-2026]]

## Related

[[mem0]] [[agent-memory]] [[procedural-memory]] [[sleep-time-compute]] [[locomo]] [[memory-arena]] [[multimodal-memory]] [[mirix]] [[neuroscience-memory]] [[synapse]] [[reconsolidation]] [[a-mem]] [[ssgm]]
