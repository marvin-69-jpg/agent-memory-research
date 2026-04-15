---
title: "Resolvers: The Routing Table for Intelligence"
author: Garry Tan
date: 2026-04-16
source: https://x.com/garrytan/status/2044479509874020852
views: 46.1K
topic: resolver, context routing, agent governance
---

# Resolvers: The Routing Table for Intelligence

Garry Tan 的第三篇長文（繼 Thin Harness Fat Skills 和 GBrain v0.10.0 之後），專門深入 resolver 概念。

## 核心定義

> A resolver is a routing table for context. When task type X appears, load document Y first.

一句話，但這一句話決定了 agent 是 compound intelligence 還是 slowly forgets what it knows。

## The 20,000-Line CLAUDE.md

Garry 的 CLAUDE.md 曾經 20,000 行。所有 quirk、pattern、convention、edge case 都塞進去。結果：
- 模型注意力退化
- 回應變慢、變不精確
- Claude Code 自己說「please cut it back」

修復：200 行 numbered decision tree + pointers to documents。
- 是人嗎？→ /people/
- 是公司？→ /companies/
- 是政策分析？→ /civic/

20,000 行知識，on-demand 存取，不污染 context window。**Resolver 取代了 20K 行的 instructions**。

## The Manidis Misfiling

Will Manidis 的 "No New Deal for OpenAI" — 政策分析文章。Agent 把它歸到 `sources/`（raw data dump 的地方），應該放 `civic/`。

原因：idea-ingest skill 硬寫了 `brain/sources/` 作為預設路徑，沒有查 resolver。

## The Audit

審計 13 個 brain-writing skills：
- **只有 3/13 參考了 resolver**
- 其他 10 個都有 hardcoded paths
- 這是 agent 系統的死因：不是 dramatic failure，是 **slow, silent drift**

修復：共享 `_brain-filing-rules.md` + 每個 skill 開頭兩行 mandate：
> Before creating any new brain page, read `brain/RESOLVER.md` and `skills/_brain-filing-rules.md`. File by primary subject, not by source format or skill name.

**結果：zero misfilings since。**

## Trigger Evals

50 個 sample inputs + expected outputs：
```
Input: "check my signatures"
Expected: executive-assistant (signature section)

Input: "who is Pedro Franceschi"
Expected: brain-ops → gbrain search

Input: "save this article to brain"
Expected: idea-ingest + RESOLVER.md
```

兩種 failure mode：
- **False negative**：skill 該 fire 但沒 fire（trigger description 錯或缺）
- **False positive**：錯的 skill fire（triggers 重疊）

都能透過編輯 markdown 修復。No code changes。

## check-resolvable — Meta-Skill

走完整個 chain：AGENTS.md → skill file → code，找 dead links。

第一次跑找到 **6/40+ unreachable skills**（15% dark）：
- Flight tracker 存在但「check my flight」不觸發
- Content-ideas generator 只在 cron 跑，不能手動觸發
- Citation fixer 在 skills/ 但不在 resolver

修復：一小時，加 triggers 到 AGENTS.md。現在每週跑。

## Context Rot

Resolver 會衰敗：
- **Day 1**：完美。每個 skill registered、每個 trigger 準確
- **Day 30**：3 個新 skill 沒人加到 resolver（sub-agents 在凌晨 3 點建的）
- **Day 60**：2 個 trigger description 跟使用者用語不 match（"track this flight" vs "is my flight delayed?"）
- **Day 90**：resolver 是歷史文件。使用者直接 "read skills/xxx/SKILL.md" 跳過 resolver

**Context rot 是 resolver 版的 memory-staleness。**

## Self-Healing Resolver（RLM）

YC office hours 有 CTO 問：能否用 RLM 解 context rot？

想法：RL loop 觀察所有 task dispatch：
- 哪個 skill fired
- 哪個 task 沒 match
- 哪個 task match 到錯的 skill

定期（nightly/weekly）based on evidence rewrite resolver。

> Claude Code's AutoDream system — memory consolidation during idle time — is a primitive version.

**A resolver that learns from its own traffic. That's the endgame for agent governance.**

## Resolvers Are Fractal

存在於系統的每一層：
1. **Skill resolver**（AGENTS.md）：task types → skill files
2. **Filing resolver**（RESOLVER.md）：content types → directories
3. **Context resolver**（inside each skill）：sub-routing within skill

> It's resolvers all the way down.

Claude Code 已經有這個 pattern：每個 skill 的 description field 就是 resolver。

## Resolver as Management

| Agent System | Organization Analogy |
|---|---|
| Skills | Employees（specialists/generalists） |
| Resolver | Org chart + escalation logic |
| Filing rules | Internal process（where info lives） |
| check-resolvable | Audit & compliance |
| Trigger evals | Performance reviews |

> The problem isn't that models aren't smart enough. The problem is that we've been building organizations with no management layer.

## GStack

新公開的 coding layer：
- Fat skills in markdown
- 72,000+ GitHub stars
- Skills call knowledge in GBrain
- Together = full architecture: intelligence on tap

## 結語

> This is the new dawn of personal software. This is not packaged software. This is software that you build for yourself, but with the fat skills and fat code and thin harness that is your own personal mini-AGI.

Links:
- GBrain: github.com/garrytan/gbrain
- GStack: github.com/garrytan/gstack
