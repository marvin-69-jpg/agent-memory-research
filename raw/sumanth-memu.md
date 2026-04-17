---
source: x.com + github
author: Sumanth (@Sumanth_077), NevaMind-AI
url: https://x.com/Sumanth_077/status/2008177201955643402
github: https://github.com/NevaMind-AI/memU
date: 2026-01-05
fetched: 2026-04-17
tags: [agent-memory, filesystem, multimodal, proactive, benchmark]
---

# MemU: Agentic Memory Framework (Filesystem-based)

Sumanth, X tweet (73.8K views, 1.3K likes), 2026-01-05. GitHub: NevaMind-AI/memU.

## Core Proposition

> Memory is not an index. It's something the model can understand.

File-system based agent memory. Markdown files. Agent decides what to remember. Open source.

## Three-Layer Architecture

| Layer | 內容 | 檔案系統比喻 |
|---|---|---|
| Resource | 原始資料（files, conversations, docs, images） | Mount points |
| Item | 提取的記憶單元 — 具體事實 | Files |
| Category | 自動組織的主題分組 | Folders |

Memory structure:
- Folders = Categories（auto-organized topics）
- Files = Memory Items（extracted facts）
- Symlinks = Cross-references
- Mount points = Resources

## Dual-Mode Retrieval

| Mode | 速度 | 成本 | 能力 |
|---|---|---|---|
| RAG (`method="rag"`) | ms | Embedding cost | Sub-second surfacing, continuous monitoring |
| LLM (`method="llm"`) | Seconds | LLM inference | Intent prediction, query evolution, anticipatory reasoning |

## Multimodal Support

```python
memorize(modality="conversation" | "document" | "image" | "video" | "audio")
```

Auto cross-references across modalities. Surfaces visual context when discussing related topics.

## Key Features

- **Continuous Learning**: zero-delay memory availability, background monitoring without constant LLM
- **Cost Optimization**: caches insights, avoids redundant LLM calls — critical for 24/7 agents
- **Auto-Categorization**: new memories self-organize into topics without manual tagging
- **Proactive Filtering**: scoped retrieval via `where` for user-specific or multi-agent coordination
- **Provider Flexibility**: custom LLM + embedding providers (Aliyun, Voyage AI, OpenRouter, beyond OpenAI)

## Benchmark

> MemU achieved **92.09% average accuracy** on the LoCoMo benchmark across reasoning tasks.

## Design Philosophy

- "Memory like a file system — structured, hierarchical, and instantly accessible"
- Agent autonomously learns what to remember, promotes frequently used knowledge, reorganizes as usage evolves
- Retrieval works top-down, falls back gracefully
- Markdown files at Category layer follow same design philosophy as Anthropic's skills.md
