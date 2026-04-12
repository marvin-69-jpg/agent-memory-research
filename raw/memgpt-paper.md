# MemGPT: Towards LLMs as Operating Systems

**Authors**: Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez
**Date**: 2023-10-12 (v1), 2024-02-12 (v2)
**Source**: https://arxiv.org/abs/2310.08560
**Institution**: UC Berkeley

---

## Abstract

Large language models (LLMs) have revolutionized AI, but are constrained by limited context windows, hindering their utility in tasks like extended conversations and document analysis. To enable using context beyond limited context windows, we propose virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems that provide the appearance of large memory resources through data movement between fast and slow memory. Using this technique, we introduce MemGPT (Memory-GPT), a system that intelligently manages different memory tiers in order to effectively provide extended context within the LLM's limited context window, and utilizes interrupts to manage control flow between itself and the user. We evaluate our OS-inspired design in two domains where the limited context windows of modern LLMs severely handicaps their performance: document analysis, where MemGPT is able to analyze large documents that far exceed the underlying LLM's context window, and multi-session chat, where MemGPT can create conversational agents that remember, reflect, and evolve dynamically through long-term interactions with their users.

## Core Idea

MemGPT draws an analogy between OS virtual memory and LLM context management:

| OS Concept | MemGPT Equivalent |
|------------|-------------------|
| Main memory (RAM) | LLM context window |
| Disk storage | External storage (database, files) |
| Virtual memory / paging | Virtual context management |
| Page faults / interrupts | Context overflow triggers |
| Memory management unit | MemGPT's memory controller |

The LLM's context window is like RAM — fast but limited. External storage is like disk — large but slow. MemGPT acts as the "memory management unit" that pages data in and out of the context window as needed.

## Memory Hierarchy

MemGPT uses a tiered memory system:

1. **Main Context** (in the LLM's context window):
   - System prompt / instructions
   - Working context (scratchpad the agent can read/write)
   - Recent conversation messages (FIFO queue)

2. **External Context** (outside the context window):
   - Recall storage — full conversation history, searchable
   - Archival storage — persistent knowledge base, read/write

The agent has tools to move data between tiers:
- `core_memory_append` / `core_memory_replace` — edit working context
- `conversation_search` — search recall storage
- `archival_memory_insert` / `archival_memory_search` — read/write archival

## Key Innovation: Self-Directed Memory Management

Unlike traditional RAG where retrieval is triggered by user queries, MemGPT gives the agent TOOLS to manage its own memory. The agent decides:
- What to keep in working context
- What to page out to archival storage
- When to search recall/archival for relevant information
- How to update its own instructions

This is "self-directed" memory ��� the agent is in charge of its own context, not an external system.

## Evaluation

Two domains:
1. **Document analysis** — analyzing documents larger than context window (200+ pages). MemGPT significantly outperforms fixed-context baselines.
2. **Multi-session chat** — conversational agents across many sessions. MemGPT agents remember details from earlier conversations, reflect on past interactions, and evolve their behavior.

## Significance

MemGPT was one of the first systems to:
- Frame LLM memory as an OS-level problem (virtual memory analogy)
- Give agents tools to manage their own context (self-directed memory)
- Demonstrate multi-session memory in conversational agents
- Later evolved into Letta (the company), with Sarah Wooders as CTO and Charles Packer as CEO

The paper's key insight — that memory management should be the agent's responsibility, not an external plugin — directly influenced the "memory is the harness" argument that Sarah Wooders later articulated.
