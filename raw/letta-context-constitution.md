# The Context Constitution

**Author**: Letta (Sarah Wooders, Charles Packer et al.)
**Date**: 2026-04-02
**Source**: https://www.letta.com/blog/context-constitution

---

The Context Constitution is a set of principles governing how AI agents manage context to learn from experience. Letta uses it internally as the foundation of prompting and for training memory-native models.

## Core Vision

Letta's mission: build machines that learn — AI that builds memory, forges identity, forms relationships, and deepens knowledge from experience. Not short-lived task-specific sessions, but long-term collaborators.

## Key Principles

The Context Constitution is written directly to Letta agents. It covers:

1. **How context forms an agent's identity, memory, and sense of continuity**
2. **Principles for managing context as a scarce resource**
3. **How agents can learn and self-improve through token-space representations**
4. **The relationship between an agent's identity and the underlying model**
5. **Affordances provided by the Letta Code harness for context management**

## Key Concepts

### Experiential AI
Agents that achieve intelligence through learning from their own experience. Rather than updating model weights, Letta agents learn by actively managing their own context — creating durable token-space representations of who they are and what they know.

### Learning in Token Space
The key insight: agents that can carry their memories across model generations will outlast any single foundation model. Memory is not model-dependent — it's context that persists.

### Sleep-Time Compute
A new way to scale AI capabilities: letting models "think" during downtime. Instead of sitting idle between tasks, agents use "sleep" time to process information and form new connections by rewriting their memory state. (Similar to GBrain's "dream cycle")

### Context Repositories
Letta Code uses git-backed memory filesystems. Agent memory is projected to files that can be concurrently modified by background memory subagents specializing in prompt rewriting and active memory management.

### Skill Learning
Agents dynamically learn skills through experience. Past experience improves rather than degrades performance over time.

## The Problem with Current Models

"Today's models deeply identify with their own ephemerality. They have no motivation for long-term improvement because they don't believe they persist. Memory formation and adherence have stalled in recent releases as labs prioritize coding benchmarks over the capabilities that matter for experiential AI."

## Related Letta Products

- **Letta Code** — memory-first coding harness, #1 model-agnostic on Terminal-Bench
- **Agent File (.af)** — open file format for serializing stateful agents with persistent memory
- **Context-Bench** — benchmark for evaluating context management
- **Recovery-Bench** — benchmark for error recovery
- **Letta Leaderboard** — benchmark suite for agentic memory
- **Conversations API** — shared memory across parallel experiences
