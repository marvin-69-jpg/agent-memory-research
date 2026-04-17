---
source: arxiv
author: Ruozhen Yang, Yucheng Jiang, Yueqi Jiang, Priyanka Kargupta, Yunyi Zhang, Jiawei Han
paper_id: "2601.10702"
url: https://arxiv.org/abs/2601.10702
date: 2026-01-15
fetched: 2026-04-17
tags: [agent-memory, retrieval, intent, benchmark]
---

# Grounding Agent Memory in Contextual Intent (STITCH)

Yang et al., UIUC + Stanford, arxiv 2601.10702v1, Jan 15 2026.

## Core Problem

在長對話中，相同的 entity 和 fact 會在不同 goal 和 constraint 下反覆出現。Similarity search 因此抓到錯誤的早期 turn — 因為文字相似但 context 不同。

例：使用者先查「紐約飯店」（出差、要會議室），後來又查「紐約飯店」（家庭旅行、要游泳池）。Similarity search 會把第一次的結果混進第二次。

## STITCH — Structured Intent Tracking in Contextual History

### Contextual Intent 三要素

每個 trajectory step 被標上 structured retrieval cue：
1. **Thematic scope** — 當前 latent goal 定義的主題段落（如「出差規劃」vs「家庭旅行」）
2. **Action type** — 行為類型（如 search、compare、book）
3. **Salient entity type** — 重要的 entity 屬性（如 Metric、Hyperparameter、Price、Rating）

### 運作方式

**寫入時**：每個 step 被 rewrite（「book it」→ 具體名稱）並標上 contextual intent tag
**檢索時**：先用 intent matching 過濾歷史（結構相容性），再用 text ranking（語意相關性）。Semantically similar but context-incompatible 的記憶被 suppress

### 與 xMemory 的比較

| 維度 | xMemory | STITCH |
|---|---|---|
| 解決的問題 | Collapsed retrieval（冗餘） | Context-mismatched retrieval（語意相似但 context 錯） |
| 方法 | 階層結構（theme → semantic → episode → message） | Intent tagging（goal + action + entity type） |
| 組織時機 | 建構記憶時 | 寫入時標 tag |
| 檢索策略 | Top-down adaptive expansion | Intent filter → text ranking |
| Benchmark | LoCoMo, PerLTQA | CAME-Bench, LongMemEval |

兩者共同的 insight：**similarity matching 不夠用，agent memory retrieval 需要額外的結構信號**。

## CAME-Bench

作者同時提出 **CAME-Bench**（Context-Aware Memory Evaluation Benchmark）：
- 目標：測 context-aware retrieval，不只是 semantic relevance
- 三個設計軸：
  1. Interleaved, non-turn-taking interaction
  2. Multi-domain coverage
  3. Controlled difficulty via diverse question types + length stratification
- 批評既有 benchmark（如 LoCoMo）：segment into independent mini-episodes、enforce strict turn-taking、queries answered immediately → mask the harder interleaved case

## Results

### CAME-Bench (S subset, N=144)
| Method | Macro-P | Macro-F1 |
|---|---|---|
| A-Mem | 0.387 | 0.376 |
| Secom | 0.532 | 0.501 |
| **STITCH** | **0.810** | **0.844** |

### LongMemEval
| Method | O | S | M |
|---|---|---|---|
| A-Mem | 0.780 | 0.740 | 0.667 |
| Secom | 0.520 | 0.580 | 0.600 |
| **STITCH** | **0.860** | **0.860** | **0.800** |

### Ablation（CAME-Bench S）
| Variant | Macro-P | Macro-F1 |
|---|---|---|
| Full STITCH | 0.810 | 0.844 |
| w/o thematic scope | 0.457 | 0.463 |
| w/o event type | 0.730 | 0.753 |
| w/o coreference | 0.554 | 0.578 |
| w/o key entity type | 0.713 | 0.735 |

Thematic scope 被移除時掉最多（0.810→0.457），代表 goal-level 的 context 是最重要的 retrieval signal。

## Key Insight

**Similarity ≠ relevance in agent memory**。兩段文字可以語意高度相似（都在講「紐約飯店」），但在不同 goal context 下完全不相關。Agent memory 需要的不只是「什麼跟什麼像」，而是「什麼跟什麼在同一個目標下被使用」。

Rohan Paul tweet (X): "wrong recall can derail the whole plan" — 在 multi-step agent 中，一次錯誤的記憶檢索會連鎖影響後面所有步驟。

## Source Tweet

- Rohan Paul (@rohanpaul_ai), X, https://x.com/rohanpaul_ai/status/2013138856141631931
