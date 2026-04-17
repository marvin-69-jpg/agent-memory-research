---
aliases: [A-Mem, agentic memory, Zettelkasten memory]
first_seen: 2026-04-15
last_updated: 2026-04-17
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

### Critique: O(N²) Scaling Problem

[[d-mem]]（arxiv 2603.14597, UCSD/CMU）直接攻擊 A-Mem 的 append-and-evolve-all 設計：
- 每個 utterance（包含 phatic filler、status update）都跑完整 evolution → write-latency O(N²)
- 在 LoCoMo-Noise（注入 75% noise）上，A-Mem 燒 1.64M tokens；D-Mem 用 RPE gating 只用 319K（−80%）且 multi-hop F1 還更高
- D-Mem 的論點：人腦的 dopamine RPE 機制已經演化出「只在 surprise + utility 都高時才 consolidate」—— A-Mem 缺這個 gate

A-Mem 不算被 obsoletes —— 它定義了 evolution semantics，D-Mem 是加一層 routing 在前面。但 deployed 系統若 conversation 含 noise（必然），A-Mem 的成本曲線會爆。

### Meta-Critique: Single-Structure Assumption

[[fluxmem]]（arxiv 2602.14038）從另一個角度看 A-Mem：graph + linked notes 只是**一種**結構，對某些 conversation pattern（時序強的、abstraction-heavy 的）不是最佳選擇。FLUXMEM 把 A-Mem 的 graph 結構當成三選項之一，動態根據 context feature 選。

## Key Sources

- **2025-02-17** — A-Mem: Agentic Memory for LLM Agents。Source: [[raw/a-mem-agentic-memory]]
- **2026-03-15** — D-MEM critique: O(N²) scaling problem，提出 RPE gating。Source: [[raw/song-d-mem]]
- **2026-02-15** — FLUXMEM meta-critique: single-structure assumption。Source: [[raw/lu-fluxmem]]

## Related

[[reconsolidation]] [[agemem]] [[graph-memory]] [[compiled-truth-pattern]] [[neuroscience-memory]] [[agent-memory]] [[memory-evaluation]] [[locomo]] [[ssgm]] [[memory-failure-modes]] [[memory-staleness]] [[d-mem]] [[fluxmem]] [[memory-worth]] [[memwright]] [[gam]] [[xmemory]]
