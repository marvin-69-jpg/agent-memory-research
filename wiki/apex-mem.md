---
aliases: [APEX-MEM, append-only memory, retrieval-time resolution, temporal event memory]
first_seen: 2026-04-20
last_updated: 2026-04-21
tags: [product, memory, architecture, retrieval, governance]
---

# APEX-MEM

Amazon AGI 的 semi-structured memory 系統（arxiv 2604.14362，2026-04-15）。核心設計選擇：**不在寫入時做 consolidation，全部 append，在 retrieval time 才 resolve 矛盾**。這跟 [[ssgm]] 的 pre-consolidation validation 和 [[d-mem]] 的 write-time gating 是光譜上的三個端點。

## Current Understanding

### 設計哲學：Write Everything, Resolve Later

既有的記憶系統大多假設寫入時就該決定「這條記憶值不值得存」「跟既有記憶衝突怎麼辦」。APEX-MEM 認為這個假設有根本問題：

1. **Consolidation 會丟資訊**：overwrite 或 merge 後，原始 context 不可恢復
2. **寫入時不知道未來的 query**：你不知道哪條細節以後會被問到，提早丟掉可能是錯的
3. **矛盾本身是有用的信號**：使用者的偏好會變，保留矛盾的歷史讓 retrieval agent 能做更好的時序推理

因此 APEX-MEM 選擇 **append-only event storage**：所有 facts 都錨定在有時間戳的 conversational events 上，保留完整歷史（含矛盾和修正），在 query time 才根據 temporal validity 做 resolution。

### 架構

**Property Graph**：G = (V, E, Π, Λ)
- 35 entity classes（Person, Organization, Place, Event, Product, CreativeWork 等），類似 YAGO taxonomy
- Facts = subject-property-value assertions，每條帶 temporal validity interval [t_from, t_to]、confidence score、evidence set
- Events 是 first-class citizens（不是 entity 的附屬品）

**Entity Resolution**：dense semantic search + structured LLM reasoning → soft-canonicalization。解決 entity confusion 問題（→ [[memory-failure-modes]]）

**Retrieval Agent**（ReAct-style，4 個工具）：
1. **SCHEMAVIEWER** — 查 schema 做 query planning
2. **ENTITYLOOKUP** — hybrid index（dense + lexical）→ 帶時序 context 的 entity documents
3. **GRAPHSQL** — read-only SQL，做精確的時序計算和 aggregation
4. **SEARCH** — 統一的 hybrid search（graph + entity + property + SQL + semantic）

### 跟其他記憶系統的定位比較

| 系統 | 何時決定「記憶品質」 | 怎麼處理矛盾 | Trade-off |
|---|---|---|---|
| [[d-mem]] | **Write time**（RPE gate，skip 80% noise） | 不寫就不矛盾 | 低寫入成本，但可能丟掉日後有用的細節 |
| [[ssgm]] | **Pre-consolidation**（validation gate） | 跟 protected facts 衝突就擋 | 防 drift，但 gate 判斷可能有 false positive |
| **APEX-MEM** | **Retrieval time**（agent 做 temporal resolution） | 保留矛盾，query 時才選 | 完整歷史，但 retrieval 成本高、依賴 agent 品質 |

這三者不是競爭關係，是同一問題的不同答案：**在 pipeline 的哪個階段花 compute 做品質把關**。

### 結果

- **LOCOMO**：88.88%（GPT5），比 MIRIX 85.38% 高 3.5pp。temporal queries 90.63%（特別強）
- **LongMemEval**：86.2%（Claude 4.5 Sonnet），比 Nemori +11.6pp
- **SealQA-Hard**：40.15%（GPT5），比 O3 +5.55pp — 在 noisy/conflicting 場景優勢明顯

Ablation 顯示四個工具缺一不可：只用 GraphSQL 需要 3.3x 的 tool calls 才達到更低的 accuracy。

### 限制

- Graph construction 的 entity resolution + fact extraction 需要 LLM calls，成本高
- Retrieval agent 的 SQL generation 品質直接影響結果
- 目前只支援 text（no multimodal）
- Highly noisy multi-document 場景仍有 performance gap

### 跟 self-refinement regimes 的連結

APEX-MEM 的 append-only + retrieval-time resolution 跟 [[refinement-regime]] 的三種體制有結構性相似：

- Write-time gating（D-MEM）≈ 外掛 judge panel（[[autoreason]]）— 在產出前就攔截
- Pre-consolidation validation（SSGM）≈ multi-dimensional rubric（De Jure）— 用明確標準做有限修復
- Retrieval-time resolution（APEX-MEM）— 接受所有輸入，把「判斷」推遲到有明確 information need 時

## Key Sources

- **2026-04-15** — APEX-MEM: Agentic Semi-Structured Memory with Temporal Reasoning（Banerjee et al., Amazon AGI）。Source: [[raw/banerjee-apex-mem]]

### 與 TA-Mem 的對比（2026-04-21 補充）

[[ta-mem]] 和 APEX-MEM 都做 multi-tool adaptive retrieval，但攻擊不同的失敗模式：

| | APEX-MEM | TA-Mem |
|--|--|--|
| 核心問題 | 哪條記憶今天「仍然有效」（staleness）| 有沒有找對工具找到「該找到的」（completeness）|
| Write-time | 原始 append，不處理 | 結構化 annotation（enrichment）|
| Read-time 模型 | GPT-5 / Claude 4.5 Sonnet | GPT-4o-mini |

TA-Mem 的 write-time enrichment 讓輕量模型在 read-time 有更多索引入口，以計算前置換取 retrieval 精準度。

## Related

[[ssgm]] [[d-mem]] [[ta-mem]] [[memr3]] [[locomo]] [[graph-memory]] [[memory-failure-modes]] [[memory-staleness]] [[reconsolidation]] [[a-mem]] [[refinement-regime]] [[agent-memory]] [[memory-worth]] [[fluxmem]] [[mem0]] [[mirix]]
