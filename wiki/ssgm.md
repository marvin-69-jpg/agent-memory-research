---
aliases: [SSGM, Stability and Safety Governed Memory, memory governance]
first_seen: 2026-04-15
last_updated: 2026-04-15
tags: [product, memory, architecture]
---

# SSGM

Stability and Safety Governed Memory（arxiv 2603.11768）。記憶進化的 **governance framework** — 解決「記憶可修改時如何不失控」的問題。與 [[a-mem]] 互補：A-Mem 讓記憶進化，SSGM 讓進化安全。

## Current Understanding

### 問題定義

如果記憶是 mutable 的（[[reconsolidation]]），新的 failure modes 會出現：

1. **Semantic drift** — 記憶語意在反覆 rewrite 中漂移
2. **Procedural drift** — 操作記憶偏離正確步驟
3. **Goal drift** — agent 目標記憶被逐步修改
4. **Memory hallucination** — 記憶系統產生不存在的「回憶」
5. **Temporal obsolescence** — 記憶過時但未被標記（→ [[memory-staleness]]）
6. **Memory poisoning** — 惡意注入假記憶（→ [[neuroscience-memory]] Memory Security）
7. **Privacy leakage** — 記憶洩漏私人資訊

前三種（semantic/procedural/goal drift）是 reconsolidation 特有的 — 記憶可改寫才會漂移。

### 四大設計原則

1. **Pre-consolidation validation** — 寫入前先驗證一致性
2. **Temporal/provenance grounding** — 每條記憶都有時間戳和來源追蹤
3. **Access-scoped retrieval** — 依權限範圍做檢索（→ [[multi-scope-memory]]）
4. **Reversible reconciliation** — 記憶變更可回溯

### 架構組件

**Write Validation Gate**：
- 新記憶或記憶更新在寫入前，先檢查是否與 protected core facts 衝突
- 防止 semantic drift 和 memory poisoning
- 相當於 [[reconsolidation]] 的 gatekeeper

**Read Filtering Gate**：
- Temporal decay：**Weibull distribution**（比 exponential 更好建模 memory 的先快後慢衰減）
- Provenance verification：驗證記憶來源的可信度
- Access control：不同 scope 的記憶有不同存取權限

**Dual Storage**：
- **Mutable Active Graph**：可被 reconsolidate 的活躍記憶
- **Immutable Episodic Log**：不可修改的事件記錄

→ 與 [[compiled-truth-pattern]] 高度呼應：Mutable Active Graph ≈ compiled truth，Immutable Episodic Log ≈ timeline

### 理論保證

**Theorem**: 在每 N 步做一次 reconciliation 的條件下，semantic drift 被限制在 O(N·ε_step)，其中 ε_step 是單步最大漂移量。

這是 agent memory 領域少見的**有理論保證**的設計。

### 與 [[memory-failure-modes]] 的關係

SSGM 的七種失敗模式與 [[chrysb]] 的十種部分重疊、部分互補：
- 重疊：temporal obsolescence ≈ stale context dominance，memory hallucination ≈ over-inference
- SSGM 獨有：semantic/procedural/goal drift（reconsolidation 特有）、memory poisoning、privacy leakage
- Chrys Bader 獨有：entity confusion、retrieval misfire、selective retrieval bias、compaction info loss

## Key Sources

- **2026-03-14** — SSGM: Stability and Safety Governed Memory for LLM Agents。Source: [[raw/ssgm-stability-safety-governed-memory]]

## Related

[[reconsolidation]] [[a-mem]] [[compiled-truth-pattern]] [[memory-failure-modes]] [[memory-staleness]] [[neuroscience-memory]] [[agent-memory]] [[multi-scope-memory]] [[actor-aware-memory]] [[open-questions]] [[agemem]] [[asg-si]] [[d-mem]] [[memory-worth]]
