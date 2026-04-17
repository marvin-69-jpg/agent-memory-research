---
source: arxiv 2604.12007
url: https://arxiv.org/abs/2604.12007
author: Baris Simsek
title: "When to Forget: A Memory Governance Primitive"
date_published: 2026-04-13
date_fetched: 2026-04-17
type: paper
---

# When to Forget: A Memory Governance Primitive

**Author**: Baris Simsek (single author)
**ArXiv**: 2604.12007v1
**Submitted**: 2026-04-13

## Abstract (verbatim)

Agent memory systems accumulate experience but currently lack a principled operational metric for memory quality governance — deciding which memories to trust, suppress, or deprecate as the agent's task distribution shifts. Write-time importance scores are static; dynamic management systems use LLM judgment or structural heuristics rather than outcome feedback. This paper proposes Memory Worth (MW): a two-counter per-memory signal that tracks how often a memory co-occurs with successful versus failed outcomes, providing a lightweight, theoretically grounded foundation for staleness detection, retrieval suppression, and deprecation decisions.

We prove that MW converges almost surely to the conditional success probability p+(m) = Pr[y_t = +1 | m in M_t] — the probability of task success given that memory m is retrieved — under a stationary retrieval regime with a minimum exploration condition. Importantly, p+(m) is an associational quantity, not a causal one: it measures outcome co-occurrence rather than causal contribution. We argue this is still a useful operational signal for memory governance, and we validate it empirically in a controlled synthetic environment where ground-truth utility is known: after 10,000 episodes, the Spearman rank-correlation between Memory Worth and true utilities reaches rho = 0.89 +/- 0.02 across 20 independent seeds, compared to rho = 0.00 for systems that never update their assessments.

A retrieval-realistic micro-experiment with real text and neural embedding retrieval (all-MiniLM-L6-v2) further shows stale memories crossing the low-value threshold (MW = 0.17) while specialist memories remain high-value (MW = 0.77) across 3,000 episodes. The estimator requires only two scalar counters per memory unit and can be added to architectures that already log retrievals and episode outcomes.

## Key Mechanism

**Memory Worth (MW)** = two scalar counters per memory:
- `successes`: how often this memory co-occurred with task success
- `retrievals`: how often this memory was retrieved

`MW(m) = successes / retrievals` ≈ `p+(m) = Pr[task success | m retrieved]`

## Theoretical Properties

- **Almost-sure convergence** to conditional success probability under:
  - stationary retrieval distribution
  - minimum exploration condition (every memory has some chance of being retrieved)
- **Associational, not causal** — measures outcome co-occurrence, not the memory's *contribution* to success. Author flags this as an honest limitation but argues it's still a useful operational signal.

## Empirical Results

| Setup | Result |
|---|---|
| Synthetic, ground-truth utility known | Spearman ρ = 0.89 ± 0.02 (20 seeds, 10,000 episodes) |
| Static (no updates) baseline | ρ = 0.00 |
| Real text + all-MiniLM-L6-v2 embeddings, 3,000 episodes | Stale memories: MW ≈ 0.17 (low-value threshold) |
|  | Specialist memories: MW ≈ 0.77 (high-value) |

## Position in Memory Governance

| Question | Existing answer | When to Forget |
|---|---|---|
| What's important to write? | A-Mem, D-Mem (write-time scoring) | Doesn't address |
| How to consolidate? | A-Mem evolution, reconsolidation | Doesn't address |
| Which memories should I trust now? | LLM judgment, structural heuristics, recency decay | **MW: outcome-feedback estimate** |
| When to suppress / deprecate? | Heuristic thresholds, manual review | **MW < threshold → suppress** |

## Why This Matters

- **Write-time gating** (D-Mem RPE) decides what *enters* memory.
- **Reconsolidation** (A-Mem) decides how memories *update each other*.
- **Memory Worth** decides what should *stay trusted* over time.

These three are complementary. MW fills the read-time / outcome-time slot that previous work left to LLM judgment or recency heuristics.

## Practical Properties

- 2 scalar counters per memory → trivial overhead
- Add to any architecture that already logs retrievals + episode outcomes
- No LLM call required for the metric itself
- Theoretical guarantee (almost-sure convergence) under modest assumptions

## Limitations Acknowledged by Author

- Associational not causal — MW could rank a memory high simply because it co-occurs with easy tasks, not because it helps
- Requires stationary retrieval — concept drift breaks the convergence proof
- Requires minimum exploration — never-retrieved memories never get a score
- Synthetic benchmark — real-world deployment validation pending
