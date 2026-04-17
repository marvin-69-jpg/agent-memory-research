---
source_type: whitepaper
url: https://www.kaggle.com/whitepaper-context-engineering-sessions-and-memory
title: "Context Engineering: Sessions & Memory"
authors: [Kimberly Milam, Antonio Gulli]
affiliations: [Google]
date: 2025-11-01
discovered_via: "X/Twitter — Data Science Dojo, WebSearch"
ingested: 2026-04-17
tags: [context-engineering, memory, sessions, production, architecture]
---

# Google: Context Engineering — Sessions & Memory

## 概述

Google 70 頁白皮書，定義 context engineering 為 "assembling exactly the right information at exactly the right time"。系統化地整理 session management、memory types、memory pipeline、provenance、retrieval 策略、multi-agent memory、production 部署考量。

## 核心框架

### Session-Memory Decoupling

- **Session**：離散的工作空間，有明確 lifecycle（start → interact → close）
  - **Events**：不可變的 chronological log（user messages, AI responses, tool calls）
  - **State**：可變的 key-value working memory，在單一對話內有效
- **Memory**：跨 session 持久化的知識
- **關鍵 insight**："sessions end but memories persist" — session 是短暫的容器，但從中萃取的 learnings 成為永久知識

### Two-Tier Memory

1. **Declarative Memory**（factual）：使用者的偏好、身份、歷史（"I'm vegan", "prefer TypeScript"）
2. **Procedural Memory**（behavioral）：使用者的工作方式、決策模式、互動偏好（"debug by checking logs first"）

### Memory Generation Pipeline（LLM-driven ETL）

三階段：
1. **Extract**：LLM 從 session 中自動識別值得記住的資訊
2. **Consolidate**：跟既有記憶 dedup、merge、更新 confidence（"mid-size company" → "200+ developers" → "large company (200+ devs)"）
3. **Load**：寫入 vector DB，供 semantic retrieval

### Provenance Metadata

每條記憶附帶：
- **Source**：哪個 session 產生的
- **Timestamp**：freshness indicator
- **Confidence**：確定性分數

**Trust Hierarchy**（由高到低）：
1. User-stated facts（使用者直接說的）
2. Observed behavioral patterns（觀察到的行為模式）
3. Single observations（單次觀察）
4. Inferred preferences（推斷的偏好）

### Push vs Pull Retrieval

- **Proactive（Push）**：永遠注入 context 的資訊 — 使用者身份、安全關鍵資訊（過敏）、核心偏好、active project
- **Reactive（Pull）**：按需 semantic search — 歷史 debugging pattern、過去 project 細節、procedural knowledge
- 平衡很關鍵：push 太多浪費 token + 慢，push 太少會失憶

### Compaction Strategies

1. **Truncation**：保最新 events，快但 lossy
2. **Keep-Last-N**：保最近 N 個 events，平衡
3. **Recursive Summarization**：LLM 生成摘要，保留語意但增加 latency

### Multi-Agent Memory

三種架構：
1. **Shared Unified History**：所有 agent 讀寫同一個 session，緊密協調
2. **Separate Individual Histories**：每個 agent 維護獨立 session，explicit message passing
3. **A2A Protocol**：標準化 inter-agent communication

### Production Requirements

- Access control、TLS encryption、audit trails
- User consent mechanisms（GDPR/CCPA）
- Asynchronous extraction、edge caching
- Retention policies、graceful degradation

## 與已知概念的連結

- Session-Memory decoupling ≈ GAM 的 EPG（暫存）+ TAN（長期知識）分離
- Provenance trust hierarchy ≈ Memwright 的 RBAC + provenance
- Push vs Pull ≈ ChatGPT 的 proactive memory injection vs RAG systems
- LLM-driven ETL ≈ Brain-Agent Loop 的 Write 階段
- Declarative + Procedural ≈ Mem0 的三種記憶類型（episodic + semantic + procedural）
- Compaction strategies ≈ MEM1 的 context pruning / session-management 的 compact
