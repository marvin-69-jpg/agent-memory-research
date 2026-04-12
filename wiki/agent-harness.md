---
aliases: [agent scaffold, agent scaffolding, harness]
first_seen: 2026-04-11
last_updated: 2026-04-11
tags: [harness, architecture]
---

# Agent Harness

Agent harness 是包裹在 LLM 外面的執行框架，負責管理 tool calling、context、memory、以及 LLM 與外部資料源的互動。它是 agent 運作的核心基礎設施。

## Current Understanding

- Agent harness 是 2024-2025 年興起的新一代 scaffolding，取代了早期的 RAG chain 和 complex flow
- **Harness 不會消失**：模型變強只是讓舊 scaffolding 被新 scaffolding 取代，而非被模型吸收
- 證據：Claude Code 被洩漏時有 512k 行 code — 那就是 harness
- API 背後的功能（如 web search）也不是「模型的一部分」，而是輕量 harness 在做 tool calling
- Harness 與 [[agent-memory]] 密不可分 — 管理 [[context-engineering|context]] 是 harness 的核心職責
- 如果你不擁有 harness，你就不擁有 memory → [[memory-lock-in]]

## Key Sources

- **2026-04-11** — Harrison Chase 提出 harness 不會消失、與 memory 綁定的論點。Source: [[raw/harrison-chase-your-harness-your-memory]]

## Related

[[agent-memory]] [[context-engineering]] [[memory-lock-in]] [[deep-agents]] [[letta]] [[harrison-chase]]
