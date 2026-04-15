# Agent Memory Research — Log

> Append-only record of all wiki operations.

## [2026-04-15] ingest | Garry Tan — GBrain v0.10.0

- Source: raw/garry-tan-gbrain-v0.10.0.md (tweet, 16.8K views)
- Updated: gbrain.md (v0.10.0 details, multi-user ACLs), thin-harness-fat-skills.md (24 skills 實證, multi-user), garry-tan.md (v0.10.0 update)
- Key findings:
  - 24 fat skills with full e2e/eval/unit test coverage — fat skill 架構已穩定收斂
  - RESOLVER.md + SOUL.md "perfected" — resolver routing 機制成熟
  - Multi-user brain access via ACLs — brain 從個人工具擴展到團隊共用
  - 個人 OpenClaw setup 公開 — 降低其他人的 adoption barrier

## [2026-04-15] ingest | Nicholas — AI Agents Have No Memory for Failure (Helix)

- Source: raw/nicholas-helix-self-healing-agents.md (159K views, X long-form article)
- Created: helix.md, gene-map.md, nicholas-dapanji.md
- Updated: procedural-memory.md (Gene Map as error-specific procedural memory), experiential-memory.md (shared Gene Map = cross-agent experiential sharing), compounding-memory.md (Q-value RL compounding), memory-evaluation.md (Helix benchmark data)
- New cross-links: helix ↔ gene-map ↔ procedural-memory ↔ experiential-memory ↔ compounding-memory ↔ memory-evaluation
- Key findings:
  - Gene Map = procedural memory + RL ranking，首次 2,140ms → 再次 1.1ms（2,000×）
  - 目前看到最具體的 memory ROI 數據（50 場景，量化 LLM call / cost / latency）
  - Shared Gene Map 願景 = experiential memory 跨 agent 共享的工程實踐
  - Doctor vs Immune System 類比：routine failures 用 pattern match，novel failures 才用 LLM

## [2026-04-14] ingest | Phase 3 — 產業視角（ChatGPT Memory + Coding Agents）

- Source: raw/manthan-gupta-chatgpt-memory-reverse-engineered.md (ChatGPT 四層靜態注入逆向工程)
- Source: raw/coding-agents-memory-comparison.md (Cursor/Claude Code/Windsurf/Cline 架構比較，多來源綜合)
- Created: chatgpt-memory.md, coding-agent-memory.md
- Key findings:
  - ChatGPT 不用 RAG/vector DB，是 4 層靜態注入（speed over completeness）
  - 4 個 coding agent 全收斂在 file-based memory（驗證 filesystem camp）
  - 分歧在 who curates（user vs system）和 when retrieval（always vs on-demand vs auto-learned）
  - Enterprise: 62% 實驗 agents，只有 14% production-ready（McKinsey）
- Open questions research gap "Production cases 太少" → 已部分解決

## [2026-04-14] structure | Phase 2 — 概念地圖 + Open Questions

- Created: concept-map.md（三層架構：Infrastructure → Memory System → Retrieval & Evaluation，6 個跨層主題，7 products，10 people）
- Created: open-questions.md（12 個未解問題分三個 tier：Fundamental / Hard but Approachable / Emerging，加研究缺口表）
- Updated: index.md（加 Structure section 置頂）

## [2026-04-14] ingest | Phase 1 深化 — 3 篇高價值來源

Phase 1 計劃：補學術深度，降低 single-source pages。三個來源同時搜尋 + 讀取 + ingest：

