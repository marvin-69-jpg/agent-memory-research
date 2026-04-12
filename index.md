# Agent Memory Research — Index

> Auto-maintained by LLM. Do not edit manually.

## Wiki Pages

| Page | Summary | Tags | Last Updated |
|------|---------|------|-------------|
| [[wiki/agent-harness\|Agent Harness]] | Agent 的執行框架/腳��架，與 memory 密不可分，不會被模型吸收消失 | harness, architecture | 2026-04-12 |
| [[wiki/agent-memory\|Agent Memory]] | Agent 記���系統���分短期/長期，三層模型（world/operational/session） | memory, architecture | 2026-04-12 |
| [[wiki/memory-lock-in\|Memory Lock-in]] | 封閉 harness 造成的記憶鎖定問題，memory 是 model provider 最強的 lock-in 武器 | lock-in, memory | 2026-04-11 |
| [[wiki/compounding-memory\|Compounding Memory]] | Agent 記憶��複合成長效應，每次互動累積知識，越用越聰明 | memory, architecture | 2026-04-12 |
| [[wiki/compiled-truth-pattern\|Compiled Truth Pattern]] | 知識頁面模式：compiled truth（可改寫）+ timeline（append-only） | memory, architecture | 2026-04-12 |
| [[wiki/thin-harness-fat-skills\|Thin Harness, Fat Skills]] | Garry Tan 的架構哲學：intelligence 在 skills，harness 保持 thin | architecture, harness | 2026-04-12 |
| [[wiki/brain-agent-loop\|Brain-Agent Loop]] | Signal→Detect→Read→Respond→Write→Sync 的核心運作 loop | memory, architecture | 2026-04-12 |
| [[wiki/brain-first-lookup\|Brain-First Lookup]] | 永遠先查 brain，external API 是 fallback | retrieval, memory | 2026-04-12 |
| [[wiki/entity-detection\|Entity Detection]] | 每個 message 自動偵測 entity 和 original thinking | memory, architecture | 2026-04-12 |
| [[wiki/enrichment-pipeline\|Enrichment Pipeline]] | 三層 tier 分配 API 資���，facts are table stakes, texture is the value | memory, architecture | 2026-04-12 |
| [[wiki/mece-resolver\|MECE Resolver]] | 每塊知識有唯一 primary home，resolver decision tree 決定放哪 | architecture, memory | 2026-04-12 |
| [[wiki/hybrid-search\|Hybrid Search]] | Vector + keyword + RRF fusion 的記憶檢索策略 | retrieval, architecture | 2026-04-12 |
| [[wiki/context-engineering\|Context Engineering]] | Harness 管理 context 的方式決定 memory 的一切，Resolver 是 routing table | context, architecture | 2026-04-12 |
| [[wiki/gbrain\|GBrain]] | Garry Tan 的個人知識庫系統，14,700+ files，compounding memory 實踐 | product, memory, architecture | 2026-04-12 |
| [[wiki/deep-agents\|Deep Agents]] | LangChain 的開源 agent harness��model agnostic，支援 agents.md/skills 標準 | product, harness | 2026-04-11 |
| [[wiki/letta\|Letta]] | Stateful agent 先驅，CTO Sarah Wooders 提出「memory 不是 plugin 而是 harness」 | product, memory | 2026-04-11 |
| [[wiki/harrison-chase\|Harrison Chase]] | LangChain CEO，主張 harness 與 memory 綁��、memory 應該 open | people | 2026-04-11 |
| [[wiki/sarah-wooders\|Sarah Wooders]] | Letta CTO，「memory isn't a plugin, it's the harness」原始提出者 | people, memory | 2026-04-11 |
| [[wiki/garry-tan\|Garry Tan]] | YC CEO，開發 GBrain，提出 thin harness fat skills 哲學 | people | 2026-04-12 |

## Raw Sources

| Date | File | Title |
|------|------|-------|
| 2026-04-12 | [[raw/garry-tan-gbrain-deep]] | GBrain Deep Dive (Skillpack, Schema, Ethos) |
| 2026-04-12 | [[raw/garry-tan-gbrain]] | GBrain README |
| 2026-04-11 | [[raw/harrison-chase-your-harness-your-memory]] | Your Harness, Your Memory |
