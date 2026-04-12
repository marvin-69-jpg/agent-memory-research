---
aliases: [MECE directories, resolver, filing rules, RESOLVER.md]
first_seen: 2026-04-12
last_updated: 2026-04-12
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

## Key Sources

- **2026-04-12** — GBrain RECOMMENDED_SCHEMA。Source: [[raw/garry-tan-gbrain-deep]]

## Related

[[gbrain]] [[compiled-truth-pattern]] [[agent-memory]] [[entity-detection]]
