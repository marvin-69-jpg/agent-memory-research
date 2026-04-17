---
aliases: [GAM, hierarchical graph memory, graph agentic memory]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [product, memory, architecture, retrieval]
---

# GAM

arxiv 2604.12285（Wu et al., 2026-04-14）。Hierarchical Graph-based Agentic Memory。核心突破：**把 memory encoding 和 consolidation 解耦**，用雙層圖結構分離即時感知和長期保留。

## Current Understanding

### 雙層圖架構

| 層 | 名稱 | 作用 | 節點 | 邊 |
|---|---|---|---|---|
| Local | Event Progression Graph（EPG） | 暫存當前對話 | 原子互動單元（utterance/response） | 時序 + 因果 |
| Global | Topic Associative Network（TAN） | 整合長期知識 | 語意主題叢集 | LLM 評分的語意相關性權重 |

**核心原則**：新輸入**只** append 到 EPG，不碰 TAN。TAN 只在 semantic boundary 時才接收整合。這防止 noise 汙染長期記憶。

### Encoding ↔ Consolidation 解耦

兩種狀態交替運作：

1. **Episodic Buffering**：持續中 — 新 utterance → EPG，不碰全域記憶
2. **Semantic Consolidation**：觸發時 — 偵測到 topic shift（semantic divergence > threshold ε）→ 把 EPG 整合成 **dual-granularity topic node**：
   - **Summary**（抽象推理用）
   - **Raw content**（細節回憶用）
   - 然後透過 LLM 評分的 semantic edges 插入 TAN

觸發機制：2048-token buffer + LLM discriminator 偵測 topic boundary。不是固定間隔，是語意轉換時才做。

**神經科學靈感**：模仿 sleep-dependent memory consolidation — encoding（清醒）和 consolidation（睡眠）是分離的。跟 [[sleep-time-compute]] 的 dream cycle 同源概念，但 GAM 把它精細化到 **conversation 內**的語意邊界。

### Multi-Factor Retrieval

Top-down 跨層檢索：

1. **Semantic Anchoring**：vector similarity 選 top-k topic nodes → 擴展到 first-order neighbors
2. **Structural Drill-Down**：跨層 link 進入 archived event graphs
3. **Multi-Factor Re-ranking**：`Score(v,q) = P_sem(v|q) · ∏β_k^I_k(v,q)`
   - Confidence（β=1.2）、Temporal（β=1.4）、Role（β=1.4）

### Benchmark

LoCoMo（Qwen 2.5-7B）：

| Method | Avg F1 | Tokens/Query | Latency |
|---|---|---|---|
| **GAM** | **40.00** | 1,370 | 0.80s |
| [[mem0]] | 35.38 | 1,533 | 0.51s |
| [[a-mem]] | 24.20 | 4,221 | 2.21s |

GAM 比 Mem0 高 13% F1、省 11% tokens。A-Mem 花 3x tokens 但 F1 低 40%。

Temporal tasks 特別強：GAM 48.97 vs Mem0 41.22 — semantic consolidation 保持了時序精度。

### Ablation：EPG 是最重要的組件

| 移除什麼 | F1 下降 |
|---|---|
| EPG（local temporal graph） | −14.94（最大） |
| SSM（semantic shift monitor） | −7.42 |
| TAN（global semantic network） | −4.93 |
| MFR（multi-factor retrieval） | −4.06 |

EPG 的 removal 造成最大損害 → **temporal/narrative coherence 是最重要的記憶組件**。

### Robustness

40% topic segmentation noise 下，F1 只掉 1.4（40.00 → 38.60），比 Fixed Window baseline（34.23）高。系統不依賴完美的 boundary detection。

## 與其他系統的比較

| | GAM | [[a-mem]] | [[d-mem]] |
|---|---|---|---|
| 結構 | 雙層圖（EPG+TAN） | 單層 linked notes | 單層 + RPE gate |
| Consolidation 觸發 | Semantic boundary | 每次寫入 | RPE surprise gate |
| Token 效率 | 1,370/query | 4,221/query | ~319K total (LoCoMo-Noise) |
| 核心 insight | 分離 encoding/consolidation | Memory evolution | 只 consolidate surprises |

GAM 跟 D-Mem 的設計哲學其實互補：D-Mem 說「不是每個 utterance 都值得 consolidate」（RPE gate），GAM 說「consolidation 只在 topic shift 時做」（semantic boundary）。兩者都在對抗 A-Mem 的 every-write-triggers-evolution。

## For Agent Memory Research

- **Dual-granularity = [[compiled-truth-pattern]] 的圖譜版**：summary（compiled truth）+ raw content（timeline），但包在 graph node 裡而不是 flat file
- **EPG 最重要的 ablation 結果**跟 [[mstar]] 的發現呼應：M★ 在 LoCoMo 上進化出的最佳架構也包含 structured metadata + source diversity，temporal coherence 是關鍵
- **對 openab-bot 的啟示**：我們目前的 memory 沒有「暫存 → 整合」的分離。每次寫 memory 都直接寫到 long-term store。GAM 暗示也許該有一個 session-level buffer，session 結束時才 consolidate 到 permanent memory

## Key Sources

- **2026-04-14** — GAM: Hierarchical Graph-based Agentic Memory, arxiv 2604.12285. Source: [[raw/wu-gam-hierarchical-graph]]

## Related

[[graph-memory]] [[a-mem]] [[d-mem]] [[sleep-time-compute]] [[neuroscience-memory]] [[compiled-truth-pattern]] [[mem0]] [[locomo]] [[memory-evaluation]] [[reconsolidation]] [[agent-memory]] [[mstar]]
