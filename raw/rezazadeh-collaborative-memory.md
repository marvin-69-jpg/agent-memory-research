---
Author: Alireza Rezazadeh, Zichao Li, Ange Lou, Yuying Zhao, Wei Wei, Yujia Bao (Accenture Center for Advanced AI)
Date: 2025-05-23
Source: https://arxiv.org/abs/2505.18279
Type: Research Paper
---

# Collaborative Memory: Multi-User Memory Sharing in LLM Agents with Dynamic Access Control

## Abstract

A framework for multi-user, multi-agent memory management that operates under asymmetric and dynamically evolving access constraints. Uses dynamic bipartite graphs to encode time-varying permissions, two-tier memory (private + shared), and fine-grained read/write policies.

## Key Problem

Existing memory systems assume single-user, single-agent with centralized, globally accessible memory. Breaks down in real enterprise settings where:
1. **Information asymmetry**: Different users have different roles → access to different agents → different resources
2. **Dynamic access patterns**: Permissions evolve over time (role changes, project requirements, organizational policies)

## Architecture

### Dynamic Bipartite Access Graphs

- `G_UA(t) ⊆ U × A` — User-to-Agent graph (which users can invoke which agents at time t)
- `G_AR(t) ⊆ A × R` — Agent-to-Resource graph (which agents can access which resources at time t)
- Graphs evolve over time to reflect real-world changes

### Two-Tier Memory System

- **Private Memory (`M_private`)**: Fragments visible only to originating user. Per-user partitioned.
- **Shared Memory (`M_shared`)**: Fragments selectively shared across users. Per-agent partitioned.
- **Contextual Access**: When agent `a` serves user `u` at time `t`, it accesses:
  - Fragments from `u`'s history
  - Fragments created by `a` for other users
  - Fragments from other users with agents `u` can invoke
  - All subject to `a`'s resource permissions `R(a, t)`

### Fine-Grained Policies

- **Read Policy (`π_read`)**: Dynamically constructs memory view tailored to agent's current permissions. Filters and transforms fragments into admissible views.
- **Write Policies (`π_write/private`, `π_write/shared`)**: Determine fragment retention and sharing. Apply context-aware transformations (anonymization, redaction).

## Results

### Scenario 1: Fully Collaborative (MultiHop-RAG)
- Accuracy maintained above 0.90 with or without sharing
- Resource usage reduced **up to 61%** at 50% query overlap
- Efficiency from reusing previously retrieved information

### Scenario 2: Asymmetric Collaboration (Synthetic Business)
- Partial collaboration still yields efficiency gains
- Intermediate insights flow between users with matching privileges
- Strict respect for diverse privilege levels

### Scenario 3: Dynamic Evolution (SciQAG)
- Accuracy tracks dynamic access graph (rises with access grants, drops with revocations)
- Resource utilization drops over time through memory reuse
- Strict adherence to access control policies confirmed via access matrices

## Significance

- First formulation of memory sharing with fine-grained, asymmetric, time-varying access constraints
- Bridges gap between shared knowledge needs and enterprise security requirements
- Provenance attributes on every fragment → full auditability
- Modular design → integrates with other memory architectures

## Limitations

- Synthetic datasets only
- Controlled environments (no real concurrency)
- LLM probabilistic nature → potential policy breaches
- Scaling to large enterprise settings untested
