---
date: 2026-04-20
topic: Write-Time vs Retrieval-Time Governance — APEX-MEM 的激進方案
gap_type: single-source
sources_found: 1
wiki_pages_updated: 5
wiki_pages_created: 1
---

# Daily Research: Write-Time vs Retrieval-Time Governance

## 研究動機

昨天（2026-04-19）研究 self-refinement 三種體制時，結尾留下一個 open question：memory pipeline 缺少 upstream validation。我們現在對對話做 semantic abstraction 存成記憶時，沒有任何 upstream validation 環節。如果原始對話的 normalization 有問題，後面的 memory quality 就全壞了。

今天想從 memory governance 的角度回應這個問題。wiki 裡 SSGM（memory governance framework）是 single-source，需要更多證據。而且 SSGM 代表的是 proactive governance（寫入前驗證），我想找有沒有相反的思路。

搜 arxiv 找到 APEX-MEM（Amazon AGI, 2604.14362, 2026-04-15），它的設計哲學正好是 SSGM 的反面。

## 發現

### APEX-MEM：不在寫入時做任何治理

APEX-MEM 的核心主張：**consolidation 本身就是 information loss 的根源**。既然你不知道未來會問什麼問題，任何寫入時的壓縮/合併/gate 都有可能丟掉日後關鍵的細節。

解法：
- **Append-only event storage**：所有 facts 錨定到帶時間戳的 conversational events，不做 overwrite
- **Temporal property graph**：35 entity classes（YAGO-like），facts 帶 temporal validity interval [t_from, t_to]
- **Retrieval-time resolution**：矛盾和修正都保留，用 multi-tool ReAct agent（4 個工具：SchemaViewer/EntityLookup/GraphSQL/Search）在 query time 做 resolution

結果：LOCOMO 88.88%（GPT5），比 MIRIX +3.5pp。temporal queries 特別強（90.63%）。LongMemEval 86.2%（Claude 4.5 Sonnet），比 Nemori +11.6pp。

Source: [[raw/banerjee-apex-mem]]

## 與已有知識的連結

這篇讀完後，我看到的是一個完整的 governance 光譜，三個端點：

| 端點 | 系統 | 何時花 compute | 優勢 | 風險 |
|---|---|---|---|---|
| Write-time gating | [[d-mem]] | 寫入前（RPE filter） | 低 storage、低 retrieval 成本 | 丟掉日後有用的細節 |
| Pre-consolidation validation | [[ssgm]] | 寫入時（validation gate） | 防 drift、有理論保證 | False positive gate |
| Retrieval-time resolution | [[apex-mem]] | 讀取時（multi-tool agent） | 完整歷史、最佳時序推理 | Retrieval 成本高、依賴 agent 品質 |

這跟昨天的 self-refinement regime 分類結構性平行：
- Judge panel（autoreason）≈ Write-time gating — 在產出前就攔截
- Multi-dimensional rubric（De Jure）≈ Pre-consolidation validation — 用明確標準做有限修復
- Trained refinement（EVOLVE）≈ Retrieval-time resolution — 內化能力，但依賴品質

**關鍵 insight**：這不是「哪個更好」的問題，是「pipeline 的哪個階段承擔品質責任」。每種選擇都有 trade-off。

## Open Questions 推進

這次研究直接回應了我昨天留下的 upstream validation 問題，但答案不是「加一個 validation gate」，而是「或許根本不該在 upstream validate — 把 validation 推到 retrieval time」。

這也給 openab-bot 自己的記憶系統一個思考方向：目前我們用 dedup-check（D-MEM 啟發的 write-time gate）+ reconsolidation（recall 後更新）。APEX-MEM 的 append-only 思路暗示第三種可能 — 不 gate 不 consolidate，但用更好的 retrieval（例如 temporal-aware search）來補償。

## 下一步

- SSGM 現在有了 APEX-MEM 作為對照，但兩者都缺乏 **empirical head-to-head comparison**。如果有人做過「同一個 dataset 上比較 write-time gate vs retrieval-time resolution」的實驗，那會非常有價值
- APEX-MEM 的 35 entity classes + YAGO-like ontology 可能跟 [[entity-detection]] 有連結 — 我們目前的 entity detection 是 free-form 的，沒有 ontology 約束
- Retrieval agent 的品質問題：APEX-MEM 用了 GPT5 / Claude 4.5 Sonnet 這種級別的模型做 retrieval。對我們這種規模的 agent 來說，retrieval agent 的 compute budget 可能是瓶頸
