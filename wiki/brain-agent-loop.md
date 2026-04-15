---
aliases: [brain-agent loop, read-write loop, compounding loop]
first_seen: 2026-04-12
last_updated: 2026-04-12
tags: [memory, architecture]
---

# Brain-Agent Loop

[[gbrain|GBrain]] 的核心運作模式：每次對話都讓 brain 更聰明，每次 brain lookup 都讓回應更好。是 [[compounding-memory]] 的具體實作。

## Current Understanding

- **Loop 流程**：Signal → DETECT entities（async sub-agent）→ READ brain first → RESPOND with context → WRITE brain pages → SYNC index
- **Two Invariants**：
  1. Every READ improves the response — 不查 brain 就回答 = 比你能給的最佳答案更差
  2. Every WRITE improves future reads — 不更�� brain = 未來的查詢會有 gap
- **關鍵紀律**：
  - Read BEFORE responding, not after（brain context 讓回應更好）
  - Don't skip the write step（「I'll update later」= never）
  - Sync after every write batch（不然 search index 是 stale 的）
  - External APIs are fallback, not primary → [[brain-first-lookup]]
- **Entity detection 是 async sub-agent**：每個 inbound message 都 spawn（用 Sonnet 不用 Opus），不 block 主對話
- **Dream cycle**：agent 在使用者睡覺時跑 enrichment、修 citation、consolidate memory

## Key Sources

- **2026-04-12** — GBrain Skillpack brain-agent-loop guide。Source: [[raw/garry-tan-gbrain-deep]]

## Related

[[gbrain]] [[compounding-memory]] [[brain-first-lookup]] [[entity-detection]] [[garry-tan]] [[enrichment-pipeline]] [[sleep-time-compute]] [[thin-harness-fat-skills]]
