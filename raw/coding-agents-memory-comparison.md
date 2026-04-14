# Coding Agent Memory Architecture Comparison (2025-2026)

- **Sources**: Multiple (aggregated from X/Twitter searches + docs)
- **Date**: 2026-04 (compiled)
- **Type**: Synthesis from multiple sources

---

## Claude Code — Three-Layer Memory

Source: @himanshustwts analysis + MindStudio blog + source code leak

- **Layer 1 — MEMORY.md index**: Always loaded into context, but only stores pointers (~150 chars/line). Design principle: "index always, content never". Hard-coded 200-line limit, silently truncates beyond.
- **Layer 2 — grep-based search**: Live codebase search on demand, no pre-loading into context
- **Layer 3 — Chyros daemon (unreleased)**: Background process for embedding-based semantic indexing and stale memory cleanup

Design philosophy: Memory is for **coordination** (defining when Claude should ask vs act), not for remembering conversations. Each session re-injects markdown files, no active cross-session learning.

Source: https://x.com/himanshustwts/status/2038924027411222533

## Cursor — Dynamic Context Discovery

Source: @cursor_ai official + @elie2222 practitioner

- Doesn't statically load large amounts into prompt
- Treats outputs, history, tools as "files the agent can selectively read"
- Agent decides what to read — on-demand, not pre-loaded
- Multiple MCP servers reduce tokens by 46.9%
- `.cursorrules` and `.cursor/rules/*.mdc` for project-level context
- **User memory hack**: `learned-memories.mdc` rule — Cursor writes past mistakes into it, auto-loaded next session

Source: https://x.com/cursor_ai/status/2008644063797387618

## Windsurf — Cascade Memories

Source: @windsurf_ai official + @jeffwsurf

- **Cascade Memories**: System automatically learns patterns from conversation during work
- Can be manually triggered or edited after the fact
- Design metaphor: senior engineer > junior not because more technical, but because accumulated context
- **Wave 2 (2025)**: Automated Memories — learns patterns from usage behavior automatically
- `.windsurfrules` for project-level rules
- Cascade Engine: preprocesses codebase into dependency graph, Rust core, local cache
- Enterprise: team-level shared memories
- ~48hr usage before it learns your architecture patterns

Source: https://x.com/windsurf_ai/status/1942373210844193201

## Cline — Memory Bank Methodology

Source: docs.cline.bot

- Memory Bank is **not a built-in feature** but a methodology using custom instructions + `.clinerules`
- Every session start: Cline **must** read all memory bank files (enforced rule)
- Core file set: `projectbrief.md`, `productContext.md`, `activeContext.md`, `systemPatterns.md`, `techContext.md`, `progress.md`
- `new_task` tool: clean session end → new session with structured summary (solves context window limit)

Source: https://docs.cline.bot/features/memory-bank

## Cross-Agent Comparison

| Axis | Claude Code | Cursor | Windsurf | Cline |
|---|---|---|---|---|
| Memory type | Markdown files (MEMORY.md + project CLAUDE.md) | Rules files (.mdc) + agent-chosen reads | Auto-learned patterns (Cascade Memories) | Methodology (manual markdown files) |
| Retrieval | Always-inject index + on-demand grep | Agent-chosen file reads | Auto-inject learned patterns | Forced full read at session start |
| Cross-session | Re-inject markdown each session | Re-load rules each session | Persistent Cascade Memories | Re-read memory bank files |
| Learning | No active learning (user writes MEMORY.md) | User writes rules + learned-memories hack | Automatic pattern learning | User maintains memory bank |
| Chrysb axis 7 | Hook-driven (MEMORY.md always injected) | Tool-driven (agent decides what to read) | Hook-driven (Cascade auto-injects) | Always-injected (forced full read) |
| Chrysb axis 8 | User is curator | User + agent are curators | System is curator | User is curator |

## Key Insight

All four coding agents converge on **file-based memory** — markdown files that can be version-controlled, edited by humans, and read by agents. This validates the [[filesystem-vs-database]] debate's file camp for this use case. But they diverge on **who curates** (user vs system) and **when retrieval happens** (always vs on-demand vs auto-learned).
