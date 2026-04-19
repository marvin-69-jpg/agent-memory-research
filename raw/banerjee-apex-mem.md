---
Author: Pratyay Banerjee, Masud Moshtaghi, Shivashankar Subramanian, Amita Misra, Ankit Chadha
Date: 2026-04-15
Source: https://arxiv.org/abs/2604.14362
Type: arxiv paper
---

# APEX-MEM: Agentic Semi-Structured Memory with Temporal Reasoning for Long-Term Conversational AI

## Authors & Affiliation
Pratyay Banerjee, Masud Moshtaghi, Shivashankar Subramanian, Amita Misra, Ankit Chadha — Amazon AGI, Sunnyvale, USA.

## Core Problem
LLMs struggle with reliable long-term conversational memory. Simply enlarging context windows or applying naive retrieval introduces noise and destabilizes responses. Existing structured memory systems (Mem0, A-MEM, Zep) either restrict entity classes, primarily store relationships (limiting nuanced attributes), or consolidate/overwrite previous information — risking loss of important contextual details for temporal reasoning and conflict resolution.

## Key Innovation: Append-Only + Retrieval-Time Resolution

APEX-MEM's radical design choice: **don't consolidate at write time. Append everything, resolve at retrieval time.**

Three key innovations:
1. **Structured Conversational Memory**: Property graph with domain-agnostic hybrid entity-event ontology (35 entity classes). Events are first-class citizens with fine-grained temporal reasoning.
2. **Append-Only Event Storage**: Facts anchored to temporally grounded events, not directly to entities. Preserves complete history including contradictions and revisions. Resolution happens at retrieval time based on temporal validity.
3. **Multi-Tool Retrieval Agent**: ReAct-style agent with 4 specialized tools for intelligent retrieval and resolution.

## Architecture

### Graph Construction
- Property graph G = (V, E, Π, Λ) with nodes for entities, events, facts
- Soft-canonicalization for entity resolution (dense semantic search + structured LLM reasoning)
- Fact extraction via few-shot prompted LLMs with schema-constrained generation
- Online construction mode for conversations > 10³ documents

### Retrieval Agent (4 Tools)
1. **SCHEMAVIEWER**: Meta-level schema inspection and query planning aid
2. **ENTITYLOOKUP**: Hybrid index (dense + lexical) → ranked entity documents with temporal context
3. **GRAPHSQL**: Read-only SQL over whitelisted tables for precise temporal computations
4. **SEARCH**: Unified hybrid graph–entity–property–SQL + semantic search

### Ontology
- 35 entity classes (Person, Organization, Place, Event, Product, CreativeWork, etc.) — analogous to YAGO taxonomies
- Facts: subject-property-value assertions with temporal validity interval [t_from, t_to], confidence score, evidence set
- All facts anchored to conversational events (timestamp, location, participants, supporting text)

## Key Design Philosophy: Write Everything, Resolve Later

The fundamental contrast with other memory governance approaches:
- **D-MEM**: Gate at write time (RPE filter, skip 80% of inputs)
- **SSGM**: Validate before consolidation (pre-consolidation validation principle)
- **APEX-MEM**: Don't gate or validate at write time. Append everything. Defer conflict resolution to retrieval agent.

Rationale: consolidation/overwriting risks losing important contextual details. By preserving full history, the system can make better-informed decisions at query time when the actual information need is known.

## Results

### LOCOMO Benchmark
- APEX-MEM + GPT5: 88.88% overall accuracy (vs MIRIX 85.38%, +3.50pp)
- Categories: single-hop 89.88%, multi-hop 86.29%, temporal 90.63%, open-domain 91.68%, adversarial 86.77%
- With GPT4o: 86.35% — generalizes across LLM backends

### LongMemEval
- APEX-MEM + Claude 4.5 Sonnet: 86.2% overall (+11.6pp over Nemori, +13.7pp over session-aware RAG)

### SealQA-Hard
- APEX-MEM + GPT5: 40.15% (vs O3 34.6%, DeepSeek-R1 15.4%)

### Ablation
- SchemaViewer + EntityLookUp alone: 77.19%
- + GraphSQL: 79.45% (+2.26pp, temporal queries 72.92% → 82.29%)
- + Search: 87% (+7.55pp) — full hybrid is crucial
- GraphSQL-only: 3.3x more tool calls for lower accuracy

## Limitations
- Computational cost: entity resolution + property extraction via LLMs is resource-intensive
- Ontology may miss domain-specific nuances
- Performance sensitive to QnA agent's SQL generation quality
- Text-only (no multimodal)
- Performance gaps in highly noisy multi-document scenarios

## Connection to Memory Governance

APEX-MEM represents the **opposite end** of the memory governance spectrum from SSGM:
- SSGM: proactive governance — validate, constrain, gate before writing
- APEX-MEM: reactive governance — store everything, govern at retrieval time

The question becomes: **when is each approach appropriate?**
- APEX-MEM works well when you have a powerful retrieval agent and the information landscape is complex/contradictory
- SSGM works well when you want to prevent drift and poisoning in long-running agents
- D-MEM works well when write throughput matters and most inputs are noise

This maps to the self-refinement regimes from yesterday's research: the "when to validate" question has no single answer — it depends on where in the pipeline you can afford to spend compute and what failure modes you most want to prevent.
