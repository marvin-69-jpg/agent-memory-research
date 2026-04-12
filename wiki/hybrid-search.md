---
aliases: [hybrid search, RRF fusion, vector + keyword search]
first_seen: 2026-04-12
last_updated: 2026-04-12
tags: [retrieval, architecture]
---

# Hybrid Search

結合 vector search 和 keyword search 的檢索策略，透過 Reciprocal Rank Fusion（RRF）合併排名。在 [[gbrain|GBrain]] 中有完整實作。

## Current Understanding

- **為什麼需要 hybrid**：
  - Keyword search 只能找到字面匹配，會錯過概念相關的結果
  - Vector search 只能找到語義相近的，exact phrase 可能被 embedding 稀釋
  - 兩者互補
- **GBrain 的完整 pipeline**：
  1. Multi-query expansion（Claude Haiku 把原始 query 展開成多種表述）
  2. Vector search（HNSW cosine，text-embedding-3-large 1536-dim）
  3. Keyword search（Postgres tsvector + ts_rank）
  4. RRF Fusion：`score = sum(1/(60 + rank))`
  5. 4-Layer Dedup：best chunk per page → cosine > 0.85 去重 → type diversity 60% cap → per-page chunk cap
  6. Stale alerts：compiled truth 比 timeline 舊的標記提醒
- Embedding、chunking、search fusion 是 engine-agnostic — 只有 raw search 是 engine-specific

## Key Sources

- **2026-04-12** — GBrain README 的 search 架構說明。Source: [[raw/garry-tan-gbrain]]

## Related

[[gbrain]] [[agent-memory]] [[context-engineering]]
