---
aliases: [coding agent memory, IDE memory, 程式助手記憶]
first_seen: 2026-04-14
last_updated: 2026-04-14
tags: [product, memory, architecture]
---

# Coding Agent Memory

2025-2026 年 coding agent（Cursor、Claude Code、Windsurf、Cline）的記憶架構比較。Coding agent 是目前 agent memory 最大的使用場景。

## Current Understanding

### 四大 coding agent 記憶架構

| Agent | Memory 媒介 | Retrieval 模式 | 學習方式 | Curator |
|---|---|---|---|---|
| **Claude Code** | MEMORY.md + CLAUDE.md | Always-inject index + on-demand grep | 無主動學習（user 寫 MEMORY.md） | User |
| **Cursor** | .cursorrules + .cursor/rules/*.mdc | Agent 自己選擇讀哪些 file | User 寫 rules + learned-memories hack | User + Agent |
| **Windsurf** | Cascade Memories（自動學習） | Auto-inject learned patterns | 自動從使用行為學習 pattern | System |
| **Cline** | Memory Bank（方法論，手動 markdown） | 強制 session 開始時全讀 | User 維護 memory bank files | User |

### 共同點：File-based Memory

四個 coding agent 全部收斂在 **file-based memory** — markdown 檔案，可 version control、可人類編輯、可 agent 讀取。這驗證了 [[filesystem-vs-database]] 辯論中 file camp 在 coding agent 場景的優勢：
- 開發者已經熟悉 file 操作
- Git 提供天然的 timeline / versioning
- 透明、可審計、可 diff

### 分歧點：Who Curates × When Retrieval

| | Always-injected | On-demand | Auto-learned |
|---|---|---|---|
| **User curates** | Cline（強制全讀） | — | — |
| **User + Agent** | Claude Code（index 全注入） | Cursor（agent 選擇性讀） | — |
| **System curates** | — | — | Windsurf（自動學習 + 注入） |

用 [[chrysb]] 的 axis 7 框架分析：
- **Always-injected**（Claude Code、Cline）：保證記憶可用，但 pollutes context
- **Tool-driven**（Cursor）：respects agent judgment，但 agent 不知道它不知道什麼
- **Auto-learned**（Windsurf）：最接近 [[compounding-memory]] 的理想，但黑盒

### Claude Code 深入

Source code analysis 揭示三層設計：
1. **MEMORY.md 索引**：永遠載入，只存 pointer（~150 chars/line），200 行硬上限
2. **grep-based 搜尋**：從 live codebase 即時撈資料
3. **Chyros daemon（未上線）**：background embedding indexing + stale memory cleanup

設計哲學：Memory 是 **coordination**（定義何時問確認、何時直接做），不是記對話。

### Cursor 的 Learned Memories Hack

使用者 @elie2222 的做法：建一個 `learned-memories.mdc` rule，instruction = "完成 task 後把犯過的錯寫進這個檔"。下次 session 自動載入。

這是 [[procedural-memory]] 的人工實現 — agent 累積 "how to do things" 的記憶，但需要 user 設定觸發機制。

### Enterprise 部署現實

- **62% 公司實驗 AI agents，只有 14% 達到 production-ready**（McKinsey）
- 最常見失敗：**context blindness** — agents 只吃到 10-20% 企業資料（structured ERP/CRM），80%+ contracts/emails/policies 看不到
- Windsurf enterprise 有 team-level shared memories — [[multi-scope-memory]] 的 org 層級實踐

### OSS Agent Memory 競爭（2026 Q1）

| System | 特點 | Trade-off |
|---|---|---|
| MemPalace（ByteDance） | 壓縮層 | 壓縮掉 12.4 分 benchmark |
| engram（Go + SQLite） | Single binary，部署簡單 | 功能有限 |
| OpenViking | Tiered context loading | 需要 heavy infra（Go + Python + C++） |

**核心未解問題**：沒有系統能同時做到 general-purpose memory + domain optimization + minimal deployment + longitudinal reliability。

## Key Sources

- **2026-04** — 多來源 coding agent memory 架構比較。Source: [[raw/coding-agents-memory-comparison]]
- **2025-08-28** — Yohei Nakajima 開發者工具生態整理。Source: [[raw/yohei-nakajima-rise-of-ai-memory]]

## Related

[[agent-memory]] [[filesystem-vs-database]] [[chrysb]] [[memory-failure-modes]] [[compounding-memory]] [[procedural-memory]] [[multi-scope-memory]] [[chatgpt-memory]] [[thin-harness-fat-skills]] [[context-engineering]] [[memory-lock-in]]
