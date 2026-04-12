---
aliases: [sarahwooders]
first_seen: 2026-04-11
last_updated: 2026-04-12
tags: [people, memory]
---

# Sarah Wooders

[[letta|Letta]] CTO。「Memory isn't a plugin, it's the harness」的原始提出者。

## Current Understanding

- [[letta|Letta]]（前 [[memgpt|MemGPT]]）CTO，MemGPT 論文共同作者（UC Berkeley）
- 核心觀點：
  - 「要求把 memory 插進 agent harness，就像要求把駕駛插進一台車」
  - 管理 context = 管理 memory = harness 的核心職責
  - Harness 決定了 memory 的一切細節（CLAUDE.md 怎麼載入、compaction 後留什麼、互動能不能查詢等）
  - MemGPT 常被誤解為 RAG 或 pluggable memory tool，但實際上是 stateful agent harness（「before the term 'harness' even existed」）
  - RAG 可以是 plugin，但 retrieval 只是 memory 的一小部分，「it's hard to do much better than just grep」
- 推動 [[context-constitution]]：定義 agent 如何管理 context 來學習
- 被 [[harrison-chase]] 在 "Your Harness, Your Memory" 中大量引用

## Key Sources

- **2026-04-03** — "Why Memory Isn't a Plugin" 原始 X 文章。Source: [[raw/sarah-wooders-memory-isnt-a-plugin]]
- **2026-04-11** — Harrison Chase 引用其觀點。Source: [[raw/harrison-chase-your-harness-your-memory]]
- **2023-10-12** — MemGPT 論文共同作者。Source: [[raw/memgpt-paper]]

## Related

[[letta]] [[memgpt]] [[agent-memory]] [[agent-harness]] [[context-engineering]] [[context-constitution]] [[harrison-chase]]
