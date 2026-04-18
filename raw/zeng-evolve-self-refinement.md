---
source: arxiv 2502.05605v6
date: 2025-02-08 (v1) / v6 latest
authors: Zeng, Cui, Jin, Mi, Liu, Sun, Yang, Li, Ma + 11
title: "Evolving LLMs' Self-Refinement Capability via Synergistic Training-Inference Optimization"
fetched: 2026-04-19
---

# EVOLVE — Evolving LLMs' Self-Refinement Capability

## 核心 claim

**LLM 原生不會 self-refinement，甚至會 degrade 回應品質。** 這是 comprehensive experiments 的結論，不是 anecdote。

EVOLVE 提出一個 framework：在 training 階段啟動 refinement capability，在 inference 階段用 generation strategy 強化它，兩階段 synergistic optimization 反覆迭代。

## 機制

### Training 階段
- 探索 optimization methods 來激活 refinement capability
- 把 refinement 視為「從初版回應 → 改進版」的 preference pair
- 疊代訓練讓模型學會「判斷哪裡要改 + 執行改的動作」

### Inference 階段
- 用 refined outputs 重建 dataset，餵回 training loop
- 「改寫資料集」變成下一輪 training signal

### Synergistic Loop
Training ↔ Inference 兩階段互相供給資料，形成 continuous evolution。refinement 不是 one-shot 能力，而是 trained-in 能力。

## 實驗結果

- Llama-3.1-8B base 經過 EVOLVE 後：
  - AlpacaEval 2: 62.3% length-controlled / 63.3% raw win rate vs GPT-4o
  - Arena-Hard: 50.3%
- OOD generalization: GSM8K、MATH 推理任務也提升
- **Llama-3.1-8B 贏 GPT-4o** — 意味著 refinement 能力可以彌補參數量差距

## 與 Autoreason 的張力

- Autoreason：強模型 self-refinement 收益遞減（Haiku 4.5 在 60% accuracy 時增益消失）
- EVOLVE：弱模型如果 training 得當，可以把 refinement 能力訓練進去
- **兩者不矛盾**：Autoreason 觀察的是 inference-time 行為（用現成模型 + 外部 judge），EVOLVE 改的是 model weight 本身
- Autoreason 的 "fresh isolated agents" 是為了避開 authorship bias；EVOLVE 則是把 refinement 內化成 policy 的一部分（承擔 bias 風險）

## 對 agent memory 的意義

- **Self-critique is not free** — 如果 LLM 原生不會 refine，那「讓 agent 判斷這條記憶該不該存/該不該更新」這件事，需要被明確訓練或用外部 judge 處理。不能假設 prompt-only 的「你覺得這條重要嗎？」會給出有用答案
- **Training-inference loop = memory consolidation analog** — EVOLVE 的 refine→retrain→refine 很像 memory 的 consolidation 循環：新記憶先以 working form 存在（inference），被驗證後 consolidate（training pressure）
- **Weight vs context trade-off** — EVOLVE 選擇把能力壓進 weights；Autoreason/De Jure 選擇把能力留在 orchestration 層。memory 系統也面對同一選擇：要把「記得」變成 fine-tune，還是 retrieval？
