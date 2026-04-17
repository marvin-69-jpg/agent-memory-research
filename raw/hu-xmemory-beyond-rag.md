---
source: arxiv
author: Zhanghao Hu, Qinglin Zhu, Di Liang, Hanqi Yan, Yulan He, Lin Gui
paper_id: "2602.02007"
url: https://arxiv.org/abs/2602.02007
date: 2026-02-02
revised: 2026-04-11
fetched: 2026-04-17
tags: [agent-memory, retrieval, hierarchy, benchmark]
---

# Beyond RAG for Agent Memory: Retrieval by Decoupling and Aggregation (xMemory)

Hu et al., arxiv 2602.02007v3, ICML submission. 77 upvotes on alphaXiv.

## Core Argument

RAG 的假設在 agent memory 場景不成立：
- RAG 假設語料庫大且異質 → agent memory 是有限、連貫的對話流，段落高度相關、常有重複
- Fixed top-k similarity retrieval → 回傳冗餘 context（多段 similarity 都是 0.96-0.98）
- Post-hoc pruning → 可能刪除時間上相連的前提知識，導致推理斷鏈

**主張**：retrieval 應該超越 similarity matching，改為在 latent components 上操作。

## xMemory Architecture

### 四層階層結構
1. **Themes** — 高層主題（如 "Caroline's career", "Melanie's painting journey"），LoCoMo 約 650 themes
2. **Semantic Nodes** — 每個 theme 下的語意單元，max 12 per theme
3. **Episodic Memories** — 完整的對話片段
4. **Original Messages** — 原始對話訊息

### Memory Construction
- **Sparsity-semantics objective** f(P)：平衡 theme 大小的均勻性（sparsity）和語意連貫性（semantics）
- **Guided split/merge**：theme 太大就 split（clustering），太小就 merge（nearest-neighbour）
- **kNN graph**：theme 和 semantic node 之間維持 k-nearest-neighbour graph，避免語意孤島

### Adaptive Retrieval（兩階段）
- **Stage I**：在 theme/semantic level 選一組 compact, diverse, query-relevant 的高層節點
- **Stage II**：只在 uncertainty 降低時才展開到 episode/message level，控制冗餘

## Baselines Compared
1. Naive RAG（top-20 chunks）
2. A-Mem（Zettelkasten-inspired）
3. MemoryOS（hierarchical memory OS）
4. LightMem（lightweight, efficiency-oriented）
5. Nemori（cognitively-inspired episodic segmentation）

## Results

### LoCoMo
| Model | Method | BLEU | F1 | Tokens/query |
|---|---|---|---|---|
| Qwen3-8B | Naive RAG | — | — | — |
| | Nemori | 28.51 baseline | 40.45 | — |
| | **xMemory** | **34.48** | **43.98** | — |
| GPT-5 nano | A-Mem | — | — | 9155 |
| | **xMemory** | **38.71** | **50.00** | **6581** |

- Temporal reasoning 提升最大：BLEU 23.60→29.58, F1 33.74→37.46
- Token 用量大幅降低：A-Mem 9103→4711（Qwen3-8B）

### PerLTQA
| Model | Method | BLEU | F1 | ROUGE-L | Tokens |
|---|---|---|---|---|---|
| Qwen3-8B | Naive RAG | 32.08 | 41.37 | 35.95 | 6274 |
| | xMemory | **36.24** | **47.08** | **42.50** | **5087** |

## Key Insights

1. **Redundancy without fragmentation**：核心主張。控制冗餘但不能打碎證據鏈（evidence chain）
2. **LLM-generated structured records 的脆弱性**：A-Mem, MemoryOS 依賴 LLM 生成結構化記錄，格式偏差會 cascade 成更新失敗
3. **Agent memory ≠ general RAG**：分佈不同（bounded coherent stream vs large heterogeneous corpus），需要專門的 retrieval 策略
4. **Temporal reasoning 最受益**：階層結構保留時間順序，比 flat retrieval 更能處理時序問題

## Implementation
- Embeddings: text-embedding-3-small
- LLMs tested: Qwen3-8B, Llama-3.1-8B-Instruct, GPT-5 nano
- Entropy detection: GPT-4.1-mini（for GPT-5 nano backbone）
- Hardware: NVIDIA A100 80G
