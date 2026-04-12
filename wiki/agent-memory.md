---
aliases: [agent memory, memory system, LLM memory]
first_seen: 2026-04-11
last_updated: 2026-04-12
tags: [memory, architecture]
---

# Agent Memory

Agent 記憶系統，讓 agent 能跨 session 累積知識、個人化體驗。Memory 本質上是 context 的一種形式，由 [[agent-harness]] 管理。

## Current Understanding

- Memory 分為兩類：
  - **短期記憶**：對話中的 messages、tool call 結果 → harness 管理
  - **長期記憶**：跨 session 記憶 → harness 負責讀寫更新
- Memory 目前仍處於**極早期**，業界尚未找到通用抽象
  - 長期記憶常不在 MVP 中 — 先讓 agent 能動，再處理個人化
  - 未來可能出現獨立的 memory 系統，但現在 memory 跟 harness 綁死
- Memory 是 agent 最強的**差異化來源**：沒有 memory 的 agent 任何人都能複製
- Memory 創造 **data flywheel**：越用越好、越換越痛 → [[memory-lock-in]]、[[compounding-memory]]
- Sarah Wooders: "memory isn't a plugin — it's the harness"
- [[gbrain|GBrain]] 提出三層記憶模型：world knowledge（gbrain）、operational state（agent memory）、session context — 三層都該被查詢
- 知識頁面的最佳實踐：[[compiled-truth-pattern]]（compiled truth 可改寫 + timeline append-only）

## Key Sources

- **2026-04-12** — GBrain 實踐三層記憶模型和 compounding memory loop。Source: [[raw/garry-tan-gbrain]]
- **2026-04-11** — Harrison Chase 論述 memory 是 context 的形式、與 harness 不可分。Source: [[raw/harrison-chase-your-harness-your-memory]]

## Related

[[agent-harness]] [[context-engineering]] [[memory-lock-in]] [[letta]] [[sarah-wooders]] [[gbrain]] [[compounding-memory]] [[compiled-truth-pattern]]
