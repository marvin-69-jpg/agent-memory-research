---
aliases: [thin harness fat skills, fat skills thin harness, skill file architecture]
first_seen: 2026-04-12
last_updated: 2026-04-15
tags: [architecture, harness]
---

# Thin Harness, Fat Skills

[[garry-tan]] 提出的 agent 架構哲學：把 intelligence 往上推進 markdown skills，把 execution 往下推進 deterministic tooling，harness 本身保持極薄。

## Current Understanding

- **三層架構**：
  1. Fat skills（top）— markdown procedures encoding judgment + process，90% of value
  2. Thin CLI harness（middle）— ~200 lines，JSON in text out
  3. Your app（bottom）— QueryDB, ReadDoc, Search，deterministic foundation
- **Skill file = method call**：接受參數，同一 skill 用不同參數產出完全不同能力。不是 prompt engineering，是 software design with markdown as programming language
- **Anti-pattern**：fat harness（40+ tool definitions 吃掉半個 context window、MCP round-trip 2-5 秒）
- **五個核心定義**：Skill File, Harness, Resolver, Latent vs. Deterministic, Diarization
- **Resolver 是關鍵**：context 的 routing table，task X 出現時自動載入 document Y。Garry 的 CLAUDE.md 從 20,000 行瘦身到 200 行 pointer — attention degradation 問題解決 → [[mece-resolver]]
- **Resolver 深化（2026-04-16）**：audit 發現 13 個 brain-writing skills 只有 3 個查 resolver。trigger evals（50 test cases）、check-resolvable（找到 15% dark skills）、[[context-rot]]（resolver Day 90 成歷史文件）。Resolver = agent 系統的 management layer
- **Self-learning loop**：skill 讀 feedback → 改寫自己的 rules → 下次自動更好（YC Startup School: OK ratings 12% → 4%）
- 跟 [[harrison-chase]] 的 harness 觀點對比：Chase 強調 harness 與 memory 綁定；Garry 強調 harness 要 thin，intelligence 在 skills 裡
- **v0.10.0 實證（2026-04-15）**：GBrain 現有 24 個 fat skills，全部有 e2e tests、evals、unit tests。Garry 稱 RESOLVER.md 和 SOUL.md 已「perfected」— 這代表 fat skill 架構經過數月迭代已穩定收斂
- **Multi-user 擴展**：ACL 機制讓多人共用同一個 brain，thin harness 的設計讓權限控制在 harness 層處理，skills 不需要改動

### 關鍵引言

> 「The bottleneck is never the model's intelligence. The bottleneck is whether the model understands your schema.」

> 「Every skill I write is a permanent upgrade. It never degrades. It never forgets. When the next model drops, every skill instantly gets better.」

## Key Sources

- **2026-04-16** — "Resolvers: The Routing Table for Intelligence"：resolver 完整理論。Source: [[raw/garry-tan-resolvers-routing-table]]
- **2026-04-15** — GBrain v0.10.0: 24 fat skills with full test coverage，perfected resolver。Source: [[raw/garry-tan-gbrain-v0.10.0]]
- **2026-04-12** — "Thin Harness, Fat Skills" essay + YC Spring 2026 talk。Source: [[raw/garry-tan-gbrain-deep]]

## Related

[[garry-tan]] [[gbrain]] [[agent-harness]] [[context-engineering]] [[brain-agent-loop]] [[autoreason]] [[coding-agent-memory]] [[context-fragment]] [[harness-engineering]] [[procedural-memory]] [[scaffolding-lifecycle]] [[mece-resolver]] [[context-rot]]
