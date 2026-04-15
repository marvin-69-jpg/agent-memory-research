# Agent Memory Research — Index

> Auto-maintained by LLM. Do not edit manually.

## Structure

- [[wiki/concept-map|Concept Map]] — 三層架構 + 跨層主題 + 人物/產品索引
- [[wiki/open-questions|Open Questions]] — 12 個未解問題，按重要性排序 + 研究缺口

## Wiki Pages

| Page | Summary | Tags | Last Updated |
|------|---------|------|-------------|
| [[wiki/agent-harness\|Agent Harness]] | Agent 的執行框架，與 memory 密不可分 | harness, architecture | 2026-04-12 |
| [[wiki/agent-memory\|Agent Memory]] | Agent 記憶系統，三層模型（world/operational/session） | memory, architecture | 2026-04-12 |
| [[wiki/memory-lock-in\|Memory Lock-in]] | 封閉 harness 造成的記憶鎖定，memory 是最強 lock-in 武器 | lock-in, memory | 2026-04-11 |
| [[wiki/compounding-memory\|Compounding Memory]] | 記憶複合成長效應，越用越聰明 | memory, architecture | 2026-04-12 |
| [[wiki/compiled-truth-pattern\|Compiled Truth Pattern]] | compiled truth（可改寫）+ timeline（append-only）的知識頁面模式 | memory, architecture | 2026-04-12 |
| [[wiki/thin-harness-fat-skills\|Thin Harness, Fat Skills]] | Garry Tan 架構哲學：intelligence 在 skills，harness 保持 thin | architecture, harness | 2026-04-12 |
| [[wiki/brain-agent-loop\|Brain-Agent Loop]] | Signal→Detect→Read→Respond→Write→Sync 核心 loop | memory, architecture | 2026-04-12 |
| [[wiki/brain-first-lookup\|Brain-First Lookup]] | 永遠先查 brain，external API 是 fallback | retrieval, memory | 2026-04-12 |
| [[wiki/entity-detection\|Entity Detection]] | 每個 message 自動偵測 entity 和 original thinking | memory, architecture | 2026-04-12 |
| [[wiki/enrichment-pipeline\|Enrichment Pipeline]] | 三層 tier 分配 API 資源 | memory, architecture | 2026-04-12 |
| [[wiki/mece-resolver\|MECE Resolver]] | 每塊知識有唯一 primary home | architecture, memory | 2026-04-12 |
| [[wiki/hybrid-search\|Hybrid Search]] | Vector + keyword + RRF fusion 檢索策略 | retrieval, architecture | 2026-04-12 |
| [[wiki/context-engineering\|Context Engineering]] | Harness 管理 context 的方式決定 memory 的一切 | context, architecture | 2026-04-12 |
| [[wiki/memgpt\|MemGPT]] | 2023 UC Berkeley 論文，OS virtual memory 類比 LLM context，Letta 前身 | product, memory, architecture | 2026-04-12 |
| [[wiki/context-constitution\|Context Constitution]] | Letta 的原則集，定義 agent 如何管理 context 來學習 | memory, architecture | 2026-04-12 |
| [[wiki/sleep-time-compute\|Sleep-Time Compute]] | Agent 閒置時的背景記憶處理（dream cycle） | memory, architecture | 2026-04-12 |
| [[wiki/gbrain\|GBrain]] | Garry Tan 的個人知識庫系統，14,700+ files | product, memory, architecture | 2026-04-12 |
| [[wiki/context-fragment\|Context Fragment]] | Context window 中每個 loaded object 作為 harness 的顯式設計決策 | context, architecture, harness | 2026-04-13 |
| [[wiki/experiential-memory\|Experiential Memory]] | Agent 經驗記憶，可跨 instances 累積 | memory, architecture | 2026-04-13 |
| [[wiki/bitter-lesson-search\|Bitter Lesson (Search)]] | Agent 資料超指數成長下的搜尋挑戰 | retrieval, memory, architecture | 2026-04-13 |
| [[wiki/deep-agents\|Deep Agents]] | LangChain 開源 agent harness，model agnostic | product, harness | 2026-04-11 |
| [[wiki/letta\|Letta]] | Stateful agent 先驅（前 MemGPT），memory-first harness + benchmarks | product, memory | 2026-04-12 |
| [[wiki/harrison-chase\|Harrison Chase]] | LangChain CEO，主張 harness 與 memory 綁定、memory 應 open | people | 2026-04-11 |
| [[wiki/sarah-wooders\|Sarah Wooders]] | Letta CTO，MemGPT 共同作者，「memory isn't a plugin」提出者 | people, memory | 2026-04-12 |
| [[wiki/garry-tan\|Garry Tan]] | YC CEO，開發 GBrain，thin harness fat skills 哲學 | people | 2026-04-12 |
| [[wiki/viv-trivedy\|Viv Trivedy]] | Agent memory 和 harness 設計思考者，Context Fragment + Search Bitter Lesson | people | 2026-04-13 |
| [[wiki/mem0\|Mem0]] | Agent memory 基礎設施，selective pipeline + graph memory，ECAI 2025 | product, memory | 2026-04-13 |
| [[wiki/locomo\|LOCOMO]] | 第一個 long-term conversational memory 標準 benchmark | benchmark, memory | 2026-04-13 |
| [[wiki/graph-memory\|Graph Memory]] | Knowledge graph 記憶，relationship-based retrieval，2026 production-ready | memory, retrieval | 2026-04-13 |
| [[wiki/procedural-memory\|Procedural Memory]] | 第三種記憶：how to do things（技能、workflow、process） | memory, architecture | 2026-04-13 |
| [[wiki/multi-scope-memory\|Multi-Scope Memory]] | 四層 scope（user/agent/session/org）+ metadata filtering | memory, architecture | 2026-04-13 |
| [[wiki/memory-staleness\|Memory Staleness]] | 高 relevance 但過時的記憶，open problem | memory, architecture | 2026-04-13 |
| [[wiki/actor-aware-memory\|Actor-Aware Memory]] | Multi-agent 記憶來源追蹤，避免 inference cascade | memory, multi-agent | 2026-04-13 |
| [[wiki/filesystem-vs-database\|Filesystem vs Database]] | Agent memory 的 file interface vs DB 辯論 | memory, architecture | 2026-04-13 |
| [[wiki/memory-arena\|MemoryArena]] | Agentic memory benchmark，測跨 session 行動能力 | benchmark, memory | 2026-04-13 |
| [[wiki/agemem\|AgeMem]] | 統一 long/short-term memory 管理，RL 訓練 agent 自己學 | product, memory | 2026-04-13 |
| [[wiki/leonie\|Leonie]] | Filesystem vs database 辯論分析者 | people | 2026-04-13 |
| [[wiki/harness-engineering\|Harness Engineering]] | Agent integration points 工程，context engineering 的上層 | harness, architecture | 2026-04-13 |
| [[wiki/scaffolding-lifecycle\|Scaffolding Lifecycle]] | Scaffolding 有生命週期，模型變強時要拆 | harness, architecture | 2026-04-13 |
| [[wiki/philipp-schmid\|Philipp Schmid]] | HuggingFace，「2026 = Agent Harnesses 年代」 | people | 2026-04-13 |
| [[wiki/aaron-levie\|Aaron Levie]] | Box CEO，brutally unsentimental architecture | people | 2026-04-13 |
| [[wiki/autoreason\|Autoreason]] | A/B/AB tournament self-refinement，memory isolation by design | product, architecture | 2026-04-14 |
| [[wiki/shl0ms\|SHL0MS]] | Autoreason 作者，與 Hermes Agent 共同撰寫論文 | people | 2026-04-14 |
| [[wiki/memory-failure-modes\|Memory Failure Modes]] | 10 種常見記憶失敗模式，raw vs derived 根本張力 | memory, architecture | 2026-04-14 |
| [[wiki/memory-evaluation\|Memory Evaluation]] | Evaluation paradox + benchmark 演進 + four-layer metric stack | benchmark, memory | 2026-04-14 |
| [[wiki/chrysb\|Chrys Bader]] | 9 軸 memory 設計框架，262K views 的 practitioner 分析 | people | 2026-04-14 |
| [[wiki/yohei-nakajima\|Yohei Nakajima]] | BabyAGI 創造者，AI Memory 全景分析 | people | 2026-04-14 |
| [[wiki/chatgpt-memory\|ChatGPT Memory]] | 四層靜態注入架構，no RAG no vector DB | product, memory | 2026-04-14 |
| [[wiki/coding-agent-memory\|Coding Agent Memory]] | Cursor/Claude Code/Windsurf/Cline 記憶架構比較 | product, memory, architecture | 2026-04-14 |
| [[wiki/concept-map\|Concept Map]] | 三層架構 + 跨層主題 + 人物/產品索引 | architecture | 2026-04-14 |
| [[wiki/helix\|Helix]] | Self-healing runtime，Gene Map 用 Q-value RL 記住修復策略 | product, memory, architecture | 2026-04-15 |
| [[wiki/gene-map\|Gene Map]] | Helix 核心概念，Q-value 排序的修復策略知識庫 | memory, architecture, retrieval | 2026-04-15 |
| [[wiki/nicholas-dapanji\|Nicholas (@dapanji_eth)]] | Helix 共同創作者，Harvard/Princeton 校友 | people | 2026-04-15 |
| [[wiki/multimodal-memory\|Multimodal Memory]] | 非文字模態記憶（影像、音訊、影片、螢幕截圖） | memory, architecture | 2026-04-15 |
| [[wiki/mirix\|MIRIX]] | 六種記憶 + Active Retrieval + 多模態原生支持 | product, memory, architecture | 2026-04-15 |
| [[wiki/neuroscience-memory\|Neuroscience Memory]] | 認知神經科學 ↔ agent memory 對照 | memory, architecture | 2026-04-15 |
| [[wiki/synapse\|SYNAPSE]] | Spreading activation 記憶檢索，LoCoMo SOTA | product, memory, retrieval | 2026-04-15 |
| [[wiki/reconsolidation\|Reconsolidation]] | 檢索即改寫：retrieval 不應是 read-only | memory, architecture | 2026-04-15 |
| [[wiki/a-mem\|A-Mem]] | Zettelkasten-inspired memory evolution | product, memory, architecture | 2026-04-15 |
| [[wiki/ssgm\|SSGM]] | 記憶進化 governance framework，drift 理論保證 | product, memory, architecture | 2026-04-15 |
| [[wiki/multi-agent-memory\|Multi-Agent Memory]] | Multi-agent memory 核心頁：paradigm + hierarchy + protocols | memory, multi-agent, architecture | 2026-04-16 |
| [[wiki/memory-consistency\|Memory Consistency]] | Multi-agent memory 一致性問題 | memory, multi-agent, architecture | 2026-04-16 |
| [[wiki/collaborative-memory-system\|Collaborative Memory]] | Multi-user memory sharing + dynamic access control | product, memory, multi-agent, architecture | 2026-04-16 |
| [[wiki/open-questions\|Open Questions]] | 12 個未解問題 + 研究缺口 | memory, architecture | 2026-04-16 |

