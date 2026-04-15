---
title: "A-Mem: Agentic Memory for LLM Agents"
source: arxiv
paper_id: "2502.12110"
date: 2025-02-17
url: https://www.alphaxiv.org/overview/2502.12110
topic: reconsolidation
---

# A-Mem: Agentic Memory for LLM Agents

## 核心概念

Zettelkasten 啟發的 agentic memory 系統。每條記憶是 atomic note，包含：keywords、tags、contextual description、links。

## Memory Evolution（記憶進化）

核心突破：**新記憶加入時，會觸發對既有歷史記憶的更新**。

- 新 memory 加入 → 找 top-k nearest neighbors → 更新這些舊記憶的 context/keywords/tags
- 這是 **reconsolidation 的直接實現**：retrieval 不是 read-only，而是會修改既有記憶
- Link Generation：新 note 自動與最近鄰形成連結，建構知識圖譜

## 三種 Memory Operation

1. **Agentic Memory Indexing**：收到 observation → LLM 提取 keywords、tags → 存為 atomic note
2. **Link Generation**：新 note 與 top-k nearest neighbors 建立 bidirectional links
3. **Memory Evolution**：LLM 判斷舊記憶是否因新資訊而需要更新 context/keywords/tags

## 實驗結果

- LoCoMo Multi-hop ROUGE-L: 44.27 vs baseline 18.09（+144%）
- 85-93% token reduction
- $0.0003 per operation
- Ablation: Link Generation 和 Memory Evolution 都是必要的，移除任一個都顯著降低效能

## 與 Reconsolidation 的關係

A-Mem 是目前最直接實現 neuroscience reconsolidation 的系統：
- 生物學：每次 retrieve 記憶都會 reconsolidate（重新寫入）
- A-Mem：每次新記憶加入都會觸發舊記憶的 evolution（更新 context/tags）
- 差異：A-Mem 是 write-triggered 而非 read-triggered，但效果類似 — 記憶是 mutable 的

## 關鍵引用

> "Unlike static memory storage, A-Mem enables memories to autonomously evolve — updating context, refining connections, and reorganizing knowledge structures."
