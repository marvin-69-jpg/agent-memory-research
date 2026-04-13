---
aliases: [experiential data, agent traces, interaction data]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [memory, architecture]
---

# Experiential Memory

Agent 在每次互動中產生的大量資料（traces、tool calls、decisions、outcomes），可以被累積為經驗記憶。與人類不同，agent 的經驗記憶可以跨所有 agent instances 共享。

## Current Understanding

- Agent 在每次互動中都產生大量資料 — 類似於人類「做了事情然後記住做過的事」
- Agent memory 相比人類有巨大優勢：agent 可以 fork、duplicate，經驗記憶可以在所有 instances 之間累積
  - 人類無法複製自己的經驗給另一個人；agent 可以
  - Dwarkesh Patel (@dwarkesh_sp) 討論過這個人工系統的根本優勢
- Memory 可以被視為 externalized object — [[agent-harness]] 負責做 contextualized retrieval，從所有 agent interaction 累積的記憶中拉出正確的資料
- 這衍生出兩個關鍵問題：
  1. **Distillation**：如何從 traces 高效蒸餾出 higher-level memory primitives？尤其在超長時間尺度上？
  2. **Retrieval**：如何做好 contextualized retrieval — 在正確的時間拉出正確的記憶？→ [[brain-first-lookup]]、[[hybrid-search]]
- 與 [[compounding-memory]] 的關係：experiential memory 是 compounding 的「燃料」— 有持續的經驗資料進來，compounding loop 才能轉動
- 與 [[sleep-time-compute]] 的關係：dream cycle 就是在 distill experiential memory — 把 raw traces 整理成 structured knowledge

## Key Sources

- **2026-04-13** — Viv Trivedy 論述 experiential memory 和跨 agent 累積的優勢。Source: [[raw/viv-trivedy-harness-memory-bitter-lesson]]

## Related

[[agent-memory]] [[compounding-memory]] [[sleep-time-compute]] [[brain-first-lookup]] [[hybrid-search]] [[viv-trivedy]]
