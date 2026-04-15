---
aliases: [memory consistency, 記憶一致性, multi-agent consistency]
first_seen: 2026-04-16
last_updated: 2026-04-16
tags: [memory, multi-agent, architecture]
---

# Memory Consistency

多個 agent 同時讀寫共享記憶時，如何保證一致性。Yu et al. 2026 認為這是 multi-agent memory 最大的未解問題。

## Current Understanding

### 來自電腦架構的類比

在電腦架構中，consistency model 定義：一個 read 能看到哪些 update、concurrent updates 以什麼順序被觀察到。Agent memory 需要類似的概念，但更難。

### 兩個面向

1. **Read-time conflict handling**：記憶會跨版本演化，stale artifacts 可能殘留。當 Agent A 在 t=1 寫入一個 fact，Agent B 在 t=2 更新了它，Agent C 在 t=3 讀取 — C 看到的是哪個版本？
2. **Update-time visibility & ordering**：一個 agent 的寫入何時對其他 agent 可見？Concurrent writes 的觀察順序應該一致嗎？

### 為什麼比經典 DB consistency 更難

- **Heterogeneous artifacts**：不只是 key-value pairs，而是 evidence、tool traces、plans、summaries — 不同型態有不同的 conflict resolution 語義
- **Semantic conflicts**：兩個 agent 寫的東西字面上不衝突但語義上矛盾。例如 Agent A 記「使用者偏好 Python」，Agent B 從使用者的新行為推斷「使用者正在轉向 Rust」
- **Environment-coupled**：記憶的正確性依賴於外部環境狀態，不是 self-contained

### 現實中的弱 consistency

大多數系統（包括 openab-bot）用的是 last-write-wins 的弱 consistency：
- 我們的 MEMORY.md 就是一個 shared file，多個 session 可能同時改
- 沒有 versioning、沒有 conflict detection、沒有 ordering guarantee
- 目前 OK 是因為 concurrent writes 極少（一次通常只有一個 session 在跑）

### Practical direction

Yu et al. 建議：make **versioning、visibility、conflict-resolution rules** explicit — 讓 agents agree on what to read and when updates take effect。

Collaborative Memory 的做法是不解決 general consistency，而是用 **access control** 縮小 conflict surface — 如果 Agent A 看不到 Agent B 的 memory，就不會有 conflict。

## Key Sources

- **2026-03-13** — Yu et al. — 定義 multi-agent consistency 為核心未解問題。Source: [[raw/yu-multi-agent-memory-architecture]]
- **2025-05-23** — Rezazadeh et al. — 用 access control 縮小 conflict surface。Source: [[raw/rezazadeh-collaborative-memory]]

## Related

[[multi-agent-memory]] [[actor-aware-memory]] [[memory-staleness]] [[memory-failure-modes]] [[multi-scope-memory]] [[collaborative-memory-system]] [[open-questions]]
