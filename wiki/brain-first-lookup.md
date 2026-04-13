---
aliases: [brain-first lookup, brain first protocol]
first_seen: 2026-04-12
last_updated: 2026-04-12
tags: [retrieval, memory]
---

# Brain-First Lookup

GBrain 的查詢優先級：永遠先查 brain，external API 是 fallback。

## Current Understanding

- **四層 fallback**：
  1. Keyword search（fast, no embeddings needed, day one 就能用）
  2. Hybrid search（needs embeddings, semantic matches）→ [[hybrid-search]]
  3. Direct slug guess（fuzzy matching）
  4. External API（FALLBACK ONLY — 只有 brain 完全沒東西才到這步）
- **為什麼 brain first**：brain 有 relationship history, 你自己的 assessments, meeting transcripts, cross-references, timeline — 沒有任何 external API 能提供這些
- 「An agent that calls Brave Search before checking the brain is wasting money and giving worse answers.」
- 連「simple questions」也要先查 brain（< 100ms for keyword search, no cost）

## Key Sources

- **2026-04-12** — GBrain brain-first-lookup guide。Source: [[raw/garry-tan-gbrain-deep]]

## Implementation

### 2026-04-12 — 應用到 openab-bot auto-memory

- **做法**：加規則到 CLAUDE.md —— 回答問題前先 `grep -r` memory/ 目錄找相關記憶，不只靠 session 開頭讀的 MEMORY.md 索引。觸發條件：使用者問過去的事、提到可能有記憶的 entity、回答可能跟 feedback 衝突時。
- **簡化**：GBrain 有四層 fallback（keyword → hybrid → slug guess → external API），我們只做第一層 keyword grep。沒有 embedding、沒有 hybrid search。
- **PR**：追溯記錄在 marvin-69-jpg/agent-memory-research#1 comment
- **觀察**：待觀察 —— 未來 session 看 bot 是否在回答前主動查 memory/

### 2026-04-13 — `memory recall` CLI：搜尋範圍擴展到 wiki

- **做法**：新增 `memory recall <query>` subcommand，同時搜尋 memory/ 和 wiki/。按 keyword 頻率排序，輸出 compiled truth 摘要。把 brain-first lookup 從「只 grep memory/」擴展到「查整個 brain（memory + wiki）」。
- **PR**：marvin-69-jpg/agent-memory-research#(pending)
- **觀察**：待觀察 —— 未來 session 回答研究相關問題時是否先跑 recall

## Related

[[gbrain]] [[hybrid-search]] [[brain-agent-loop]] [[compounding-memory]]
