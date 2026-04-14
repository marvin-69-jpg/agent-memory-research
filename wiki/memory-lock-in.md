---
aliases: [memory lock-in, vendor lock-in, platform lock-in, 鎖住, 綁定, 平台鎖定]
first_seen: 2026-04-11
last_updated: 2026-04-11
tags: [lock-in, memory]
---

# Memory Lock-in

封閉 harness 和 stateful API 造成的記憶鎖定問題。Model provider 有強烈動機透過 memory 製造 lock-in，因為單靠模型本身無法鎖住用戶。

## Current Understanding

- 三層嚴重程度：
  1. **Mildly bad** — Stateful API（OpenAI Responses API、Anthropic server-side compaction）：state 存在 provider server，換模型就斷了
  2. **Bad** — Closed harness（Claude Agent SDK）：不知道 harness 怎麼跟 memory 互動，格式不透明、不可轉移
  3. **Worst** — 整個 harness + long-term memory 都在 API 後面（如 Claude Managed Agents）：零控制權、零可見性
- Codex 雖然開源，但生成 **encrypted compaction summary**，無法在 OpenAI 生態外使用
- Model provider API 之間切換很容易（stateless），但一旦有 state 就被綁住
- Harrison Chase 親身經歷：email assistant 被刪除後重建，體驗大幅退步，才體會 memory 的黏性
- 解法：用 open harness（如 [[deep-agents]]），把 memory 控制權留在自己手上
- **新解法 — MCP（Model Context Protocol）**：Mem0 的 OpenMemory MCP 讓記憶存在使用者本機，透過 MCP 標準與 Claude / ChatGPT / Perplexity 整合。記憶不離開機器 = 不被任何平台鎖住。Export/import 功能（Sep 2025）進一步強化 portability
- **19 種 vector store backend**：Mem0 支援從 Qdrant 到 PGVector 到 FAISS，storage layer 也不鎖定
- **"Memory as moat"**（[[yohei-nakajima]]）：AI 越了解你就越難離開，各平台有動機鎖住記憶。消費端（ChatGPT / Claude / Gemini / Grok）都各自建 memory 系統，互不相通
- **"Memory's Plaid"**（Yohei）：中立層讓使用者跨 assistant 攜帶記憶。跟 Mem0 OpenMemory 概念類似但更廣 — 不只是 API 層，是消費者可見的 portability layer

## Key Sources

- **2026-04-01** — Mem0 OpenMemory MCP：local-first memory with portability。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]
- **2026-04-11** — Harrison Chase 分析三層 lock-in 程度，呼籲 open memory。Source: [[raw/harrison-chase-your-harness-your-memory]]

## Related

[[agent-memory]] [[agent-harness]] [[deep-agents]] [[harrison-chase]] [[mem0]] [[yohei-nakajima]]
