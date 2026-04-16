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
- **Temporal knowledge graph**（[[yohei-nakajima]]）：Zep / Graphiti 代表時序知識圖譜方向 — 不只是 entity relationships，還追蹤 relationships 的時間演化。支援「X 在 2024 年用 Python，2025 年改用 Go」這種時序推理
- **Graph 在 retrieval 中的角色**（[[chrysb]]）：Graph traversal 擅長「系統知道什麼關於這個 entity 以及所有相連的東西」。跟 semantic search（概念相似）和 full-text（精確詞組）互補，不是替代 → [[hybrid-search]]
- **Forgetting propagation 問題**（[[chrysb]]）：刪除 source conversation 時，graph 中 extracted facts 變成 orphaned — 真正的 forgetting 需要 provenance tracking + cascade delete → [[memory-staleness]]
- **Survey 定位**（Pengfei Du）：graph 屬於 Representational Substrate 中的 "structured stores" 分類。適合 complex entity relationships，但加了 ~1s latency overhead
- **多模態延伸**（M3-Agent）：entity-centric multimodal graph — 同一 entity 的臉、聲音、文字知識相連。用 weight-based voting 解決衝突，外部工具做 face_id / voice_id 跨 clip 追蹤。Graph memory 從純文字 relationship 擴展到多模態 entity binding → [[multimodal-memory]]
- **Spreading Activation**（SYNAPSE）：受 Collins & Loftus 1975 啟發，記憶檢索 = graph 上的 energy propagation。加入 fan effect（出度 dilute）、lateral inhibition（注意力選擇）、temporal decay（Ebbinghaus）。LoCoMo F1 40.5 SOTA，multi-hop +8.7。graph 不只是 static structure，加入 cognitive dynamics 後成為 active reasoning mechanism → [[synapse]]、[[neuroscience-memory]]

## Key Sources

- **2026-04-01** — Mem0 報告：graph memory 從實驗到 production。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]
- **2026-04-12** — Chrys Bader: graph traversal 在 retrieval 中的角色 + forgetting propagation 問題。Source: [[raw/chrysb-long-term-memory-unsolved]]
- **2025-08-28** — Yohei Nakajima: Zep/Graphiti temporal knowledge graph。Source: [[raw/yohei-nakajima-rise-of-ai-memory]]

## Related

[[mem0]] [[hybrid-search]] [[agent-memory]] [[brain-first-lookup]] [[entity-detection]] [[chrysb]] [[yohei-nakajima]] [[memory-staleness]] [[multimodal-memory]] [[mirix]] [[neuroscience-memory]] [[synapse]] [[a-mem]] [[reconsolidation]] [[fluxmem]]
