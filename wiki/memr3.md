---
aliases: [MemR3, MemR³, Memory Retrieval via Reflective Reasoning, reflective retrieval]
first_seen: 2026-04-21
last_updated: 2026-04-21
tags: [product, memory, retrieval, architecture]
---

# MemR3

Memory Retrieval via Reflective Reasoning for LLM Agents（arxiv 2512.20237, 2025-12-31）。核心主張：**記憶搜尋最常見的失敗原因不是記憶格式不對，而是停得太早**。讓 retrieval agent 顯式追蹤「我還缺什麼」，把搜尋變成迭代 loop，直到缺口填滿。

## Current Understanding

### 核心診斷：Single-Shot Retrieval 的失敗模式

現有記憶系統大多做 one-shot retrieval：問題進來 → 做一次搜尋 → 拿到結果 → 回答。這個流程的問題不是搜尋工具不夠好，而是控制邏輯太簡單：

- 一次搜尋拿到的是 noisy pile（一堆可能相關但不確定的段落）
- Agent 沒有機制問自己「我需要的東西有沒有都找到了」
- 停得太早 = 用不完整的 context 做推理

記憶錯誤通常不是模型太笨，而是「拿到錯的過去資訊」或「太早停下來只有一半事實」。

### 機制：Explicit Gap Tracking

MemR3 強迫 retrieval agent 在每次搜尋結束後明確維持兩個狀態：

1. **What I know so far** — 目前已搜到的相關資訊摘要
2. **What is still missing** — 為了回答問題，我還需要什麼

然後用 **「我還缺什麼」** 構造下一次的搜尋 query，直到「缺口」為空。

這個設計讓每一輪搜尋都有明確的方向（不是 random walk），也讓失敗路徑可被追蹤（因為 gaps 是顯式的，開發者可以 inspect 為什麼每一步這樣搜）。

### Plug-in 架構

MemR3 的關鍵設計選擇：**不改底層記憶系統，只改控制邏輯**。

- 可以疊在 chunk search 上
- 可以疊在 graph memory 上
- 不需要改資料庫格式、不需要改記憶 schema

這讓 MemR3 成為其他系統的可組合 controller，而不是要替換既有系統的競爭者。

### 結果

在 LOCOMO benchmark 上，把基礎的 search-then-answer retriever 的分數提升 **7.29%**。

Gaps 的顯式記錄讓 debugging 變得可行：可以逐步看 retrieval agent 的推理路徑，找出系統性失敗的原因。

### 與 TA-Mem 的關係

MemR3 和 [[ta-mem]] 都是 iterative read-time retrieval，但設計重點不同：

| | MemR3 | TA-Mem |
|--|--|--|
| 核心創新 | 控制流（explicit gap tracking）| 工具多樣性（adaptive tool selection）|
| Write-time | 不處理 | 結構化 annotation |
| 底層搜尋 | 任何現有搜尋（plug-in）| 三種專用工具 |
| 透明度 | 高（gaps 可 inspect）| 中（tool choice 可見）|

兩者可以組合：TA-Mem 的 adaptive tools + MemR3 的 gap-tracking loop 理論上是互補的。

### 對「Retrieval Completeness」問題的定位

MemR3 和 TA-Mem 共同指向一個在記憶品質討論裡常被忽略的維度：

**Quality（記憶是否正確）** vs **Completeness（搜尋有沒有找全）**

- D-MEM、SSGM、APEX-MEM 都在處理 quality（哪條記憶是對的、最新的）
- MemR3、TA-Mem 在處理 completeness（有沒有找到所有該找到的東西）

這是兩種不同的失敗模式，需要不同的解法。

## Key Sources

- **2025-12-31** — Rohan Paul (@rohanpaul_ai) 介紹 MemR3，8876 views，132 likes。Source: [[raw/rohanpaul-memr3-reflective-retrieval]]
- **2025-12-31** — Paper: arxiv.org/abs/2512.20237

## Related

[[ta-mem]] [[apex-mem]] [[stitch]] [[locomo]] [[memory-failure-modes]] [[xmemory]] [[a-mem]]
