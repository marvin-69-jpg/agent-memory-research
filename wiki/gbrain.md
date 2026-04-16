---
aliases: [GBrain, garry brain]
first_seen: 2026-04-12
last_updated: 2026-04-15
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
- 實際規模：14,700+ 檔案、3,000+ 人物 dossier、13 年日曆、280+ 會議逐字稿、20+ cron jobs
- **v0.10.0（2026-04-15）— 重大更新**：
  - 24 個 fat skills（有完整 e2e tests、evals、unit tests）
  - RESOLVER.md 和 SOUL.md 完善（Garry 稱「perfected」）
  - **Multi-user brain access** — ACL 機制讓多人共用同一個 brain
  - 個人 OpenClaw setup 公開，讓其他人可以直接使用 Garry 的配置
- **Dream cycle**：agent 在使用者睡覺時自動跑 enrichment、修 citation、consolidate memory
- **Resolvers 深化（2026-04-16）**：Garry 發表 Resolver 長文，完整闡述 resolver = context routing table。20K→200 行 CLAUDE.md 瘦身、trigger evals（50 test cases）、check-resolvable meta-skill（找到 15% unreachable skills）、[[context-rot]] 衰敗時間線、self-healing resolver 方向
- **GStack**：coding layer，fat skills in markdown，72K+ GitHub stars。Skills call GBrain knowledge，together = full architecture
- 設計給 OpenClaw / Hermes Agent，但也支援任何 MCP client（Claude Code、Cursor 等）
- MIT 授權

## Key Sources

- **2026-04-16** — Resolver 長文：routing table for intelligence、trigger evals、check-resolvable、context rot。Source: [[raw/garry-tan-resolvers-routing-table]]
- **2026-04-15** — v0.10.0 發布：24 fat skills、perfected RESOLVER.md/SOUL.md、multi-user ACLs。Source: [[raw/garry-tan-gbrain-v0.10.0]]
- **2026-04-12** — Deep dive: Skillpack, schema, ethos docs。Source: [[raw/garry-tan-gbrain-deep]]
- **2026-04-12** — GitHub README 完整架構文件。Source: [[raw/garry-tan-gbrain]]

## Related

[[garry-tan]] [[compiled-truth-pattern]] [[hybrid-search]] [[compounding-memory]] [[agent-memory]] [[agent-harness]] [[thin-harness-fat-skills]] [[brain-agent-loop]] [[brain-first-lookup]] [[entity-detection]] [[enrichment-pipeline]] [[mece-resolver]] [[filesystem-vs-database]] [[multi-scope-memory]] [[sleep-time-compute]] [[context-rot]] [[self-improving-agent]] [[skillfoundry]]
