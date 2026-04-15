---
aliases: [Letta, Letta Code, MemGPT]
first_seen: 2026-04-11
last_updated: 2026-04-12
tags: [product, memory]
---

# Letta

Stateful agent 領域的先驅公司，CTO 是 [[sarah-wooders]]。前身為 MemGPT 研究專案。

## Current Understanding

- 前身為 [[memgpt|MemGPT]]（2023 UC Berkeley 論文），最早提出 self-directed memory management
- 核心主張：memory 不是可插拔的 plugin，而是 [[agent-harness]] 的核心能力
- 產品線：
  - **Letta Code** — memory-first coding harness，#1 model-agnostic on Terminal-Bench
  - **Context Repositories** — git-backed memory filesystem，背景 subagent 做 prompt rewriting
  - **Agent File (.af)** — open file format for serializing stateful agents
  - **Context-Bench / Recovery-Bench / Letta Leaderboard** — memory 相關 benchmarks
  - **Conversations API** — 跨 parallel experiences 共享 memory
  - **Skill Learning** — 從經驗中動態學習 skills
- 發布 [[context-constitution]]：定義 agent 如何管理 context 來從經驗學習
- [[sleep-time-compute]]：agent 閒置時重寫 memory state
- 「Today's models deeply identify with their own ephemerality」— 呼籲 labs 重視 experiential AI 而非只 coding benchmarks
- **Yohei Nakajima 定位**：Letta = Berkeley spinout，$10M funding，model-agnostic agent memory，portable state。在 tools & startups landscape 中是 memory-first 的代表

## Key Sources

- **2026-04-03** — Sarah Wooders "Memory isn't a plugin" 文章。Source: [[raw/sarah-wooders-memory-isnt-a-plugin]]
- **2026-04-02** — Context Constitution 發布。Source: [[raw/letta-context-constitution]]
- **2026-04-11** — Harrison Chase 引用 Letta 觀點。Source: [[raw/harrison-chase-your-harness-your-memory]]
- **2023-10-12** — MemGPT 原始論文。Source: [[raw/memgpt-paper]]

## Related

[[sarah-wooders]] [[memgpt]] [[agent-memory]] [[agent-harness]] [[context-constitution]] [[sleep-time-compute]] [[deep-agents]] [[harrison-chase]] [[yohei-nakajima]] [[memory-lock-in]] [[mem0]]
