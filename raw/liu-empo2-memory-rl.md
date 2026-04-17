---
source_type: paper
url: https://arxiv.org/abs/2602.23008
title: "Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization"
authors: [Zeyuan Liu, Jeonghye Kim, Xufang Luo, Dongsheng Li, Yuqing Yang]
affiliations: [Microsoft Research, KAIST]
date: 2026-02-01
venue: ICLR 2026
discovered_via: "X/Twitter — Ihtesham Ali (@Ihtesham_Ali97)"
ingested: 2026-04-17
tags: [rl, memory, exploration, agent]
---

# EMPO²: Exploratory Memory-Augmented On- and Off-Policy Optimization

## 核心問題

LLM agent 用 RL 訓練時有 exploration bottleneck：agent 傾向 exploit 既有 prior knowledge，不願 explore 新狀態。現有 memory-augmented 方法（如 Reflexion）的 experience 是用 static parameters 收集的，diversity 不夠，performance 會 saturate。

## 方法

### Self-Generated Memory

- Policy π_θ 自己 review 過去 rollouts，生成 natural-language "self-guidance tips"
- Tips 存在 memory buffer M = {tip_1, tip_2, ...}
- 設計目標不只是 iterative verbal guidance（像 Reflexion），而是最終要透過 parametric updates 內化

### Hybrid Rollout（兩種模式隨機切換）

1. **Without Memory（機率 p）**：policy 只看 state + task
2. **Memory-Augmented（機率 1-p）**：retrieval operator 從 M 找最相關的 tips（最多 10 條），policy 同時看 state + task + tips

### Hybrid Update（三種 learning mode）

1. **On-policy without memory**：標準 GRPO update
2. **On-policy with memory（機率 1-q）**：用 memory-augmented rollout 的 trajectory，importance ratio 也 condition on tips
3. **Off-policy（機率 q）**：關鍵創新 — rollout 時用了 tips，但 update 時把 log-prob 換成 *不帶 tips* 的版本。效果是 reward-guided knowledge distillation：高 advantage 的 memory-guided actions 被強化進 base policy，低 advantage 的被抑制

### Stabilization

- Masking mechanism：token probability 低於閾值 δ 時 suppress advantage term，防止 off-policy 的 likelihood ratio 爆掉
- Intrinsic reward：r_intrinsic = 1/n（n = 與當前 novel state 相似的過去 state 數量），鼓勵探索新狀態

## 結果

### ScienceWorld（text-based science experiments）

| Method | Avg Return |
|---|---|
| Naive prompting | ~10 |
| Reflexion（non-parametric RL） | ~25 |
| Retrospex（offline RL） | ~30 |
| GRPO（online RL） | 33.2 |
| **EMPO²** | **75.9**（+128.6% vs GRPO） |

- 7 個原本 negative reward 的 task 達到滿分 100
- GRPO 常 premature convergence，EMPO² 持續改善

### WebShop（HTML-based online shopping）

| Method | Avg Score | Success Rate |
|---|---|---|
| GiGPO | 86.2 | 75.2% |
| **EMPO²** | **88.3** | **76.9%** |

### OOD Adaptation（zero-shot transfer to new tasks）

- EMPO²（帶 memory）在 unseen tasks 上 10 steps 內平均 +136%
- GRPO 高 variability，有些 case 反而比 base model 差

### Ablation

- 拿掉 off-policy update → 性能下降（無法內化 memory-guided reasoning）
- 拿掉 on-policy with memory → 性能下降（缺少 memory-guided exploration）
- 完全拿掉 intrinsic reward → 學習 plateau，探索不足
- Memory overhead：每個 training iteration 約 +19%（50.4 秒），但 time-performance 效率遠高於 GRPO

## 核心洞察

1. **Memory 是 exploration 工具**：不是用來讓 agent 記事情（像 DeltaMem），而是用來引導 agent 探索新狀態
2. **Off-policy distillation**：memory-guided 的好行為可以蒸餾回 base policy，test time 不需要 memory
3. **Parametric + non-parametric 互補**：on-policy 提供穩定學習，off-policy 提供 memory knowledge 內化，兩者缺一不可
4. **Intrinsic reward 防 collapse**：沒有 exploration bonus，policy 會 premature convergence

## 與 DeltaMem 的對比

| 維度 | DeltaMem | EMPO² |
|---|---|---|
| Memory 角色 | Agent 管理的知識庫（CRUD） | Agent 探索的引導工具（tips） |
| RL 訓練什麼 | 訓練 agent 做出正確的 memory 操作 | 訓練 agent 內化 memory-guided 行為 |
| Test time | 需要 memory | 不需要 memory |
| Reward | Memory-based Levenshtein Distance | Task reward + intrinsic exploration bonus |
| 規模 | 7B model，PersonaMem benchmark | 7B model，ScienceWorld + WebShop |
| 核心創新 | Single-agent 取代 multi-agent pipeline | Hybrid on/off-policy 內化 memory |
