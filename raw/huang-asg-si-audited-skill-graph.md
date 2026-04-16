---
title: "Audited Skill-Graph Self-Improvement for Agentic LLMs via Verifiable Rewards, Experience Synthesis, and Continual Memory"
author: Ken Huang, Jerry Huang
date: 2025-12-28
source: https://arxiv.org/abs/2512.23760
paper: arxiv 2512.23760
topic: self-improving agent, skill graph, verifiable rewards, governance
---

# ASG-SI: Audited Skill-Graph Self-Improvement

## 核心問題

Deployed self-improving agents 有三個未解的 governance 問題：

1. **Reward hacking** — 優化壓力會讓 agent 學會鑽 reward 漏洞
2. **Behavioral drift** — 行為改變難以 audit 或 reproduce
3. **Opaque parameter updates** — 改進綁在不透明的權重裡，不是可重用、可驗證的 artifacts

## 核心提案

把 self-improvement 重新框定為「把 agent 編譯進一個成長中、可審計的 skill graph」的迭代過程。

### Pipeline

```
Successful trajectory
       ↓
Extract candidate skill (with explicit interface)
       ↓
Verifier-backed replay + contract check
       ↓
Pass? → Promote to skill graph
Fail? → Reject (audit log 留痕)
```

### 三個關鍵設計

1. **Skill normalization with explicit interface**：每個 skill 是一個有明確輸入/輸出/前後條件的可重用單位，不是 fine-tune 後的權重 delta
2. **Verifier-backed replay**：promotion 之前必須能在 verifier 上 replay，否則拒絕
3. **Reward decomposition into reconstructible components**：reward 拆解成可從 replayable evidence 重建的組件，讓 promotion 決定可被獨立 audit

## 額外組件

- **Experience synthesis**：合成 stress test scenarios 來考驗候選 skill 的 robustness
- **Continual memory control**：在 bounded context 下維持 long-horizon performance

## 哲學立場

> "ASG-SI reframes agentic self-improvement as **accumulation of verifiable, reusable capabilities**, offering a practical path toward reproducible evaluation and operational governance of self-improving AI agents."

對比傳統 RL fine-tuning：
| | RL fine-tuning | ASG-SI |
|---|---|---|
| 學到的東西在哪 | weights（不透明） | skill graph（可讀、可審計） |
| 改進是否可重用 | 綁在這個 model | 可移植到其他 agent |
| 是否可 audit | 難（黑盒） | 是（有 contract、有 replay log） |
| Reward hacking 防護 | 弱 | 強（verifier + contract） |

## 與其他工作的關係

- 跟 Voyager (Wang et al 2023) 的 skill library 類似，但 Voyager 沒有 audit/governance
- 跟 Anthropic Claude Skills 的 reusable skill 概念類似，但 Anthropic 是 hand-crafted
- 跟 Meta-Harness 的 filesystem-based history 類似，都是把 agent 學到的東西外化成可檢視的 artifact
- 與 weight-based continual learning 對立

## 潛在影響

如果 self-improving agents 要 deploy 到真實場景，governance 是必經之路。ASG-SI 提供一條技術路徑：把改進變成 verifiable artifacts，這樣 audit、rollback、reproducibility 都變可能。
