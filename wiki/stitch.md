---
aliases: [STITCH, contextual intent, Grounding Agent Memory in Contextual Intent, CAME-Bench]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [product, memory, retrieval, benchmark]
---

# STITCH

Yang et al.（UIUC + Stanford）提出的 agentic memory system（arxiv 2601.10702, 2026-01-15）。核心主張：**similarity ≠ relevance** — 在長對話中相同 entity 會在不同 goal 下出現，similarity search 會抓到 context 錯誤的記憶。

## Current Understanding

### 核心問題：Context-Mismatched Retrieval

跟 [[xmemory]] 的 collapsed retrieval 是姊妹問題但角度不同：
- **xMemory** 處理的是冗餘（很多段落說同一件事，top-k 全回同樣的內容）
- **STITCH** 處理的是混淆（文字相似但 goal context 不同，retrieval 抓到錯誤的早期 turn）

兩者共享的 insight：**standard similarity matching 不夠用，agent memory 需要額外的結構信號**。

### Contextual Intent 三要素

每個 trajectory step 被標上：
1. **Thematic scope** — 當前的 latent goal（如「出差」vs「家庭旅行」）
2. **Action type** — 行為類別（search / compare / book）
3. **Salient entity type** — 重要屬性（Price / Rating / Location）

寫入時標 tag + rewrite（「book it」→ 明確名稱），檢索時先 intent matching 過濾再 text ranking。

### Benchmark: CAME-Bench

作者同時提出新 benchmark — 批評 [[locomo]] 等既有 benchmark 會切成獨立 mini-episodes、enforce strict turn-taking，masking 了真實場景中 interleaved goals 的難度。

CAME-Bench 三軸：interleaved non-turn-taking / multi-domain / controlled difficulty。

### 結果

| Benchmark | Method | Score |
|---|---|---|
| CAME-Bench (S) | **STITCH** | **Macro-F1 0.844** |
| | A-Mem | 0.376 |
| | Secom | 0.501 |
| LongMemEval (O/S/M) | **STITCH** | **0.860 / 0.860 / 0.800** |
| | A-Mem | 0.780 / 0.740 / 0.667 |

Ablation：移除 thematic scope 掉最多（F1 0.844→0.463），代表 **goal-level context 是最重要的 retrieval signal**。

### 跟其他系統的連結

| System | 解決什麼 | 方法 |
|---|---|---|
| [[xmemory]] | Collapsed retrieval（冗餘） | 階層結構 + adaptive expansion |
| **STITCH** | Context-mismatched retrieval（混淆） | Intent tagging + intent-first filter |
| [[memwright]] | Non-deterministic retrieval | Zero-LLM 5-layer pipeline |
| [[gam]] | Short→long 寫入時機 | 暫存區 + 語意轉換觸發 |

四個系統各解 retrieval 的不同面向，但都指向同一個結論：**naive similarity search 是 agent memory 的瓶頸**。

## For Agent Memory Research

- **我們的 grep 只做 keyword matching**，連 similarity search 都還沒有，更別說 intent-aware retrieval。但我們目前 scale 小（~40 memories），keyword 夠用
- **Thematic scope 的概念可以低成本實作**：memory 的 `type` field（user/feedback/project/reference）某種程度就是 thematic scope，只是粒度很粗
- **CAME-Bench 對 LoCoMo 的批評值得注意**：如果我們用 LoCoMo 分數比較各系統，要知道 LoCoMo 可能低估了 interleaved goal 場景的難度

## Key Sources

- **2026-01-15** — Yang et al., arxiv 2601.10702v1, UIUC + Stanford. Source: [[raw/yang-stitch-contextual-intent]]
- **Tweet** — Rohan Paul (@rohanpaul_ai), X thread 介紹。Source: [[raw/yang-stitch-contextual-intent]]

## Related

[[xmemory]] [[agent-memory]] [[hybrid-search]] [[a-mem]] [[locomo]] [[memory-evaluation]] [[memory-arena]]
