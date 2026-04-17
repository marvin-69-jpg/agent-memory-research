---
aliases: [enrichment, tiered enrichment]
first_seen: 2026-04-12
last_updated: 2026-04-12
tags: [memory, architecture]
---

# Enrichment Pipeline

GBrain 的分層 enrichment 策略：根據 entity 重要性分配不同等級的 API 資源。

## Current Understanding

- **三層 Tier**：
  | Tier | API Calls | 適用對象 |
  |------|-----------|----------|
  | Tier 1 | 10-15 | Key people, inner circle — 全套 pipeline |
  | Tier 2 | 3-5 | Notable people — web + social + cross-ref |
  | Tier 3 | 1-2 | Minor mentions — brain cross-ref + social |
- **Raw data 分開存**：每次 enrichment 的原始 API response 存在 `.raw/` sidecar（auditable, re-processable）
- **Person page 不只是 LinkedIn scrape** — sections: Executive Summary, State, What They Believe, What They're Building, What Motivates Them, Assessment, Trajectory, Relationship, Contact, Timeline
- 「Facts are table stakes. TEXTURE is the value.」— 要抽取 opinions, emotions, recurring topics, energy level
- **不 overwrite human-written assessments** — API data goes into State/Contact/Timeline，使用者的 Assessment 是 sacrosanct
- **X/Twitter 是 most underrated data source** — tweets reveal beliefs, building, hobby horses, network, trajectory
- **Cross-references 不是 optional** — enrich 完一個 person，要更新他的 company page，反之亦然
- Enrichment fires on every signal — brain grows as side effect of normal operations

## Key Sources

- **2026-04-12** — GBrain enrichment-pipeline guide。Source: [[raw/garry-tan-gbrain-deep]]

## Related

[[gbrain]] [[entity-detection]] [[brain-agent-loop]] [[compiled-truth-pattern]] [[memu]]
