---
aliases: [reconsolidation, 記憶再鞏固, memory reconsolidation, retrieval-triggered update]
first_seen: 2026-04-15
last_updated: 2026-04-17
tags: [memory, architecture]
---

# Reconsolidation

記憶在被檢索時會被重新寫入（reconsolidate），而非單純被讀取。源自認知神經科學，對 agent memory 設計有深遠影響：**retrieval 不應是 read-only operation**。

## Current Understanding

### 神經科學基礎

每次回想一段記憶，大腦會：
1. 從長期儲存中提取記憶（destabilize）
2. 在工作記憶中重新處理（可能被修改）
3. 重新存回長期儲存（reconsolidate）

這意味著記憶是 **mutable by design** — 不是 bug，是生物演化出來的 feature。每次 recall 都是一次更新的機會。

### Agent Memory 中的實現光譜

| 系統 | Reconsolidation 方式 | 觸發時機 | 程度 |
|------|---------------------|---------|------|
| 大多數系統 | ❌ 完全 read-only | — | 無 |
| [[compiled-truth-pattern]] | Manual rewrite | 新資訊進入時人工觸發 | 中（依賴觸發） |
| [[a-mem]] | **Memory Evolution** | 新記憶寫入時自動更新鄰近舊記憶 | 高（write-triggered） |
| [[sleep-time-compute]] | Batch improvement | Session 閒置時批量改善 | 中（delayed） |
| 理想的 reconsolidation | Auto-update on retrieve | 每次檢索都觸發 | 最高（read-triggered） |

### A-Mem: Write-Triggered Reconsolidation

[[a-mem]]（arxiv 2502.12110）是目前最直接的實現：

- 新記憶加入 → 找 top-k nearest neighbors → **更新舊記憶的 context/keywords/tags**
- Zettelkasten 啟發：每條記憶是 atomic note，有 keywords、tags、contextual description、links
- Link Generation：新 note 自動與最近鄰形成 bidirectional links
- LoCoMo Multi-hop ROUGE-L: 44.27 vs baseline 18.09（+144%）

差異：A-Mem 是 **write-triggered**（新記憶觸發），神經科學是 **read-triggered**（檢索觸發）。但核心精神一致 — 記憶是活的，不是死的。

### SSGM: Reconsolidation 的 Safety Wrapper

[[ssgm]]（arxiv 2603.11768）解決了 reconsolidation 的安全問題：如果記憶可以被自動修改，怎麼防止失控？

- **Write Validation Gate**：reconsolidate 前先檢查是否與 protected core facts 衝突
- **Dual Storage**：Mutable Active Graph（可 reconsolidate）+ Immutable Episodic Log（audit trail）
- **Drift bound**：每 N 步 reconciliation → semantic drift ≤ O(N·ε_step)

Dual storage 與 [[compiled-truth-pattern]] 高度呼應：
- Mutable Active Graph ≈ compiled truth
- Immutable Episodic Log ≈ timeline

### 與其他概念的關係

- **[[memory-staleness]]**：reconsolidation 是 staleness 的解法之一 — 記憶被頻繁 retrieve 且每次都有機會被更新，就不容易過時
- **[[memory-failure-modes]]**：reconsolidation 本身可能引入新的 failure mode（semantic drift、over-modification）→ SSGM 的 governance 是必要的
- **[[compounding-memory]]**：reconsolidation 讓記憶 compound 的方式從「累積新記憶」變成「既有記憶越用越精確」

### Selective vs Uniform Reconsolidation

[[a-mem]] 的 evolution 是 **uniform write-triggered** —— 每個新記憶都觸發鄰居更新。但 [[d-mem]]（arxiv 2603.14597）證明這太昂貴而且不必要：在 LoCoMo-Noise 上 A-Mem 燒 1.64M tokens，D-Mem 用 dopamine RPE gating 只在 high-surprise + high-utility 時觸發 evolution，−80% tokens 還更準。

