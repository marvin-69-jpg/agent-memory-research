---
aliases: [memory staleness, 記憶過時, stale memory, memory decay]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [memory, architecture]
---

# Memory Staleness

記憶庫中高 relevance 但已不正確的記憶 — 跟「低 relevance 的舊記憶」不同，是「被高度信任但已經錯了」的記憶。目前是 open research problem。

## Current Understanding

- **Staleness ≠ low relevance**：
  - Low relevance 的舊記憶：可以用 decay 處理（自然降權）
  - High relevance 但過時的記憶：「使用者在 Google 工作」— 被頻繁 retrieve、高信任度，直到使用者換了公司。此時它變成 **confidently wrong** 而不是 outdated
- **Dynamic forgetting**：Mem0 有 decay 機制降低 low-relevance 記憶的權重。但這解決的是 irrelevance，不是 staleness
- **偵測困難**：怎麼知道一條高頻 retrieve 的記憶已經過時？需要使用者明確更正，或透過矛盾偵測（新事實與舊記憶衝突）
- **我們的經驗**：openab-bot 的 memory lint 會標記 14 天未更新的 project 記憶，但這只是 heuristic。feedback 記憶可能永遠不過時，也可能一天就過時
- **與 compiled truth pattern 的關係**：GBrain 的做法是 rewrite compiled truth 而非 append。如果做得好，staleness 在 write 時就被處理。但前提是有東西觸發 rewrite

## Key Sources

- **2026-04-01** — Mem0 報告列為 open problem：detecting when high-relevance memories become stale。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]

## Related

[[mem0]] [[compounding-memory]] [[compiled-truth-pattern]] [[sleep-time-compute]] [[agent-memory]]
