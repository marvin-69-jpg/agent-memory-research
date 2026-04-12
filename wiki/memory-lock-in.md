---
aliases: [memory lock-in, vendor lock-in, platform lock-in]
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

## Key Sources

- **2026-04-11** — Harrison Chase 分析三層 lock-in 程度，呼籲 open memory。Source: [[raw/harrison-chase-your-harness-your-memory]]

## Related

[[agent-memory]] [[agent-harness]] [[deep-agents]] [[harrison-chase]]
