---
source: arxiv
arxiv_id: "2604.11811"
author: Wenbo Pan, Shujie Liu, Xiangyang Zhou, Shiwei Zhang, Wanlu Shi, Mirror Xu, Xiaohua Jia
url: https://arxiv.org/abs/2604.11811
date: 2026-04-10
fetched: 2026-04-17
tags: [agent-memory, meta-optimization, evolution, benchmark]
---

# M★: Every Task Deserves Its Own Memory Harness

Wenbo Pan et al., arxiv 2604.11811, 2026-04-10

## Abstract

Large language model agents rely on specialized memory systems to accumulate and reuse knowledge during extended interactions. Recent architectures typically adopt a fixed memory design tailored to specific domains. However, a memory system optimized for one purpose frequently fails to transfer to others. M★ automatically discovers task-optimized memory harnesses through executable program evolution. Specifically, M★ models an agent memory system as a memory program written in Python, encapsulating Data Schema, Storage Logic, and Agent Workflow Instructions. Optimized jointly using reflective code evolution with population-based search.

## Memory Program Architecture

Three components:
1. **Schema**: Python dataclasses with typed fields — what info is stored
2. **Logic**: Backend operations — embedding, SQL, LLM calls for processing/storing/retrieving
3. **Instructions**: Prompt constants guiding knowledge extraction, querying, response generation

Whitelisted toolkit: SQLite, ChromaDB, LLM endpoints.

## Evolution Process

Three stages:
1. **Validation Feedback**: Rotating validation set → targeted improvement signals; static set → comparable metrics across iterations
2. **Coding Agent Iteration**: LLM analyzes execution trajectories + underperforming cases → generates targeted code patches
3. **Quality Gates**: Static analysis (whitelist verification, compilation), smoke testing, performance constraints (3000-char output, 2-min timeout)

### Population-Based Search
- Population pool initialized with 3 structurally diverse seeds
- Softmax temperature sampling (T=0.15) — high-scoring programs get higher selection probability
- k-means clustering on embeddings for validation subset diversity
- Facility location optimization for episode selection

## Experimental Results

| Benchmark | Configuration | M★ Score | Best Baseline | Δ |
|-----------|---|---|---|---|
| LoCoMo | F1/LLM-Judge | 0.459/0.610 | Mem0: 0.373/0.540 | +23%/+13% |
| ALFWorld | Unseen | 0.881 | GEPA: 0.857 | +2.8% |
| ALFWorld | Seen | 0.700 | GEPA+VS: 0.820 | -14.6% |
| HealthBench | Data Tasks | 0.390 | GEPA+VS: 0.327 | +19% |
| HealthBench | Emergency | 0.493 | ReasoningBank: 0.470 | +5% |
| PRBench | Legal | 0.660 | GEPA: 0.568 | +16% |
| PRBench | Finance | 0.586 | GEPA: 0.449 | +30% |

7/8 best scores. Largest gains on conversation (LoCoMo) and professional reasoning (PRBench).

### 9 Baselines spanning 3 paradigm categories:
- **Retrieval-based** (raw episodes): Vector Search, G-Memory, Mem0
- **Self-evolution** (distilled experiences): Trajectory Retrieval, ReasoningBank, Dynamic Cheatsheet
- **Prompt-optimizing** (traction): GEPA variants

No single baseline consistent across all domains.

## Task-Specific Memory Structures

### Architectural Diversity (key finding)

- **ALFWorld**: Deterministic action cache, SQLite, canonical state normalization, keyword scoring + exact-match bonuses. 97 lines of logic, NO vector retrieval. Top-6 memories → single LLM call for step-by-step guidance.
- **LoCoMo**: 290-line hybrid — SQLite for structured metadata + ChromaDB for semantic search. 7 metadata fields per item. Source diversity enforced (max 2 chunks per dialogue). Semantic+lexical score fusion + person-focused boosting.
- **HealthBench/PRBench**: SQLite-centric + LLM calls during read. 6-21 schema fields.

### Cross-Task Transfer
Native programs consistently outperformed transferred ones. Most transferred programs worse than baseline seeds → "memory structure must be co-optimized with the target task."

## Evolution Dynamics

Three-phase pattern:
1. Early: correct structural issues from seeds
2. Middle: largest gains — discover task-relevant indexing/retrieval
3. Late: refine precision, diminishing returns

Stability: 5 random seeds, CoV < 9% (5.7-8.9%). 14/15 seeds beat strongest baseline.

### Ablation (LoCoMo)
- Remove code evolution: F1 0.459 → 0.256 (−44%) ← biggest drop
- Remove instruction optimization: 0.459 → 0.353 (−23%)
- Code structure is primary driver, instructions are amplifier.

## Key Insights

1. Task-specific memory designs substantially outperform generalist approaches
2. Population-based search explores diverse architectural families (LLM-centric, semantic search, hybrid, relational, RAG)
3. Uniform improvement: highest minimum category score
4. Multi-component joint optimization (schema + logic + instructions) > single-component
