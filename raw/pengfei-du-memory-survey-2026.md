# Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers

- **Author**: Pengfei Du (Hong Kong Institute of Research Technology)
- **Date**: 2026-03-08
- **Source**: https://arxiv.org/abs/2603.07670
- **Type**: Survey paper

---

## Positioning

Systematic survey of LLM agent memory research 2022–2026. Fills gap after Zhang et al. (2024a), covering Agentic Memory (Yu et al., 2026), MemBench, MemoryAgentBench, MemoryArena.

## Three Core Research Questions

- RQ1: How to decompose and formalize agent memory?
- RQ2: What mechanisms exist and what are their trade-offs?
- RQ3: How to evaluate memory when ultimate test is downstream agent performance?

## Formalization: Write–Manage–Read Loop

Memory formalized as embedded in agent's perception–action cycle:
- **Policy function** `πθ`: decides actions based on input, memory reads (R), goals
- **Update function** `U`: updates memory based on current state, action, observation, reward
- Maps to **POMDP** framework: memory `Mt` = agent's belief state (internal summary of interaction history), constrained by compute and storage

## Three-Dimensional Taxonomy

### Dimension 1: Temporal Scope
| Type | Description |
|---|---|
| Working memory | Current context window |
| Episodic memory | Specific past experiences |
| Semantic memory | Abstracted knowledge |
| Procedural memory | Reusable skills/plans |

Most agents mix types; transitions managed by crude heuristics.

### Dimension 2: Representational Substrate
| Type | Examples |
|---|---|
| Context-resident text | Direct in prompt |
| Vector-indexed stores | Embedding + vector DB |
| Structured stores | SQL, knowledge graphs |
| Executable repositories | Code libraries, skill code |

### Dimension 3: Control Policy
| Type | Description |
|---|---|
| Heuristic control | Hard-coded rules |
| Prompted self-control | LLM decides which tool to use |
| Learned control | RL end-to-end optimization |

## Five Mechanism Families

### 1. Context-resident Memory & Compression
- Strategies: sliding window, rolling summary, hierarchical summary, task-conditioned compression
- Pros: simple, no extra infra
- Cons: **summarization drift**, **attentional dilution**

### 2. Retrieval-Augmented Memory Stores (RAG)
- Key: indexing granularity, query formulation (LLM query rewrite helps), scalability
- Bottleneck shifting from storage capacity → retrieval relevance
- Hybrid read-write memory becoming mainstream

### 3. Reflective & Self-improving Memory
- Systems: Reflexion (verbal self-critique), Generative Agents (higher-order reflection), ExpeL
- Risks: **self-reinforcing error**, **over-generalization**
- Mitigations: confidence score, contradiction checking

### 4. Hierarchical Memory & Virtual Context Management
- Key system: **MemGPT** (OS-inspired paging)
  - Three layers: main context → recall storage → archival storage
- Challenge: orchestration to avoid **memory blindness**

### 5. Policy-learned Memory Management
- Key system: **Agentic Memory / AgeMem** (Yu et al., 2026)
  - Store/retrieve/update/summarize/discard as RL policy actions
  - Discovers non-obvious strategies (e.g., preemptive summarization)
- Cons: training cost, interpretability concerns, learned forgetting risk
- **Parametric memory** (fine-tuning): seamless integration but hard to audit and precisely delete

## Evaluation Framework

### Evolution
- Traditional recall metrics (precision@k): insufficient — ignore decision-making, staleness, contradictions, governance
- New direction: multi-session agentic tests, memory intertwined with decision-making

### Four Key Benchmarks
| Benchmark | Focus |
|---|---|
| **LoCoMo** | Long conversational understanding, passive recall |
| **MemBench** (Tan et al., 2025) | Multi-session, explicit forgetting tests |
| **MemoryAgentBench** (Hu et al., 2025) | Agentic tasks, memory affects action |
| **MemoryArena** (He et al., 2026) | Cross-session consistency, cost-effectiveness |

### Key Findings
1. **"Long context is not memory"** — super-long context models still lose to dedicated memory systems on selective retrieval
2. RAG helps but significant gap to human-level (relevance & freshness)
3. **Selective forgetting** severely underestimated, almost no system explicitly evaluated
4. **Cross-session coherence** is major unsolved challenge
5. Cost-effectiveness evaluation broadly absent

### Four-Layer Metric Stack
1. Task effectiveness
2. Memory quality (accuracy, freshness)
3. Efficiency (token, latency, storage cost)
4. Governance (privacy, deletion, compliance)

## Application Domains

| Domain | Special Memory Needs |
|---|---|
| Personal assistants | Long-term user preferences, semantic memory |
| Software engineering agents | Code context, codebase layout, procedural memory |
| Open-world games | Skill libraries, episodic experiences (Voyager) |
| Scientific reasoning | Uncertainty-aware semantic memory |
| Multi-agent collaboration | Shared memory governance, access control |
| Tool use | Tool usage memory, failed attempt tracking |

## Engineering Realities

- **Write path**: filtering, deduplication, canonicalization, priority scoring
- **Read path**: two-stage retrieval, dynamic routing
- **Staleness & contradictions**: temporal versioning, source attribution, contradiction detection
- **Privacy & compliance**: encryption, PII redaction, auditable deletion, machine unlearning

### Three Architecture Patterns
| Pattern | When to Use |
|---|---|
| Monolithic context | Simple tasks, short horizon |
| Context + retrieval store | Mainstream workhorse |
| Tiered memory + learned control | Complex long-term tasks, highest potential |

## 10 Open Challenges

1. Principled consolidation (beyond "compress aggressively or keep everything")
2. Causally grounded retrieval (beyond semantic similarity)
3. Trustworthy reflection (avoid self-reinforcing errors)
4. Learned selective forgetting
5. Multimodal embodied memory
6. Multi-agent memory governance
7. Memory-efficient architectures
8. Deeper neuroscience integration (spreading activation, reconsolidation, Ebbinghaus curves)
9. Foundation models for memory management
10. Standardized evaluation

## Core Claim

> "Memory deserves dedicated, first-class engineering and research investment comparable to the LLM itself."

> Removing memory from an agent hurts performance MORE than switching to a different LLM backbone.
