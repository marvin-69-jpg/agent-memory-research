---
aliases: [multi-scope memory, four-scope model, 多層 scope 記憶, memory scoping]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [memory, architecture]
---

# Multi-Scope Memory

記憶的分層 scope 模型 — 每條記憶綁定一個或多個 scope identifier，決定 retrieval 時看到什麼。Mem0 的四層 scope 是目前 API 設計的典範。

## Current Understanding

- **四層 scope**：
  1. **user_id** — 屬於特定使用者，跨所有 session 持久
  2. **agent_id** — 屬於特定 agent instance
  3. **run_id / session_id** — 限定在單次對話或 workflow run
  4. **app_id / org_id** — 組織級共享 context
- **Scope 可組合**：query 可以限定「某個 user 在某個 run 內」，或「某個 user 跨所有 run」。Retrieval pipeline 自動 merge，user memories 排在 session context 上面
- **Metadata filtering**（v1.0.0 新增）：除了 scope 之外，記憶可帶 structured metadata（如 `{"context": "healthcare"}`），search 時可按 tag 過濾。解決 multi-tenant 場景
- **與 GBrain 的對比**：GBrain 用 folder hierarchy 做 scope（`world/` vs `operational/` vs 各 entity folder），是 filesystem-based scoping。Mem0 用 API-level identifier，更靈活但需要外部系統管 identity
- **與 openab-bot 的對比**：我們的 auto-memory 有 type（user/feedback/project/reference）但沒有 scope。所有記憶都是全域的。如果有多個使用者，需要手動加 user 標記

## Key Sources

- **2026-04-01** — Mem0 四層 scope 模型和 metadata filtering。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]

## Related

[[mem0]] [[agent-memory]] [[gbrain]] [[actor-aware-memory]] [[context-engineering]] [[coding-agent-memory]] [[mirix]] [[multimodal-memory]] [[neuroscience-memory]] [[ssgm]] [[collaborative-memory-system]] [[memory-consistency]] [[multi-agent-memory]] [[session-management]] [[fluxmem]]
