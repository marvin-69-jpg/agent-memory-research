---
aliases: [procedural memory, 程序記憶, 技能記憶, how-to memory]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [memory, architecture]
---

# Procedural Memory

第三種記憶類型：儲存「怎麼做」而非「發生了什麼」（episodic）或「知道什麼」（semantic）。在人類認知中對應 skills — 騎腳踏車、打字。在 AI agents 中對應學到的 workflow、tool-use pattern、process knowledge。

## Current Understanding

- **三種記憶的區分**：
  - Episodic：what happened（對話歷史、事件）
  - Semantic：what is known（事實、偏好、知識）
  - Procedural：how to do things（流程、技能、慣例）
- **實際案例**：coding assistant 學到某團隊的 PR 結構、偏好的測試 pattern、部署 workflow。這不是 user preference（「我喜歡 dark mode」），不是事實記憶（「使用者用 TypeScript」），是一個 process
- **Mem0 的實作**：`memory_type="procedural_memory"` 參數路由到不同的 extraction prompt，專注 distilling procedures 和 workflows 而非 facts 和 preferences
- **與 GBrain 的對比**：GBrain 的 thin-harness-fat-skills 架構隱含了 procedural memory — skills 本身就是 procedure 的具體化。但 GBrain 是 explicit skills（寫成 markdown），Mem0 的 procedural memory 是 extracted implicit procedures
- **與 openab-bot 的對比**：我們的 feedback memory 其實部分扮演了 procedural memory 的角色（「日報配圖要用彩蛋不要氛圍」= 一種 procedure），但沒有明確區分 type

## Key Sources

- **2026-04-01** — Mem0 v1.0.0 引入 procedural memory API。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]

## Related

[[mem0]] [[agent-memory]] [[thin-harness-fat-skills]] [[compounding-memory]]
