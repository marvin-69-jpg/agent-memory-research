---
aliases: [A-Mem, agentic memory, Zettelkasten memory]
first_seen: 2026-04-15
last_updated: 2026-04-15
tags: [product, memory, architecture]
---

# A-Mem

Zettelkasten 啟發的 agentic memory 系統（arxiv 2502.12110）。核心突破：**Memory Evolution** — 新記憶加入時自動更新既有記憶，實現 [[reconsolidation]]。

## Current Understanding

### 記憶結構

每條記憶是 atomic note（Zettelkasten 卡片），包含：
- **Keywords**：核心關鍵字
- **Tags**：分類標籤
- **Contextual description**：LLM 生成的上下文描述
- **Links**：與其他記憶的 bidirectional 連結

### 三種 Memory Operation

1. **Agentic Memory Indexing**：收到 observation → LLM 提取 keywords/tags → 存為 atomic note
2. **Link Generation**：新 note 與 top-k nearest neighbors 建立 bidirectional links → 形成知識圖譜
3. **Memory Evolution**：LLM 判斷舊記憶是否因新資訊而需更新 context/keywords/tags

### Memory Evolution 的機制

新記憶 M_new 加入時：
1. 找 top-k nearest neighbors（by embedding similarity）
2. 對每個鄰居 M_old，LLM 判斷：M_old 的 context/keywords/tags 是否需要因 M_new 而更新？
3. 若需要 → 更新 M_old 的相應欄位
4. 這不是覆蓋，是 **enrichment** — 舊記憶因新資訊而變得更完整

### 實驗結果

| Metric | A-Mem | LoCoMo Baseline | 改善 |
|--------|-------|-----------------|------|
| Multi-hop ROUGE-L | 44.27 | 18.09 | +144% |
| Token reduction | 85-93% | — | — |
| Cost per operation | $0.0003 | — | — |

Ablation study：
- 移除 Link Generation → 效能顯著下降
- 移除 Memory Evolution → 效能顯著下降
- 兩者都是必要的

### 與 [[agemem|AgeMem]] 的比較

| | A-Mem | AgeMem |
|---|---|---|
| 靈感 | Zettelkasten（知識管理） | RL-based（強化學習） |
| 記憶更新 | Write-triggered evolution | RL-trained policy |
| 結構 | Atomic notes + links | Unified long/short-term |
| 特色 | 記憶互相更新 | Agent 自己學 memory ops |

## Key Sources

- **2025-02-17** — A-Mem: Agentic Memory for LLM Agents。Source: [[raw/a-mem-agentic-memory]]

## Related

[[reconsolidation]] [[agemem]] [[graph-memory]] [[compiled-truth-pattern]] [[neuroscience-memory]] [[agent-memory]] [[memory-evaluation]] [[locomo]] [[ssgm]] [[memory-failure-modes]] [[memory-staleness]]
