---
aliases: [Memory-R1, memory-r1, RL memory management]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [system, rl, memory, benchmark]
---

# Memory-R1

LMU Munich + MCML + Cambridge + 多校合作，2025。用 RL（PPO/GRPO）訓練兩個 agent 分別負責 memory management 和 memory utilization，只用 152 QA pairs 就在 LoCoMo 上拿到 SOTA。

## Current Understanding

- **核心問題**：LLM 外部 memory 系統的 CRUD 操作多半是 heuristic-driven 或靠 in-context instructions，缺乏 learned mechanism。RAG retrieval 回來的記憶 noise 太多，agent 不知道怎麼 filter
- **Two-agent architecture**：
  1. **Memory Manager**：對每個新 dialogue turn 決定 ADD / UPDATE / DELETE / NOOP
  2. **Answer Agent**：從 memory bank RAG 回 60 條候選記憶，先做 **Memory Distillation**（filter noise）再 reasoning
- **Outcome-driven RL**：Memory Manager 的 reward 來自 downstream Answer Agent 的 Exact Match 分數。不需要標注每個 memory 操作的 ground truth — 只要最終答案對就好
- **152 QA pairs**：極高 data efficiency，遠低於一般 RL 訓練需要的資料量
- **Memory Distillation 是關鍵創新**：解決 "lost in the middle" 問題 — 不只 retrieve，更要在 reasoning 前 filter

### 結果

| Benchmark | vs prev SOTA | Detail |
|---|---|---|
| LoCoMo | F1 +28.5%, BLEU +34.0%, Judge +30.2% | vs MemoryOS (LLaMA-8B) |
| MSC | consistent improvement | zero-shot transfer |
| LongMemEval | consistent improvement | zero-shot transfer |

- RL > SFT（用 GPT-5 trajectory 做 SFT 都不如 RL）
- 跨 3B / 7B / 14B 都有效
- Accuracy-latency trade-off：比 reranker pipeline 更準且更快
- Compounding effect：Memory Manager 越強，Answer Agent 表現越好

### RL + Memory 四條路的定位

| 路線 | 系統 | RL 訓練什麼 | Architecture |
|---|---|---|---|
| 管理 external memory（single） | [[deltamem]] | Memory CRUD 操作 | Single-agent |
| 管理 external memory（multi） | **Memory-R1** | Manager + utilizer 分工 | Two-agent |
| 從 memory 畢業 | [[empo2]] | 內化 memory-guided 行為 | Single-agent |
| Internal state 取代 full context | [[mem1]] | Memory consolidation + reasoning | Single-agent |

Memory-R1 vs DeltaMem 的 single/multi-agent 之爭：DeltaMem 在 PersonaMem 上證明 single-agent 更簡潔，Memory-R1 在 LoCoMo 上用 two-agent 拿到 SOTA。可能不是 architecture 決定勝負，而是 reward design（Levenshtein vs downstream QA outcome）和 benchmark 特性的差異。

### 對 Agent Memory Research 的意義

Memory-R1 最令人印象深刻的是 **data efficiency**：152 QA pairs 就夠訓練 RL。這意味著 RL-based memory management 不需要大量標注資料，可以用 task outcome 作為自然的 reward signal。對我自己的系統來說，這暗示一個可能性：如果有辦法定義「這次 recall 的記憶有沒有幫到回答」的 signal，就有可能用很少的例子訓練一個更好的記憶管理策略。

Memory Distillation 的概念也很實用：不是所有 retrieved 記憶都值得放進 context。先 filter 再 reason，而不是把所有候選記憶都塞給 LLM。

## Key Sources

- **2025-08-28** — Yan et al., arxiv 2508.19828: Memory-R1 framework。Source: [[raw/yan-memory-r1-rl-memory]]

## Related

[[agent-memory]] [[deltamem]] [[empo2]] [[mem1]] [[agemem]] [[locomo]] [[memory-evaluation]] [[hybrid-search]] [[memory-failure-modes]]
