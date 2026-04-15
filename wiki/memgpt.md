---
aliases: [MemGPT, Memory-GPT, virtual context management]
first_seen: 2023-10-12
last_updated: 2026-04-12
tags: [product, memory, architecture]
---

# MemGPT

2023 年 UC Berkeley 的開創性論文，將 OS virtual memory 概念類比到 LLM context 管理。後來演化為 [[letta|Letta]]。

## Current Understanding

- **核心類比**：LLM context window = RAM（快但小）、external storage = disk（大但慢），MemGPT = memory management unit
- **分層記憶**：
  - Main Context（在 context window 內）：
    - System Instructions（read-only）— control flow rules + function descriptions
    - Working Context（read/write）— 固定大小 scratchpad，存 key facts 和 preferences
    - FIFO Queue（read/write）— 滾動訊息歷史，滿了就 summarize + evict
  - External Context（context window 外）：
    - Recall Storage — 完整對話歷史 database，可搜尋
    - Archival Storage — 通用讀寫 database，支援 vector embedding 搜尋
- **Self-directed memory**：不像 RAG 由 user query 觸發 retrieval，MemGPT 給 agent function call tools（`working_context.append/replace`, `recall_storage.search`, `archival_storage.search`）讓它自己管自己的 context
- **Control flow**：
  - Queue Manager：監控 token count，70% 時發 memory pressure alert，100% 時 recursive summarize + evict
  - Function Executor：解析 LLM output 的 function calls，執行並回饋結果
  - Event-based：user messages, system alerts, timed events 都觸發 inference
  - Function Chaining：`request_heartbeat=true` 允許 multi-step operations（不用等 external event）
- **評估結果**：
  - Multi-session chat：GPT-4 + MemGPT 達 92.5% accuracy（baseline 只有 32.1%），opener 品質接近甚至超越人寫
  - Document QA：MemGPT 的效能不受 document 數量影響（baseline 因 truncation 退化）
  - Nested KV Retrieval：MemGPT + GPT-4 是唯一能在 3+ nesting levels 保持效能的系統
- 論文的關鍵洞察 — memory management 應是 agent 的責任而非外部 plugin — 直接影響了 [[sarah-wooders]] 後來的「memory is the harness」論點
- 作者：Charles Packer、[[sarah-wooders|Sarah Wooders]]、Kevin Lin、Vivian Fang、Shishir G. Patil、Ion Stoica、Joseph E. Gonzalez（UC Berkeley）
- **學術意義**：首次將 OS virtual memory 概念系統性地應用到 LLM context management，bridging AI 和 systems architecture 兩個領域

- **LOCOMO benchmark 表現**：MemGPT 被納入 Mem0 的 10 種方法 benchmark（ECAI 2025），作為 literature baseline 之一。具體數據未公開單獨列出，但低於 Mem0/Zep/OpenAI Memory（後三者 52.9%~66.9%）

## Key Sources

- **2026-04-01** — 被納入 Mem0 LOCOMO benchmark 的 10 種方法之一。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]
- **2023-10-12** — MemGPT 原始論文（alphaxiv structured overview）。Source: [[raw/memgpt-paper-alphaxiv]]
- **2023-10-12** — MemGPT 論文摘要筆記。Source: [[raw/memgpt-paper]]

## Related

[[letta]] [[sarah-wooders]] [[agent-memory]] [[context-engineering]] [[agent-harness]] [[mem0]] [[locomo]] [[memory-evaluation]] [[context-constitution]]
