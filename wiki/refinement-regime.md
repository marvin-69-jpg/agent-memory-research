---
aliases: [refinement regime, self-refinement regime, refinement taxonomy]
first_seen: 2026-04-19
last_updated: 2026-04-19
tags: [architecture, reasoning, system]
---

# Refinement Regime — Self-Refinement 的三種體制

把 self-refinement 研究分成三種體制，每種靠不同機制解決「LLM 原生不會 self-critique」的核心困境。

## Current Understanding

### 為什麼需要這個分類

三篇獨立來源都觀察到相同的 empirical fact：**LLM 原生無法有效 self-refinement，prompt-only 的 "please refine your answer" 經常 degrade 品質**。見：
- [[autoreason]]：強模型在 subjective task 上 self-refinement 增益遞減，單一 agent critique 有 authorship bias
- [[evolve-self-refinement]]：comprehensive experiments 顯示 untrained LLM self-refinement 會 degrade
- [[raw/guliani-dejure-iterative-refinement]]：De Jure 論文間接證實需要 multi-criteria 外部 judge 才能 monotonic improve

三篇選了三條完全不同的路線繞過這個障礙。這三條路線構成三種 regime。

### 三種 Regime

**1. Panel Regime**（[[autoreason]] 代表）
- 機制：多個 **fresh isolated agents** 做 blind pairwise comparison + Borda count
- 評分信號：**implicit preference**（不拆維度，judge panel 隱式整合）
- 收斂：A 連贏 k 次
- 適用：主觀創作（沒有 objective metric）
- 可審計性：低（panel decision 黑盒）
- 代價：每次 refinement 要跑 N 個 judge call

**2. Criteria Regime**（De Jure 代表）
- 機制：**multi-dim explicit judge**（例如 19 維 rubric）+ upstream-first repair
- 評分信號：**explicit criteria vector**
- 收斂：regeneration budget 用盡
- 適用：結構化抽取、有 domain rubric 的任務
- 可審計性：高（每個維度分數可見、可調權重）
- 代價：需要 domain expert 設計 criteria

**3. Training Regime**（[[evolve-self-refinement]] 代表）
- 機制：把 refinement 能力訓練進 weight（preference pair + synergistic loop）
- 評分信號：**gradient**
- 收斂：training loss / eval metric
- 適用：通用 capability 提升
- 可審計性：無（內化成 weight）
- 代價：training compute + 有 overfit 風險

### 對比表

| 面向 | Panel | Criteria | Training |
|---|---|---|---|
| 訊號 | implicit preference | explicit criteria vector | gradient |
| 修改在哪 | orchestration | orchestration | weight |
| 收斂 | k consecutive wins | budget | training convergence |
| 審計 | 低 | 高 | 無 |
| Domain 要求 | 低 | 高（需 rubric） | 中 |
| 推論成本 | 高（多 judge call） | 中 | 低（內化後） |

### 三者共同預設

都承認「LLM 不會 self-critique」。差別在於外掛什麼機制補。沒有一條路線說「再 prompt 一次就好」。

## For Agent Memory Research

Memory 系統在做記憶品質判斷（要不要存、要不要更新、哪條優先）時，等同於在做 self-refinement。因此同樣適用這三種 regime：

- **Panel regime → 多 agent 投票決定記憶**：接近 [[collaborative-memory-system]] 的機制
- **Criteria regime → multi-dim memory quality scoring**：[[memory-worth]] 是 outcome-based 後驗信號；De Jure-style 是前驗 criteria-based。兩者可互補
- **Training regime → fine-tune memory policy**：[[memory-r1]]、[[agemem]]、[[d-mem]] 都屬於這類

**反面教訓**：任何 prompt-only 的「你覺得這條重要嗎？」策略不屬於以上任何 regime，應該視為 anti-pattern，跟 EVOLVE 證實會 degrade 的 raw self-refinement 同類。

## Open Questions

- **Regime Selection Criteria**：什麼任務該用哪種 regime？目前無 framework。見 [[open-questions]] Q17（新增）
- **Hybrid regimes**：能不能 criteria judge + training loop 疊用？De Jure 的 criteria 當 reward signal 餵進 EVOLVE 的訓練框架？
- **Memory-specific criteria**：De Jure 的 19 dim 哪幾個通用、哪幾個要 domain-specific 才能搬到 memory quality scoring？

## Key Sources

- **2026-04-12** — autoreason via SHL0MS: [[autoreason]]
- **2025-02** / **v6** — EVOLVE (arxiv 2502.05605): [[evolve-self-refinement]]、[[raw/zeng-evolve-self-refinement]]
- **2026-04-02** — De Jure (arxiv 2604.02276): [[raw/guliani-dejure-iterative-refinement]]

## Related

[[autoreason]] [[evolve-self-refinement]] [[memory-evaluation]] [[memory-worth]] [[open-questions]] [[rl-capability-boundary]] [[collaborative-memory-system]] [[memory-r1]] [[d-mem]]
