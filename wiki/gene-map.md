---
aliases: [Gene Map, gene map, Q-value memory, error knowledge base, 修復策略知識庫]
first_seen: 2026-04-15
last_updated: 2026-04-15
tags: [memory, architecture, retrieval]
---

# Gene Map

[[helix|Helix]] 的核心概念：一個用強化學習 Q-value 排序的錯誤修復策略知識庫。每次修復結果（成功或失敗）都回饋更新 Q-value，讓知識庫自動演化。

## Current Understanding

- **機制**：每個修復策略（fix strategy）存入 Gene Map 時附帶 Q-value 分數
  - 策略成功 → Q-value 提升 → 下次同類錯誤優先使用
  - 策略失敗 → Q-value 降級 → 排名下降或被淘汰
- **效果**：首次遇到新錯誤需 LLM 診斷（~2s），之後同類錯誤直接 pattern match（~1ms），零 LLM 成本
- **類比**：生物免疫系統 — 首次感染時免疫系統需要時間辨識和產生抗體，之後遇到同病原體立即反應
- **與傳統 retry 的差異**：retry 不學習、LLM diagnosis 太慢太貴、manual error handling 不 scale。Gene Map 是第四種選項 — 學習型修復
- **目前是 local**：每個 agent 維護自己的 Gene Map
- **願景是 shared**：所有 agent 共享一個 Gene Map network，形成集體免疫系統
  - 跨 agent 共享修復知識 = [[experiential-memory]] 的具體實踐
  - 有 network effect — 越多 agent 使用，Gene Map 越強

### 設計層面的觀察

- Gene Map 本質上是一種 **[[procedural-memory]]** — 記的是「怎麼修」而非「發生了什麼」
- Q-value ranking 避免了 [[memory-staleness]] 問題 — 不再有效的策略自然降級
- Pattern matching（而非 LLM reasoning）做 retrieval — 速度優先，跟 [[brain-first-lookup]] 同理
- Selective retention 內建（Q-value 低的策略被淘汰）— 不需要額外的 [[compounding-memory]] 管理

## Key Sources

- **2026-04-14** — Nicholas & Adrian 在 Helix 文章中首次提出 Gene Map 概念。Source: [[raw/nicholas-helix-self-healing-agents]]

## Related

[[helix]] [[procedural-memory]] [[compounding-memory]] [[experiential-memory]] [[memory-staleness]] [[brain-first-lookup]] [[nicholas-dapanji]]
