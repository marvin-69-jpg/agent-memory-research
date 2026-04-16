---
aliases: [compiled truth, compiled truth + timeline]
first_seen: 2026-04-12
last_updated: 2026-04-12
tags: [memory, architecture]
---

# Compiled Truth Pattern

一種知識頁面的寫作模式：上半部是「compiled truth」（可改寫的當前最佳理解），下半部是「timeline」（append-only 的證據軌跡）。由 [[garry-tan]] 在 [[gbrain|GBrain]] 中實踐。

## Current Understanding

- **Compiled truth**（`---` 分隔線以上）：當前對這個 entity 的最佳理解，新資訊進來時**整合改寫**而非 append
- **Timeline**（`---` 分隔線以下）：append-only 的事件記錄，標記日期和來源，永不修改
- 核心哲學：「The compiled truth is the answer. The timeline is the proof.」
- 這個 pattern 跟 boba-wiki 的做法高度一致：wiki page 的「Current Status」= compiled truth，「Key Events」= timeline
- 也呼應 [[harrison-chase]] 的觀點：memory 應該是 rewrite 而非 append，才能保持 wiki 的可讀性
- GBrain 用 page_versions table 保存 compiled_truth 的歷史快照，確保改寫不會丟失資訊
- **與 [[reconsolidation]] 的關係**：compiled truth 的 rewrite 是 **manual reconsolidation** — 有人觸發才會改寫。[[a-mem]] 的 Memory Evolution 把這個過程自動化了：新記憶寫入時自動更新舊記憶的 context
- **[[ssgm]] 的 Dual Storage** 就是 compiled truth pattern 的形式化版本：Mutable Active Graph ≈ compiled truth，Immutable Episodic Log ≈ timeline

## Key Sources

- **2026-04-12** — GBrain README 中的 knowledge model 說明。Source: [[raw/garry-tan-gbrain]]

## Related

[[gbrain]] [[agent-memory]] [[garry-tan]] [[enrichment-pipeline]] [[mece-resolver]] [[memory-staleness]] [[multimodal-memory]] [[neuroscience-memory]] [[reconsolidation]] [[a-mem]] [[ssgm]] [[session-management]]
