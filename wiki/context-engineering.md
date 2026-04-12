---
aliases: [context management, context window management]
first_seen: 2026-04-11
last_updated: 2026-04-11
tags: [context, architecture]
---

# Context Engineering

Harness 管理 LLM context 的方式，決定了 [[agent-memory]] 的一切運作方式。

## Current Understanding

- [[agent-harness]] 的核心職責就是管理 context
- Context engineering 涵蓋的面向（Sarah Wooders 列舉）：
  - AGENTS.md / CLAUDE.md 怎麼載入 context？
  - Skill metadata 怎麼呈現給 agent？（system prompt? system messages?）
  - Agent 能不能改自己的 system instructions？
  - Compaction 後什麼留下、什麼消失？
  - 互動紀錄有沒有被存起來、能不能查詢？
  - Memory metadata 怎麼呈現給 agent？
  - Working directory 怎麼表示？暴露多少 filesystem 資訊？
- Memory 本質上就是 context 的一種形式 — 短期記憶是 in-context，長期記憶是跨 session 載入 context
- 封閉 harness 把 context engineering 藏在 API 後面 → 用戶看不到也控制不了 → [[memory-lock-in]]

## Key Sources

- **2026-04-11** — Sarah Wooders 列出 harness-context 關係的具體面向，被 Harrison Chase 引用。Source: [[raw/harrison-chase-your-harness-your-memory]]

## Related

[[agent-harness]] [[agent-memory]] [[sarah-wooders]] [[memory-lock-in]]
