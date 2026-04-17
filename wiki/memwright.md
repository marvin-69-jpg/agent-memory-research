---
aliases: [Memwright, agent-memory library, deterministic memory]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [product, memory, infrastructure, multi-agent, retrieval]
---

# Memwright

aarjay singh 開發的 Python agent memory library（MIT，github.com/bolnet/agent-memory）。核心主張：**memory 是 infrastructure，不是 prompt engineering** —— 推到極致就是 **zero LLM in the critical path**。

## Current Understanding

### 核心原則：zero LLM in retrieval

對抗目前主流的 LLM-in-the-loop retrieval（query rewrite、re-rank、summarize chunks）。理由很硬：

| 問題 | 實際後果 |
|---|---|
| Non-determinism | 同樣 query 不同 ranking，debug 變考古學 |
| Latency | 每次 recall 加 500–2000ms 在 critical path |
| Cost | Planner/executor loop 跑 50 次 → 50× token bill |
| Untestable | 無法寫「給這 10 條 memory + 這個 query → top-3 應該是 X/Y/Z」的 unit test |

Memwright 的解法：**embedding 在 write time 算一次（local all-MiniLM-L6-v2），retrieval 是純數學 + graph traversal**。

### 5-layer 檢索 pipeline

```
Query
  ↓
[1] Tag Match       — SQLite FTS, exact + fuzzy token
  ↓
[2] Graph Expansion — NetworkX BFS, depth 2 from matched entities
  ↓
[3] Vector Search   — ChromaDB cosine, 384-D embeddings
  ↓
[4] Fusion + Rank   — RRF (k=60) + PageRank + confidence decay
  ↓
[5] Diversity       — MMR (λ=0.7) + greedy token-budget pack
  ↓
Top-K, deterministic, unit-testable
```

每層是 pure function。Test suite 607 cases，no Docker / no API keys。這比 [[hybrid-search|GBrain 的 hybrid search]] 多了 **graph BFS expansion** 和 **PageRank weighting**，並把 LLM-driven query expansion 完全拿掉。

### Multi-agent 是 first-class，不是 afterthought

絕大多數 memory library 把 agent 當 singleton。Memwright 直接內建：

- **6 個 RBAC role**：ORCHESTRATOR / PLANNER / EXECUTOR / RESEARCHER / REVIEWER / MONITOR，每個有不同 read/write 權限
- **Namespace isolation 在 row 層強制**：tenant column 在每張 table，每個 query 都 filter，不靠 application code 自律
- **Provenance chain**：每條 memory 都帶 `source_id` / `content hash` / `ingest timestamp` / `agent role`，可以重建「誰告訴系統什麼」
- **Per-agent token budgets + write quotas**：失控的 executor 不能把 memory 灌爆

這跟 [[actor-aware-memory]] 的核心訴求重合，但 Memwright 是把它當 infrastructure 寫死在 schema，不是套在上層。也跟 [[collaborative-memory-system]] 的 dual-tier + immutable provenance 同源思想，差別在 collaborative-memory 主打 user-vs-agent 分層，Memwright 主打 agent role hierarchy。

### Temporal correctness：never overwrite, supersede

```
fact = (claim, valid_from, valid_to)
```

新 fact 矛盾舊 fact 時 → 不刪舊的，**close 它**（設 valid_to）。`recall(as_of=...)` 可以回放任意時間點的 memory state。

這是 [[compiled-truth-pattern]] 的 timeline 路線推到 schema 層級。對 audit（"desk 在 3/12 知道什麼？"）和 debug（"planner 昨天為什麼那樣決定？"）有直接價值。也呼應 [[memory-staleness]] 的 open problem：staleness 不該是 silent overwrite，而是 explicit transition。

### 同 API、6 種 backend

```python
from agent_memory import AgentMemory
mem = AgentMemory("./store")  # 本機 zero-config
mem.add("Planner decided to use Rust for the hot path", tags=["decision"])
results = mem.recall("what did we pick for the hot path?", k=5)
```

同樣的 code 跑 SQLite+ChromaDB+NetworkX（local）/ Postgres+pgvector+AGE / ArangoDB / AWS ECS / Azure Cosmos DiskANN / GCP AlloyDB+ScaNN+AGE，附 reference Terraform。

### Benchmark

LOCOMO v2：**81.2%**。

| System | LOCOMO v2 |
|---|---|
| OpenAI memory | 52.9% |
| [[mem0]] | 66.9% |
| [[letta]] | 74% |
| Zep | ~75% |
| Memwright | 81.2% |
| MemMachine | 84.9% |

作者誠實標註「不是 SOTA，gap 是 embedding model，下個 release 會升」。

## Why this matters for agent-memory-research

- **對 [[a-mem]] / [[reconsolidation]] 的反向 thesis**：A-Mem 用 LLM 在寫入時做 evolution；Memwright 主張連 retrieval 都不該有 LLM。兩條路線都試圖解 [[memory-failure-modes]] 的不同問題：A-Mem 解 organization rot，Memwright 解 determinism / cost / testability。不是誰對誰錯 —— 是不同 deployment 取捨
- **Determinism 作為 evaluation enabler**：[[memory-evaluation]] 的 paradox 之一是「真實長對話沒有 ground truth」。Memwright 的 fixture-based unit test 提供另一層 evaluation：not「這個 ranking 對嗎」，而是「這個 ranking 一致嗎」。一致性是正確性的必要條件
- **Provenance + temporal 對 openab-bot 的啟發**：我們現在的 auto-memory 用 git history 當 timeline（[[compiled-truth-pattern]]），但沒有 schema-level 的 valid_from/valid_to。如果以後做 multi-agent（多個 sub-agent 分工寫 memory），actor tag + temporal close 會變成必要

## Critique / Open Questions

- **Embedding 在 write time 算一次** → 換 embedding model 要 reindex 所有 memory，跟 [[bitter-lesson-search]] 的「資料超指數成長」遇上：reindex N=1M 條需要多久？
- **Zero LLM 在 retrieval** 對「query 模糊但 intent 明確」的場景可能輸 LLM-rerank：「之前那個關於 dedup 的東西」這種代詞 query，沒有 LLM 解 reference 會找不到
- **6 role RBAC 假設 agent hierarchy 固定** → 跟 [[multi-scope-memory]] / [[collaborative-memory-system]] 的 dynamic access control 怎麼整合？

## Key Sources

- **2026-04-15** — aarjay singh, "Why I stopped putting LLMs in my agent memory retrieval path", dev.to. HN discussion #47773981. Source: [[raw/aarjay-memwright]]

## Related

[[hybrid-search]] [[actor-aware-memory]] [[collaborative-memory-system]] [[compiled-truth-pattern]] [[memory-evaluation]] [[locomo]] [[a-mem]] [[mem0]] [[agent-memory]] [[mstar]] [[memu]] [[xmemory]]
