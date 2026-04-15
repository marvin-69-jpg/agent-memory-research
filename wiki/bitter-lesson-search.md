---
aliases: [search bitter lesson, bitter lesson for agents, agent data explosion]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [retrieval, memory, architecture]
---

# Bitter Lesson (Search)

Rich Sutton 的 Bitter Lesson 應用在 agent 記憶搜尋領域：隨著 agent 部署時間拉長到年級距，產生的資料量將超指數成長，現有的搜尋和組織基礎設施會被挑戰到極限。

## Current Understanding

- 當 agent 在現實世界中部署到**年級距**時，資料量將呈超指數（hyper-exponential）成長
- 兩個必要條件：
  1. **Own that data** — 開放生態系很重要，不能被平台鎖定 → [[memory-lock-in]]
  2. **Use that data** — 要能搜尋、蒸餾、組織這些資料
- 人類大腦在這方面做得很好：contextually 使用過去經驗、commit the right stuff to memory — 但這需要刻意練習
- 現有基礎設施（search、indexing、storage）會在新的資料 regime 下被考驗甚至崩潰
- 核心開放問題：
  - 如何高效地把 experiences（Traces）蒸餾成 higher-level memory primitives？在超長時間尺度上怎麼做？
  - 未來搜尋是 **just-in-time**（runtime retrieval）還是 **integrated into model weights**（training-time）？
  - 如何讓 model 更好地自我管理 context window？如何降低 agent 操作 external objects 時的 error rate？
- 這個框架把 [[hybrid-search]]、[[sleep-time-compute]]（offline distillation）、[[compounding-memory]]（growth dynamics）統一在一個更大的問題下：**大規模 agent 資料的搜尋與組織**

## Key Sources

- **2026-04-13** — Viv Trivedy 將 Bitter Lesson 框架應用到 agent memory search 問題上。Source: [[raw/viv-trivedy-harness-memory-bitter-lesson]]

## Related

[[hybrid-search]] [[agent-memory]] [[experiential-memory]] [[compounding-memory]] [[sleep-time-compute]] [[memory-lock-in]] [[viv-trivedy]] [[filesystem-vs-database]]
