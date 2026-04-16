---
aliases: [MECE directories, resolver, filing rules, RESOLVER.md]
first_seen: 2026-04-12
last_updated: 2026-04-16
tags: [architecture, memory]
---

# MECE Resolver

GBrain 的 knowledge organization 原則：每塊知識有且只有一個 primary home，由 resolver decision tree 決定放哪。

## Current Understanding

- **MECE directories**：Mutually Exclusive, Collectively Exhaustive — 每個 directory 管一個 knowledge domain，每個 entity 只有一個 page
- **Resolver 層級**：
  1. `RESOLVER.md`（頂層 decision tree，agent 建任何 page 前必讀）
  2. 每個 directory 的 `README.md`（local resolver — what goes here, what does NOT go here）
- **常見 disambiguation**：
  - Concept vs Idea：能教的 framework → concept；能建的東西 → idea
  - Idea vs Project：有人在做 → project；沒有 → idea
  - Person vs Company：about them as human → people/；about the org → companies/
- **MECE applies to directories, not reality** — 人物可以是多面向的，用 cross-links 和 typed backlinks 表達，不是用多個 page
- **Inbox 是 signal** — 放不進任何 directory 的東西進 `inbox/`，代表 schema 需要演化
- **Dedup protocol**：建 page 前 search + grep aliases + check .raw/ sidecars → match 就 UPDATE 不 CREATE
- **四個 database primitives**：Entity registry, Event ledger, Fact store（contradictions are data not bugs）, Relationship graph

### 核心洞察

> 「Knowledge management has failed for 30 years because maintenance falls on humans. LLM agents change the equation — they don't get bored, don't forget to update cross-references, and can touch 50 files in one pass.」

### Resolver 是 Context 的 Routing Table

Garry Tan 在 Resolvers 長文中把 resolver 定義拉到更高層次：

> A resolver is a routing table for context. When task type X appears, load document Y first.

**20K → 200 行的故事**：Garry 的 CLAUDE.md 從 20,000 行瘦身到 200 行 numbered decision tree + pointers。模型注意力退化立刻解決 — 不是模型變聰明了，是不再被 noise 淹沒。

### The Audit：3/13 Skills

審計 13 個 brain-writing skills 後發現只有 3 個參考 resolver，其他 10 個都有 hardcoded paths。修復：共享 `_brain-filing-rules.md` + 每個 skill 開頭 mandate "read RESOLVER.md first"。**Zero misfilings since。**

### Trigger Evals

50 個 sample inputs + expected routing 的 test suite：
- **False negative**：skill 該 fire 沒 fire（trigger description 錯或缺）
- **False positive**：錯的 skill fire（triggers 重疊）
- 修復只需要編輯 markdown，不用改 code

### check-resolvable（Meta-Skill）

走完 AGENTS.md → skill file → code，找不可達的 skill。首次跑發現 **6/40+ skills（15%）是 dark** — 存在但使用者無法觸發。每週跑，等同 linter for resolvers。

### Resolvers Are Fractal

存在於系統的每一層：
1. **Skill resolver**（AGENTS.md）：task types → skill files
2. **Filing resolver**（RESOLVER.md）：content types → directories
3. **Context resolver**（inside each skill）：sub-routing within skill

Claude Code 的 skill description 就是 resolver。It's resolvers all the way down。

### Resolver as Management

| Agent System | Organization Analogy |
|---|---|
| Skills | Employees |
| Resolver | Org chart + escalation logic |
| Filing rules | Internal process |
| check-resolvable | Audit & compliance |
| Trigger evals | Performance reviews |

> The problem isn't that models aren't smart enough. The problem is that we've been building organizations with no management layer.

### Context Rot

Resolver 會自然衰敗 → [[context-rot]]。Day 30 新 skill 沒 register，Day 60 trigger 跟用語失配，Day 90 resolver 成為歷史文件。需要 check-resolvable + trigger evals + self-healing loop 持續維護。

## Key Sources

- **2026-04-16** — Garry Tan: "Resolvers: The Routing Table for Intelligence"，完整 resolver 理論 + audit + trigger evals + check-resolvable + context rot。Source: [[raw/garry-tan-resolvers-routing-table]]
- **2026-04-12** — GBrain RECOMMENDED_SCHEMA。Source: [[raw/garry-tan-gbrain-deep]]

## Related

[[gbrain]] [[compiled-truth-pattern]] [[agent-memory]] [[entity-detection]] [[thin-harness-fat-skills]] [[garry-tan]] [[context-rot]] [[context-engineering]] [[scaffolding-lifecycle]] [[brain-first-lookup]] [[sleep-time-compute]] [[harness-engineering]] [[meta-harness]]
