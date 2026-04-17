---
aliases: [Mem0, mem0ai, Mem0g]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [product, memory, architecture]
---

# Mem0

專門的 AI agent memory 基礎設施，提供 selective memory pipeline：從對話中抽取離散事實、去重、只 retrieve 相關的記憶。ECAI 2025 論文驗證其方法優於 10 種替代方案。

## Current Understanding

- **核心機制**：extraction phase 從每組訊息中抽取顯著事實，與現有記憶比對後執行四種操作之一：ADD、UPDATE、DELETE、NOOP。這讓記憶庫隨時間保持準確
- **Mem0g（graph-enhanced）**：在 vector store 旁邊建 directed labeled knowledge graph。三步驟：entity extractor（識別 nodes）→ relations generator（推斷 labeled edges）→ conflict detector（寫入前檢查矛盾）
- **LOCOMO benchmark 表現**：
  - Full-context: 72.9% accuracy, 9.87s latency, ~26,000 tokens
  - Mem0g: 68.4%, 1.09s, ~1,800 tokens
  - Mem0: 66.9%, 0.71s, ~1,800 tokens
  - Zep: 61.0%, 0.70s
  - OpenAI Memory: 52.9%
- **Trade-off**：接受 6% accuracy 差距換取 91% latency 降低和 90% token 節省。Graph variant 再追回 ~1.5% accuracy
- **四層 memory scope**：user_id（跨 session）、agent_id（特定 agent）、run_id/session_id（單次對話）、app_id/org_id（組織共享）
- **三種記憶類型**：episodic（what happened）、semantic（what is known）、procedural（how to do things）
- **Actor-aware memory**（June 2025）：multi-agent 場景下追蹤每條記憶的來源 actor，避免 agent A 的推論被 agent B 當成使用者原話
- **OpenMemory MCP**：本地 privacy-first 替代方案，透過 MCP 與 Claude / ChatGPT / Perplexity 整合，資料不離開使用者機器
- **生態系統**（Q1 2026）：13 agent framework 整合、3 voice agent 整合、19 vector store backends、多個 developer tool 整合
- **Production lessons**：async 寫入（不 block response）、reranker 二次排序、metadata filtering、memory depth + usecase 配置、structured exception

## Key Sources

- **2026-04-01** — State of AI Agent Memory 2026 全景報告：benchmark 數據、graph memory production-ready、四層 scope 模型、procedural memory。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]

## Related

[[locomo]] [[graph-memory]] [[procedural-memory]] [[multi-scope-memory]] [[actor-aware-memory]] [[memory-staleness]] [[memgpt]] [[letta]] [[hybrid-search]] [[agent-memory]] [[memory-lock-in]] [[agemem]] [[compounding-memory]] [[filesystem-vs-database]] [[memory-arena]] [[yohei-nakajima]] [[mirix]] [[multimodal-memory]] [[neuroscience-memory]] [[synapse]] [[collaborative-memory-system]] [[fluxmem]] [[memwright]]
