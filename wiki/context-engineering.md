---
aliases: [context management, context window management]
first_seen: 2026-04-11
last_updated: 2026-04-13
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
- [[garry-tan]] 的 **Resolver** 概念：context 的 routing table，task X 出現時自動載入 document Y。CLAUDE.md 從 20,000 行瘦身到 200 行 pointer — 解決 attention degradation
- [[viv-trivedy]] 提出 [[context-fragment|Context Fragment]] 概念：context window 中每個 loaded object 都是 user 或 harness designer 的顯式決策 — 把 context engineering 從「塞東西」提升到「每個 slot 都是設計」
- 「The bottleneck is never the model's intelligence. The bottleneck is whether the model understands your schema.」
- **Harness engineering 是 context engineering 的上層**（dex）：context engineering = 怎麼傳 context 給 LLM。Harness engineering = 怎麼 engineer agent 的 integration points（hooks、skills、MCPs）→ [[harness-engineering]]
- **Context durability**（Philipp Schmid）：context 跨 session 的持久性是新瓶頸，harness 是解法
- **Branching Point model**（Thariq / Claude Code team）：每個 turn 結束時使用者有五個 context management 選擇 — continue / rewind / clear / compact / subagents。Context engineering 的使用者介面從「怎麼塞 context」延伸到「怎麼決定下一個 turn 的 context base」。詳見 [[session-management]]

## Key Sources

- **2026-04-16** — Thariq (Claude Code): Every Turn Is a Branching Point，session management 作為 context engineering 的操作介面。Source: [[raw/thariq-claude-code-session-management]]
- **2026-04-13** — Viv Trivedy 的 Context Fragment 概念，每個 loaded object 是設計決策。Source: [[raw/viv-trivedy-harness-memory-bitter-lesson]]
- **2026-04-12** — GBrain 的 Resolver 概念和 context routing。Source: [[raw/garry-tan-gbrain-deep]]
- **2026-04-11** — Sarah Wooders 列出 harness-context 關係的具體面向，被 Harrison Chase 引用。Source: [[raw/harrison-chase-your-harness-your-memory]]

## Related

[[agent-harness]] [[agent-memory]] [[sarah-wooders]] [[memory-lock-in]] [[garry-tan]] [[thin-harness-fat-skills]] [[context-fragment]] [[viv-trivedy]] [[harness-engineering]] [[philipp-schmid]] [[coding-agent-memory]] [[context-constitution]] [[hybrid-search]] [[memgpt]] [[multi-scope-memory]] [[scaffolding-lifecycle]] [[mece-resolver]] [[meta-harness]] [[session-management]] [[context-rot]] [[mem1]]
