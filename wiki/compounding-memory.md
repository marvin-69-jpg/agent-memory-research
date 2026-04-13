---
aliases: [compounding knowledge, data flywheel, memory flywheel]
first_seen: 2026-04-12
last_updated: 2026-04-13
tags: [memory, architecture]
---

# Compounding Memory

Agent 記憶的複合成長效應：每次互動都累積知識，agent 隨使用越來越聰明。是 [[agent-memory]] 最重要的價值主張。

## Current Understanding

- **Core loop**（GBrain 的實踐）：
  - Signal 進來（meeting、email、tweet）→ 偵測 entity → 讀 brain 取得 context → 帶著完整 context 回應 → 把新資訊寫回 brain → 索引更新
  - 每次循環都增加知識，下次同個 entity 出現時 agent 已有 context
- **Dream cycle**：agent 在閒置時自動跑 enrichment、修 citation、consolidate memory — 「I wake up and the brain is smarter than when I went to sleep」
- [[harrison-chase]] 的親身經歷也證實這點：email assistant 被刪後重建，體驗大幅退步 — memory 的黏性來自於 compounding
- 沒有 compounding memory 的 agent 每次都從零開始 → 容易被複製 → [[memory-lock-in]] 的反面論述
- Agent 相比人類的根本優勢：可以 fork/duplicate，[[experiential-memory|經驗記憶]]跨所有 instances 共享累積 — compounding 不限於單一 agent
- 隨著部署時間拉長，compounding 產生的資料量將超指數成長，搜尋和組織成為瓶頸 → [[bitter-lesson-search]]
- GBrain 的實際數字：從零到 10,000+ 檔案只花了一週（有大量自動化 enrichment）

## Key Sources

- **2026-04-13** — Viv Trivedy: 跨 agent 累積的優勢和超指數成長的 search 挑戰。Source: [[raw/viv-trivedy-harness-memory-bitter-lesson]]
- **2026-04-12** — GBrain README 的 compounding thesis。Source: [[raw/garry-tan-gbrain]]
- **2026-04-11** — Harrison Chase 論 memory 的 data flywheel 和黏性。Source: [[raw/harrison-chase-your-harness-your-memory]]

## Related

[[gbrain]] [[agent-memory]] [[garry-tan]] [[harrison-chase]] [[memory-lock-in]] [[experiential-memory]] [[bitter-lesson-search]] [[viv-trivedy]]
