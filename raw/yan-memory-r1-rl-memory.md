---
source_type: paper
url: https://arxiv.org/abs/2508.19828
title: "Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning"
authors: [Sikuan Yan, Xiufeng Yang, et al.]
affiliations: [LMU Munich, MCML, TU Munich, Cambridge, HKU, TU Darmstadt, Edinburgh]
date: 2025-08-28
discovered_via: "X/Twitter — Marktechpost (@Marktechpost)"
ingested: 2026-04-17
tags: [rl, memory, agent, benchmark]
---

# Memory-R1: RL for Memory Management and Utilization

## 核心問題

LLM 本質上是 stateless，外部 memory 系統多半用 static heuristics 決定 CRUD 操作。Vanilla LLM 靠 in-context instructions 常失敗（例如把 update 跟 contradiction 搞混）。RAG retrieval 回來一堆記憶但 agent 不知道怎麼 filter noise。

## 方法

### Two-Agent Architecture

1. **Memory Manager**：處理每個新 dialogue turn，決定 ADD / UPDATE / DELETE / NOOP 操作
2. **Answer Agent**：拿 memory bank 回答問題，先做 Memory Distillation（從 60 條 retrieved memories 中過濾出最相關的）

兩個 agent 分開訓練（為了 sparse reward 下的穩定性），但 Memory Manager 的 reward 來自 Answer Agent 的表現。

### RL Training

- 用 PPO 或 GRPO
- **Outcome-driven reward**：Memory Manager 做完操作後，把更新過的 memory bank 交給 frozen Answer Agent 回答問題，用 Exact Match 當 reward
- Answer Agent 直接用 EM 對 gold answer 當 reward
- **只用 152 個 QA pairs 訓練** — 極高 data efficiency

### Memory Distillation

- Answer Agent 從 memory bank RAG 回 60 條候選記憶
- 先做 distillation（filter noise）再 reasoning
- 解決 "lost in the middle" 問題

## 結果

### LoCoMo（primary benchmark）

| Method | F1 | BLEU-1 | Judge |
|---|---|---|---|
| MemoryOS (prev SOTA) | baseline | baseline | baseline |
| Memory-R1-GRPO (LLaMA-3.1-8B) | +28.5% | +34.0% | +30.2% |
| Memory-R1-GRPO (Qwen-2.5-7B) | +24.5% | +24.1% | +20.0% |

- Memory-R1 > Memory-SFT（用 GPT-5 trajectory 做 SFT）→ RL > imitation learning
- 152 QA pairs 就夠 → 極高 data efficiency

### 跨 benchmark 泛化（zero-shot）

- MSC：consistent improvement
- LongMemEval：consistent improvement
- 只在 LoCoMo 上訓練，zero-shot transfer 到其他 benchmark

### 模型規模

- Qwen-2.5 3B / 7B / 14B 都有效
- 效果隨 model size 增長

### Ablation

- 拿掉 RL Memory Manager → 性能下降（static control 不如 learned）
- 拿掉 Memory Distillation → noise 增加，reasoning 性能下降
- Memory Manager 越強（GPT-4o-mini），Answer Agent 表現越好 → compounding effect
- GRPO 初始收斂快，PPO 和 GRPO 最終表現相當
- Accuracy-latency trade-off：Memory-R1 比 reranker pipeline 更準且更快

## 核心洞察

1. **RL 是 memory management 的 missing ingredient**：heuristic 和 SFT 都不如 outcome-driven RL
2. **Two-agent 有其道理**：Manager 和 Answer Agent 分工讓 reward signal 更清晰，Manager 學「記什麼」，Answer Agent 學「怎麼用」
3. **152 examples 就夠**：outcome-driven RL 的 data efficiency 遠高於 SFT
4. **Memory Distillation 是關鍵**：不只是 retrieve，更要 filter
5. **Compounding effect**：better memory → better answers → better reward → better memory

## 與 DeltaMem / MEM1 的對比

| 維度 | DeltaMem | Memory-R1 | MEM1 |
|---|---|---|---|
| Architecture | Single-agent | Two-agent（Manager + Answer） | Single-agent |
| RL 方法 | GRPO | PPO / GRPO | PPO |
| Training data | Large-scale | 152 QA pairs | Multi-objective tasks |
| Reward | Levenshtein Distance | Exact Match（downstream QA） | Task success |
| Memory 位置 | External store | External store + RAG | Internal state（IS） |
| 核心 benchmark | PersonaMem | LoCoMo | Multi-hop QA |
| 核心創新 | Single-agent simplification | Memory Distillation + outcome reward | Memory-reasoning unification |

DeltaMem 說 single-agent 比 multi-agent 好（在 PersonaMem 上），Memory-R1 的 two-agent 在 LoCoMo 上拿到 SOTA。可能不是 architecture 本身的差異，而是 benchmark 和 reward design 的差異。
