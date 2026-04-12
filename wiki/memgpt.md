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
  - Main Context（在 context window 內）：system prompt + working context（可讀寫 scratchpad）+ 近期對話（FIFO）
  - External Context（context window 外）：recall storage（完整對話歷史）+ archival storage（持久知識庫）
- **Self-directed memory**：不像 RAG 由 user query 觸發 retrieval，MemGPT 給 agent tools 讓它自己決定：
  - 什麼留在 working context
  - 什麼 page out 到 archival
  - 什麼時候 search recall/archival
  - 怎麼更新自己的 instructions
- **Interrupts**：借用 OS 中斷概念，管理 agent 與 user 之間的 control flow
- **評估**：document analysis（200+ 頁文件）和 multi-session chat 兩個場景都顯著優於 fixed-context baseline
- 論文的關鍵洞察 — memory management 應是 agent 的責任而非外部 plugin — 直接影響了 [[sarah-wooders]] 後來的「memory is the harness」論點
- 作者：Charles Packer、[[sarah-wooders|Sarah Wooders]] 等（UC Berkeley）

## Key Sources

- **2023-10-12** — MemGPT 原始論文。Source: [[raw/memgpt-paper]]

## Related

[[letta]] [[sarah-wooders]] [[agent-memory]] [[context-engineering]] [[agent-harness]]
