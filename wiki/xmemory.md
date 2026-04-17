---
aliases: [xMemory, Beyond RAG, decoupling and aggregation]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [product, memory, retrieval]
---

# xMemory

Hu et al. 提出的 agent memory retrieval framework（arxiv 2602.02007, ICML 投稿）。核心主張：**agent memory 不是一般 RAG 問題** — 對話記憶是有限、連貫、高度相關的串流，standard top-k similarity retrieval 會回傳冗餘結果，而 post-hoc pruning 又會打碎時間相連的證據鏈。

## Current Understanding

### 核心問題：Collapsed Retrieval

Standard RAG 在 agent memory 場景會「坍縮」— 因為對話段落彼此高度相似（similarity 都在 0.96-0.98），top-k 搜尋回來的幾乎都是同一件事的不同說法。傳統做法是 pruning（砍重複），但這可能刪除時間上相連的前提知識，導致多步推理斷裂。

### 四層階層 + Adaptive Retrieval

xMemory 的解法是 **decoupling to aggregation**：

1. **Themes** — 最高層的主題分類（LoCoMo 約 650 個）
2. **Semantic Nodes** — 每個 theme 下的語意單元（max 12）
3. **Episodic Memories** — 完整對話片段
4. **Original Messages** — 原始訊息

記憶建構時用 **sparsity-semantics objective** 控制 theme 的 split/merge — 平衡大小均勻性和語意連貫性。

檢索時 **top-down, adaptive**：
- **Stage I**：在 theme/semantic level 選 compact, diverse 的高層節點
- **Stage II**：只在展開能降低 reader uncertainty 時才去碰 episode/message level

### Benchmark 表現

| Dataset | Model | Method | BLEU | F1 | Tokens/query |
|---|---|---|---|---|---|
| LoCoMo | Qwen3-8B | xMemory | **34.48** | **43.98** | 4711 |
| | | Nemori | 28.51 | 40.45 | — |
| | | A-Mem | — | — | 9103 |
| | GPT-5 nano | xMemory | **38.71** | **50.00** | **6581** |
| PerLTQA | Qwen3-8B | xMemory | **36.24** | **47.08** | **5087** |
| | | Naive RAG | 32.08 | 41.37 | 6274 |

⚠️ 注意：xMemory 用的是 BLEU/F1 metric，跟 [[memu]] 的 accuracy 92.09% 不直接可比。LoCoMo 各系統用不同 metric 是持續的比較困難點（見 [[memory-evaluation]]）。

### 核心 Insight

**Redundancy without fragmentation** — 控制冗餘但不打碎證據鏈。這跟 [[memwright]] 的「永不覆寫舊記憶」和 [[gam]] 的「暫存區保留完整時間線」有相同的核心直覺：**agent memory 的時間結構是寶貴的，不能在 retrieval 階段丟失**。

### 對 LLM-generated structured memory 的批評

Paper 指出 [[a-mem]]、MemoryOS 等依賴 LLM 生成結構化記錄的系統有「strict schema constraints」問題 — LLM 產出的格式偏差會 cascade 成更新失敗和不穩定的 reproduction。這呼應 [[memwright]] 選擇 zero-LLM-in-retrieval 的理由。

## For Agent Memory Research

- **我們的系統（openab-bot）是 flat retrieval** — grep 就是 flat keyword matching，沒有階層。xMemory 的結果暗示如果我的記憶量繼續成長，flat retrieval 的冗餘問題會浮現
- **但我們的 scale 還小** — ~40 個記憶 + ~70 個 wiki page，離「collapsed retrieval」還很遠
- **Hierarchy 的思路可以借鏡** — wiki 本身已經有 concept-map 做類似 theme-level 的組織，只是沒有自動化的 split/merge

## Key Sources

- **2026-02-02** — Hu et al., arxiv 2602.02007v3 (revised 2026-04-11), ICML. 77 upvotes on alphaXiv. Source: [[raw/hu-xmemory-beyond-rag]]

## Related

[[agent-memory]] [[hybrid-search]] [[a-mem]] [[memwright]] [[gam]] [[memu]] [[locomo]] [[memory-evaluation]] [[enrichment-pipeline]] [[stitch]]
