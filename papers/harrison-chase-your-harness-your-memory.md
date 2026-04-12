# Your Harness, Your Memory

- **作者**: Harrison Chase（LangChain CEO）
- **日期**: 2026-04-11
- **來源**: https://x.com/hwchase17/status/2042978500567609738
- **引用**: Sarah Wooders（Letta CTO）的 blog "Memory isn't a plugin, it's the harness"

---

## 核心論點

**Agent harness 與 memory 密不可分。如果你用了封閉的 harness（尤其是放在 proprietary API 後面的），你就把 memory 的控制權交給了第三方。Memory 應該是 open 的。**

## 重點摘要

### 1. Agent harness 不會消失
- 2023 → simple RAG chains（LangChain）
- 模型變好 → complex flows（LangGraph）
- 模型更好 → agent harnesses（Claude Code、Deep Agents、Codex、Letta Code 等）
- 有人覺得模型會吸收掉 scaffolding，但事實是舊 scaffolding 消失、新 scaffolding 出現
- 證據：Claude Code 被洩漏時有 512k 行 code — 那就是 harness
- API 背後的 web search 等功能也不是「模型的一部分」，而是輕量 harness 在做 tool calling

### 2. Harness 跟 memory 綁在一起
- 引用 Sarah Wooders：「要求把 memory 插進 agent harness，就像要求把駕駛插進一台車」
- Memory 就是一種 context：
  - **短期記憶**：對話中的 messages、大型 tool call 結果 → harness 管理
  - **長期記憶**：跨 session 記憶 → harness 負責讀寫
- Harness 決定了記憶的一切細節：
  - AGENTS.md / CLAUDE.md 怎麼載入 context？
  - Skill metadata 怎麼呈現？
  - Agent 能不能改自己的 system instructions？
  - Compaction 後什麼留下、什麼消失？
  - 互動紀錄有沒有被存起來、能不能查詢？

### 3. 不擁有 harness = 不擁有 memory（三層嚴重程度）

| 程度 | 情境 | 問題 |
|------|------|------|
| Mildly bad | 用 stateful API（OpenAI Responses API、Anthropic server-side compaction） | State 存在他們 server，換模型就斷了 |
| Bad | 用 closed harness（如 Claude Agent SDK，底層是非開源的 Claude Code） | 不知道 harness 怎麼跟 memory 互動，格式不透明、不可轉移 |
| **Worst** | **整個 harness + long-term memory 都在 API 後面** | 零控制權、零可見性，連 memory 都不是你的 |

### 4. Memory 是 lock-in 的終極武器
- **沒有 memory 的 agent 任何人都能複製**（只要有同樣的 tools）
- 有了 memory → proprietary dataset → 差異化體驗 → 越用越好
- 模型 API 之間切換很容易（stateless），但一旦有 state 就被綁住了
- Harrison 的親身經歷：內部 email assistant 被意外刪除，重建後體驗大幅退步，才意識到 memory 有多黏

### 5. 解法：Open Memory, Open Harnesses
- Memory（及 harness）應該跟 model provider 分離
- LangChain 的答案：**Deep Agents**
  - 開源
  - Model agnostic
  - 用 open standards（agents.md、skills）
  - 有 Mongo / Postgres / Redis 等 memory store plugins
  - 可部署在任何雲、可自帶 database

---

## 關鍵引用

> "Asking to plug memory into an agent harness is like asking to plug driving into a car. Managing context, and therefore memory, is a core capability and responsibility of the agent harness." — Sarah Wooders

> "Without memory, your agents are easily replicable by anyone who has access to the same tools."

> "If you use a closed harness, especially if it's behind an API, you don't own your memory."

> "Memory will become locked into a single platform, a single model."

---

## 提到的工具 / 專案

| 名稱 | 類型 | 連結 |
|------|------|------|
| Claude Code | Closed harness | code.claude.com |
| Deep Agents | Open harness (LangChain) | github.com/langchain-ai/deepagents |
| Codex | Open harness (OpenAI) | openai.com/codex |
| Letta Code | Open harness | letta.com/blog/letta-code |
| OpenCode | Open harness | opencode.ai |
| Pi (OpenClaw) | Harness | github.com/badlogic/pi-mono |
| Claude Managed Agents | Closed platform | platform.claude.com |
| Fleet | LangChain no-code platform | langchain.com/langsmith/fleet |

## 相關人物
- **Sarah Wooders** — Letta CTO，寫了 "Memory isn't a plugin" blog
- **Sydney Runkle** — Deep Agents & memory work
- **Viv Trivedy** — Agent harnesses 觀點領袖
- **Nuno Campos** — Context engineering for finance agents
