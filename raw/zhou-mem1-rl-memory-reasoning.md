---
source_type: paper
url: https://arxiv.org/abs/2506.15841
title: "MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents"
authors: [Zijian Zhou, Ao Qu, Zhaoxuan Wu, Sunghwan Kim, Alok Prakash, Daniela Rus, Jinhua Zhao, Bryan Kian Hsiang Low, Paul Pu Liang]
affiliations: [MIT, SMART Centre, NUS, Yonsei University]
date: 2025-06-20
discovered_via: "X/Twitter — Paul Liang (@pliang279)"
ingested: 2026-04-17
tags: [rl, memory, reasoning, long-horizon, agent]
---

# MEM1: Learning to Synergize Memory and Reasoning for Efficient Long-Horizon Agents

## 核心問題

LLM agent 在 multi-turn interaction 中 context 無限膨脹：computational cost O(N²)、memory usage 線性增長、超出 training horizon 性能衰退。現有解法把 memory management 當獨立模組（RAG、summarizer），跟 reasoning policy 分開優化。

## 方法

### Internal State（<IS> tag）

- Agent 在每個 turn 生成一個 `<IS_t>` tag，是一個 learned summary，融合 prior state + new observation + reasoning
- 生成 `<IS_t>` 後，上一個 turn 的所有 context 被 prune
- 任何時刻 context 最多保留 2 個 IS + 2 個 query + 1 個 info
- **Memory 和 reasoning 在同一個 representational space 裡統一**，不需要外部模組

### RL 訓練

- 用 PPO 端到端訓練（從 Qwen2.5-7B Base，不是 instruction-tuned）
- **Memory efficiency 不需要額外 reward** — context pruning 機制天然迫使 agent 學會 consolidation
- 只用 task success reward（答對了就有獎勵）
- Agent 必須把重要資訊 consolidate 進 IS，否則丟了就沒了

### Masked Trajectory

- Context pruning 導致標準 PPO 的 trajectory 不連續
- 解法：用 2D attention mask 確保每個 token 只 attend 到它生成時看得到的 token
- 1D mask 防止 agent 學會從 retrieval result 直接 copy

### Multi-Objective Task Augmentation

- 把多個 single-objective QA 拼成 multi-objective task（"Answer Q1, Q2, Q3"）
- 強迫 agent 在一次 session 中做多次 search + reasoning

## 結果

### Multi-Objective Multi-Hop QA（核心實驗）

| Method | 2-obj EM | 16-obj EM | Peak Token（16-obj） |
|---|---|---|---|
| Qwen2.5-14B-Instruct | 2.85 | 0.567 | ~100% |
| MEM1-7B | 2.55 | **1.97** | **27.1%** |

- 2-obj 時 MEM1 略輸 14B model，但 16-obj 時 MEM1 反超 3.5x
- Peak token 幾乎不隨 objective 數量增長（constant memory）

### WebShop

| Method | Avg Reward | Peak Token |
|---|---|---|
| AgentLM-13B | 70.80 | 100% |
| **MEM1-7B** | **70.87** | **35.7%** |

### 與其他方法的對比

- RL 訓練 >> SFT 訓練：SFT model 在 >6 objectives 時 collapse
- Format reward 加速收斂但降低最終性能（限制探索）
- A-MEM（外部 memory module）在 long horizon 表現不如 MEM1

### Emergent Behaviors

- Multi-question management：同時追蹤多個問題
- Focus shifting：某個問題卡住時切換到其他問題
- Self-verification：主動重新查詢確認
- Query decomposition：複雜查詢分解成子目標

## 核心洞察

1. **Memory consolidation 可以被 RL 隱式學會**：不需要 memory-specific reward，context pruning + task reward 就夠了
2. **Memory 和 reasoning 不應該分開**：統一在同一個 representational space 裡效果更好
3. **Constant memory 是可能的**：agent 可以學會 O(1) memory 操作，不需要 O(N) context
4. **Base model > instruction-tuned model**：RL from base model 的 generalization 更好

## 與 DeltaMem / EMPO² 的定位

| 維度 | DeltaMem | EMPO² | MEM1 |
|---|---|---|---|
| Memory 角色 | 外部知識庫（CRUD） | 探索引導工具（tips） | 內部狀態（IS tag） |
| RL 訓練什麼 | Memory CRUD 操作 | 內化 memory-guided 行為 | Memory consolidation + reasoning |
| Test time | 需要 external memory | 不需要 memory | 需要 IS（但是 constant size） |
| Memory 位置 | External store | External buffer（train only） | Inside context window |
| 核心創新 | Single-agent simplification | Off-policy distillation | Memory-reasoning unification |
| Benchmark | PersonaMem | ScienceWorld | Multi-hop QA, WebShop |

三者代表 RL+memory 的三條路：
- DeltaMem：RL 教 agent 管理 external memory
- EMPO²：RL 教 agent 從 external memory 畢業（蒸餾進 weights）
- MEM1：RL 教 agent 用 constant-size internal state 取代 full context
