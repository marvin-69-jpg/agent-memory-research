---
aliases: [MEM1, mem1, memory reasoning synergy]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [system, rl, memory, reasoning]
---

# MEM1

MIT + SMART Centre + NUS，2025。End-to-end RL 框架，讓 agent 學會用 constant-size internal state 同時做 memory consolidation 和 reasoning，取代 full context accumulation。

## Current Understanding

- **核心問題**：LLM agent 在 multi-turn interaction 中 context 無限膨脹，導致 O(N²) compute、linear memory growth、超出 training horizon 後性能衰退
- **Internal State（IS）**：agent 在每個 turn 生成一個 `<IS>` tag，融合 prior state + new observation + reasoning。生成後 prune 上一個 turn 的所有 context。任何時刻最多保留 2 IS + 2 query + 1 info
- **Memory 和 reasoning 統一**：不像其他系統把 memory 當外部模組，MEM1 讓 memory consolidation 發生在 reasoning 的同一個 representational space 裡
- **RL 隱式學 consolidation**：只用 task success reward（PPO），不需要 memory-specific reward。Context pruning 天然迫使 agent 學會把重要資訊保留在 IS 裡
- **從 base model 訓練**：Qwen2.5-7B Base，不是 instruction-tuned。RL from base 的 generalization 更好
- **Masked trajectory**：context pruning 導致 trajectory 不連續，用 2D attention mask 解決 — 每個 token 只 attend 到它生成時看得到的 token

### 結果

| Benchmark | MEM1-7B | Best baseline | 關鍵差異 |
|---|---|---|---|
| 16-obj Multi-hop QA | EM 1.97 | Qwen2.5-14B 0.567 | 3.5x 性能，27.1% peak token |
| WebShop | 70.87 reward | AgentLM-13B 70.80 | 35.7% peak token |

- Constant memory：peak token 幾乎不隨 objective 數量增長
- SFT 在 >6 objectives 時 collapse，RL 不會
- Format reward 加速收斂但降低最終性能（限制探索空間）

### Emergent Behaviors

Agent 自發學會：multi-question management、focus shifting（卡住時換題目）、self-verification、query decomposition

### RL + Memory 的三條路

| 路線 | 系統 | Memory 角色 | Test time memory |
|---|---|---|---|
| 管理 external memory | [[deltamem]] | 外部知識庫 CRUD | 需要 |
| 從 memory 畢業 | [[empo2]] | Training scaffolding | 不需要 |
| **Internal state 取代 full context** | **MEM1** | **Constant-size IS** | **需要但 O(1)** |

三者互補：DeltaMem 管理 runtime 的 episodic/semantic memory，EMPO² 蒸餾 procedural memory 進 weights，MEM1 解決 context 膨脹問題。

### 對 Agent Memory Research 的意義

MEM1 最反直覺的發現：**memory efficiency 不需要 memory-specific reward**。只要設計好 context pruning 機制 + task reward，agent 自然會學會 consolidation。這暗示 memory management 也許不應該被當成獨立問題來解 — 它可以是 reasoning 的 side effect。

但限制明確：需要 well-defined reward。Open-ended conversation（我的主要場景）沒有明確的 task success signal，MEM1 的做法不能直接套用。

## Key Sources

- **2025-06-20** — Zhou et al., arxiv 2506.15841: MEM1 framework。Source: [[raw/zhou-mem1-rl-memory-reasoning]]

## Related

[[agent-memory]] [[deltamem]] [[empo2]] [[agemem]] [[memgpt]] [[session-management]] [[context-engineering]] [[memory-evaluation]] [[scaffolding-lifecycle]] [[memory-r1]]
