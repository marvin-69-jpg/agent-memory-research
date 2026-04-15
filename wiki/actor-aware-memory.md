---
aliases: [actor-aware memory, 來源追蹤記憶, memory provenance]
first_seen: 2026-04-13
last_updated: 2026-04-16
tags: [memory, multi-agent, architecture]
---

# Actor-Aware Memory

Multi-agent 系統中追蹤每條記憶的來源 actor — 避免一個 agent 的推論被另一個 agent 當成使用者原話。

## Current Understanding

- **問題**：naive memory 在多 agent 共享對話時失去 provenance。記憶「使用者需要部署幫助」— 是使用者自己說的？monitoring agent 推斷的？planning agent 的中間步驟？
- **Mem0 的做法**（June 2025 Group-Chat v2）：每條 stored memory 標記 source actor。Retrieval 時可按 actor 過濾
- **為什麼重要**：planning agent 搜尋記憶時可以區分「使用者實際說的」vs「另一個 agent 的推論」，避免 inference cascade（一個 agent 的猜測被下游 agent 當事實）
- **更廣的意義**：隨 agent 系統越複雜（多個 specialized agents 處理不同面向），memory layer 的 provenance tracking 對 debugging 和 reliability 越來越關鍵
- **與 entity detection 的關係**：GBrain 的 entity detection 也需要判斷「是誰說的」— user 的 original thinking 最高優先。Actor-aware memory 是同一概念在 multi-agent 場景的延伸
- **Autoreason 的反向策略**：[[autoreason]] 刻意用 fresh isolated agents（無共享 context）來切斷 authorship bias — 不是追蹤記憶來源，而是直接切斷記憶。這是 memory isolation by design，跟 actor-aware 的 provenance tracking 是同一問題的兩種解法
- **Collaborative Memory 的 formalization**：Rezazadeh et al. 2025 把 provenance 正式化為每條 fragment 的 immutable metadata（creation time、contributing user、agent、resource），用 dynamic bipartite graphs 管理存取權限。這讓 provenance 從 "nice to have" 變成 access control 的基礎
- **Memory consistency 的子問題**：Yu et al. 2026 指出 actor-aware 是 [[memory-consistency]] 的子集 — provenance 解決 "who wrote this"，但不解決 ordering/visibility（"when do others see it"、"in what order"）

## Key Sources

- **2026-04-01** — Mem0 Group-Chat v2 actor-aware memory。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]
- **2025-05-23** — Collaborative Memory 正式化 provenance 為 fragment metadata + access control 基礎。Source: [[raw/rezazadeh-collaborative-memory]]
- **2026-03-13** — Yu et al. 把 actor-aware 定位為 memory consistency 的子問題。Source: [[raw/yu-multi-agent-memory-architecture]]

## Related

[[mem0]] [[multi-scope-memory]] [[entity-detection]] [[agent-memory]] [[autoreason]] [[memory-failure-modes]] [[memory-staleness]] [[multimodal-memory]] [[mirix]] [[ssgm]] [[multi-agent-memory]] [[memory-consistency]] [[collaborative-memory-system]]
