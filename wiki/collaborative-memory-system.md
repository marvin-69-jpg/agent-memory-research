---
aliases: [collaborative memory, Collaborative Memory, 協作記憶系統]
first_seen: 2026-04-16
last_updated: 2026-04-16
tags: [product, memory, multi-agent, architecture]
---

# Collaborative Memory

Accenture Center for Advanced AI 提出的 multi-user, multi-agent memory sharing framework。第一個明確處理**動態、非對稱存取控制**的 agent memory 系統。

## Current Understanding

### 核心架構

**Dynamic Bipartite Access Graphs**：
- `G_UA(t) ⊆ U × A` — User-to-Agent graph（哪些 user 能用哪些 agent）
- `G_AR(t) ⊆ A × R` — Agent-to-Resource graph（哪些 agent 能存取哪些 resource）
- 兩張圖**隨時間演化**，反映 role 變更、project 調整、policy 更新

**Two-Tier Memory**：
- **Private**（`M_private`）：只有 originating user 看得到。保護機密和個人資訊。
- **Shared**（`M_shared`）：跨 user 選擇性共享。每條 fragment 帶完整 provenance（建立時間、user、agent、resource）。

**Fine-Grained Policies**：
- **Read policy**（`π_read`）：根據 agent 當前權限動態建構 memory view。Filter + transform。
- **Write policy**（`π_write`）：決定新 fragment 是 private 還是 shared。可執行 anonymization、redaction。

### 實驗結果

| Scenario | Dataset | Key Finding |
|---|---|---|
| Fully collaborative | MultiHop-RAG | Accuracy >0.90 不變，resource usage 降 **61%** |
| Asymmetric access | Synthetic Business | 部分共享也有效率增益，strict policy adherence |
| Dynamic evolution | SciQAG | Accuracy 隨 access grant/revoke 即時變化，resource usage 因 memory reuse 持續下降 |

### 意義

- 第一個 formalize **asymmetric, time-varying** access constraints 的 agent memory 系統
- 每條 fragment 帶 provenance → full auditability（跟 [[actor-aware-memory]] 的追蹤需求一致）
- Resource reduction 61% 證明 memory sharing 的 practical value
- 局限：只用 synthetic datasets、沒測 real concurrency、LLM 本身可能 breach policy

### 跟 openab-bot 的對比

| 面向 | Collaborative Memory | openab-bot |
|---|---|---|
| Access control | Dynamic bipartite graphs | 無（所有 session 看同一個 PVC） |
| Memory tiers | Private + Shared | 全 Shared（MEMORY.md + wiki/） |
| Provenance | 每條 fragment 標記 | 無標記（靠 git blame 推斷） |
| Policy | Read/write policy 可配置 | 無 policy |

## Key Sources

- **2025-05-23** — Rezazadeh et al. "Collaborative Memory: Multi-User Memory Sharing in LLM Agents with Dynamic Access Control"。Source: [[raw/rezazadeh-collaborative-memory]]

## Related

[[multi-agent-memory]] [[memory-consistency]] [[actor-aware-memory]] [[multi-scope-memory]] [[mem0]] [[agent-memory]] [[memwright]] [[refinement-regime]]
