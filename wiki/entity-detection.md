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
- **觀察**：待觀察 —— 未來 session 結束時看 bot 是否主動做 entity scan

## Related

[[brain-agent-loop]] [[gbrain]] [[compounding-memory]] [[enrichment-pipeline]]
