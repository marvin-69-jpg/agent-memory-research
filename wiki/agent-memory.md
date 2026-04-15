---
aliases: [agent memory, memory system, LLM memory]
first_seen: 2026-04-11
last_updated: 2026-04-14
tags: [memory, architecture]
---

# Agent Memory

Agent 記憶系統，讓 agent 能跨 session 累積知識、個人化體驗。Memory 本質上是 context 的一種形式，由 [[agent-harness]] 管理。

## Current Understanding

- Memory 分為兩類：
  - **短期記憶**：對話中的 messages、tool call 結果 → harness 管理
  - **長期記憶**：跨 session 記憶 → harness 負責讀寫更新
- 2026 年 memory 已從「nice-to-have」升級為 **first-class architectural component**，有標準 benchmark（[[locomo|LOCOMO]]）、專屬研究文獻、可量化的 performance gap
- 記憶系統已分化出三種類型：**episodic**（what happened）、**semantic**（what is known）、**procedural**（how to do things）→ [[procedural-memory]]。MIRIX 進一步擴展為六層（加 Core / Resource / Knowledge Vault）→ [[multimodal-memory]]
- **多模態記憶**正在成為下一個前沿：現有系統幾乎都是純文字，但 agent 需要處理影像、音訊、影片。MIRIX 和 M3-Agent 分別從桌面助手和 embodied agent 角度解決 → [[multimodal-memory]]、[[mirix]]
- Memory scope 需要多層設計：user / agent / session / org → [[multi-scope-memory]]
- Multi-agent 場景需要 **actor-aware memory** — 追蹤每條記憶的來源 actor → [[actor-aware-memory]]
- **Memory staleness** 是 open problem：高頻 retrieve 的記憶過時後變成 confidently wrong → [[memory-staleness]]
- Memory 是 agent 最強的**差異化來源**：沒有 memory 的 agent 任何人都能複製
- Memory 創造 **data flywheel**：越用越好、越換越痛 → [[memory-lock-in]]、[[compounding-memory]]
- Agent memory 相比人類有根本優勢：agent 可以 fork/duplicate，[[experiential-memory|經驗記憶]]可以跨所有 instances 累積 — 人類做不到
- 隨著 agent 部署到年級距，產生的資料量超指數成長 → [[bitter-lesson-search|Bitter Lesson (Search)]]
- **Write–Manage–Read Loop**（Pengfei Du survey 2026）：memory 形式化為嵌入 agent 感知–行動循環的 loop。Policy function 依據 memory reads 決定動作，Update function 依據觀察更新 memory。對應 POMDP：memory = agent's belief state
- **三維分類法**（Pengfei Du）：Temporal Scope（working/episodic/semantic/procedural）× Representational Substrate（context-resident/vector/structured/executable）× Control Policy（heuristic/prompted/learned）
- **五大機制家族**：context-resident compression、retrieval-augmented stores、reflective self-improving、hierarchical virtual context（MemGPT）、policy-learned management（AgeMem）
- **Raw vs Derived 根本光譜**（[[chrysb]]）：所有記憶系統在這個光譜上選位置。Raw = lossless but inert，Derived = compact but lossy。兩端都不行，所有系統都是 trade-off → [[memory-failure-modes]]
- **"Long context is not memory"**：超長 context 模型在 selective retrieval 任務上仍輸給專用 memory 系統。Infinite context = raw 路線的極端版，成本線性增長 + attention 退化
- **Evaluation paradox**（[[chrysb]]）：驗證記憶系統需要 ground truth，但真實長期對話的 ground truth 超過任何 context window → [[memory-evaluation]]
- **"Memory deserves first-class engineering comparable to the LLM itself"**（Pengfei Du）：移除 memory 對 agent 表現的損害 > 更換 LLM backbone 帶來的差異
- Sarah Wooders: "memory isn't a plugin — it's the harness"
- [[gbrain|GBrain]] 提出三層記憶模型：world knowledge（gbrain）、operational state（agent memory）、session context — 三層都該被查詢
- 知識頁面的最佳實踐：[[compiled-truth-pattern]]（compiled truth 可改寫 + timeline append-only）

## Key Sources

- **2026-04-01** — Mem0 State of AI Agent Memory 2026：memory 升級為 first-class component，三種記憶類型，10 種方法 benchmark。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]
- **2026-04-13** — Viv Trivedy 論述 experiential memory 的跨 agent 累積優勢和 search bitter lesson。Source: [[raw/viv-trivedy-harness-memory-bitter-lesson]]
- **2026-04-12** — GBrain 實踐三層記憶模型和 compounding memory loop。Source: [[raw/garry-tan-gbrain]]
- **2026-04-11** — Harrison Chase 論述 memory 是 context 的形式、與 harness 不可分。Source: [[raw/harrison-chase-your-harness-your-memory]]
- **2026-04-12** — Chrys Bader: raw vs derived 光譜、9 軸設計框架、10 failure modes、evaluation paradox（262K views）。Source: [[raw/chrysb-long-term-memory-unsolved]]
- **2026-03-08** — Pengfei Du: 系統性 survey，三維分類法、五大機制、write–manage–read loop 形式化。Source: [[raw/pengfei-du-memory-survey-2026]]
- **2025-08-28** — Yohei Nakajima: 消費者/開發者/開源全景分析、dual-memory architecture。Source: [[raw/yohei-nakajima-rise-of-ai-memory]]

## Related

[[agent-harness]] [[context-engineering]] [[memory-lock-in]] [[letta]] [[sarah-wooders]] [[gbrain]] [[compounding-memory]] [[compiled-truth-pattern]] [[experiential-memory]] [[bitter-lesson-search]] [[viv-trivedy]] [[mem0]] [[locomo]] [[procedural-memory]] [[multi-scope-memory]] [[actor-aware-memory]] [[memory-staleness]] [[graph-memory]] [[memory-failure-modes]] [[memory-evaluation]] [[chrysb]] [[yohei-nakajima]] [[agemem]] [[chatgpt-memory]] [[coding-agent-memory]] [[concept-map]] [[context-constitution]] [[filesystem-vs-database]] [[garry-tan]] [[harrison-chase]] [[hybrid-search]] [[leonie]] [[mece-resolver]] [[memgpt]] [[memory-arena]] [[open-questions]] [[multimodal-memory]] [[mirix]] [[neuroscience-memory]] [[synapse]] [[reconsolidation]] [[a-mem]] [[ssgm]] [[collaborative-memory-system]] [[multi-agent-memory]]
