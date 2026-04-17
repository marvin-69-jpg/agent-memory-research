---
source: x.com (multiple)
author: Ksenia_TuringPost, Shannon Sands (@max_paperclips), Andy Nguyen (@kevinnguyendn)
date: 2026-04-03 to 2026-04-07
fetched: 2026-04-17
tags: [filesystem, markdown, memory, convergence]
---

# Markdown Memory Convergence — Multiple Systems, Same Design

多個獨立開發的系統同時收斂到 markdown + filesystem 作為 agent memory 基底。

## Source 1: OpenClaw (Ksenia_TuringPost)

https://x.com/TheTuringPost/status/2024540032590368790

> How OpenClaw is built (and why it's so different)
> The key design decision – it's a workspace directory of Markdown files
> Identity, memory, skills, tool policies, heartbeat rules – all live on disk
> At the center is Gateway – a single long-running process. Everything flows through it
> WhatsApp, Telegram, Slack, Discord, etc. are just channel adapters
> Sessions are persisted JSONL transcripts. A session key encodes agent, provider, thread scope, and isolation
> Agents are execution runtimes. Each agent has its own identity, workspace directory, model configuration, and tool policy
> Memory is file-backed Markdown as source of truth, with hybrid semantic + keyword retrieval layered on top
> In general, OpenClaw behaves like a stateful AI control plane – a small AI operating system centered on the Gateway

Key: memory 是 file-backed Markdown，retrieval（semantic + keyword）是 layer on top，不是 source of truth。Source of truth 永遠是 file。

## Source 2: Shannon Sands (@max_paperclips)

https://x.com/max_paperclips/status/2039911819545076222
12.6K views, 233 likes. Apr 3, 2026.

> markdown works stupidly well for memory systems. especially with obsidian to visualise it. add YAML front matter and you kinda have something that just works well, is easy to read by users and agents

回覆 Karpathy (@karpathy) 的 "LLM Knowledge Bases" 貼文：
> Something I'm finding very useful recently: using LLMs to build personal knowledge bases for various topics of research interest. In this way, a large fraction of my recent token throughput is going less into manipulating code, ...

## Source 3: ByteRover / Hermes (Andy Nguyen @kevinnguyendn)

https://x.com/kevinnguyendn/status/2040446986277777595

> ByteRover is now live in the Hermes Agent memory update @NousResearch
> One minute setup: just run hermes memory setup and your agent gets memory.
> Fully open-source & local, no cloud API keys. Built on native markdown architecture (validated by @karpathy), but we automated the entire curation (management) layer so memory actually scales with projects.
> Prompt as usual, and the agent will recall the exact knowledge and historical decisions.
> Proven in real production with teams. Optimized for accuracy, latency & token reduction.

Andy Nguyen 是 byterover.dev 創辦人，自述 "Building an agentic memory layer for coding agents to help millions of devs vibe code better"

## Convergence Pattern

| System | Markdown as Source of Truth | Retrieval Layer | Automated Curation |
|---|---|---|---|
| OpenClaw | ✅ workspace dir | hybrid semantic + keyword | — |
| ByteRover/Hermes | ✅ native markdown | — | ✅ automated management |
| MemU | ✅ markdown files | ✅ RAG + LLM dual mode | ✅ auto-categorization |
| GBrain | ✅ 14,700+ markdown files | vector search | — |
| Claude Code | ✅ CLAUDE.md + memory/*.md | grep | — |
| Cursor | ✅ .cursor/rules | — | — |

所有系統共享的設計決策：
1. Markdown 是 source of truth（不是 DB dump 的 view）
2. LLM 直接看得懂 markdown（不需要 serialize/deserialize）
3. Git-compatible（history 免費拿）
4. Human-readable（debugging 不需要工具）
5. Retrieval 是加在上面的 layer，不是 mandatory
