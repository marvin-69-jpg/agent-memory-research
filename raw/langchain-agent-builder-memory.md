---
source_type: blog
url: https://www.langchain.com/conceptual-guides/how-we-built-agent-builders-memory
title: "How we built Agent Builder's memory system"
authors: [Harrison Chase]
affiliations: [LangChain]
date: 2026-02-01
discovered_via: "X/Twitter — Harrison Chase (@hwchase17)"
ingested: 2026-04-17
tags: [production, memory, architecture, filesystem]
---

# How We Built Agent Builder's Memory System

## 概述

LangChain 的 Agent Builder（現 LangSmith Fleet）的 memory 系統實作細節。用 COALA paper 的三種記憶分類，Postgres 上架虛擬 filesystem，所有 memory 修改需 human-in-the-loop 審核。核心教訓：**prompting 是最難的部分**。

## Memory Types（COALA mapping）

1. **Procedural Memory**：`AGENTS.md` + `tools.json` — agent 的行為規則
2. **Semantic Memory**：agent skills + knowledge files — 世界知識
3. **Episodic Memory**：**刻意跳過**。認為 task agent 不需要，計畫未來加（把過去對話當 filesystem 暴露）

## 架構

### Virtual Filesystem over Postgres

- 不用真的 filesystem，用 Postgres + wrapper 暴露成 file interface
- LLM 很會操作 filesystem pattern
- Database 提供 scalability + operational 優勢
- DeepAgents 支援 pluggable storage backends（S3, MySQL 等）

### Memory Files

- `AGENTS.md`：核心指令集
- `tools.json`：MCP 配置（限制子集防 context overflow）
- Agent Skills：專門任務指令
- Subagent Definitions：模仿 Claude Code 架構
- User-generated knowledge files：任意 markdown/JSON

## Memory Update 機制

### In-the-Hot-Path

Agent 在 active session 中直接修改 memory files。例如 LinkedIn recruiter agent 維護 JD 文件和 subagent configs。

### Human-in-the-Loop

**所有 memory 修改都需要 human approval** — 主要防 prompt injection。可開 "yolo mode" 跳過。

### Validation Layer

Typed files 有 schema validation（tools.json MCP validity、skill frontmatter）。Invalid files 觸發 LLM error handling。

## 生產教訓

### 1. Prompting 是最難的

> "the hardest part of building an agent that could remember things is prompting"

有一個全職工程師專門做 memory prompting。常見失敗：
- Agent 記不住該記的東西
- 寫到錯誤的 file 位置
- 格式違規
- 不理解 skill 文檔結構

### 2. Agents 不會自動 compact

Agent 很會 append 具體事實，但**不擅長 compact learnings**。例如列出每個 vendor 名字，而不是歸納成通則。

解法：
- End-of-session reflection prompts
- `/remember` 指令（計畫中）
- 背景 daily process review conversations + update memory

### 3. 使用者的明確指示仍然有用

即使 agent 有自動 update 能力，使用者明確說「reflect on this conversation and update memory」仍然有價值。特別是 agent 記了 specific cases 但沒有 generalize 的時候。

### 4. Iterative development 比 upfront config 好

用自然語言糾正 agent → agent 更新 AGENTS.md → 漸進式累積。例子：meeting summarizer agent 從簡單 prompt 開始，三個月後累積出 formatting preferences、meeting-type handling、participant-specific protocols — 全靠反覆反饋，不需手動設定。

## 計畫中的改進

1. Episodic memory（歷史對話存取）
2. Background processes（異步 memory reflection + consolidation）
3. Semantic search（超越 grep/glob）
4. Multi-level memory（user-scope + org-scope）

## 與研究的對照

| 生產發現 | 對應研究概念 |
|---|---|
| Prompting 最難 | Memory-R1 用 RL 取代 prompting → 152 examples 就夠 |
| 不會自動 compact | MEM1 用 context pruning 強迫 consolidation |
| Human-in-the-loop 所有 memory | SSGM 的 governance — 不是所有 update 都該被允許 |
| Virtual filesystem over DB | Markdown convergence — file interface wins |
| 跳過 episodic memory | GAM 的 EPG 說短期暫存很重要 |
| End-of-session reflection | Sleep-time compute / GAM 的 topic-switch consolidation |
| Iterative natural language correction | DeltaMem 的 outcome-driven learning |
