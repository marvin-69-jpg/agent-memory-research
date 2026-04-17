---
url: https://arxiv.org/abs/2604.14877
arxiv_id: 2604.14877
title: "Does RL Expand the Capability Boundary of LLM Agents? A PASS@(k,T) Analysis"
authors: Zhiyuan Zhai, Wenjing Yan, Xiaodan Shao, Xin Wang
date: 2026-04-16
fetched: 2026-04-18
---

# Does RL Expand the Capability Boundary of LLM Agents?

## 核心問題

RL 對 LLM agent 到底是：
- (A) 真的擴展 capability boundary（能做新的事）
- (B) 只是提升 reliability（讓現有能力更穩定）

Static reasoning 的既有結論：**(B)**。Base 跟 RL 的 pass@k curve 在大 k 下會收斂。

本文問：tool use（multi-turn interactive agent）是否也如此？

## PASS@(k,T) 指標

2D metric，同時變動：
- **k**：sampling budget（每個 task 採樣幾次）
- **T**：interaction depth（每次最多幾輪 tool call）

這個 metric 可以把「capability expansion」（k 增大仍維持 gap）跟「efficiency improvement」（k 增大 gap 收斂）分開。

## 主要發現

**與 static reasoning 結論相反**，**tool-use RL 真的擴大 capability boundary**：

1. RL agent 的 pass-curve **拉到 base model 之上**
2. Gap 在大 k 仍然 **widening**（不是收斂）
3. Expansion 特別發生在 **compositional, sequential information gathering** 的 task
4. 簡單 task 上，RL 仍然只是 efficiency 提升（照既有預測走）

## 機制分析

- RL **重加權 base strategy distribution**，偏向下游 reasoning 更常得正確答案的 subset
- 改進集中在「**agent 如何 integrate retrieved information**」
- 這是 base model 的潛能被 RL 顯現、不是 RL 注入新能力

## 關鍵對照：SFT vs RL

在**相同 training data** 下：
- **SFT regresses** 同樣的 compositional task
- **只有 self-directed exploration（= RL）** 才能擴展 boundary
- 這 isolate 了 **self-directed exploration 是 causal factor**

## 意義

本文把過去兩派說法 reconcile：
- 樂觀派（RL 擴展能力）：在 compositional tool-use task 是對的
- 悲觀派（RL 只提升 reliability）：在 static reasoning 是對的
- 兩者都對，只是 task type 不同

## 跟 skill-based self-improvement 的張力（我的觀察）

跟 ASG-SI、SkillX 這類 skill-based 路徑對照：

- ASG-SI/SkillX 把 RL fine-tuning 視為 opaque 的 alternative，提議改用 skill graph/library
- 但本文指出 tool-use 的 capability expansion **來自 self-directed exploration**（RL 的本質）、SFT/distillation 會 regress
- SkillX 的「強模型蒸餾給弱模型 → Pass@4 提升」看起來是 capability expansion，但 SkillX 沒做 PASS@(k,T) 分析；可能是 efficiency improvement 在 Pass@4 上偽裝成 capability expansion
- **核心開放問題**：skill-based self-improvement 提供的是 efficiency 還是真正的 capability expansion？用 PASS@(k,T) 才能分辨
