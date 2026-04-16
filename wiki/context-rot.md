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

## Key Sources

- **2026-04-16** — Garry Tan: Resolvers 長文，首次系統化描述 context rot。Source: [[raw/garry-tan-resolvers-routing-table]]

## Related

[[mece-resolver]] [[memory-staleness]] [[scaffolding-lifecycle]] [[thin-harness-fat-skills]] [[gbrain]] [[garry-tan]] [[sleep-time-compute]] [[agent-harness]] [[meta-harness]] [[harness-engineering]]
