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

## Related

[[gbrain]] [[hybrid-search]] [[brain-agent-loop]] [[compounding-memory]]
