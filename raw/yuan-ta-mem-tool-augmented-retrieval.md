---
source_type: arxiv
paper_id: 2603.09297
title: "TA-Mem: Tool-Augmented Autonomous Memory Retrieval for LLM in Long-Term Conversational QA"
authors: Mengwei Yuan, Jianan Liu, Jing Yang, Xianyou Li, Weiran Yan, Yichao Wu, Penghao Liang
date: 2026-03-10
---

# TA-Mem: Tool-Augmented Autonomous Memory Retrieval

## Core Claim
Static top-k retrieval is the bottleneck in memory systems. The agent should autonomously select which retrieval tool to use based on question type, rather than always doing the same embedding similarity search.

## Architecture
Three stages:

**Write time (Episodic Memory Constructor)**
- LLM agent does semantic chunking (not fixed size)
- In single pass, extracts structured note per chunk:
  - Summary
  - Keywords
  - Persons mentioned
  - Facts per person
  - Events with temporal references
  - Semantic tag
- Memory page = original dialogue segment + extracted note + timestamp
- Key: stores original + structured annotation (not just annotation)

**Multi-Indexed Database**
- Indexed by: person names (string), tags, keywords, vector embeddings of events/facts
- Query tools exposed:
  - Q_s: key-based string query (person/tag/keyword)
  - Q_k: top-k similarity (events/facts)
  - Q_p: person-specific (all events/facts for a person)

**Read time (Memory Retrieval Agent)**
- Agentic loop: receives question → selects tool → fetches context → decide continue or finalize
- Memory cache prevents redundant re-fetching in same session
- Max 7 iterations, avg 2.71 iterations per question
- 97.73% of questions resolved by 4 iterations

## Results (LOCOMO benchmark)
- Best F1 on temporal questions: 55.95 (best overall)
- Best BLEU-1 on temporal, multi-hop, open-domain questions
- Token efficiency: 3755 avg tokens/question (competitive despite loop)

## Key Insights
- Temporal questions benefit most from adaptive retrieval (uses event queries predominantly)
- Open-domain questions use fact queries predominantly
- Tool use pattern varies significantly by question type → validates adaptive approach
- LLM-based chunking ≈ semantic chunking (44.34% vs 43.73% F1) but does it in one pass
