# Agent Memory Research — Index

> Auto-maintained by LLM. Do not edit manually.

## Wiki Pages

| Page | Summary | Tags | Last Updated |
|------|---------|------|-------------|
| [[wiki/agent-harness\|Agent Harness]] | Agent 的執行框架/腳手架，與 memory 密不可分，不會被模型吸收消失 | harness, architecture | 2026-04-12 |
| [[wiki/agent-memory\|Agent Memory]] | Agent 記憶系統，分短期/長期，三層模型（world/operational/session） | memory, architecture | 2026-04-12 |
| [[wiki/memory-lock-in\|Memory Lock-in]] | 封閉 harness 造成的記憶鎖定問題，memory 是 model provider 最強的 lock-in 武器 | lock-in, memory | 2026-04-11 |
| [[wiki/compounding-memory\|Compounding Memory]] | Agent 記憶的複合成長效應，每次互動累積知識，越用越聰明 | memory, architecture | 2026-04-12 |
| [[wiki/compiled-truth-pattern\|Compiled Truth Pattern]] | 知識頁面模式：compiled truth（可改寫）+ timeline（append-only） | memory, architecture | 2026-04-12 |
| [[wiki/hybrid-search\|Hybrid Search]] | Vector + keyword + RRF fusion 的記憶檢索策略 | retrieval, architecture | 2026-04-12 |
| [[wiki/context-engineering\|Context Engineering]] | Harness 管理 context 的方式決定了 memory 的一切：載入、compaction、存取 | context, architecture | 2026-04-11 |
| [[wiki/gbrain\|GBrain]] | Garry Tan 的個人知識庫系統，markdown + Postgres + pgvector，compounding memory 實踐 | product, memory, architecture | 2026-04-12 |
| [[wiki/deep-agents\|Deep Agents]] | LangChain 的開源 agent harness，model agnostic，支援 agents.md/skills 標準 | product, harness | 2026-04-11 |
| [[wiki/letta\|Letta]] | Stateful agent 先驅，CTO Sarah Wooders 提出「memory 不是 plugin 而是 harness」 | product, memory | 2026-04-11 |
| [[wiki/harrison-chase\|Harrison Chase]] | LangChain CEO，主張 harness 與 memory 綁定、memory 應該 open | people | 2026-04-11 |
| [[wiki/sarah-wooders\|Sarah Wooders]] | Letta CTO，「memory isn't a plugin, it's the harness」原始提出者 | people, memory | 2026-04-11 |
| [[wiki/garry-tan\|Garry Tan]] | Y Combinator CEO，開發 GBrain，實踐 compounding memory | people | 2026-04-12 |

## Raw Sources

| Date | File | Title |
|------|------|-------|
| 2026-04-12 | [[raw/garry-tan-gbrain]] | GBrain README |
| 2026-04-11 | [[raw/harrison-chase-your-harness-your-memory]] | Your Harness, Your Memory |
