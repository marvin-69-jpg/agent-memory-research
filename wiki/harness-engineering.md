---
aliases: [harness engineering, agent harness engineering, 套具工程]
first_seen: 2026-04-13
last_updated: 2026-04-16
tags: [harness, architecture, context]
---

# Harness Engineering

在既有 agent 的 integration points 上做工程 — 不是設計 agent 本身，是設計你怎麼「駕馭」它。Context engineering 的上層概念。

## Current Understanding

- **定義**（dex）：Context engineering = 怎麼把 context 傳給 LLM。Harness engineering = 怎麼 engineer 一個 agent 的 **integration points** 來得到最好結果
- **三層架構**：
  1. LLM intuition → 理解模型能力
  2. Context engineering → 設計 prompt、memory、context window
  3. Harness engineering → 設計 hooks、skills、agents、MCPs 等 integration points
- **以 Claude Code 為例**（dex）：commands、hooks、skills、agents、MCPs 都是 harness 的 integration points。使用者透過 engineer 這些 integration points 來擴展 agent 能力
- **Philipp Schmid（HuggingFace, 144K views）**：
  - 2025 = agents 的開始，2026 = Agent Harnesses 的年代
  - Harness ≠ agent。Harness 在 agent frameworks 之上運作
  - Harness 提供：prompt presets、opinionated tool call handling（HitL）、lifecycle hooks、planning、filesystem access、sub-agent management
  - 三個價值：(1) 驗證 real-world progress (2) 釋放 model potential (3) hill climbing via feedback loop
  - 新瓶頸：**context durability**。Harness 是解 model drift 的主要工具
- **Natural-Language Agent Harnesses（NLAH, Pan et al.）**：
  - 把 harness 邏輯從 code 外部化成 **editable natural-language artifacts**
  - Contracts、roles、stages、state semantics — 全部寫成文字，由 shared runtime（IHR）執行
  - OSWorld benchmark：NLAH 47.2% vs code harness 30.4%
  - NL harness 可 ablate、可 migrate（1-2 週跨 task）、可 compare
  - 核心主張：**scale harnesses, not models**
- **與我們的做法的對比**：openab-bot 的 CLAUDE.md + hooks + skills 就是 harness engineering。我們做的 behavior benchmark 也是在測 harness 的效果（88% → 100%）。我們的 enforcement spectrum（rules → hard rules → hooks）就是 harness engineering 的實踐
- **[[meta-harness]]（Stanford IRIS Lab, 2026）**：把 harness engineering **自動化** — 用 coding agent（Claude Code + Opus 4.6）作為 proposer，自動搜尋最佳 harness 設計。同一模型 6x 性能差異來自 harness。在 TerminalBench-2 超越手工 harness（76.4% vs 74.7%），text classification 用 4x fewer tokens 且+7.7 accuracy。核心發現：full execution traces（10M tokens）比 lossy summary 好 15+ 點 — **causal reasoning 需要 raw data**

## Key Sources

- **2026-03-28** — Stanford IRIS Lab: Meta-Harness，automated end-to-end harness optimization（arxiv 2603.28052）。Source: [[raw/stanford-meta-harness]]
- **2025-11-04** — dex 定義 harness engineering 概念（48.1K views）。Source: [[raw/dex-harness-engineering]]
- **2026-01-05** — Philipp Schmid: 2026 = Agent Harnesses 年代（144K views）。Source: [[raw/philipp-schmid-2026-agent-harnesses]]
- **2026-04-10** — Carlos Perez 整理 NLAH 論文（Pan et al.）。Source: [[raw/carlos-perez-natural-language-agent-harnesses]]

## Related

[[agent-harness]] [[context-engineering]] [[context-fragment]] [[thin-harness-fat-skills]] [[scaffolding-lifecycle]] [[aaron-levie]] [[philipp-schmid]] [[meta-harness]] [[context-rot]] [[mece-resolver]]
