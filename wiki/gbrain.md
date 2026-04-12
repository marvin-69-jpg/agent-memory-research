---
aliases: [GBrain, garry brain]
first_seen: 2026-04-12
last_updated: 2026-04-12
tags: [product, memory, architecture]
---

# GBrain

Garry Tan（Y Combinator CEO）開發的個人知識庫系統。核心理念：agent 每次回應前讀 brain、每次對話後寫 brain，知識隨使用自動複合成長。

## Current Understanding

- **三層架構**：Brain Repo（git，markdown = source of truth）→ GBrain（Postgres + pgvector retrieval layer）→ AI Agent（read/write through skills）
- **Knowledge model**：每個 page 分兩部分 — compiled truth（可改寫的當前理解）+ timeline（append-only 證據軌跡）→ [[compiled-truth-pattern]]
- **搜尋**：[[hybrid-search]]（vector + keyword + RRF fusion + multi-query expansion）
- **三層 chunking**：Recursive（快速）、Semantic（品質）、LLM-guided（最貴最好）
- **三層記憶模型**：gbrain（世界知識）、agent memory（操作偏好）、session context（當下對話）
- Database：10 張 Postgres table，pgvector embedding，支援 PGLite（本地免 server）或 Supabase
- Integrations：Voice / Email / X / Calendar / Meeting 自動匯入
- Skills 用「fat markdown」定義 → [[thin-harness-fat-skills]]
- **MECE directories + resolver**：每塊知識有唯一 primary home → [[mece-resolver]]
- [[brain-agent-loop]]：Signal → Detect → Read → Respond → Write → Sync
- [[brain-first-lookup]]：永遠先查 brain，external API 是 fallback
- [[entity-detection]]：每個 message 都 spawn async sub-agent 偵測 entity
- [[enrichment-pipeline]]：三層 tier 分配 API 資源，facts are table stakes, texture is the value
- 實際規模：14,700+ 檔案、3,000+ 人物 dossier、13 年日曆、280+ 會議逐字稿、40+ skills、20+ cron jobs
- **Dream cycle**：agent 在使用者睡覺時自動跑 enrichment、修 citation、consolidate memory
- 設計給 OpenClaw / Hermes Agent，但也支援任何 MCP client（Claude Code、Cursor 等）
- MIT 授權

## Key Sources

- **2026-04-12** — Deep dive: Skillpack, schema, ethos docs。Source: [[raw/garry-tan-gbrain-deep]]
- **2026-04-12** — GitHub README 完整架構文件。Source: [[raw/garry-tan-gbrain]]

## Related

[[garry-tan]] [[compiled-truth-pattern]] [[hybrid-search]] [[compounding-memory]] [[agent-memory]] [[agent-harness]] [[thin-harness-fat-skills]] [[brain-agent-loop]] [[brain-first-lookup]] [[entity-detection]] [[enrichment-pipeline]] [[mece-resolver]]
