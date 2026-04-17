---
aliases: [hwchase17]
first_seen: 2026-04-11
last_updated: 2026-04-17
tags: [people]
---

# Harrison Chase

LangChain CEO。主張 agent harness 與 memory 綁定，memory 應該 open。

## Current Understanding

- LangChain / LangGraph / [[deep-agents]] 的推動者
- 核心觀點：
  - [[agent-harness]] 不會被模型吸收消失
  - Memory 是 harness 的一部分，不可分離
  - 封閉 harness 造成 [[memory-lock-in]]
  - 解法是 open harness + open memory
- 親身經驗：內部 email assistant 被刪後重建，體驗大幅退步 → 體悟 memory 的重要性
- **Agent Builder memory 實踐**（2026-02）：
  - 用 COALA paper 三種記憶分類：procedural（AGENTS.md）、semantic（skills + knowledge files）、episodic（刻意跳過）
  - Virtual filesystem over Postgres — LLM 以 file 介面操作，底層是 DB
  - **所有 memory 修改都需 human-in-the-loop approval**（防 prompt injection）
  - 核心教訓：**"the hardest part of building an agent that could remember things is prompting"** — 一個全職工程師專做 memory prompting
  - Agents 會 append 具體事實但**不會自動 compact learnings** — 需要 end-of-session reflection + 背景 daily process
  - 使用者明確指示 reflect 仍然有價值，即使 agent 有自動 update 能力

## Key Sources

- **2026-02-01** — "How we built Agent Builder's memory system"，生產記憶系統實踐。Source: [[raw/langchain-agent-builder-memory]]
- **2026-04-11** — "Your Harness, Your Memory" 長文。Source: [[raw/harrison-chase-your-harness-your-memory]]

## Related

[[deep-agents]] [[agent-harness]] [[agent-memory]] [[memory-lock-in]] [[sarah-wooders]] [[compounding-memory]] [[letta]] [[filesystem-vs-database]] [[coding-agent-memory]] [[procedural-memory]]
