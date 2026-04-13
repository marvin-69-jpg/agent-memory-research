---
aliases: [graph memory, knowledge graph memory, 圖記憶, 知識圖譜記憶]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [memory, architecture, retrieval]
---

# Graph Memory

用 knowledge graph 儲存記憶的方法 — 記憶不只是語意相似的事實，而是透過 relationships 連結的節點。2024 年還是實驗性質，2026 年初已進入 production。

## Current Understanding

- **Vector vs Graph 的精確區別**：
  - Vector memory：retrieve semantically similar facts（「使用者提到 Python」）
  - Graph memory：retrieve facts connected through relationships（「使用者用 Python 做 data pipeline，用 pandas，公司用 dbt，正在從 Spark 遷移」）
- **Mem0g 的實作三步驟**：
  1. Entity extractor — 從對話文字中識別 nodes
  2. Relations generator — 推斷 nodes 間的 labeled edges
  3. Conflict detector — 寫入前檢查新資訊是否與現有 graph 矛盾
- **Benchmark 結果**（LOCOMO）：Mem0g 68.4% vs Mem0 vector-only 66.9%。改善在 complex multi-hop questions（需要 relationship reasoning）
- **Latency trade-off**：Mem0g p95 2.59s vs vector-only 1.44s — graph 加了 ~1s 的 overhead
- **何時該用 graph**：complex entity relationships（醫療病人 context、企業帳號階層、技術系統相依性）。簡單的 user preference 場景用 vector-only 就夠
- **Graph backends**：Neo4j、Kuzu（embedded，不需要獨立 server process）、Neptune Analytics（AWS-native）

## Key Sources

- **2026-04-01** — Mem0 報告：graph memory 從實驗到 production。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]

## Related

[[mem0]] [[hybrid-search]] [[agent-memory]] [[brain-first-lookup]] [[entity-detection]]