對應到神經科學：人腦的 dopamine 也不是每次經驗都觸發 consolidation —— 只有 prediction error 高時才觸發。A-Mem 缺了這個 gate，D-Mem 補上。

**對 openab-bot 的啟示**：目前 `memory.py reconsolidate` 是 manual triggered（每次 brain-first lookup 後判斷）。要不要學 D-Mem 加 RPE-style gate 自動 SKIP 低 utility 的 recall？但我們的「對話」結構跟 LoCoMo 不同 —— openab-bot 收到的訊息已經 pre-filtered（使用者明確要做事），phatic filler 比例低，gating 收益可能小。

### 未解問題

1. **Read-triggered reconsolidation**：目前沒有系統在每次 retrieve 時自動 reconsolidate。A-Mem 是 write-triggered（間接的）
2. **Reconsolidation vs forgetting**：reconsolidate 可能反而 reinforce 該被遺忘的記憶。需要 selective reconsolidation。**[[d-mem]] 的 SKIP tier 是一個解 —— 直接不存進長期記憶**。
3. **Reconsolidation 的成本**：每次 retrieve 都觸發 LLM call 來判斷是否需要更新？太昂貴。需要輕量級 heuristic 先篩選。**D-Mem 的 Surprise（embedding-based, no LLM）+ Utility（minimal LLM call）二元分解是可借鏡的成本結構**。

## Implementation

### openab-bot Reconsolidation（2026-04-16）

**已實作**：`memory.py reconsolidate <files>` — 對 recalled memories 做輕量 staleness 檢查（age、description-body drift、thin content、missing structure）。

**規則變更**：Brain-First Lookup 規則新增 reconsolidation 步驟 — recall 完記憶後，判斷是否需要更新。不是每次都更新，只在有 evidence 時才改。

**保護機制**（受 [[ssgm]] 啟發）：不改核心事實（使用者身份、明確規則），只改可能過時的描述和 context。

**觀察（2026-04-22）**：
- **觸發頻率**：低。主要路徑是 session 開頭的 `memory improve` batch；session 中的 brain-first recall 後手動 reconsolidate 幾乎不執行。
- **stale 捕捉**：`memory improve` 的 REVIEW 項目（>14 天的 project 記憶）能捕捉到顯性過時。但 recalled memories 在對話中被動發現「描述跟現實不符」時的即時更新仍依賴人工判斷，沒有自動觸發。
- **read-triggered 升級**：尚未實作。升級路徑是：每次 `memory recall` 完自動 call `reconsolidate <recalled_files>`。成本可接受（只掃被 recall 的少量檔案），但目前還沒有足夠的 stale-miss 案例推動這個改動。
- **現狀評估**：write-triggered（session 開頭 batch）目前已足夠，主要 stale 問題能被 REVIEW 攔截。只有在 brain-first lookup 使用率變高後，read-triggered 才有明顯的 ROI。

## Key Sources

- **2025-02-17** — A-Mem: Zettelkasten-inspired memory evolution，write-triggered reconsolidation。Source: [[raw/a-mem-agentic-memory]]
- **2026-03-14** — SSGM: Governance framework for evolving memory。Source: [[raw/ssgm-stability-safety-governed-memory]]
- **2025-12-29** — AI Meets Brain survey: reconsolidation 的神經科學基礎。Source: [[raw/ai-meets-brain-memory-survey]]
- **2026-03-15** — D-MEM: Selective evolution via dopamine RPE gating，解 A-Mem 的 O(N²) 成本問題。Source: [[raw/song-d-mem]]

## Related

[[neuroscience-memory]] [[compiled-truth-pattern]] [[memory-staleness]] [[memory-failure-modes]] [[a-mem]] [[ssgm]] [[sleep-time-compute]] [[compounding-memory]] [[agent-memory]] [[agemem]] [[graph-memory]] [[open-questions]] [[session-management]] [[d-mem]] [[memory-worth]] [[gam]] [[apex-mem]]
