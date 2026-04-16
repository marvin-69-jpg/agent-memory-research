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
- **Derivation drift**（[[chrysb]]）：staleness 的另一個成因 — 不是外在事實變了，而是連鎖 summarization 累積小誤差。「photocopy of a photocopy」。每次 derivation 稍微 lossy，累積後記憶偏離實際對話。更隱蔽因為沒有明確的「變化時間點」
- **Stale context dominance**（[[chrysb]]）：舊的、被高頻引用的記憶擠掉新的。系統不斷 surface 過時 context — staleness 不只是「不正確」，還會主動壓制正確的新資訊
- **Forgetting propagation**（[[chrysb]]）：刪除 raw turns 不會刪除從中衍生的 summaries。Knowledge graph 中刪除 source conversation 留下 orphaned facts。真正的 forgetting 需要 provenance tracking + cascade delete，或定期 re-derive（昂貴）
- **Survey 觀點**（Pengfei Du 2026）：selective forgetting 嚴重被低估，幾乎沒有系統被明確評估。10 大 open challenges 中排第 4 — "learned selective forgetting"
- **[[reconsolidation]] 是 staleness 的天然解法**：如果記憶每次被 retrieve 都有機會被更新，就不容易變 stale。[[a-mem]] 的 Memory Evolution 讓舊記憶因新資訊而自動更新 context/tags
- **[[ssgm]] 的 Weibull decay**：比 exponential decay 更好建模 memory 衰減（先快後慢），是 temporal obsolescence 的理論基礎。Weibull distribution 同時建模了 staleness 和 forgetting

## Key Sources

- **2026-04-01** — Mem0 報告列為 open problem：detecting when high-relevance memories become stale。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]
- **2026-04-12** — Chrys Bader: derivation drift、stale context dominance、forgetting propagation 三種 staleness 機制。Source: [[raw/chrysb-long-term-memory-unsolved]]
- **2026-03-08** — Pengfei Du survey: selective forgetting 被低估，列為 10 大 open challenges 第 4。Source: [[raw/pengfei-du-memory-survey-2026]]

## Related

[[mem0]] [[compounding-memory]] [[compiled-truth-pattern]] [[sleep-time-compute]] [[agent-memory]] [[chrysb]] [[memory-failure-modes]] [[memory-consistency]] [[actor-aware-memory]] [[autoreason]] [[gene-map]] [[graph-memory]] [[memory-evaluation]] [[neuroscience-memory]] [[synapse]] [[reconsolidation]] [[a-mem]] [[ssgm]] [[context-rot]] [[self-improving-agent]]
