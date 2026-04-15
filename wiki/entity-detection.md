---
aliases: [entity detection, signal detection]
first_seen: 2026-04-12
last_updated: 2026-04-12
tags: [memory, architecture]
---

# Entity Detection

在每個 inbound message 上自動偵測 entity 和 original thinking，讓 brain 持續成長。是 [[brain-agent-loop]] 的第一步。

## Current Understanding

- **Async sub-agent**：spawn on EVERY message，不 block 回應。用 Sonnet（便宜快速），不用 Opus
- **優先級**：Ideas FIRST（original thinking 最重要）→ Entity mentions → Back-linking → Sync
- **Filing rules**：
  - 使用者自己的想法 → `originals/`（保留原始措辭，語言本身就是洞察）
  - 世界概念 → `concepts/`
  - 產品/商業想法 → `ideas/`
  - 人物 → `people/`，公司 → `companies/`
- **Iron Law of Back-Linking**：每個 entity mention 必須從 entity page 建 back-link 到 source。Unlinked mention = broken brain
- **Notability filtering**：不是每個提及都建 page — passing references, metaphors, one-off encounters 跳過
- **Dedup**：建 page 前必須先 `gbrain search`。Variant spellings / nicknames 會造成重複
- **不建 stubs**：如果建 page 就做好，跑 web search 填充 compiled truth

## Key Sources

- **2026-04-12** — GBrain entity-detection guide。Source: [[raw/garry-tan-gbrain-deep]]

## Implementation

### 2026-04-12 — 應用到 openab-bot auto-memory

- **做法**：加規則到 CLAUDE.md —— 對話收尾時批次掃一遍整段對話，檢查有沒有該存但漏存的 entity（人、專案、偏好/決策、外部資源）。判斷標準：「下一個 session 的我遇到類似情境，會需要知道什麼？」
- **簡化**：GBrain 是每條 message 都跑 async sub-agent，我們簡化為對話結束時一次掃。沒有 async sub-agent、沒有 notability filtering、沒有自動 web search enrichment。是即時存記憶的 safety net，不是取代它。
- **PR**：追溯記錄在 marvin-69-jpg/agent-memory-research#1 comment
- **觀察**（2026-04-13）：在 04-11 ~ 04-13 的多個 session 中，bot 有在對話中**即時**存 feedback memory（被糾正時立刻寫），但**收尾時的批次 entity scan 從未被觸發過**。原因：(1) 對話通常沒有明確「收尾」時刻（使用者直接離開或換 thread），(2) CLAUDE.md 裡的觸發條件（「使用者說謝謝 / 沒有後續 / 明確收尾」）太模糊。**結論：即時存記憶運作良好，但 safety net 掃描機制形同虛設。需要更明確的觸發點，或改成 CLI 定期掃。**

### 2026-04-13 — UserPromptSubmit Hook：每則訊息注入提醒

- **做法**：在 `UserPromptSubmit` hook 中同時注入 entity-detection 提醒 — 使用者透露身份/角色/偏好時，立即存記憶
- **機制**：與 brain-first lookup 共用同一個 hook，每次使用者送訊息都提醒
- **為什麼不用獨立機制**：entity detection 的問題不是「不知道該做」而是「回答優先級比存記憶高」。透過 hook 在回答前注入提醒，強制 agent 先處理 entity 再回答
- **預期效果**：從 0% → 有改善（最難的 pattern，因為需要 agent 改變優先級而非只是加一步操作）
- **觀察**：待下次 benchmark 驗證

## Related

[[brain-agent-loop]] [[gbrain]] [[compounding-memory]] [[enrichment-pipeline]] [[actor-aware-memory]] [[graph-memory]] [[mece-resolver]] [[memory-failure-modes]] [[multimodal-memory]]
