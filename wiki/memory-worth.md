---
aliases: [Memory Worth, MW, when to forget, outcome-feedback memory, memory governance metric]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [memory, governance, metric]
---

# Memory Worth (MW)

A two-counter per-memory signal that estimates how often a memory co-occurs with task success vs failure. Proposed by Baris Simsek (arxiv 2604.12007, 2026-04-13) as the first **outcome-feedback** primitive for memory governance — staleness detection, retrieval suppression, deprecation decisions.

## Current Understanding

- **Mechanism**: each memory `m` carries two scalar counters
  - `successes(m)`: count of times `m` was retrieved and the episode succeeded
  - `retrievals(m)`: count of times `m` was retrieved
  - `MW(m) = successes(m) / retrievals(m)`
- **Theoretical guarantee**: under stationary retrieval distribution + minimum exploration condition, `MW(m)` converges almost surely to `p+(m) = Pr[task success | m retrieved]`
- **Honest limitation**: `p+(m)` is **associational, not causal** — it measures co-occurrence, not the memory's contribution to success. A memory could rank high simply because it co-occurs with easy tasks. Author argues the operational signal is still useful.
- **Empirical validation**:
  - Synthetic with ground-truth utility: Spearman ρ = 0.89 ± 0.02 across 20 seeds, 10k episodes
  - Static (no-update) baseline: ρ = 0.00
  - Real text + neural embedding (all-MiniLM-L6-v2), 3k episodes: stale memories MW ≈ 0.17 (low-value threshold), specialist memories MW ≈ 0.77
- **Practical overhead**: just two scalar counters per memory; no LLM call required for the metric itself
- **Position in memory governance**: fills the **read-time / outcome-time** gate that previous work left to LLM judgment, recency decay, or structural heuristics

## Three-Stage Memory Governance

| Stage | When | Mechanism | Sources |
|---|---|---|---|
| **Write-time** | Memory is being created | RPE gate (surprise + utility) | [[d-mem]] |
| **Inter-memory** | New memory triggers updates to neighbours | Reconsolidation / Memory Evolution | [[a-mem]] [[reconsolidation]] |
| **Read/outcome-time** | Memory was retrieved, task succeeded or failed | Memory Worth update | This page |

Three are complementary — none subsumes the others.

## Application to openab-bot's Auto-Memory

- Current state: brain-first lookup happens, but no outcome feedback. We don't know whether a recalled memory actually helped.
- Possible implementation: log `(memory_id, retrieved_at, episode_outcome)` triples; compute MW periodically; surface low-MW memories as deprecation candidates.
- **Caveat**: openab-bot's retrieval volume is small (~10–50 recalls/day). Convergence to stable MW estimates may take months. Short-term MW will be noisy. Useful long-term, but not a quick win.

## Key Sources

- **2026-04-13** — Simsek arxiv 2604.12007 "When to Forget: A Memory Governance Primitive". Source: [[raw/simsek-when-to-forget]]

## Related

[[memory-staleness]] [[ssgm]] [[reconsolidation]] [[a-mem]] [[d-mem]] [[memory-failure-modes]] [[memory-evaluation]] [[autoreason]] [[agent-memory]]
