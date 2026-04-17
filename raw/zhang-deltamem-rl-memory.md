---
source: arxiv
author: Qi Zhang, Shen Huang, Chu Liu +4
paper_id: "2604.01560"
url: https://arxiv.org/abs/2604.01560
date: 2026-04-02
fetched: 2026-04-17
tags: [agent-memory, reinforcement-learning, memory-management, persona]
---

# DeltaMem: Towards Agentic Memory Management via Reinforcement Learning

Zhang et al., arxiv 2604.01560v1, ICML submission, Apr 2 2026.

## Core Proposition

Multi-agent memory management systems（多個 agent 各負責一部分記憶操作）fragile、information loss。
DeltaMem 用 **single agent** 做 end-to-end memory management + **RL** 強化。

## Architecture

### Memory State Formulation

記憶狀態 S_t 是 ID → (content, timestamp) 的映射。
Memory management = `S_{t+1} = f(S_t, d_{t+1})`：吃進當前記憶 + 新對話，產出更新後的記憶。

建在 Mem0 的 backend 之上。每條記憶 = factual, atomic sentence + timestamp + unique ID。

### Memory Operations

Agent 可以執行的操作：
- ADD：新增一條記憶
- UPDATE(id)：修改某條記憶
- DELETE(id)：刪除某條記憶
- NOOP：不做任何事

### Memory-based Levenshtein Distance (Reward)

RL 的 reward signal 不用 vector similarity，而是用 **keyword coverage**：
- 每條 target memory 有一組 factual keywords
- Score = 預測記憶覆蓋了多少 target keywords
- 正距離 = false positives（多存的）
- 負距離 = true negatives（漏存的）

**關鍵設計**：reward 基於事實正確性，不基於向量距離。

### RL Training (GRPO)

用 GRPO（Group Relative Policy Optimization）訓練 agent 做更好的記憶管理決策。
Data synthesis：用 memory evolution 過程合成訓練資料。

## Results

### LoCoMo
DeltaMem-8B-RL outperforms all product-level baselines。

### PersonaMem
| System | Overall |
|---|---|
| **DeltaMem-8B-RL** | **63.61** |
| Memobase | — |
| Zep | — |
| Mem0 | — |

- New-Ideas metric：24.73 → **40.14** with RL (+62%)
- Recall-Facts：**76.47** — 不會遺忘核心事實

### Memory Extraction
Training-free: 68.02 → RL: **80.65**

## Key Insights

1. **Single agent > multi-agent for memory management**：複雜的多 agent pipeline 反而脆弱，single agent end-to-end 更穩定
2. **RL reward 基於 factual keywords, not vector similarity**：跟 Memory Worth 的 outcome-based evaluation 有類似直覺 — 不要用 proxy metric
3. **Memory updating 是最難的操作**：LightMem 等系統 extraction 好但 updating 差，DeltaMem 用 RL 平衡兩者
4. **Persona memory evolution**：使用者的偏好會變，記憶系統要能 evolve without losing core facts
