---
aliases: [context fragments, loaded object]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [context, architecture, harness]
---

# Context Fragment

Context window 中每個被載入的物件（CLAUDE.md、memory、tool schema、skill metadata 等）都是一個 Context Fragment，代表 user 或 [[agent-harness]] 設計者對「agent 此刻需要什麼資訊才能工作」的顯式決策。

## Current Understanding

- [[agent-harness]] 最重要的工作是把資料正確且高效地 route 進 context window — 每個被載入的物件就是一個 Context Fragment
- Context window 是「precious artifact」— 空間有限，每個 fragment 的載入都是取捨
- Context Fragment 的概念讓 [[context-engineering]] 從「把東西塞進去」變成「每個 slot 都是設計決策」
- 與 @a1zhang 提出的 RLMs（Reasoning Language Models）中「externalizing objects + loading into context window」的思路一脈相承
- 這個 framing 解釋了為什麼 [[thin-harness-fat-skills]] 有效：harness 負責 routing（選擇載入哪些 fragments），skills 是 fragments 本身
- 也解釋了 [[garry-tan]] 的 Resolver 概念：Resolver 就是 context fragment 的 routing table

## Key Sources

- **2026-04-13** — Viv Trivedy 提出 Context Fragment 概念：每個 loaded object 是 harness designer 的顯式決策。Source: [[raw/viv-trivedy-harness-memory-bitter-lesson]]

## Related

[[context-engineering]] [[agent-harness]] [[thin-harness-fat-skills]] [[garry-tan]] [[viv-trivedy]]
