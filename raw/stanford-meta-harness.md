---
title: "Meta-Harness: End-to-End Optimization of Model Harnesses"
author: Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, Chelsea Finn
date: 2026-03-28
source: https://github.com/stanford-iris-lab/meta-harness
paper: arxiv 2603.28052
institution: Stanford IRIS Lab + KRAFTON + MIT
topic: harness engineering, automated optimization
---

# Meta-Harness: End-to-End Optimization of Model Harnesses

## 核心概念

Harness = 包裹 LLM 的外部程式，決定 store 什麼、retrieve 什麼、show 什麼。
**同一個模型，不同 harness 可以產生 6x 性能差異。**

Meta-Harness 是一個 **automated search framework**，用 coding agent（Claude Code + Opus 4.6）作為 proposer，自動搜尋最佳 harness 設計。

## 方法論

### Search Loop（核心）

1. **初始化**：提供一組 initial harnesses + 空 filesystem D
2. **評估**：跑每個 harness，存 code + scores + execution traces 到 D
3. **迭代**（20 iterations, ~60 harness evaluations）：
   - Proposer（Claude Code）用 grep/cat 檢查 filesystem D 中所有歷史 candidates
   - 基於 failure 分析，提出 k 個新 harness candidates
   - 驗證 + 評估 → 結果存回 D
4. **輸出**：D 中的 Pareto frontier

### 關鍵設計

- **Filesystem-based full history access**：每個 candidate 的完整 source code + evaluation scores + execution traces（prompt、tool calls、model outputs、state updates）。單次 evaluation 可產生 10M tokens 診斷資料
- **Agentic proposer**：不是固定 heuristic，是 autonomous coding agent 自己決定檢查什麼、修改什麼
- **Code-space search**：直接在 code space 優化，不是 prompt tuning

## 實驗結果

### Online Text Classification（GPT-OSS-120B）
- Meta-Harness 48.6% accuracy vs hand-designed ACE 40.9%（+7.7）
- **4x fewer context tokens**（11.4K vs 50.8K）
- 10x fewer evaluations than OpenEvolve/TTT-Discover 達到同等水準
- OOD generalization: 73.1% avg on 9 unseen datasets（vs ACE 70.2%）

### Retrieval-Augmented Math Reasoning（IMO-level）
- +4.7 points avg across 5 held-out models
- 發現的 harness 是 compact four-route BM25 program + dedup + difficulty reranking

### Agentic Coding on TerminalBench-2
- Opus 4.6: 76.4% pass rate（#2 on leaderboard，超過 hand-engineered Terminus-KIRA 74.7%）
- Haiku 4.5: 37.6%（#1 among all Haiku agents）

## Ablation: Full Traces 的重要性

| Feedback Level | Median Accuracy | Best Accuracy |
|---|---|---|
| Scores only | 34.6% | 41.3% |
| Scores + summary | 34.9% | 38.7% |
| **Full Meta-Harness** | **50.0%** | **56.7%** |

Raw traces 比 summary 好 15+ 點。Lossy feedback 不夠做 causal reasoning。

## 與其他概念的關係

- **Harness engineering 自動化**：之前是人工迭代（inspect failures → adjust heuristics → repeat），Meta-Harness 讓 coding agent 做這件事
- **Scaffolding lifecycle**：Meta-Harness 的 proposer 會自動 add/remove scaffolding — 在 TerminalBench-2 實驗中觀察到 proposer 從 aggressive rewrites 轉向 safe, additive modifications
- **Context rot 的解法**：如果 resolver/harness 會 rot，Meta-Harness 可以自動重新優化
- **Memory system search**：text classification 實驗中，Meta-Harness 發現的 harnesses 包含 memory-based context construction strategies（Draft Verification、Label-Primed Query）
- **Omar Khattab**：DSPy 作者，也是 Meta-Harness 共同作者 — 從 prompt optimization 到 harness optimization 的自然延伸

## 關鍵引言

> "The harness can lead to substantial performance variations. A single model's output can vary by a factor of six depending on its harness."

> "Rich, uncompressed access to full historical diagnostic information is crucial. Lossy summaries and scalar rewards are insufficient for causal reasoning."

## 開源

- Framework code: github.com/stanford-iris-lab/meta-harness
- TerminalBench-2 artifact: stanford-iris-lab/meta-harness-tbench2-artifact
- Proposer: Claude Code + Opus 4.6
