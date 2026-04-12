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

## Related

[[brain-agent-loop]] [[gbrain]] [[compounding-memory]] [[enrichment-pipeline]]
