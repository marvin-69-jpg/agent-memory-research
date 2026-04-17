---
aliases: [neuroscience memory, 神經科學記憶, cognitive memory, brain-inspired memory]
first_seen: 2026-04-15
last_updated: 2026-04-17
tags: [memory, architecture]
---

# Neuroscience Memory

認知神經科學中的記憶機制，以及如何啟發 agent memory 設計。從生物學原理到 AI 實作的對照。

## Current Understanding

### Brain ↔ Agent Memory 對照

| Brain 機制 | 功能 | Agent 對應 | 啟示 |
|---|---|---|---|
| **海馬體 + 新皮質** | 海馬體索引 + 新皮質儲存 | Memory bank + context window | 分離索引和儲存 |
| **Hippocampal replay** | 睡眠時重播記憶做 consolidation | [[sleep-time-compute]] | dream cycle 有生物學基礎 |
| **Reconsolidation** | 檢索會修改記憶本身 | [[compiled-truth-pattern]] rewrite | retrieval 不應是 read-only |
| **Prediction error** | 只在預期不符時更新 | Selective update（ADD/UPDATE/DELETE/NOOP）、[[d-mem]] dopamine RPE gating | 不是所有 input 都該更新記憶 |
| **Cognitive maps** | 抽象地圖組織知識和經驗 | [[graph-memory]] | 記憶 = 圖結構，不是線性列表 |
| **Episodic ↔ Semantic** | 個人經歷 vs 去情境化知識 | Inside-trail vs Cross-trail memory | 兩種記憶有不同管理策略 |

### Spreading Activation（擴散激活）

Collins & Loftus (1975) 的理論：人類記憶檢索不是搜尋，是圖上的 energy propagation。

**SYNAPSE 的實作**（arxiv 2601.02744）把這個理論落地：
1. 收到 query → BM25 + dense retrieval 找 anchor nodes
2. Activation 沿圖邊傳播（temporal edges 有 time decay，semantic edges 有 cosine weight）
3. **Fan effect**（Anderson 1983）：出度越大 activation 越 dilute → 防 hub 壟斷
4. **Lateral inhibition**：高激活抑制低激活 → 注意力選擇
5. 3 輪迭代收斂 → Top-k 檢索

結果：LoCoMo F1 40.5（SOTA），multi-hop +8.7，95% token reduction，11x cost reduction

**對 open question #7（Causally Grounded Retrieval）的意義**：spreading activation 通過結構傳播而非 semantic similarity 做檢索，是目前最接近 causal retrieval 的方法。

### Dopamine / Reward Prediction Error（VTA gating）

Ventral Tegmental Area 的 dopamine 神經元在 prediction error 高時釋放 dopamine，觸發海馬體選擇性 consolidation。低 prediction error 的 routine input 不被 consolidate —— 這是腦的「節能」機制。

**[[d-mem]] 的實作**（arxiv 2603.14597）：
- Surprise = max cosine distance vs existing memory（z-score normalize + sigmoid，無 LLM 成本）
- Utility = lightweight LLM 分類 transient/short-term/persistent
- 三層 router：SKIP（bypass）/ CONSTRUCT_ONLY（STM）/ FULL_EVOLUTION（graph 重組）
- 結果：80% token reduction vs [[a-mem]]，multi-hop F1 還更高

**對 [[reconsolidation]] 的意義**：A-Mem 的 uniform 更新 vs D-Mem 的 selective 更新，後者更接近真實大腦運作 —— prediction error 是 gate，不是所有經驗都該重塑既有記憶。

### Ebbinghaus Forgetting Curve（遺忘曲線）

記憶強度隨時間 exponentially decay，除非被主動強化。

**在 agent memory 中的應用**：
- SYNAPSE：temporal edges 用 exponential decay（ρ=0.01）。Ablation 移除 decay → temporal F1 從 50.1 → 14.2
- 對 [[memory-staleness]] 的啟示：staleness 不是 bug，是 feature — 遺忘是正常的認知機制，問題是如何 selective forgetting

### Reconsolidation（記憶再鞏固）

每次檢索記憶都會重新寫入（reconsolidation），記憶是 mutable 的。

**對 agent memory 的啟示**：
- 目前大多數系統的 retrieval 是 read-only
- [[compiled-truth-pattern]] 的 rewrite 機制最接近 reconsolidation
- [[a-mem]] 的 **Memory Evolution** 是最直接的實現：新記憶寫入時自動更新鄰近舊記憶的 context/keywords/tags（write-triggered reconsolidation）
- [[ssgm]] 提供 reconsolidation 的 **safety wrapper**：Write Validation Gate 防止 semantic drift，Dual Storage 保留 audit trail
- 理想的做法：每次 retrieve 後都更新記憶的 metadata（access count、freshness、confidence）
- 詳見 [[reconsolidation]]

### Memory Security（記憶安全）

AI Meets Brain survey 首次系統化分類：
- **攻擊**：Extraction-based（隱私洩漏）、Poisoning-based（注入惡意資料、植入後門）
- **防禦**：Retrieval-based（異常偵測）、Response-based（多 agent review）、Privacy-based（隔離私有記憶、匿名化）

這是 agent memory 領域的新興議題，大多數現有系統完全不考慮安全。

### 記憶分類的 Scope-based 維度

AI Meets Brain survey 提出的雙維度分類：
- **Nature-based**：Episodic（what happened）vs Semantic（what is known）
- **Scope-based**：Inside-trail（單次軌跡，transient）vs Cross-trail（跨軌跡，persistent，generalizable）

Scope-based 維度補充了我們現有的 [[multi-scope-memory]]（user/agent/session/org）—— Inside-trail ≈ session scope，Cross-trail ≈ user/agent/org scope。

## Key Sources

- **2025-12-29** — AI Meets Brain: 跨學科 survey，400+ 引用，neuroscience ↔ agent memory 完整對照。Source: [[raw/ai-meets-brain-memory-survey]]
- **2026-01-06** — SYNAPSE: Spreading activation + episodic-semantic graph，LoCoMo SOTA。Source: [[raw/synapse-spreading-activation-memory]]
- **2026-03-15** — D-MEM: Dopamine-gated agentic memory via Reward Prediction Error。Source: [[raw/song-d-mem]]

## Related

[[agent-memory]] [[graph-memory]] [[memory-staleness]] [[sleep-time-compute]] [[compiled-truth-pattern]] [[hybrid-search]] [[mem0]] [[multi-scope-memory]] [[memory-evaluation]] [[memory-failure-modes]] [[locomo]] [[agemem]] [[entity-detection]] [[open-questions]] [[synapse]] [[reconsolidation]] [[a-mem]] [[ssgm]] [[d-mem]] [[gam]]
