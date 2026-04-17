---
source: dev.to
author: aarjay singh
url: https://dev.to/aarjay_singh_0f76e7ca03bf/why-i-stopped-putting-llms-in-my-agent-memory-retrieval-path-4bia
date: 2026-04-15
fetched: 2026-04-17
tags: [agent-memory, infrastructure, multi-agent, governance, retrieval, locomo]
---

# Why I stopped putting LLMs in my agent memory retrieval path

aarjay singh, dev.to, 2026-04-15

> Every agent pipeline I've touched in the last eighteen months reinvents memory, and most of them do it badly.
>
> Planner decisions never reach the executor. Giant prompts get passed between agents as "context." Tokens burn on stale data. An LLM call sits in the retrieval path, so the same query returns different ranked results on different runs — which makes the system impossible to reason about and impossible to unit-test.
>
> The fix, once I'd seen it happen enough times, is boring: **treat memory as infrastructure, not as prompt engineering.**
>
> That's what Memwright is.

## The problem with LLM-in-the-loop retrieval

A lot of "agentic memory" libraries shell out to an LLM during recall — to rewrite the query, to re-rank results, to summarize retrieved chunks. In production, it's a liability:

- **Non-determinism.** Same inputs, different outputs. Debugging a misranked memory becomes an archaeology expedition.
- **Latency.** You just added 500–2000ms to every recall, in the critical path of every agent step.
- **Cost.** Every retrieval is a paid call. In a planner/executor loop that fires 50 times, that's 50× the token bill.
- **Untestable.** You can't write a unit test that says "given these ten memories and this query, the top three results should be X, Y, Z."

> Memwright's first rule: **zero LLM in the critical path.** Embeddings are computed once at write time, locally, using all-MiniLM-L6-v2. Retrieval is pure math and graph traversal.

## The 5-layer pipeline

```
Query
  ↓
[1] Tag Match      — SQLite FTS, exact + fuzzy token hits
  ↓
[2] Graph Expansion — NetworkX BFS, depth 2 from matched entities
  ↓
[3] Vector Search  — ChromaDB cosine similarity on 384-D embeddings
  ↓
[4] Fusion + Rank  — Reciprocal Rank Fusion (k=60) + PageRank + confidence decay
  ↓
[5] Diversity      — MMR (λ=0.7) + greedy token-budget pack
  ↓
Top-K memories, fits your prompt budget, deterministic, unit-testable
```

> Each layer is a pure function. You can unit-test the whole thing by feeding it fixtures and asserting on rankings. The test suite is 607 cases and runs without Docker or API keys.

## Multi-agent primitives are first-class

> Most memory libraries treat the agent as a singleton. Real pipelines have an orchestrator coordinating a planner that dispatches to executors that report to reviewers. They should not all share a single memory pool.

- **Six RBAC roles**: ORCHESTRATOR, PLANNER, EXECUTOR, RESEARCHER, REVIEWER, MONITOR. Each has different read/write permissions.
- **Namespace isolation enforced at the row level**, not in application code. A tenant column is on every table, every query filters on it, no escape.
- **Provenance chain**: every memory carries source_id, content hash, ingest timestamp, and the agent role that wrote it. You can reconstruct who told the system what.
- **Per-agent token budgets and write quotas.** A runaway executor cannot fill the memory with junk.

## Temporal correctness

> Memwright never overwrites. It supersedes. Every fact has a validity window (valid_from, valid_to). Newer contradicting facts don't delete older ones — they close them. recall(as_of=...) replays the past.
>
> This matters for audit ("what did the desk know on March 12?"), for debugging ("why did the planner make that call yesterday?"), and for any regulated domain.

## Same API, six backends

```python
from agent_memory import AgentMemory
mem = AgentMemory("./store")    # SQLite + ChromaDB + NetworkX, zero config
mem.add("Planner decided to use Rust for the hot path", tags=["decision"])
results = mem.recall("what did we pick for the hot path?", k=5)
```

That's the local mode. Identical code runs against:
- Postgres (pgvector + Apache AGE)
- ArangoDB (doc + vector + graph in one engine)
- AWS ECS + ArangoDB
- Azure Cosmos DB DiskANN
- GCP AlloyDB (pgvector + ScaNN + AGE)

## Benchmarks

> LOCOMO v2 (long-context memory benchmark): **81.2%**.
> For reference: OpenAI memory 52.9%, Mem0 66.9%, Letta 74%, Zep ~75%, MemMachine 84.9%. Honest competitive, not state-of-the-art, and I know exactly why the gap exists (embedding model — next release bumps it).

## Install

```
pip install memwright
memwright api --host 0.0.0.0 --port 8080
```

For Claude Code users: type `install agent memory` in Claude Code and the MCP server interviews you, installs itself, wires hooks, runs a health check.

MIT. Repo: github.com/bolnet/agent-memory. HN discussion: news.ycombinator.com/item?id=47773981
