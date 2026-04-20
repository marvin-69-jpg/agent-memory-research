---
aliases: [TA-Mem, tool augmented memory, adaptive retrieval tools, TA-Mem framework]
first_seen: 2026-04-21
last_updated: 2026-04-21
tags: [product, memory, retrieval, architecture]
---

# TA-Mem

Yuan et al.（Independent + WashU + NYU + Northeastern, 2026-03-10, arxiv 2603.09297）。核心主張：**靜態 top-k 相似度搜尋是記憶系統的瓶頸，不是記憶結構本身**。讓 retrieval agent 根據問題類型自主選擇搜尋工具，比固定用 embedding 相似度搜尋更準確、更高效。

## Current Understanding

### 核心問題：One-Size-Fits-All Retrieval

現有系統幾乎都用同一種 retrieval 方式：把問題轉成向量，找最近的記憶段落（top-k embedding search）。這在三種問題類型上都可以，但沒有一種表現最好：
- **時序問題**（「上週我和誰見了面？」）→ 需要事件時間軸查詢
- **人物問題**（「Alice 的偏好是什麼？」）→ 需要人名索引，拉出所有跟 Alice 有關的資訊
- **開放式問題**（「關於旅遊計畫有什麼記憶？」）→ 需要語意相似度 + 事實查詢

### 三階段架構

**寫入：Episodic Memory Constructor**

在寫入時做結構化 annotation（不是 gating，不會擋任何記憶）：

- 語意分段（識別對話裡的 topic 轉換）
- 每段抽取一份 structured note，包含：Summary、Keywords、Persons、Facts per person、Events with timestamps、Semantic tag
- 最終存的是：原始對話段落 + structured note + 會話時間戳

關鍵選擇：**同時存原始 + annotation，不只存 annotation**。這讓 retrieval agent 在 annotation 找到後可以回查原始對話，避免 annotation 本身的 bias。

**儲存：Multi-Indexed Database**

多重索引：人名字串、語意 tag、關鍵字、事件/事實的 embedding。

暴露三種 query 工具：
- `Q_s(v)` — key-based 字串查（人名、tag、關鍵字）
- `Q_k(v, k)` — top-k 相似度查（事件或事實 embedding）
- `Q_p(v)` — 人物 profile 查（某人的所有事件或事實）

**讀取：Memory Retrieval Agent**

Agentic loop：收到問題 → 選工具 → 查記憶 → 判斷繼續或結束

- Memory cache：同一次 QA session 內，已拿到的 memory page 不重複拉
- 最多 7 次迭代，**平均 2.71 次**，97.73% 的問題 4 次內收斂
- 使用模型：GPT-4o-mini（不是 GPT-5），相對輕量

### 結果（LOCOMO benchmark）

| 問題類型 | TA-Mem 表現 |
|---------|------------|
| 時序 | F1 55.95（所有系統最高）|
| 多跳 | BLEU-1 最高 |
| 開放式 | BLEU-1 最高 |
| 單跳 | 接近最高 |

Token 效率：avg 3755 tokens/問題（競爭力，不因 loop 而暴增）

**工具使用分布**驗證 adaptive 的必要性：時序問題主要用 event query；開放式問題主要用 fact query — 問題類型決定工具選擇，不是固定分配。

### 與 APEX-MEM 的對比

| 維度 | TA-Mem | APEX-MEM |
|------|--------|---------|
| Write-time 處理 | 結構化 annotation（enrichment）| 原始存入（nothing）|
| Read-time 模型 | GPT-4o-mini（輕量）| GPT-5 / Claude 4.5 Sonnet |
| 解決的問題 | Retrieval completeness（有沒有找到對的工具）| Staleness resolution（哪條事實今天有效）|
| 多工具 | 3 種（string/similarity/person）| 4 種（graph/time-series/semantic/dialogue）|

兩個系統都做 multi-tool adaptive retrieval，但攻擊不同的失敗模式。TA-Mem 用 write-time enrichment 換取 read-time 的更多索引入口；APEX-MEM 用更強的 read-time 模型直接判斷時效性。

### Write-time Enrichment vs Write-time Gating 的區別

TA-Mem 的設計揭示了一個在 [[apex-mem]] 的 write/read governance 框架裡被忽略的維度：

- **Gating**（D-MEM, SSGM）= 決定是否寫入
- **Enrichment**（TA-Mem）= 決定用什麼格式寫入

兩個操作的時間點相同，影響完全不同。Gating 可能丟失後來有用的資訊；enrichment 保留所有資訊但增加 write-time 成本。

## Key Sources

- **2026-03-10** — Yuan et al.: TA-Mem: Tool-Augmented Autonomous Memory Retrieval for LLM in Long-Term Conversational QA. arxiv 2603.09297. Source: [[raw/yuan-ta-mem-tool-augmented-retrieval]]

## Related

[[apex-mem]] [[memr3]] [[stitch]] [[locomo]] [[xmemory]] [[a-mem]] [[mem0]] [[memory-failure-modes]]
