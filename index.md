# Agent Memory Research — Index

> Auto-maintained by LLM. Do not edit manually.

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
| [[wiki/deep-agents\|Deep Agents]] | LangChain 開源 agent harness，model agnostic | product, harness | 2026-04-11 |
| [[wiki/letta\|Letta]] | Stateful agent 先驅（前 MemGPT），memory-first harness + benchmarks | product, memory | 2026-04-12 |
| [[wiki/harrison-chase\|Harrison Chase]] | LangChain CEO，主張 harness 與 memory 綁定、memory 應 open | people | 2026-04-11 |
| [[wiki/sarah-wooders\|Sarah Wooders]] | Letta CTO，MemGPT 共同作者，「memory isn't a plugin」提出者 | people, memory | 2026-04-12 |
| [[wiki/garry-tan\|Garry Tan]] | YC CEO，開發 GBrain，thin harness fat skills 哲學 | people | 2026-04-12 |

## Raw Sources

| Date | File | Title |
|------|------|-------|
| 2026-04-12 | [[raw/garry-tan-gbrain-deep]] | GBrain Deep Dive (Skillpack, Schema, Ethos) |
| 2026-04-12 | [[raw/garry-tan-gbrain]] | GBrain README |
| 2026-04-11 | [[raw/harrison-chase-your-harness-your-memory]] | Your Harness, Your Memory |
| 2026-04-03 | [[raw/sarah-wooders-memory-isnt-a-plugin]] | Why Memory Isn't a Plugin (It's the Harness) |
| 2026-04-02 | [[raw/letta-context-constitution]] | The Context Constitution |
| 2023-10-12 | [[raw/memgpt-paper-alphaxiv]] | MemGPT: Towards LLMs as Operating Systems (alphaxiv deep analysis) |
| 2023-10-12 | [[raw/memgpt-paper]] | MemGPT: Towards LLMs as Operating Systems (summary) |
