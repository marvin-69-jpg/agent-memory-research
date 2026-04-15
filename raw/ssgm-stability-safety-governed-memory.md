---
title: "SSGM: Stability and Safety Governed Memory for LLM Agents"
source: arxiv
paper_id: "2603.11768"
date: 2026-03-14
url: https://www.alphaxiv.org/overview/2603.11768
topic: reconsolidation
---

# SSGM: Stability and Safety Governed Memory

## 核心概念

記憶進化的 **governance framework** — 解耦 memory evolution 和 execution，確保 evolving memory 不會失控。

## Failure Taxonomy（七種記憶失敗）

1. **Semantic drift** — 記憶語意在反覆 rewrite 中漂移
2. **Procedural drift** — 操作記憶偏離原本的正確步驟
3. **Goal drift** — agent 的目標記憶被逐步修改
4. **Memory hallucination** — 記憶系統產生不存在的「回憶」
5. **Temporal obsolescence** — 記憶過時但未被標記
6. **Memory poisoning** — 惡意注入假記憶
7. **Privacy leakage** — 記憶洩漏私人資訊

## 四大設計原則

1. **Pre-consolidation validation** — 寫入前先驗證
2. **Temporal/provenance grounding** — 每條記憶都有時間戳和來源
3. **Access-scoped retrieval** — 依權限範圍做檢索
4. **Reversible reconciliation** — 記憶變更可回溯

## 架構

### Write Validation Gate
- 新記憶寫入前，檢查是否與 protected core facts 衝突
- 防止 semantic drift 和 memory poisoning

### Read Filtering Gate
- **Temporal decay**：Weibull distribution（比 exponential 更好建模 memory 的先快後慢衰減）
- **Provenance verification**：驗證記憶來源的可信度
- **Access control**：不同 scope 的記憶有不同存取權限

### Dual Storage
- **Mutable Active Graph**：可被 reconsolidate 的活躍記憶
- **Immutable Episodic Log**：不可修改的事件記錄（audit trail）

## 理論保證

**Theorem**: 在每 N 步做一次 reconciliation 的條件下，semantic drift 被限制在 O(N·ε_step)。

## 與 Reconsolidation 的關係

SSGM 是對 reconsolidation 的 **safety wrapper**：
- A-Mem 解決了「記憶應該可修改」的問題
- SSGM 解決了「可修改的記憶如何不失控」的問題
- Dual storage（mutable + immutable）呼應 compiled-truth-pattern（compiled truth + timeline）
- Write Validation Gate 是 reconsolidation 的 gatekeeper — 不是所有 reconsolidation 都該被允許
