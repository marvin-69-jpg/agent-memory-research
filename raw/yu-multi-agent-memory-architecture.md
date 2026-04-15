---
Author: Zhongming Yu, Naicheng Yu, Hejia Zhang, Wentao Ni, Mingrui Yin, Jiaying Yang, Yujie Zhao, Jishen Zhao
Date: 2026-03-13
Source: https://arxiv.org/abs/2603.10062
Type: Position Paper
---

# Multi-Agent Memory from a Computer Architecture Perspective: Visions and Challenges Ahead

## Abstract

As LLM agents evolve into collaborative multi-agent systems, their memory requirements grow rapidly in complexity. This position paper frames multi-agent memory as a computer architecture problem. We distinguish shared and distributed memory paradigms, propose a three-layer memory hierarchy (I/O, cache, and memory), and identify two critical protocol gaps: cache sharing across agents and structured memory access control. We argue that the most pressing open challenge is multi-agent memory consistency. Our architectural framing provides a foundation for building reliable, scalable multi-agent systems.

## 1. Introduction

LLM agents are moving from single-agent tools to multi-agent systems: tool-using agents, planner–orchestrator stacks, debate teams, and specialized sub-agents that collaborate. The context these agents operate within is becoming more complex: longer histories, multiple modalities, structured traces, and customized environments. This combination creates a bottleneck that looks surprisingly familiar to computer architects: memory.

In computer systems, performance and scalability are often limited not by compute but by memory hierarchy, bandwidth, and consistency. Multi-agent systems are heading toward the same wall—except their "memory" is not raw bytes, but semantic context used for reasoning.

## 2. Why Memory Matters: Context Is Changing

- **Longer context windows**: RULER emphasizes reasoning over long histories, not just retrieval
- **Multimodal inputs**: MMMU and VideoMME require joint reasoning over images and videos
- **Structured data & traces**: Text-to-SQL datasets show agents operate over structured, executable traces
- **Customized environments**: SWE-bench and OSWorld stress long-horizon state tracking and grounded actions

Context is no longer a static prompt; it is a dynamic memory system with bandwidth, caching, and coherence constraints.

## 3. Shared vs. Distributed Agent Memory

Two basic prototypes mirroring classical memory systems:

- **Shared memory**: All agents access a shared pool (vector store, document database). Makes knowledge reuse easy but requires coherence support; without coordination, agents overwrite each other, read stale information, or rely on inconsistent versions.
- **Distributed memory**: Each agent owns local memory and synchronizes selectively. Improves isolation and scalability but requires explicit synchronization; state divergence common unless carefully managed.

Most real systems sit between: local working memory with selectively shared artifacts.

## 4. An Architecture-Inspired Memory Hierarchy

Three-layer hierarchy:

1. **Agent I/O layer**: Interfaces that ingest and emit information (audio, text, images, network calls)
2. **Agent cache layer**: Fast, limited-capacity memory for immediate reasoning (compressed context, recent tool calls, KV caches, embeddings)
3. **Agent memory layer**: Large-capacity, slower memory optimized for retrieval and persistence (dialogue history, vector DBs, graph DBs, document stores)

Key principle: agent performance is an end-to-end data movement problem. If relevant information is stuck in the wrong layer (or never loaded), reasoning accuracy and efficiency degrade. Caching is not optional.

## 5. Protocol Extensions for Multi-Agent Scenarios

Architecture layers need protocols. Two missing pieces:

### Missing piece 1: Agent cache sharing protocol

Recent work explores KV cache sharing, but we lack a principled protocol for sharing cached artifacts across agents. Goal: enable one agent's cached results to be transformed and reused by another, analogous to cache transfers in multiprocessors.

### Missing piece 2: Agent memory access protocol

Agentic memory frameworks (MemGPT, A-MEM, etc.) propose many strategies for maintaining and optimizing agents' memory. Yet even when some support shared state, the standard access protocol (permissions, scope, granularity) remains under-specified. Key questions:
- Can one agent read another's long-term memory?
- Is access read-only or read-write?
- What is the unit of access: document, chunk, key-value record, or trace segment?

## 6. The Next Frontier: Multi-Agent Consistency

The largest conceptual gap. In computer architecture, consistency models specify which updates are visible to a read and in what order concurrent updates may be observed.

For agent memory, multi-agent consistency decomposes into:
1. **Read-time conflict handling** under iterative revisions — records evolve across versions and stale artifacts may remain visible
2. **Update-time visibility and ordering** — when an agent's writes become observable to others, how concurrent writes are observed

This is harder than classical settings because memory artifacts are heterogeneous (evidence, tool traces, plans), and conflicts are often semantic and coupled to environment state.

Practical direction: make versioning, visibility, and conflict-resolution rules explicit, so agents agree on what to read and when updates take effect.

## 7. Conclusion

Many agent memory systems today resemble human memory: informal, redundant, and hard to control. To move from ad-hoc prompting to reliable multi-agent systems, we need better hierarchies, explicit protocols for cache sharing and memory access, and principled consistency models that keep shared context coherent.
