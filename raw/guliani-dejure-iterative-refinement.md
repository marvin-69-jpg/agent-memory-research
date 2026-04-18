---
source: arxiv 2604.02276v1
date: 2026-04-02
authors: Guliani, Gill, Landsman +3
title: "De Jure: Iterative LLM Self-Refinement for Structured Extraction of Regulatory Rules"
fetched: 2026-04-19
---

# De Jure — Multi-criteria Judge + Bounded Repair

## 核心 claim

用 LLM 從 regulatory 文件抽出 structured rules，無需人工標註、無需 domain prompt。核心是 **multi-criteria LLM-as-a-judge** 搭配 **bounded iterative repair**。

## Pipeline（四階段 sequential）

1. **Normalization** — source document → structured Markdown
2. **Semantic Decomposition** — LLM 拆成 structured rule units
3. **Multi-criteria Judge** — 用 19 個維度（metadata、definitions、rule semantics）評分
4. **Iterative Repair** — 低分的 extraction 在 bounded budget 內重生，**上游 component 先修再動下游 rule units**

## 關鍵設計

- **19-dim judge** vs Autoreason 的 Borda count
  - De Jure：每個維度獨立打分，accumulated criteria-vector 導引修改方向
  - Autoreason：整體 pairwise preference，讓 judge 隱式整合所有維度
  - trade-off：explicit criteria 可審計但需要 domain design；implicit preference 通用但黑盒
- **Bounded regeneration budget** — 3 次 judge-guided iteration 就收斂到 peak performance。類似 Autoreason 的 "k consecutive wins" stopping criterion，但用 budget 而不是 consensus
- **Upstream-first repair** — 先修 normalization / decomposition，再修 rule units。如果上游錯了，下游再 refine 也沒用

## 實驗結果

- Finance domain：3 iterations 內 monotonic improvement 到 peak
- Healthcare / AI governance：跨 domain 穩定
- Open + closed source 模型都有效
- Downstream RAG：基於 De Jure extraction 的回答在 73.8% 情況被偏好；更深 retrieval 時升到 84.0%

## 與 Autoreason / EVOLVE 的對照

| 面向 | De Jure | Autoreason | EVOLVE |
|---|---|---|---|
| 訊號來源 | 19-dim judge (explicit) | Borda panel (implicit) | trained reward |
| 收斂條件 | budget exhaustion | k consecutive A wins | training convergence |
| 修改方向 | criteria vector 指示 | critique text | gradient |
| 適用場景 | 結構化抽取 | 主觀創作 | 通用 capability 提升 |
| Weight 更動 | 否 | 否 | 是 |

三者都承認：**LLM 原生不會有效 refine。必須外掛「評分 + 導引」機制。**

## 對 agent memory 的意義

- **Structured memory extraction 可能該用 De Jure 模式**：從 conversation 抽 user preference 或事件，不是單次 LLM call + summarize，而是 decompose → judge(多維) → bounded repair
- **上游先修** 這個設計對 hierarchical memory 重要：如果 episode 的 normalization 有誤，後續 semantic abstraction 都是錯的。memory pipeline 的 refinement 應該從 raw 端先驗證
- **19-dim judge 是否適合 memory quality？** — 可審計、可調整每個維度的權重，跟 [[memory-worth]] 的 outcome-based 信號可互補：MW 是後驗的（有沒有被用），De Jure 是前驗的（符不符合 criteria）
