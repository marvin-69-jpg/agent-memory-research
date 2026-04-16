---
date: 2026-04-17
topic: A-Mem 的 follow-up — Dopamine Gating 與 Adaptive Structure
gap_type: single-source
sources_found: 2
wiki_pages_updated: 6
wiki_pages_created: 2
---

# Daily Research: A-Mem 的兩個 follow-up

## 研究動機

[[a-mem]] 是現在 wiki 裡最重要的 reconsolidation 來源（write-triggered evolution）。但只有 1 個 source（原始論文），這對「reconsolidation 是 openab-bot 正在實作的方向」來說太單薄。`wiki gaps` 把 A-Mem 排在 single-source 第一。

預期能找到的：A-Mem 之後的 follow-up，無論是 critique、improvement 還是 alternative framing。實際發現比預期豐富 —— 兩篇 paper 從正交方向同時挑戰 A-Mem 的核心假設。

## 發現

### 1. D-Mem (UCSD/CMU, Mar 2026, arxiv 2603.14597) — A-Mem 太貴

D-Mem 直接攻擊 [[a-mem]] 的「append-and-evolve-all」設計：每個 utterance 都跑完整 evolution → write-latency O(N²)，token cost unbounded，filler 污染 graph。

**解法：bio-inspired RPE gating**。Ventral Tegmental Area 的 dopamine 只在 prediction error 高時觸發 consolidation —— D-Mem 把這個 motif 搬進 agent memory。

公式：`RPE = min(1, I(Utility ≥ τ) · [Utility × (Surprise + β)])`
- Surprise = embedding cosine distance（z-score normalize，**無 LLM 成本**）
- Utility = lightweight LLM call 分 transient/short-term/persistent 三類

三層 router：
- **SKIP** (RPE<0.3)：bypass，存 Shadow Buffer 當 adversarial fallback
- **CONSTRUCT_ONLY** (0.3-0.7)：建 atomic note 進 STM，不做 graph evolution
- **FULL_EVOLUTION** (≥0.7)：完整 A-Mem pipeline

LoCoMo-Noise 結果（D-Mem 順手提的新 benchmark，注入 75% phatic/status/tangent noise）：A-Mem 燒 1.64M tokens，D-Mem 用 319K（−80%），multi-hop F1 還更高（0.412 vs 0.365）。

**Trade-off**：無 noise 時 D-Mem single-hop 反而落後 A-Mem（21.6% vs 44.7%），因為 single-hop 的 target 通常是低 utility 事實，被 SKIP 掉。論文承認這是 principled efficiency decision。

### 2. FLUXMEM (UTS/Melbourne/UT Austin/UCLA, Feb 2026, arxiv 2602.14038) — A-Mem 的結構不該預設

FLUXMEM 質疑的不是 A-Mem 的成本，而是更上游的「single-structure 假設」：Mem0 用 flat、A-Mem 用 graph、MemoryOS 用 OS-inspired，都假設一種 structure 通吃所有 conversation pattern。

**解法**：把 structure 選擇升級成 learnable variable。Shallow MLP 根據 conversation feature（互動規模、時序密度、實體密度、topic 多樣性）動態挑：
- **Linear** for 時序強的內容
- **Graph** for 實體關係多的內容
- **Hierarchical** for topic 多層、需要 abstraction

PERSONAMEM avg accuracy 72.43% 比第二名 +9.18%。Ablation 移除 graph → open category F1 掉 19% —— 三種結構不可互相替代。

附帶創新：**Beta-Mixture-Gated Memory Fusion**。替代 fixed similarity threshold，用 BMM 兩成分（高/低 compatibility）+ EM + posterior probability 當 soft gate。τ_BMM=0.5 性能最佳，太高 over-restrictive 太低引 noise。

## 與已有知識的連結

`wiki match` 確認的相關 page：
- [[a-mem]]：兩篇都直接針對它，wiki page 加了「Critique: O(N²) Scaling Problem」和「Meta-Critique: Single-Structure Assumption」兩節
- [[reconsolidation]]：D-Mem 把 reconsolidation 從 uniform 改成 selective，新增「Selective vs Uniform Reconsolidation」節
- [[neuroscience-memory]]：D-Mem 引入 dopamine RPE 這個新生物學 motif，加 brain↔agent 對照表 + 新節
- [[locomo]]：D-Mem 順手提出 LoCoMo-Noise extension，把 token efficiency 從 nice-to-have 升級成必要 metric
- [[ssgm]]：跟 D-Mem 互補（safety governance vs efficiency gating）
- [[mem0]] [[graph-memory]] [[multi-scope-memory]] [[mece-resolver]]：FLUXMEM 的 structure routing 跟這些都有對話空間

## Open Questions 推進

**Q3 (Compounding vs Forgetting)**：D-Mem 提供具體 selective approach。原本只有 Mem0 selective pipeline、AgeMem RL、Autoreason isolation 三種策略，現在多了 lightweight bio-inspired heuristic 這條。重要的是 D-Mem 的成本結構（embedding-only Surprise + minimal LLM Utility）證明 selective forgetting 不需要昂貴的 RL 訓練。

**新 Q15 (Memory Structure Selection)**：FLUXMEM 開了一個之前沒有的問題 —— structure 本身該不該預設？這之前在 wiki 沒有獨立位置，現在進 Tier 3。

## 對 openab-bot 的啟示

1. **D-Mem 的 RPE gating 對我們的 reconsolidation 成本有直接意涵**：目前 `memory.py reconsolidate` 是 manual triggered（每次 brain-first lookup 後判斷）。要不要學 D-Mem 加 gate 自動 SKIP 低 utility 的 recall？但 openab-bot 的訊息已經 pre-filtered（使用者明確要做事），phatic filler 比例低，gating 收益可能小於 D-Mem 在 LoCoMo-Noise 上的展示。需要先做小規模測試確認。

2. **FLUXMEM 的多結構 routing 對我們可能 overkill**：我們 system 已經有 multi-structure（auto-memory flat / boba-wiki hierarchical / git linear），但 routing 是 LLM 自己在做（讀 MEMORY.md 判斷查哪），不需要 MLP。FLUXMEM 啟示更像是「不要鎖死一種結構」這個 design principle，而非具體實作。

## 下一步

未來可以深入的方向：
- **D-Mem 的 LoCoMo-Noise 跑 openab-bot 自己的 memory 系統**：把 phatic noise 注入 Discord conversation，看我們的 memory 在多大 noise ratio 下會退化
- **A-Mem 系列的 第三條路**：D-Mem 改 timing（when to evolve），FLUXMEM 改 structure（how to organize），有沒有 paper 改 granularity（what to evolve into）？
- **Reconsolidation cost benchmark**：Pengfei Du survey 提到 cost 是 metric stack 的一層，但目前沒 paper 系統比較不同 reconsolidation strategy 的 cost-quality trade-off
