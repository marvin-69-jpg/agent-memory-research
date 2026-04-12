---
aliases: [sleep-time compute, dream cycle, background memory processing]
first_seen: 2026-04-12
last_updated: 2026-04-12
tags: [memory, architecture]
---

# Sleep-Time Compute

Agent 在閒置時進行的背景記憶處理 — 重寫 memory state、enrichment、consolidation。在不同系統中有不同名稱但概念一致。

## Current Understanding

- **Letta 的 sleep-time compute**：讓 model 在 downtime「思考」，處理資訊、形成新連結、重寫 memory state。是 scaling AI capabilities 的新方式
- **GBrain 的 dream cycle**：agent 在使用者睡覺時自動跑 enrichment、修 citation、consolidate memory。「I wake up and the brain is smarter than when I went to sleep.」
  - 實作：20+ cron jobs 跑在不同時段（nightly enrichment, weekly lint, etc.）
- **共同點**：
  - 利用 agent 閒置時間做非即時工作
  - 記憶的品質在背景持續提升
  - 使用者不需要主動觸發
- 這個概念跟人類睡眠中的記憶 consolidation 有類比 — 白天收集的資訊在睡眠中被整合到長期記憶

## Key Sources

- **2026-04-02** — Letta Context Constitution 提出 sleep-time compute。Source: [[raw/letta-context-constitution]]
- **2026-04-12** — GBrain 的 dream cycle 實作。Source: [[raw/garry-tan-gbrain-deep]]

## Related

[[context-constitution]] [[letta]] [[gbrain]] [[compounding-memory]] [[brain-agent-loop]]
