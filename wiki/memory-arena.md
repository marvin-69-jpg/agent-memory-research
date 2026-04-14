---
aliases: [MemoryArena, memory arena benchmark, agentic memory benchmark]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [benchmark, memory]
---

# MemoryArena

專門測試 agent 在 multi-session agentic tasks 中使用記憶能力的 benchmark — 跟 [[locomo|LOCOMO]] 的差異在於測的是「能不能用記憶做正確行動」，不只是「能不能回憶」。

## Current Understanding

- **核心洞察**：memory benchmarks are misleading — 在 LOCOMO 這類 recall benchmark 上分數接近飽和的模型，放到 real agentic scenarios 表現很差
- **LOCOMO 的不足**：測 memorization 和 action 分開測、只看 single session。不反映 agent 跨 session 學習和決策的能力
- **MemoryArena 的設計**：
  - Human-crafted agentic tasks（不是合成的）
  - Interdependent multi-session tasks：agent 必須從之前的互動中學習，應用知識解決後續挑戰
  - 測的是「在正確時機應用正確 context 做出好決策」
- **與我們的 behavior benchmark 的對比**：我們的 behavior_benchmark.py 也在做類似的事 — 不只測 recall（recall_benchmark.py），還測 agent 是否真的會使用記憶（搜尋 brain、存 entity 等）。MemoryArena 是學術版本的 behavior-level evaluation
- **Paper**: arxiv.org/abs/2602.16313
- **Survey 定位**（Pengfei Du 2026）：MemoryArena 被列為四大 benchmark 之一，專注 cross-session consistency 和 cost-effectiveness。Survey 確認了 MemoryArena 的核心發現：「Long context is not memory」→ [[memory-evaluation]]
- **Evaluation paradox**（[[chrysb]]）：更深的問題是，真實長期對話的 ground truth 超過任何 context window — 評估本身就有理論限制

## Key Sources

- **2026-02-19** — DAIR.AI 推文介紹 MemoryArena（37.8K views）。Source: [[raw/dair-ai-memory-benchmarks-misleading]]

## Related

[[locomo]] [[mem0]] [[agent-memory]] [[compounding-memory]] [[memory-evaluation]] [[chrysb]]
