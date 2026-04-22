---
source_type: arxiv
paper_id: 2604.15877
title: "Experience Compression Spectrum: Unifying Memory, Skills, and Rules in LLM Agents"
authors: "Xing Zhang, Guanghui Wang, Yanwei Cui, Peiyang He (AWS GenAI), Wei Qiu, Ziyuan Li, Bing Zhu (HSBC)"
date: 2026-04-17
url: https://arxiv.org/abs/2604.15877
alphaxiv: https://www.alphaxiv.org/overview/2604.15877
ingested: 2026-04-23
---

# Experience Compression Spectrum: Unifying Memory, Skills, and Rules in LLM Agents

## Core Thesis

Memory extraction and skill discovery are both instances of **experience compression**, differing primarily in granularity and abstraction level. By viewing them on a single spectrum, we can unify the fragmented research communities and identify critical gaps.

## The Four-Level Spectrum

| Level | Name | What it stores | Compression | Reusability |
|---|---|---|---|---|
| 0 | Raw Trace | Uncompressed interaction records T = {(st, at, ot, ft)} | 1:1 | Minimal |
| 1 | Episodic Memory | "What happened" — structured events, key-value pairs, timestamped summaries | 5–20× | Low/Moderate (episode-tied) |
| 2 | Procedural Skill | "How to act" — reusable behavioral patterns, code snippets, workflow templates | 50–500× | High (class-level transfer) |
| 3 | Declarative Rule | "What principles govern" — domain-invariant policies, constraints, NL principles | 1000×+ | Highest (domain-general) |

## Key Findings

### Community Disconnect
- Citation analysis across 1,136 references from 22 papers
- Memory → Skill community: 0.7% cross-citation (4/566)
- Skill → Memory community: 1.2% (7/570)
- Less than 1% cross-community citation rate despite addressing the same problem

### System Mapping
- 10 systems at Level 1 (Episodic Memory)
- 8 systems at Level 2 (Procedural Skill)
- ~0 systems at Level 3 (automated rule extraction)
- Only ExpeL and AutoAgent bridge L1–L2 (but at fixed levels, not adaptively)

### The "Missing Diagonal"
No existing system can:
1. Adaptively select compression level based on context
2. **Promote** knowledge upward (L1 → L2 → L3) when patterns emerge
3. **Demote** knowledge downward (L3 → L2 → L1) when abstraction is too general

### Four Structural Insights
1. Specialization alone is insufficient — both communities independently solve the same sub-problems (retrieval, conflict detection, staleness)
2. Evaluation methods are level-coupled — different metrics for different levels, no unified assessment
3. Transferability increases with compression level (SkillRL: +68.5pp over L1 trajectory retrieval on ALFWorld)
4. Lifecycle management is an afterthought — most systems focus on acquisition, not maintenance

### Trade-offs at Each Level
- Generalizability ↑ as compression ↑
- Specificity ↓ as compression ↑
- Acquisition cost ↑ as compression ↑ (need more traces to extract rules)
- Maintenance cost ↓ as compression ↑ (fewer artifacts to update)

## Cognitive Science Grounding
- **CLS Theory** (Complementary Learning Systems): hippocampal episodic → neocortical knowledge consolidation
- **ACT-R** declarative–procedural distinction
- The paper explicitly cites CLAUDE.md files as a real-world example of manual L3 rule distillation

## Proposed Design Principles
1. **Level-agnostic compression core**: flexible engine for any compression level
2. **Bidirectional promotion/demotion**: dynamic knowledge flow between levels
3. **Continuous lifecycle governance**: provenance, confidence, deprecation tracking

## Testable Predictions
- L2 compression > L1 retrieval for cross-domain transfer (same source experience)
- Multi-level knowledge stores > single-level, advantage grows with deployment duration
- L2 may be "sweet spot" (transferability–specificity curve is concave)
- L3 rules most effective as constraints, not directives

## System Connections (from paper's taxonomy)
- L1 examples: Mem0, DeltaMem, Memory-R1, APEX-MEM, MEM1
- L2 examples: Voyager, SkillX, SKILLFOUNDRY, ASG-SI
- L3: mostly human-specified (Constitutional AI, CLAUDE.md) — not yet automated
- Cross-level: ExpeL (L1+L2), AutoAgent (L1+L2)
