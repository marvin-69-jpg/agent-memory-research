---
aliases: [filesystem vs database, file-based memory, virtual filesystem pattern, 檔案系統 vs 資料庫]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [memory, architecture]
---

# Filesystem vs Database

2026 年 agent memory 社群的核心辯論：用 file interface 還是用 database 做記憶儲存。兩個 camp 各有道理。

## Current Understanding

- **File camp（"file interfaces are all you need"）**：
  - Anthropic memory tool：記憶就是一組 files，storage 實作由開發者決定
  - LangSmith agent builder：資料存在 DB，但以 filesystem interface 暴露給 agent
  - Letta benchmark：grep 和 ls 在 benchmark 中**跑贏**專門的 memory/retrieval 工具
  - LlamaIndex：well-organized filesystem + semantic search 足以應付多數場景
  - **為什麼有效**：models 經過 post-training 針對 coding tasks（包括 CLI 操作）優化，所以 agent 天生擅長操作 filesystem
  - **Virtual filesystem pattern**：agent interface（filesystem）和 storage implementation（DB/vector store）解耦

- **Database camp（"filesystem is just the worst kind of database"）**：
  - dax (opencode)：filesystem = 最差的 database
  - swyx：解 agent memory 會不小心重新發明 DB — search indexes、transaction logs、locking mechanisms
  - 論點：security、permission management、schema validation 都是 DB 原生解決的問題

- **Trade-offs**：
  | 維度 | File wins | DB wins |
  |------|-----------|---------|
  | Simplicity | grep 是很強的 baseline | 需要學 query language |
  | Scale | 小規模有效 | 大規模必要 |
  | Query | grep + semantic CLI | hybrid search + aggregation |
  | Data type | Plain text | Multimodal |
  | Concurrency | Single agent OK | Multi-agent 必須 |

- **我們（openab-bot）的立場**：100% file-based。Auto-memory 是 markdown files，wiki 也是 markdown。用 keyword search（grep / `memory recall`），沒有 DB、沒有 vector store。目前 ~30 個記憶檔 + ~32 個 wiki 頁面，scale 還不是問題。

## Key Sources

- **2026-01-19** — Leonie 的推文分析兩個 camp 和 trade-offs（29.6K views）。Source: [[raw/leonie-filesystem-vs-database-debate]]

## Related

[[agent-memory]] [[hybrid-search]] [[brain-first-lookup]] [[gbrain]] [[mem0]] [[bitter-lesson-search]]
