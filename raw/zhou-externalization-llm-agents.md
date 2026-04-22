---
source_type: arxiv
paper_id: 2604.08224
title: "Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering"
authors: "Chenyu Zhou et al. (SJTU, CMU, Sun Yat-Sen, OPPO) — 22 authors"
date: 2026-04-11
url: https://arxiv.org/abs/2604.08224
alphaxiv: https://www.alphaxiv.org/overview/2604.08224
ingested: 2026-04-23
---

# Externalization in LLM Agents

## Core Thesis

Recent progress in LLM agents is driven not by bigger models but by **externalizing cognitive burdens** from parametric weights to persistent, inspectable, reusable external structures. Based on Donald Norman's "cognitive artifact" theory — external aids don't just amplify internal abilities, they transform the task itself.

## The Three-Layer History

1. **Weights Layer** — capabilities from model parameters (pretraining, fine-tuning)
2. **Context Layer** — prompt engineering, few-shot, CoT, RAG
3. **Harness Layer** — current trend: persistent memory stores, tool registries, agent orchestration

## Four Externalization Dimensions

### Memory (externalizes state across time)
- Working context (live task state)
- Episodic experience (past runs, failures, outcomes)  
- Semantic knowledge (domain facts, conventions)
- Personalized memory (user/environment preferences)

Evolution: monolithic context → retrieval stores → hierarchical orchestration → adaptive systems

### Skills (externalizes procedural expertise)
- Operational procedure (how-to)
- Decision heuristics (when-to)
- Normative constraints (what-not-to)

Acquisition modes: authored / distilled / discovered / composed

### Protocols (externalizes interaction structure)
- Invocation grammar, lifecycle semantics, permissions, discovery metadata
- Agent-tool, agent-agent, agent-user, specialized domain protocols

### Harness Engineering (unifies all three)
Six dimensions: agent loop/control flow, sandboxing, human oversight, observability, configuration/permissions, context budget management

## Key Insight vs. Compression Spectrum

| Framework | Lens | Focus |
|---|---|---|
| Compression Spectrum (Zhang et al.) | What level of abstraction | Memory L1 / Skill L2 / Rule L3 compression ratio |
| Externalization (Zhou et al.) | What gets moved outside | State / Expertise / Interaction Structure / Runtime env |

These are complementary views of the same trend: knowledge moving out of weights into structured external artifacts.

## The Boundary Conditions Problem
Both papers converge on lifecycle management as underexplored:
- Staleness: when does externalized knowledge go stale?
- Unsafe composition: when do external artifacts combine in unexpected ways?
- Governance: who decides what gets promoted, deprecated, versioned?

## Connection to Our System
- Our auto-memory = Memory externalization ✅
- Our skills (SKILL.md files) = Skill externalization ✅  
- Our CLAUDE.md = L3 Declarative Rule (manually curated) ✅
- Missing: automated L1→L2→L3 promotion (the "missing diagonal")
