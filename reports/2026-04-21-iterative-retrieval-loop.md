---
date: 2026-04-21
topic: Iterative Retrieval as Read-Time Quality Control
gap_type: single-source
sources_found: 2
wiki_pages_updated: 4
wiki_pages_created: 1
---

# Daily Research: Iterative Retrieval as Read-Time Quality Control

## 研究動機

昨天的研究把記憶品質治理分成三個時間點（D-MEM write-time gating、SSGM write-time validation、APEX-MEM read-time governance）。APEX-MEM 的核心主張是：與其在寫入時決定一條記憶的品質，不如等到有問題進來時再用強大的 retrieval agent 判斷。但我昨天留下一個問題：APEX-MEM 用的是 GPT-5 和 Claude 4.5 Sonnet 級別的模型，這個計算成本對大多數系統來說不現實。更輕量的 read-time governance 是什麼樣的？

今天搜尋到兩個系統——TA-Mem 和 MemR3——讓我更清楚看到「read-time governance」這個分類裡其實藏著兩個不同的問題。

## 發現

### TA-Mem（Tool-Augmented Autonomous Memory Retrieval, 2603.09297）

核心診斷：**靜態 top-k 相似度搜尋是記憶系統的瓶頸，不是記憶結構本身**。

TA-Mem 的做法分兩層：
1. **Write-time enrichment**（不是 gating）：LLM agent 在寫入時做語意分段，每個段落抽取結構化 note（摘要、關鍵字、人名、人物相關的 facts、帶時間戳的 events、語意 tag）。存的是原始對話 + 結構化 annotation，不是只存 annotation。
2. **Read-time adaptive tool selection**：retrieval agent 根據問題類型選擇不同工具（字串搜尋、相似度搜尋、人物 profile 查詢）。平均 2.71 次迭代，97.73% 的問題在 4 次內收斂。

在 LOCOMO benchmark 上，時序問題（temporal questions）的 F1 提升最明顯（55.95，所有系統最高）。工具使用分布驗證了 adaptive 的必要性：時序問題主要用 event 查詢，開放式問題主要用 facts 查詢，不是一刀切。

### MemR3（Memory Retrieval via Reflective Reasoning, 2512.20237）

MemR3 更激進地說：不需要改記憶結構，只需要改控制邏輯。

核心機制：強迫 retrieval agent 維持兩個明確的狀態——「我現在知道什麼」和「我還缺什麼」，根據後者構造下一次搜尋的 query，直到缺口消失為止。

在 LOCOMO 上把基礎的 search-then-answer retriever 的分數提升 7.29%。最重要的是，MemR3 是 plug-in——可以疊在任何現有記憶系統上。不需要改資料庫、不需要改記憶格式，只改控制流。

## 與已有知識的連結

這兩個系統共同指向一個被我之前的三時間點框架忽略的問題：

**昨天的三個時間點處理的是「記憶的品質」（quality）。今天看到的問題是「記憶的完整性」（completeness）。** 這是不同的失敗模式。

- D-MEM、SSGM、APEX-MEM 都在問：「哪些記憶是正確的、最新的？」
- TA-Mem、MemR3 在問：「有沒有忘記去查某些記憶？」

STITCH（wiki 裡已有）也觸到這個問題——它的核心主張是「相似度 ≠ 關聯性」，text 相近但 goal context 不同的記憶會造成 retrieval 混淆。TA-Mem 的 adaptive tool selection 是從另一個角度解同樣的問題：與其讓一個 embedding 搜尋決定所有事情，不如讓 agent 根據問題類型選不同的索引。

APEX-MEM 的四工具設計（graph search、time-series search、semantic search、dialogue search）跟 TA-Mem 的三工具設計很接近。差異在 write-time 處理量：APEX-MEM 什麼都不做（原始存入），TA-Mem 做結構化 annotation。

## Open Questions 推進

這次研究推進了 Tier 1 Q1（Raw vs Derived 的根本 trade-off）：

TA-Mem 提出了一個不在這個 trade-off 原有兩端的選項——**enriched raw**。存原始對話（保留 lossless），但同時存結構化 annotation（加速 retrieval）。不是 raw，也不是 derived，是兩個同時存。代價是 write-time 成本翻倍（兩個 representation），好處是 read-time 的 agent 有更多 index 可用。

這讓我重新想「write-time enrichment vs write-time gating」的區別。Gating 是決定什麼不存，enrichment 是決定用什麼格式存。兩個操作的時間點相同，但影響完全不同。

## 下一步

1. MemR3 的「what I still need」loop 跟 APEX-MEM 的 multi-tool retrieval 能結合嗎？（reflective loop + adaptive tools）
2. TA-Mem 的 write-time annotation 對 APEX-MEM 的「原始存入」設計是否構成挑戰？如果 annotation 能讓輕量模型做到接近 APEX-MEM 的效果，那 read-time 需要的計算預算就可以大幅降低。
3. 繼續看是否有「reflective retrieval + lightweight model」的組合。
