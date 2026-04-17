---
source: arxiv
arxiv_id: "2604.12285"
author: Zhaofen Wu, Hanrong Zhang, Fulin Lin, Wujiang Xu, Xinran Xu, Yankai Chen, Henry Peng Zou, Shaowen Chen, Weizhi Zhang, Xue Liu, Philip S. Yu, Hongwei Wang
url: https://arxiv.org/abs/2604.12285
date: 2026-04-14
fetched: 2026-04-17
tags: [agent-memory, graph, architecture, neuroscience, benchmark]
---

# GAM: Hierarchical Graph-based Agentic Memory for LLM Agents

Wu et al., arxiv 2604.12285, 2026-04-14

## Abstract

Balancing acquisition of new information against retention of existing knowledge. Current approaches struggle with noise vulnerability or inflexibility. GAM explicitly decouples memory encoding from consolidation to resolve the conflict between rapid context perception and stable knowledge retention.

## Architecture: Dual-Graph Hierarchy

### Event Progression Graph (EPG) — local/temporal
- Temporary buffer for ongoing dialogue
- Nodes = atomic interaction units (utterances/responses), captured in real-time
- Edges = temporal and causal evolution of current dialogue flow
- New utterances append directly without touching global memory → prevents contamination

### Topic Associative Network (TAN) — global/semantic
- High-level thematic clusters from historical interactions
- Nodes = consolidated semantic themes
- Edges = deep semantic correlations, weighted by LLM-based scoring
- Protected from transient noise

## Decoupling Mechanism

Two operational states:

1. **Episodic Buffering**: New input → append to EPG only. No global memory touched.
2. **Semantic Consolidation**: When semantic boundary detected (topic shift > threshold ε):
   - Consolidate EPG into dual-granularity topic node: (1) summary for abstract reasoning + (2) raw content for fine-grained recall
   - Integrate into TAN via LLM-scored semantic edges
   - Trigger: semantic divergence detection via 2048-token buffer + LLM discriminator for topic boundaries

Inspired by sleep-dependent memory consolidation from neuroscience.

## Multi-Factor Retrieval

Top-down across layers:
1. **Semantic Anchoring**: top-k topic nodes via vector similarity → expand to first-order neighbors
2. **Structural Drill-Down**: traverse cross-layer links to access archived event graphs
3. **Multi-Factor Re-ranking**: multiplicative modulation
   - `Score(v,q) = P_sem(v|q) · ∏β_k^I_k(v,q)`
   - Factors: confidence (β_conf=1.2), temporal (β_time=1.4), role (β_role=1.4)

## Results

### LoCoMo (Qwen 2.5-7B)

| Method | Avg F1 | Avg BLEU-1 |
|---|---|---|
| Mem0 | 35.38 | 28.67 |
| **GAM** | **40.00** | **32.99** |
| A-Mem | 24.20 | 19.49 |
| MemoryOS | 28.86 | 22.25 |

Temporal tasks: GAM 48.97 F1 vs Mem0 41.22 — semantic consolidation preserves chronological precision.

### LongDialQA (Qwen 2.5-7B)

| Method | Avg F1 | Avg BLEU-1 |
|---|---|---|
| Mem0 | 10.27 | 9.91 |
| **GAM** | **12.55** | **12.43** |
| MemoryOS | 6.76 | 5.11 |

### Efficiency

| Method | Tokens/Query | Latency (s) | F1 |
|---|---|---|---|
| GAM | 1,370 | 0.80 | 40.00 |
| Mem0 | 1,533 | 0.51 | 35.38 |
| A-Mem | 4,221 | 2.21 | 24.20 |

GAM: -11% tokens vs Mem0, +13% F1. A-Mem: 3x tokens, 40% lower F1.

## Ablation (LoCoMo)

| Ablation | Avg F1 | Δ |
|---|---|---|
| Full GAM | 40.00 | — |
| w/o EPG | 25.06 | -14.94 (largest) |
| w/o SSM | 32.58 | -7.42 |
| w/o TAN | 35.07 | -4.93 |
| w/o MFR | 35.94 | -4.06 |

EPG removal causes biggest drop → temporal/narrative coherence most important.

## Robustness

Under 40% topic segmentation noise: GAM maintains 38.60 F1 (vs 34.23 Fixed Window baseline).
