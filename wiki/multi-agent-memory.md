---
aliases: [multi-agent memory, 多 agent 記憶, shared agent memory]
first_seen: 2026-04-16
last_updated: 2026-04-16
tags: [memory, multi-agent, architecture]
---

# Multi-Agent Memory

多個 LLM agent 共享、同步、存取記憶的系統設計。是 agent memory 最複雜的子領域 — 把單 agent 的所有問題乘以 N，再加上 consistency 和 access control。

## Current Understanding

### 兩種基本 paradigm（來自電腦架構）

| Paradigm | 優點 | 缺點 | Agent 世界的例子 |
|---|---|---|---|
| **Shared memory** | 知識重用容易 | 需要 coherence protocol，否則互相覆蓋、讀到 stale data | 共享 vector store、shared PVC filesystem |
| **Distributed memory** | 隔離性好、scalable | 需要顯式同步，state divergence 常見 | 每個 agent 自有 memory + 選擇性 sync |

實際系統都在中間：local working memory + selectively shared artifacts。openab-bot 目前是 shared memory paradigm（PVC filesystem），最弱的 consistency model（last-write-wins on MEMORY.md）。

### 三層 memory hierarchy

Yu et al. 2026 提出跟電腦架構對照的三層：

1. **I/O layer**：agent 的輸入輸出介面（文字、圖片、API calls）
2. **Cache layer**：快速、有限容量，用於即時 reasoning（KV cache、embedding、recent tool calls）
3. **Memory layer**：大容量、慢存取，用於 retrieval 和 persistence（vector DB、graph DB、document store）

核心原則：agent performance 是 **end-to-end data movement problem**。資訊卡在錯的 layer → reasoning 品質下降。

### 兩個缺失的 protocol

1. **Cache sharing protocol** — 一個 agent 的 cache 結果如何被另一個 agent 重用？KV cache compaction（Latent Briefing）是早期嘗試。
2. **Memory access protocol** — 權限、scope、granularity 都沒標準化。一個 agent 能讀另一個的 long-term memory 嗎？Read-only 還是 read-write？存取單位是 document、chunk、還是 trace segment？

### Collaborative Memory：第一個完整實作

Rezazadeh et al. 2025（Accenture）提出了具體架構：

- **Dynamic bipartite access graphs**：User↔Agent 和 Agent↔Resource 兩張圖隨時間演化
- **Two-tier memory**：Private（per-user）+ Shared（per-agent，跨 user）
- **Fine-grained policies**：Read policy 動態建構 memory view；Write policy 決定 fragment 是 private 還是 shared，可做 anonymization/redaction
- **結果**：accuracy 不降（>0.90），resource usage 降 61%（memory reuse 效果）
- **動態 access control**：permission grant/revoke 即時反映，strict policy adherence

### 核心未解問題：Memory Consistency

見 [[memory-consistency]]。這是 multi-agent memory 最根本的問題。

## Key Sources

- **2026-03-13** — Yu et al. "Multi-Agent Memory from a Computer Architecture Perspective" — 定義問題框架。Source: [[raw/yu-multi-agent-memory-architecture]]
- **2025-05-23** — Rezazadeh et al. "Collaborative Memory" — 第一個帶 access control 的完整實作。Source: [[raw/rezazadeh-collaborative-memory]]
- **2026-04-01** — Mem0 Group-Chat v2 actor-aware memory。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]

## Related

[[memory-consistency]] [[actor-aware-memory]] [[multi-scope-memory]] [[agent-memory]] [[collaborative-memory-system]] [[filesystem-vs-database]] [[brain-first-lookup]] [[open-questions]]
