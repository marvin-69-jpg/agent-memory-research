---
aliases: [MemU, memU, filesystem memory framework]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [product, memory, infrastructure]
---

# MemU

NevaMind-AI 開發的開源 agent memory framework（GitHub: NevaMind-AI/memU）。核心主張：**memory 像 filesystem — structured, hierarchical, instantly accessible**。用 Markdown 檔案存記憶，agent 自己決定記什麼。

## Current Understanding

### 三層架構

| Layer | 內容 | Filesystem 比喻 |
|---|---|---|
| **Resource** | 原始資料（對話、文件、圖片、音訊） | Mount points |
| **Item** | 提取的記憶單元 — 具體事實 | Files |
| **Category** | 自動組織的主題分組 | Folders |

Resource → Item → Category 的流程就是 [[compiled-truth-pattern]] 的三步實作：raw 保留 → facts 提取 → 主題整理。跟 [[enrichment-pipeline]] 的 tier 設計呼應。

### Dual-Mode Retrieval

兩種檢索模式：
- **RAG**（embedding-based）：毫秒級，持續監控用
- **LLM**（deep reasoning）：秒級，做 intent prediction 和 query evolution

跟 [[memwright]] 的「zero LLM in retrieval」完全相反 — MemU 把 LLM retrieval 當 feature。但兩者不矛盾：MemU 讓你選（RAG for speed, LLM for depth），Memwright 則認為 determinism 比 depth 重要。

### Multimodal 原生支持

```python
memorize(modality="conversation" | "document" | "image" | "video" | "audio")
```

自動跨模態 cross-reference。跟 [[multimodal-memory]] / [[mirix]] 的問題域相同，但 MemU 把多模態做成 API 層級的一等公民而非另加模組。

### Benchmark

LoCoMo：**92.09%** average accuracy。

| System | LoCoMo |
|---|---|
| **MemU** | **92.09%** |
| MemMachine | 84.9% |
| [[memwright]] | 81.2% |
| [[letta]] | 74% |
| [[mem0]] | 66.9% |
| OpenAI memory | 52.9% |

⚠️ 注意：不同系統在 LoCoMo 上用的 metric 可能不同（F1 vs accuracy vs ROUGE），直接比較要小心。MemU 用的是 accuracy，[[gam]] 用的是 F1。

### 為什麼 filesystem 路線有效

MemU 證明了 [[filesystem-vs-database]] 辯論中 filesystem 路線的可行性。原因可能是：
- Markdown 檔案 **LLM 直接看得懂** — 不需要 deserialize 或 format conversion
- 階層結構（folder/file）天然對應 category/fact — 不需要額外的 schema
- Git-friendly — 每次變更都有 history
- 人也看得懂 — debugging 不需要 DB client

這跟 [[coding-agent-memory]] 中 Claude Code 的 CLAUDE.md / memory 系統用一樣的設計哲學。

### Proactive Agent 設計

MemU 專為 **24/7 proactive agents** 設計：
- Background monitoring 不需要持續 LLM invocation
- Cache insights，避免 redundant LLM calls
- Auto-categorization — 記憶自動組織，不需手動 tagging
- Scoped retrieval via `where` — 支持多用戶/多 agent

## For Agent Memory Research

- **我們自己（openab-bot）就在用類似架構**：markdown files + grep + git history。MemU 的 LoCoMo 92.09% 某種程度上驗證了這條路線可行
- **三層對應我們的結構**：Resource ≈ raw/、Item ≈ wiki 裡的 facts、Category ≈ wiki pages（主題分組）
- **Dual retrieval 值得考慮**：我們目前只有 grep（相當於 keyword search），沒有 embedding search。MemU 證明兩者混用效果最好

## Key Sources

- **2026-01-05** — Sumanth (@Sumanth_077) X thread, 73.8K views. GitHub: NevaMind-AI/memU. Source: [[raw/sumanth-memu]]

## Related

[[filesystem-vs-database]] [[compiled-truth-pattern]] [[enrichment-pipeline]] [[multimodal-memory]] [[mirix]] [[memwright]] [[coding-agent-memory]] [[locomo]] [[mem0]] [[agent-memory]] [[xmemory]]