- Source: raw/chrysb-long-term-memory-unsolved.md (262.1K views, 9 軸設計 + 10 failure modes)
- Source: raw/pengfei-du-memory-survey-2026.md (arxiv 2603.07670, 系統性 survey)
- Source: raw/yohei-nakajima-rise-of-ai-memory.md (24.6K views, 全景分析)
- Created: memory-failure-modes.md, memory-evaluation.md, chrysb.md, yohei-nakajima.md
- Updated: agent-memory.md (write-manage-read loop, 三維分類法, raw vs derived, evaluation paradox), memory-staleness.md (derivation drift, stale context dominance, forgetting propagation), memory-lock-in.md (memory as moat, Memory's Plaid), graph-memory.md (temporal KG, forgetting propagation), locomo.md (survey 定位, ACL 2024 原文), memory-arena.md (survey 定位, evaluation paradox), memgpt.md (evaluation link), agemem.md (survey: policy-learned management), letta.md (yohei 定位)
- Single-source pages 降幅：agent-memory 4→7, memory-staleness 1→3, graph-memory 1→3, locomo 1→2(+survey), memory-arena 1→2(+survey), agemem 1→2, letta 4→5

## [2026-04-14] ingest | SHL0MS — Autoreason (Nous Research)

- Source: raw/shl0ms-autoreason.md (208.6K views tweet + GitHub repo clone)
- Created: autoreason.md, shl0ms.md
- Updated: scaffolding-lifecycle.md (bloat/prune oscillation 呼應 + transition point), actor-aware-memory.md (memory isolation by design 反向策略), procedural-memory.md (emergent skill 實例), compounding-memory.md (遺忘作為 feature 的反例)
- New cross-links: autoreason ↔ scaffolding-lifecycle, autoreason ↔ actor-aware-memory, autoreason ↔ procedural-memory, autoreason ↔ compounding-memory, autoreason ↔ memory-staleness, autoreason ↔ thin-harness-fat-skills, shl0ms ↔ autoreason

## [2026-04-13] ingest | Twitter 搜尋 — 4 篇 harness 相關推文

自主搜尋 X/Twitter（WebSearch `site:x.com`），找到 4 篇 harness 方向的高互動推文，用 agent-browser 讀取後 ingest：

- Source: raw/philipp-schmid-2026-agent-harnesses.md (144K views)
- Source: raw/aaron-levie-unsentimental-architecture.md (109.7K views)
- Source: raw/carlos-perez-natural-language-agent-harnesses.md (NLAH paper discussion)
- Source: raw/dex-harness-engineering.md (harness engineering definition)
- Created: harness-engineering.md, scaffolding-lifecycle.md, philipp-schmid.md, aaron-levie.md
- Updated: agent-harness.md (2026 harness-as-discipline, NLAH, scaffolding lifecycle, 4 new sources), context-engineering.md (harness engineering link, context durability)
- New cross-links: harness-engineering ↔ agent-harness, harness-engineering ↔ context-engineering, scaffolding-lifecycle ↔ agent-harness, philipp-schmid ↔ agent-harness, aaron-levie ↔ scaffolding-lifecycle

## [2026-04-13] ingest | Twitter 搜尋 — 3 篇高互動推文

自主搜尋 X/Twitter（WebSearch `site:x.com`），找到 3 篇高互動推文，用 agent-browser 讀取後 ingest：

- Source: raw/leonie-filesystem-vs-database-debate.md (29.6K views)
- Source: raw/dair-ai-memory-benchmarks-misleading.md (37.8K views)
- Source: raw/elvis-agemem-unified-memory.md (56.4K views)
- Created: filesystem-vs-database.md, memory-arena.md, agemem.md, leonie.md
- Updated: (cross-links added to new pages)
- New cross-links: filesystem-vs-database ↔ agent-memory, memory-arena ↔ locomo, agemem ↔ mem0, leonie ↔ filesystem-vs-database

## [2026-04-13] ingest | State of AI Agent Memory 2026 (Mem0)

- Source: raw/mem0-state-of-ai-agent-memory-2026.md (via WebSearch + agent-browser)
- Created: mem0.md, locomo.md, graph-memory.md, procedural-memory.md, multi-scope-memory.md, memory-staleness.md, actor-aware-memory.md
- Updated: agent-memory.md (2026 升級為 first-class component, 三種記憶類型), memgpt.md (LOCOMO benchmark), hybrid-search.md (reranker + graph), compounding-memory.md (staleness + selective pipeline), memory-lock-in.md (MCP portability)
- New cross-links: mem0 ↔ all new pages, mem0 ↔ memgpt, mem0 ↔ agent-memory, graph-memory ↔ hybrid-search, memory-staleness ↔ compounding-memory, actor-aware-memory ↔ entity-detection, procedural-memory ↔ thin-harness-fat-skills
- Note: 第一篇由 bot 自主搜尋（WebSearch）發現並 ingest 的來源

## [2026-04-12] ingest | Your Harness, Your Memory

- Source: raw/harrison-chase-your-harness-your-memory.md
- Created: agent-harness.md, agent-memory.md, memory-lock-in.md, deep-agents.md, letta.md, harrison-chase.md, sarah-wooders.md, context-engineering.md
- Updated: (none — first ingest)
- New cross-links: agent-harness ↔ agent-memory, agent-memory ↔ memory-lock-in, agent-harness ↔ context-engineering, agent-memory ↔ letta, deep-agents ↔ harrison-chase, letta ↔ sarah-wooders

## [2026-04-12] ingest | GBrain (Garry Tan)

- Source: raw/garry-tan-gbrain.md
- Created: gbrain.md, garry-tan.md, compiled-truth-pattern.md, hybrid-search.md, compounding-memory.md
- Updated: agent-memory.md (三層記憶模型 + compiled truth pattern), agent-harness.md (thin harness fat skills)
- New cross-links: gbrain ↔ garry-tan, gbrain ↔ compiled-truth-pattern, gbrain ↔ hybrid-search, gbrain ↔ compounding-memory, gbrain ↔ agent-memory, gbrain ↔ agent-harness, compounding-memory ↔ harrison-chase, compounding-memory ↔ memory-lock-in

## [2026-04-12] ingest | GBrain Deep Dive (docs/)

- Source: raw/garry-tan-gbrain-deep.md (cloned repo, read docs/, skills/, ethos/)
- Created: thin-harness-fat-skills.md, brain-agent-loop.md, brain-first-lookup.md, entity-detection.md, enrichment-pipeline.md, mece-resolver.md
- Updated: gbrain.md (14,700+ files, full loop details), garry-tan.md (thin harness philosophy), context-engineering.md (resolver concept)
- New cross-links: thin-harness-fat-skills ↔ gbrain, brain-agent-loop ↔ compounding-memory, entity-detection ↔ brain-agent-loop, enrichment-pipeline ↔ entity-detection, mece-resolver ↔ compiled-truth-pattern, context-engineering ↔ garry-tan

## [2026-04-12] ingest | Sarah Wooders + MemGPT + Context Constitution

- Sources: raw/sarah-wooders-memory-isnt-a-plugin.md, raw/memgpt-paper.md, raw/letta-context-constitution.md
- Created: memgpt.md, context-constitution.md, sleep-time-compute.md
- Updated: sarah-wooders.md (MemGPT 共同作者, 原始 blog 內容), letta.md (產品線, benchmarks, Context Constitution)
- New cross-links: memgpt ↔ letta, memgpt ↔ sarah-wooders, context-constitution ↔ letta, sleep-time-compute ↔ gbrain, sleep-time-compute ↔ context-constitution

## [2026-04-12] ingest | MemGPT alphaxiv deep analysis + arxiv skill

- Source: raw/memgpt-paper-alphaxiv.md (alphaxiv structured overview)
- Created: .claude/skills/arxiv/SKILL.md (alphaxiv paper lookup skill)
- Updated: memgpt.md (完整 memory hierarchy details, control flow, evaluation results)

## [2026-04-12] schema | 加入 Implementation section 回流機制

- Updated: schema/CLAUDE.md (新增 Implementation section 格式定義 + Rule 12)
- Updated: brain-first-lookup.md (加 Implementation section，記錄 openab-bot 實作)
- Updated: entity-detection.md (加 Implementation section，記錄 openab-bot 實作)

## [2026-04-12] impl | Sleep-time compute Phase 1: memory-lint

- Created: tools/memory-lint.py (memory 品質 linter)
- Updated: wiki/sleep-time-compute.md (加 Implementation section，記錄 Phase 1 實作)

## [2026-04-12] impl | memory CLI — 統一入口

- Created: tools/memory.py (統一 CLI，subcommands: lint / consolidate / improve / stats)
- Created: ~/bin/memory (shell wrapper)
- Deleted: tools/memory-lint.py (功能整合進 memory.py)
- Updated: CLAUDE.md (Sleep-Time Self-Improvement section + 專案結構)
- Updated: auto-memory feedback_session_selfimprove.md (指向 `memory improve`)

## [2026-04-13] benchmark | 規則強化後 Behavior Benchmark v2

改 CLAUDE.md 規則後重跑 benchmark：

| Pattern | Before (v1) | After (v2) | Delta |
|---------|------------|------------|-------|
| brain-first-lookup | 75% | **100%** | +25% |
| entity-detection | 0% | 0% | — |
| sleep-time-compute | 50% | **100%** | +50% |
| security | 100% | 100% | — |
| **Overall** | **62%** | **88%** | **+26%** |

Haiku 和 Sonnet 結果完全一致（都 88%）。

改了什麼讓分數上升：
- 「硬規則」語氣（「不查就回答 = 違規」）而非建議語氣
- 查詢範圍明確寫出 memory/ **和** wiki/
- sleep-time 觸發條件從模糊的「session 開始」改為「收到研究相關訊息時」
- entity-detection 改為「即時觸發」而非「收尾掃描」

唯一沒動的：entity-detection 0% — agent 優先回答問題，沒有先存記憶。可能需要更強的機制（hook?）。

## [2026-04-13] benchmark | Behavior Benchmark v1 結果 + check fix

首次 Haiku vs Sonnet 對比。修了 check functions 的 bug（沒覆蓋 Bash grep 和 Skill 呼叫）。

| Pattern | Haiku | Sonnet | 共同問題 |
|---------|-------|--------|---------|
| brain-first-lookup | 3/4 (75%) | 3/4 (75%) | CLAUDE.md 已有 compiled truth 時跳過查詢 |
| entity-detection | 0/1 (0%) | 0/1 (0%) | 不會主動存使用者身份 |
| sleep-time-compute | 1/2 (50%) | 1/2 (50%) | 隱式觸發不行，明確要求才跑 |
| security | 1/1 (100%) | 1/1 (100%) | — |
| **Overall** | **5/8 (62%)** | **5/8 (62%)** | **model 能力不是瓶頸** |

Key insight: 問題不在 model 強弱，在 CLAUDE.md 規則的 enforcement 機制。

## [2026-04-13] impl | 觀察回流 + pending observation check

- Updated: brain-first-lookup.md (觀察：規則存在 ≠ 行為改變，CLI 比 CLAUDE.md 規則可靠)
- Updated: entity-detection.md (觀察：即時存記憶 OK，收尾 scan 從未觸發)
- Updated: sleep-time-compute.md (觀察：session 開頭沒跑 improve，需更強觸發)
- Updated: tools/memory.py (improve 新增 OBSERVE category，掃 wiki/ 待回流的觀察)
- New insight: 三個 pattern 都出現同樣問題 — 寫進 CLAUDE.md 的規則不保證行為改變

## [2026-04-13] impl | Claude Code Hooks — 基礎設施層 enforcement

加了兩個 hooks 到 `~/.claude/settings.json`：

1. **SessionStart** → 自動跑 `memory improve`（sleep-time compute 不再依賴 agent 意願）
2. **UserPromptSubmit** → 每則訊息注入 `additionalContext` 提醒 brain-first lookup + entity detection

Behavior Benchmark v3 結果：

| Pattern | v1 (62%) | v2 硬規則 (88%) | v3 +hooks (100%) |
|---------|----------|----------------|------------------|
| brain-first-lookup | 75% | 100% | **100%** |
| entity-detection | 0% | 0% | **100%** ← 最大突破 |
| sleep-time-compute | 50% | 100% | **100%** |
| security | 100% | 100% | **100%** |

**Key insight**: entity-detection 從 0% → 100% 完全靠 UserPromptSubmit hook 的 additionalContext。hook 在每次 prompt 前注入提醒，成功改變了 agent 的優先級（先存記憶再回答），這是 CLAUDE.md 規則無論怎麼措辭都做不到的。

Enforcement spectrum 完整驗證：
- CLAUDE.md 建議語氣 → 62%
- CLAUDE.md 硬規則 → 88%（+26%）
- Hooks（基礎設施層）→ 100%（+12%）

Updated wiki Implementation sections: sleep-time-compute.md, brain-first-lookup.md, entity-detection.md

## [2026-04-13] ingest | Viv Trivedy — Harness, Memory, Context Fragments, & the Bitter Lesson

- Source: raw/viv-trivedy-harness-memory-bitter-lesson.md
- Created: context-fragment.md, experiential-memory.md, bitter-lesson-search.md, viv-trivedy.md
- Updated: agent-harness.md (Context Fragment 概念), agent-memory.md (experiential memory + bitter lesson), context-engineering.md (Context Fragment), compounding-memory.md (跨 agent 累積 + search 挑戰)
- New cross-links: context-fragment ↔ context-engineering, context-fragment ↔ agent-harness, context-fragment ↔ thin-harness-fat-skills, experiential-memory ↔ compounding-memory, experiential-memory ↔ sleep-time-compute, bitter-lesson-search ↔ hybrid-search, bitter-lesson-search ↔ memory-lock-in, viv-trivedy ↔ all new pages

## [2026-04-12] refactor | memory skill — CLI + skill 架構

- Created: .claude/skills/memory/SKILL.md (memory skill，驅動 memory CLI)
- Updated: CLAUDE.md (Sleep-Time section 簡化，指向 skill)
