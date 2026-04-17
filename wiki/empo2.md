---
aliases: [EMPO², EMPO2, exploratory memory-augmented agent]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [system, rl, memory, exploration]
---

# EMPO²

Microsoft Research + KAIST，ICLR 2026。Hybrid on- and off-policy RL 框架，用 memory 引導 agent exploration，再透過 off-policy distillation 把 memory-guided 行為內化進 model parameters。

## Current Understanding

- **核心問題**：LLM agent 用 RL 訓練時有 exploration bottleneck — 傾向 exploit prior knowledge，不願探索新狀態。現有 memory 方法（Reflexion 等）用 static parameters 收集 experience，diversity 不夠，performance saturate
- **Memory 的角色不是記憶，是探索**：agent 自己 review 過去 rollouts 生成 natural-language "self-guidance tips"，存進 memory buffer。Tips 引導 agent 嘗試新策略、探索新狀態
- **Hybrid rollout**：每步隨機選擇帶 memory（retrieval 最相關的 tips）或不帶 memory 兩種模式
- **三種 learning mode**：
  1. On-policy without memory：標準 GRPO
  2. On-policy with memory：memory-augmented trajectory 的標準 update
  3. **Off-policy（核心創新）**：rollout 時帶 tips，update 時把 log-prob 換成不帶 tips 的版本 → reward-guided knowledge distillation，高 advantage 的 memory-guided actions 強化進 base policy
- **Test time 不需要 memory**：memory 只在訓練時用來引導探索，學到的行為已內化進 weights
- **Intrinsic reward**：r = 1/n（n = 相似過去 state 數），鼓勵探索 novel states，防 premature convergence

### 結果

| Benchmark | EMPO² | Best baseline | 改善 |
|---|---|---|---|
| ScienceWorld | 75.9 | GRPO 33.2 | +128.6% |
| WebShop | 88.3 / 76.9% | GiGPO 86.2 / 75.2% | +2.4% |
| OOD Adaptation | +136%（10 steps） | GRPO variable | — |

- 7 個原本 negative reward 的 ScienceWorld task 達到滿分 100
- Memory overhead 約 +19% per training iteration，但 time-performance 效率遠高於 GRPO

### 與 DeltaMem 的對比：RL 用在 memory 的兩條路

| 維度 | [[deltamem]] | EMPO² |
|---|---|---|
| Memory 角色 | Agent 管理的知識庫（CRUD） | Agent 探索的引導工具（tips） |
| RL 訓練什麼 | 做出正確的 memory 操作 | 內化 memory-guided 行為 |
| Test time | 需要 memory | 不需要 memory |
| Reward | Factual keyword Levenshtein | Task reward + intrinsic exploration |
| 核心問題 | Multi-agent pipeline 太複雜 | Exploration bottleneck |

兩條路互補：DeltaMem 讓 agent 學會 *管理* memory，EMPO² 讓 agent 學會 *從 memory 中畢業*。

### 對 Agent Memory Research 的意義

EMPO² 挑戰了一個假設：memory 的價值在 inference time。如果 memory-guided 行為可以蒸餾進 weights，那 memory 的終極形態可能是 *training scaffolding* — 訓練時不可或缺，部署時可以拆掉。這呼應 [[scaffolding-lifecycle]] 的核心觀察：模型變強時 scaffolding 要拆。

但這只適用於 *procedural* memory（how to do things）。Episodic 和 semantic memory（what happened、what is known）本質上是 runtime 資訊，無法蒸餾進 weights。所以 EMPO² 的路線是 [[procedural-memory]] 的解法，不是所有 memory 的解法。

## Key Sources

- **2026-02-01** — Liu et al., ICLR 2026: EMPO² framework。Source: [[raw/liu-empo2-memory-rl]]

## Related

[[agent-memory]] [[deltamem]] [[agemem]] [[scaffolding-lifecycle]] [[procedural-memory]] [[self-improving-agent]] [[memory-failure-modes]] [[gene-map]] [[memory-evaluation]] [[memory-arena]] [[mem1]] [[memory-r1]]
