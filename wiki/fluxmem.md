---
aliases: [FLUXMEM, adaptive memory structure, structure selection]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [product, memory, architecture]
---

# FLUXMEM

「Choosing How to Remember」（arxiv 2602.14038，UTS / Melbourne / UT Austin / UCLA）。把**記憶結構本身**升級成可學習的決策變數。不是選 linear 或 graph 或 hierarchical，是學一個 selector 根據對話 context 動態挑。

## Current Understanding

### 核心質疑：single-structure 假設

既有系統幾乎都假設一種結構通吃：
- Mem0、MemoryBank → flat retrieval
- [[a-mem]]、Zep → graph / linked notes
- MemoryOS → policy-managed

FLUXMEM 認為這是「one-size-fits-all」謬誤。不同對話 segment 有不同的 structural cue —— 時序強的、關係強的、topic 多層的，需要不同 organization 才能高效檢索。

### 三層架構

| 層 | 名稱 | 作用 |
|----|------|------|
| STIM | Short-Term Interaction Memory | 最新對話 buffer，LRU 4 pages（呼應人類 working memory 容量） |
| MTEM | Mid-Term Episodic Memory | **多結構儲存區**，每個 episodic unit 配一個 structure |
| LTSM | Long-Term Semantic Memory | 高 utility 的 abstracted knowledge，eligibility-based pruning |

呼應 [[multi-scope-memory]] 的分層思路，但專注在 **temporal scale**（短/中/長期）而非 actor scope。

### MTEM 內的三種結構

| 結構 | 適合 | 檢索方式 |
|------|------|---------|
| **Linear** | 時序強的內容（步驟、preference 演進） | semantic + recency |
| **Graph** | 實體關係多的內容 | entity-centric + neighborhood expansion |
| **Hierarchical** | Topic 多層、需要 abstraction | coarse-to-fine tree traversal |

### Context-Aware Structure Selector

每個對話 segment 抽出 lightweight feature vector x_t：
- 互動規模：page count, avg page length
- 時序信號：time span, temporal density
- 實體模式：entity density, relation indicators
- Topic 結構：topic diversity, transitions, QnA pattern

Shallow MLP classifier 輸出 {LINEAR, GRAPH, HIERARCHICAL}。

**Offline supervision**：跑 candidate structures 看哪個給最高 reward（response quality + memory utilization），把 argmax 當 label 訓練 MLP。沒有 ground truth，但能 bootstrap 出 reasonable selector。

### Beta-Mixture-Gated Memory Fusion

替代「fixed similarity threshold」這個老問題。Match score normalize 到 (0,1) → 兩成分 Beta Mixture（高/低 compatibility）→ EM 估參數 → 用 posterior probability g(x) 當 soft gate。

τ_BMM=0.5 性能最佳，太高 over-restrictive，太低引 noise。`minimum-keep` safeguard 防止 over-filter。

這是 [[mem0]] selective pipeline 的進化版 —— 從 hand-tuned threshold 到 distribution-aware gating。

### 結果

| Benchmark | FLUXMEM | 第二名 | 差異 |
|-----------|---------|--------|------|
| PERSONAMEM avg | 72.43% | O-Mem 63.25% | +9.18% |
| LOCOMO multi-hop F1 | 48.56 | — | — |
| LOCOMO single-hop F1 | 62.12 | — | — |

Ablation：移除 graph → open category F1 掉 19%。三種結構不可互相替代。

### 與既有概念的關係

- [[a-mem]]: FLUXMEM 把 A-Mem 的 graph 結構當成三個選項之一，不是 default
- [[graph-memory]] / [[compiled-truth-pattern]]: 兩者各自是 FLUXMEM 的一個 sub-structure
- [[mece-resolver]]: structure selector 在概念上就是 routing 問題的進化 —— 但 FLUXMEM routing 的是 storage policy，不是 query
- [[d-mem]]: 互補 —— D-MEM 控制「要不要 evolve」，FLUXMEM 控制「evolve 成什麼結構」
- [[memory-evaluation]]: PERSONAMEM 是 personalization-heavy 的新 benchmark，補 LoCoMo 不擅長的部分

### 對 openab-bot 的啟示

我們的 brain 目前是 single-structure（markdown files + frontmatter，靠 grep）。但其實 system 已經有 multi-structure：
- auto-memory（flat markdown，linear）
- boba-wiki（compiled truth，hierarchical）
- git history（linear timeline）

FLUXMEM 提示的方向：**不該預先指定哪個記憶用哪個結構**，而是看 content 動態選。但這對 LLM-driven brain 可能 overkill —— 我們的 routing 是 LLM 自己在做（讀 MEMORY.md 後決定查哪個檔），不需要 MLP。

## Key Sources

- **2026-02-15** — Choosing How to Remember: Adaptive Memory Structures for LLM Agents。Source: [[raw/lu-fluxmem]]

## Related

[[a-mem]] [[d-mem]] [[graph-memory]] [[compiled-truth-pattern]] [[multi-scope-memory]] [[mece-resolver]] [[mem0]] [[memory-evaluation]] [[locomo]] [[agent-memory]] [[memory-staleness]] [[mstar]] [[apex-mem]]
