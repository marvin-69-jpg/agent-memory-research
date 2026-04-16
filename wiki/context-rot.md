---
aliases: [context rot, resolver decay, routing decay, 上下文腐敗]
first_seen: 2026-04-16
last_updated: 2026-04-16
tags: [architecture, harness]
---

# Context Rot

Agent 系統的 routing tables、resolvers、skill descriptions 隨時間自然衰敗。由 [[garry-tan]] 在 Resolver 長文中首次命名。是 [[memory-staleness]] 在 infrastructure 層的對應物。

## Current Understanding

### 衰敗時間線

| 時間 | 狀態 | 症狀 |
|------|------|------|
| Day 1 | 完美 | 每個 skill registered，每個 trigger 準確 |
| Day 30 | 漂移 | 3 個新 skill（sub-agents 凌晨 3 點建的）沒人加到 resolver |
| Day 60 | 失配 | Trigger descriptions 跟使用者用語不 match（"track this flight" vs "is my flight delayed?"） |
| Day 90 | 歷史文件 | Resolver 描述過去的系統，不是現在的。使用者直接呼叫 skill 跳過 resolver |

### Root Cause

Context rot 的根本原因是 **creation 和 registration 分離**：
- Skill 可以被建立（by human、by sub-agent、by cron）
- 但 resolver 不會自動更新
- 隨著 skill 數量成長，drift 不可避免

### 與 Memory Staleness 的關係

| | [[memory-staleness]] | Context Rot |
|---|---|---|
| 層級 | Memory layer | Infrastructure layer |
| 什麼在腐敗 | 記憶的正確性 | Routing/filing 的正確性 |
| 後果 | Confidently wrong answers | Skills unreachable / misfiled content |
| 機制 | 外在事實改變 + derivation drift | 系統演化但 routing table 沒跟上 |
| 解法 | Reconsolidation, decay | check-resolvable, trigger evals, self-healing resolver |

### 偵測機制

[[garry-tan]] 在 GBrain 中開發了兩套偵測工具：

1. **check-resolvable**（meta-skill）：走完 AGENTS.md → skill file → code，找 dead links。首次跑找到 **6/40+ skills（15%）unreachable**
2. **Trigger evals**：50 個 sample inputs + expected routing。偵測 false negatives（skill 該 fire 沒 fire）和 false positives（錯的 skill fire）

### Self-Healing（前瞻方向）

RL loop 觀察 task dispatch traffic → 定期 rewrite resolver：
- 觀察哪個 skill fired、哪個 task 沒 match、哪個 match 錯
- Based on evidence 調整 trigger descriptions 和 priority
- Claude Code 的 AutoDream（sleep-time memory consolidation）是原始版本

> A resolver that learns from its own traffic. That's the endgame for agent governance.

### 與 Scaffolding Lifecycle 的關係

Context rot 是 [[scaffolding-lifecycle]] 的一種表現：scaffolding 不只因為模型變強而需要拆（Levie 的觀點），也因為**系統演化而自然腐敗**（Garry 的觀點）。兩者都指向同一結論：agent 系統需要持續維護機制。

### Meta-Harness: Automated Rot Repair

[[meta-harness]]（Stanford, 2026）提供了 context rot 的自動修復路徑 — 不是人工維護 resolver，而是讓 coding agent 定期搜尋最佳 harness 配置。Garry 的 self-healing resolver（RLM loop）是方向，Meta-Harness 是學術驗證。

### Context Rot 的第二個戰場：Compaction Timing

Thariq（Claude Code team）在 session management 長文中點出一個關鍵推論：

> **Due to context rot, the model is at its least intelligent point when compacting.**

Context rot 不只在 resolver / routing 層發生。它也決定了 **compact 本身的品質** — 當 context 滿到要 autocompact 時，model 已經處在最弱的狀態，卻正好要被要求做最重要的事（決定什麼該保留、什麼該丟）。

**推論**：
- **Autocompact 是反模式**：等到 context rot 已經發生才壓縮 = 用最弱的 model 做最關鍵的決定
- **Proactive compact with intent**：趁 model 還清醒時，帶著「我接下來要做什麼」的 context 下手 `/compact focus on X, drop Y`
- **/rewind > /compact**：能 rewind 就不要 compact，因為 rewind 是 lossless 的裁剪，compact 是 lossy 的總結

這把 context rot 從單純的 infrastructure 問題（resolver decay）擴展到**整個 session lifecycle** — rot 影響的不只是找得到什麼 skill，還影響了壓縮記憶本身的品質。詳見 [[session-management]]。

## Key Sources

- **2026-04-16** — Garry Tan: Resolvers 長文，首次系統化描述 context rot。Source: [[raw/garry-tan-resolvers-routing-table]]
- **2026-04-16** — Thariq (Claude Code): context rot 決定 compaction 品質。Source: [[raw/thariq-claude-code-session-management]]

## Related

[[mece-resolver]] [[memory-staleness]] [[scaffolding-lifecycle]] [[thin-harness-fat-skills]] [[gbrain]] [[garry-tan]] [[sleep-time-compute]] [[agent-harness]] [[meta-harness]] [[harness-engineering]] [[session-management]] [[context-engineering]] [[memory-failure-modes]]
