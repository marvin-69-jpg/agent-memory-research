---
aliases: [agent scaffold, agent scaffolding, harness]
first_seen: 2026-04-11
last_updated: 2026-04-13
tags: [harness, architecture]
---

# Agent Harness

Agent harness 是包裹在 LLM 外面的執行框架，負責管理 tool calling、context、memory、以及 LLM 與外部資料源的互動。它是 agent 運作的核心基礎設施。

## Current Understanding

- Agent harness 是 2024-2025 年興起的新一代 scaffolding，取代了早期的 RAG chain 和 complex flow
- **Harness 不會消失**：模型變強只是讓舊 scaffolding 被新 scaffolding 取代，而非被模型吸收
- 證據：Claude Code 被洩漏時有 512k 行 code — 那就是 harness
- API 背後的功能（如 web search）也不是「模型的一部分」，而是輕量 harness 在做 tool calling
- Harness 與 [[agent-memory]] 密不可分 — 管理 [[context-engineering|context]] 是 harness 的核心職責
- Harness 最重要的工作：高效且正確地把資料 route 進 context window — 每個被載入的物件都是一個 [[context-fragment|Context Fragment]]，代表設計者的顯式決策
- 如果你不擁有 harness，你就不擁有 memory → [[memory-lock-in]]
- **2026 年 harness 成為獨立學科**：
  - Philipp Schmid（HuggingFace）：「2025 = agents 的開始，2026 = Agent Harnesses 的年代」。Harness 在 agent framework 之上運作，新瓶頸是 **context durability**
  - dex 定義 [[harness-engineering]]：在既有 agent 的 integration points（hooks、skills、MCPs）上做工程，是 context engineering 的上層
  - **NLAH（Natural-Language Agent Harnesses）**：把 harness 邏輯從 code 外部化成 natural-language artifacts，可 ablate、可 migrate、可 compare。OSWorld 上 NLAH 47.2% vs code harness 30.4%
- **Scaffolding lifecycle**（Aaron Levie）：模型變強時 scaffolding 從「有幫助」變「有害」，必須 ruthlessly jettison → [[scaffolding-lifecycle]]

## Key Sources

- **2026-04-10** — Carlos Perez 整理 NLAH 論文：harness 外部化為 NL artifacts（Pan et al.）。Source: [[raw/carlos-perez-natural-language-agent-harnesses]]
- **2026-04-03** — Aaron Levie: brutally unsentimental architecture — scaffolding lifecycle loop。Source: [[raw/aaron-levie-unsentimental-architecture]]
- **2026-01-05** — Philipp Schmid: 2026 = Agent Harnesses 的年代。Source: [[raw/philipp-schmid-2026-agent-harnesses]]
- **2025-11-04** — dex 定義 harness engineering 概念。Source: [[raw/dex-harness-engineering]]
- **2026-04-13** — Viv Trivedy: harness 的核心工作是 route data into context window，每個 loaded object 是 Context Fragment。Source: [[raw/viv-trivedy-harness-memory-bitter-lesson]]
- **2026-04-12** — GBrain 的 "thin harness, fat skills" 哲學：harness 是薄殼，knowledge 在 markdown skills 裡。Source: [[raw/garry-tan-gbrain]]
- **2026-04-11** — Harrison Chase 提出 harness 不會消失、與 memory 綁定的論點。Source: [[raw/harrison-chase-your-harness-your-memory]]

## Related

[[agent-memory]] [[context-engineering]] [[context-fragment]] [[memory-lock-in]] [[deep-agents]] [[letta]] [[harrison-chase]] [[gbrain]] [[viv-trivedy]] [[harness-engineering]] [[scaffolding-lifecycle]] [[philipp-schmid]] [[aaron-levie]] [[thin-harness-fat-skills]]
