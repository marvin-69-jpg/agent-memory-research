---
aliases: [garrytan]
first_seen: 2026-04-12
last_updated: 2026-04-15
tags: [people]
---

# Garry Tan

Y Combinator CEO。開發了 [[gbrain|GBrain]] — 個人 AI agent 知識庫系統。

## Current Understanding

- Y Combinator CEO，從個人 OpenClaw agent 的 markdown brain repo 開始，累積到 14,700+ 檔案
- 提出 [[thin-harness-fat-skills]] 架構哲學（YC Spring 2026 talk）
- 核心觀點：
  - 「The bottleneck is never the model's intelligence. The bottleneck is whether the model understands your schema.」
  - Skill file = method call，markdown is actually code
  - Harness 要 thin（~200 lines），intelligence 在 skills 裡
  - 「If I have to ask you for something twice, you failed.」— codify everything into skills
- 實踐了 [[compounding-memory]]：agent 每天自動 enrich，14,700+ files, 20+ cron jobs
- 將 GBrain 開源（MIT），設計為可搭配任何 agent 使用
- **v0.10.0（2026-04-15）**：公開個人 OpenClaw setup，perfected RESOLVER.md + SOUL.md，24 fat skills with full test coverage，新增 multi-user brain access（ACL）

## Key Sources

- **2026-04-15** — GBrain v0.10.0 發布推文。Source: [[raw/garry-tan-gbrain-v0.10.0]]
- **2026-04-12** — GBrain deep docs (Skillpack, schema, ethos)。Source: [[raw/garry-tan-gbrain-deep]]
- **2026-04-12** — GBrain GitHub repo README。Source: [[raw/garry-tan-gbrain]]

## Related

[[gbrain]] [[compounding-memory]] [[agent-memory]] [[thin-harness-fat-skills]] [[brain-agent-loop]] [[compiled-truth-pattern]] [[context-engineering]] [[context-fragment]]
