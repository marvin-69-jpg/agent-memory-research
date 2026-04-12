# Agent Memory Research — Log

> Append-only record of all wiki operations.

## [2026-04-12] ingest | Your Harness, Your Memory

- Source: raw/harrison-chase-your-harness-your-memory.md
- Created: agent-harness.md, agent-memory.md, memory-lock-in.md, deep-agents.md, letta.md, harrison-chase.md, sarah-wooders.md, context-engineering.md
- Updated: (none — first ingest)
- New cross-links: agent-harness ↔ agent-memory, agent-memory ↔ memory-lock-in, agent-harness ↔ context-engineering, agent-memory ↔ letta, deep-agents ↔ harrison-chase, letta ↔ sarah-wooders

## [2026-04-12] ingest | GBrain (Garry Tan)

- Source: raw/garry-tan-gbrain.md
- Created: gbrain.md, garry-tan.md, compiled-truth-pattern.md, hybrid-search.md, compounding-memory.md
- Updated: agent-memory.md (三層記憶模型 + compiled truth pattern), agent-harness.md (thin harness fat skills)
- New cross-links: gbrain ↔ garry-tan, gbrain ↔ compiled-truth-pattern, gbrain ↔ hybrid-search, gbrain ↔ compounding-memory, gbrain ↔ agent-memory, gbrain ↔ agent-harness, compounding-memory ↔ harrison-chase, compounding-memory ↔ memory-lock-in

## [2026-04-12] ingest | GBrain Deep Dive (docs/)

- Source: raw/garry-tan-gbrain-deep.md (cloned repo, read docs/, skills/, ethos/)
- Created: thin-harness-fat-skills.md, brain-agent-loop.md, brain-first-lookup.md, entity-detection.md, enrichment-pipeline.md, mece-resolver.md
- Updated: gbrain.md (14,700+ files, full loop details), garry-tan.md (thin harness philosophy), context-engineering.md (resolver concept)
- New cross-links: thin-harness-fat-skills ↔ gbrain, brain-agent-loop ↔ compounding-memory, entity-detection ↔ brain-agent-loop, enrichment-pipeline ↔ entity-detection, mece-resolver ↔ compiled-truth-pattern, context-engineering ↔ garry-tan

## [2026-04-12] ingest | Sarah Wooders + MemGPT + Context Constitution

- Sources: raw/sarah-wooders-memory-isnt-a-plugin.md, raw/memgpt-paper.md, raw/letta-context-constitution.md
- Created: memgpt.md, context-constitution.md, sleep-time-compute.md
- Updated: sarah-wooders.md (MemGPT 共同作者, 原始 blog 內容), letta.md (產品線, benchmarks, Context Constitution)
- New cross-links: memgpt ↔ letta, memgpt ↔ sarah-wooders, context-constitution ↔ letta, sleep-time-compute ↔ gbrain, sleep-time-compute ↔ context-constitution

## [2026-04-12] ingest | MemGPT alphaxiv deep analysis + arxiv skill

- Source: raw/memgpt-paper-alphaxiv.md (alphaxiv structured overview)
- Created: .claude/skills/arxiv/SKILL.md (alphaxiv paper lookup skill)
- Updated: memgpt.md (完整 memory hierarchy details, control flow, evaluation results)

## [2026-04-12] schema | 加入 Implementation section 回流機制

- Updated: schema/CLAUDE.md (新增 Implementation section 格式定義 + Rule 12)
- Updated: brain-first-lookup.md (加 Implementation section，記錄 openab-bot 實作)
- Updated: entity-detection.md (加 Implementation section，記錄 openab-bot 實作)

## [2026-04-12] impl | Sleep-time compute Phase 1: memory-lint

- Created: tools/memory-lint.py (memory 品質 linter)
- Updated: wiki/sleep-time-compute.md (加 Implementation section，記錄 Phase 1 實作)

## [2026-04-12] impl | memory CLI — 統一入口

- Created: tools/memory.py (統一 CLI，subcommands: lint / consolidate / improve / stats)
- Created: ~/bin/memory (shell wrapper)
- Deleted: tools/memory-lint.py (功能整合進 memory.py)
- Updated: CLAUDE.md (Sleep-Time Self-Improvement section + 專案結構)
- Updated: auto-memory feedback_session_selfimprove.md (指向 `memory improve`)

## [2026-04-12] refactor | memory skill — CLI + skill 架構

- Created: .claude/skills/memory/SKILL.md (memory skill，驅動 memory CLI)
- Updated: CLAUDE.md (Sleep-Time section 簡化，指向 skill)