## Raw Sources

| Date | File | Title |
|------|------|-------|
| 2026-04-12 | [[raw/garry-tan-gbrain-deep]] | GBrain Deep Dive (Skillpack, Schema, Ethos) |
| 2026-04-12 | [[raw/garry-tan-gbrain]] | GBrain README |
| 2026-04-11 | [[raw/harrison-chase-your-harness-your-memory]] | Your Harness, Your Memory |
| 2026-04-03 | [[raw/sarah-wooders-memory-isnt-a-plugin]] | Why Memory Isn't a Plugin (It's the Harness) |
| 2026-04-02 | [[raw/letta-context-constitution]] | The Context Constitution |
| 2023-10-12 | [[raw/memgpt-paper-alphaxiv]] | MemGPT: Towards LLMs as Operating Systems (alphaxiv deep analysis) |
| 2026-04-13 | [[raw/viv-trivedy-harness-memory-bitter-lesson]] | Harness, Memory, Context Fragments, & the Bitter Lesson |
| 2023-10-12 | [[raw/memgpt-paper]] | MemGPT: Towards LLMs as Operating Systems (summary) |
| 2026-04-01 | [[raw/mem0-state-of-ai-agent-memory-2026]] | State of AI Agent Memory 2026 |
| 2026-01-19 | [[raw/leonie-filesystem-vs-database-debate]] | Filesystem vs Database Debate (tweet, 29.6K views) |
| 2026-02-19 | [[raw/dair-ai-memory-benchmarks-misleading]] | Memory Benchmarks Are Misleading — MemoryArena (tweet, 37.8K views) |
| 2026-01-12 | [[raw/elvis-agemem-unified-memory]] | AgeMem: Unified Memory via RL (tweet, 56.4K views) |
| 2026-04-12 | [[raw/shl0ms-autoreason]] | Autoreason: Self-Refinement That Knows When to Stop (208.6K views + GitHub) |
| 2026-04-12 | [[raw/chrysb-long-term-memory-unsolved]] | Why Long-Term Memory for LLMs Remains Unsolved (262.1K views) |
| 2026-03-08 | [[raw/pengfei-du-memory-survey-2026]] | Memory for Autonomous LLM Agents: Survey (arxiv 2603.07670) |
| 2025-08-28 | [[raw/yohei-nakajima-rise-of-ai-memory]] | The Rise of AI Memory (24.6K views) |
| 2025-12-09 | [[raw/manthan-gupta-chatgpt-memory-reverse-engineered]] | ChatGPT Memory Reverse Engineered (四層靜態注入) |
| 2026-04-15 | [[raw/garry-tan-gbrain-v0.10.0]] | GBrain v0.10.0 — 24 fat skills, perfected resolver, multi-user ACLs |
| 2026-04-14 | [[raw/nicholas-helix-self-healing-agents]] | AI Agents Have No Memory for Failure — Helix Self-Healing Runtime |
| 2026-04-14 | [[raw/coding-agents-memory-comparison]] | Coding Agent Memory Comparison (Cursor/Claude Code/Windsurf/Cline) |
| 2025-07-10 | [[raw/mirix-multiagent-memory-system]] | MIRIX: Multi-Agent Memory System for LLM-Based Agents (arxiv 2507.07957) |
| 2025-08 | [[raw/m3-agent-multimodal-long-term-memory]] | M3-Agent: Multimodal Agent with Long-Term Memory (arxiv 2508.09736) |
| 2025-12-29 | [[raw/ai-meets-brain-memory-survey]] | AI Meets Brain: Cognitive Neuroscience ↔ Agent Memory Survey (arxiv 2512.23343) |
| 2026-01-06 | [[raw/synapse-spreading-activation-memory]] | SYNAPSE: Spreading Activation Memory for LLM Agents (arxiv 2601.02744) |
| 2025-02-17 | [[raw/a-mem-agentic-memory]] | A-Mem: Agentic Memory for LLM Agents (arxiv 2502.12110) |
| 2026-03-14 | [[raw/ssgm-stability-safety-governed-memory]] | SSGM: Stability and Safety Governed Memory (arxiv 2603.11768) |
| 2026-03-13 | [[raw/yu-multi-agent-memory-architecture]] | Multi-Agent Memory from a Computer Architecture Perspective (arxiv 2603.10062) |
| 2025-05-23 | [[raw/rezazadeh-collaborative-memory]] | Collaborative Memory: Multi-User Memory Sharing with Dynamic Access Control (arxiv 2505.18279) |
