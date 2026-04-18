---
aliases: [EVOLVE, evolve-self-refinement, trained self-refinement]
first_seen: 2026-04-19
last_updated: 2026-04-19
tags: [training, reasoning, system]
---

# EVOLVE — Trained Self-Refinement

Zeng et al. (arxiv 2502.05605, latest v6) 提出的 framework：用 synergistic training-inference optimization 把 self-refinement 能力訓練進 LLM 權重。

## Current Understanding

### 起因（empirical claim）
- Comprehensive experiments 顯示 **LLM 原生沒有有效的 self-refinement 能力**
- 更關鍵：self-refinement 不只是「沒提升」，而是經常 **degrade** 品質
- 這跟 [[autoreason]] 的 inference-time 觀察互補：autoreason 發現強模型做 self-refinement 收益遞減；EVOLVE 發現所有未訓練模型做 self-refinement 甚至會退化

### 機制

兩階段 synergistic loop：

**Training 階段**
- 把「原版回應 → refined 回應」當成 preference pair
- 用這些 pair 訓練 refinement policy
- 模型學到的不是「生出更好答案」而是「判斷哪裡該改 + 如何改」

**Inference 階段**
- 用當前模型生成初版 + refined 版
- Refined 版變成下一輪 training 的正例
- 生成策略（例如 best-of-N sampling）強化這個 refinement signal

**Loop**：Training ↔ Inference 互相供給資料。每次迭代，refinement 能力加深一點。

### 結果
- Llama-3.1-8B base 經過 EVOLVE：
  - AlpacaEval 2: **62.3% LC / 63.3% raw win** vs GPT-4o
  - Arena-Hard: **50.3%**
- **OOD generalization**：GSM8K、MATH 等 reasoning 任務也改善
- 小模型贏大模型 — refinement 能力可部分彌補參數量差距

## For Agent Memory Research

- **Self-critique is not free**：如果 LLM 原生不會 refine，那「讓 agent 判斷這條記憶該不該存 / 該不該更新」這種 prompt-only 記憶管理可能是 anti-pattern。prompt 問 "Should we remember this?" 得到的答案可能系統性 degrade
- **Training-inference loop = consolidation analog**：EVOLVE 的 refine→retrain→refine 跟 memory consolidation 的結構類似：新資訊先以 working form 存在（inference），被驗證後經訓練 pressure consolidate 進 weight
- **Weight vs context trade-off**：EVOLVE 選擇把能力壓進 weight；[[autoreason]] / [[refinement-regime]] 的 Panel/Criteria 路線選擇留在 orchestration。memory 系統面對同一選擇：[[memory-r1]]、[[agemem]] 走 weight；[[mem0]]、[[d-mem]] 走 orchestration
- **跟 [[rl-capability-boundary]] 的關係**：EVOLVE 在 OOD 數學任務上的提升，看起來是 capability expansion 不是 reliability improvement，但原論文沒做 PASS@(k,T) 分析，不能確定

## Regime

屬於 **Training Regime**（見 [[refinement-regime]]）：把 refinement 從 orchestration 壓進 weight。可審計性最低，但一旦訓好不需要 inference overhead。

## Key Sources

- **2025-02-08** (v1) / **v6 latest** — arxiv 2502.05605, Zeng et al. Source: [[raw/zeng-evolve-self-refinement]]

## Related

[[autoreason]] [[refinement-regime]] [[memory-r1]] [[agemem]] [[rl-capability-boundary]] [[compounding-memory]] [[memory-staleness]] [[memory-evaluation]]
