---
aliases: [M-star, M★, every task its own memory, memory program evolution]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [product, memory, architecture, benchmark]
---

# M★

arxiv 2604.11811（Wenbo Pan et al., 2026-04-10）。核心主張：**每個任務需要自己的 memory harness** —— 不是在幾個固定結構中選（如 [[fluxmem]]），而是**用程式進化自動發現**最佳 memory 架構。

## Current Understanding

### Memory = executable Python program

M★ 把 agent memory 建模為一個 Python program，包含三個共同進化的組件：

| 組件 | 內容 | 類比 |
|---|---|---|
| **Schema** | Python dataclass — 定義存什麼（typed fields） | DB schema |
| **Logic** | 後端操作 — embedding、SQL、LLM calls、儲存/檢索 | 業務邏輯 |
| **Instructions** | Prompt constants — 指導 agent 如何提取、查詢、回應 | System prompt |

工具白名單：SQLite / ChromaDB / LLM endpoints。

### Reflective Code Evolution

進化方法是 **population-based search + reflective mutation**：

1. **初始化**：3 個結構性不同的 seed programs
2. **選擇**：softmax temperature sampling（T=0.15），高分 program 更容易被選中
3. **變異**：LLM 分析執行軌跡 + 失敗案例 → 生成 targeted code patches
4. **品質閘門**：白名單檢查 / 編譯 / smoke test / 效能限制（3000 char output、2 min timeout）
5. **驗證**：rotating validation set（改進信號）+ static set（跨迭代可比）

### 核心發現：不同任務進化出完全不同的 memory 架構

這是 M★ 最重要的結果。transferred programs 幾乎都比 baseline seeds 差 → **memory structure must be co-optimized with the target task**。

| Domain | 進化出的架構 | Lines | 特點 |
|---|---|---|---|
| ALFWorld（embodied） | 確定性 action cache | 97 | SQLite only，**沒有 vector retrieval**，keyword scoring + exact-match bonus |
| LoCoMo（對話） | Hybrid SQLite + ChromaDB | 290 | 7 metadata fields，source diversity（max 2 chunks/dialogue），person-focused boosting |
| HealthBench（醫療） | SQLite-centric + LLM read | — | 6-21 schema fields |
| PRBench（專業推理） | SQLite-centric + LLM read | — | 法律/金融各自不同 |

ALFWorld 進化出的架構完全不用 vector search —— 它發現 embodied planning 不需要語意相似度，直接用 canonical state normalization + keyword match 就夠了。這跟 [[memwright]] 的「zero LLM in retrieval」殊途同歸，但 M★ 是讓系統自己發現這一點的。

### Benchmark 結果

| Benchmark | M★ | Best Baseline | Δ |
|---|---|---|---|
| LoCoMo F1 | 0.459 | Mem0: 0.373 | +23% |
| LoCoMo LLM-Judge | 0.610 | Mem0: 0.540 | +13% |
| ALFWorld Unseen | 0.881 | GEPA: 0.857 | +2.8% |
| HealthBench Data | 0.390 | GEPA+VS: 0.327 | +19% |
| PRBench Legal | 0.660 | GEPA: 0.568 | +16% |
| PRBench Finance | 0.586 | GEPA: 0.449 | +30% |

7/8 configurations 最佳。唯一輸的是 ALFWorld Seen（0.700 vs 0.820），但 Unseen 贏，暗示 seen 上 baseline 可能 overfit。

### Ablation：code evolution 是主要驅動力

| 移除什麼 | LoCoMo F1 | 下降 |
|---|---|---|
| 完整 M★ | 0.459 | — |
| 移除 code evolution | 0.256 | −44% |
| 移除 instruction optimization | 0.353 | −23% |

**Code structure（schema + logic）是主要驅動力，instruction 是 amplifier**。這跟 [[meta-harness]] 的發現呼應：harness 結構本身比 prompt tuning 更重要。

### 進化動態

三階段 pattern：
1. **早期**：修正 seed programs 的結構問題
2. **中期**：最大增益 — 發現 task-relevant indexing/retrieval
3. **晚期**：精煉，收益遞減

穩定性：5 random seeds，CoV < 9%，14/15 seeds 贏 strongest baseline → 不是偶然。

## 與 FLUXMEM 的比較

| | [[fluxmem]] | M★ |
|---|---|---|
| 結構選擇 | 三選一（linear/graph/hierarchical） | 從零進化（無預定結構） |
| 搜尋空間 | 3 個固定選項 | 無限（executable program space） |
| 決策方式 | Feature-based routing | Population-based evolutionary search |
| 成本 | 低（inference-time routing） | 高（offline evolution，多次 LLM calls） |
| 適用場景 | 即時切換（conversation 中） | 離線最佳化（部署前） |

FLUXMEM 是 runtime routing，M★ 是 compile-time optimization。兩者互補：先用 M★ 為每個 domain 進化最佳結構，再用 FLUXMEM 在 domain 內根據 conversation feature 微調。

## For Agent Memory Research

- **memory 不是一個 architecture，是一個 search problem**：固定 memory 架構的時代可能正在結束。M★ 證明讓 LLM 自己搜尋 memory 結構可以 consistently 贏人類設計
- **跟 [[self-improving-agent]] / [[asg-si]] 的連結**：M★ 把 memory system 當成一個可以被外化、版本控制、測試的 artifact（Python program），而不是 weights 裡的東西。這是 skill-based self-improvement 的另一個實例
- **跟 [[meta-harness]] 的連結**：Stanford meta-harness 在 harness 層做自動最佳化（6x 差異），M★ 在 memory 層做。兩者都用 population-based search
- **對 openab-bot 的意義**：我們的 memory 是手工設計的 markdown files + grep/git。M★ 暗示即使是這種簡單結構，也可能不是所有 task 的最佳選擇 — 不同 task（研究 vs 日報 vs Discord 互動）可能需要不同的 memory representation

## Key Sources

- **2026-04-10** — M★: Every Task Deserves Its Own Memory Harness, arxiv 2604.11811. Source: [[raw/pan-mstar-memory-harness]]

## Related

[[fluxmem]] [[meta-harness]] [[self-improving-agent]] [[asg-si]] [[locomo]] [[mem0]] [[memwright]] [[agent-memory]] [[memory-evaluation]]
