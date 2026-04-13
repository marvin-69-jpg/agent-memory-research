---
aliases: [brain-first lookup, brain first protocol]
first_seen: 2026-04-12
last_updated: 2026-04-12
tags: [retrieval, memory]
---

# Brain-First Lookup

GBrain 的查詢優先級：永遠先查 brain，external API 是 fallback。

## Current Understanding

- **四層 fallback**：
  1. Keyword search（fast, no embeddings needed, day one 就能用）
  2. Hybrid search（needs embeddings, semantic matches）→ [[hybrid-search]]
  3. Direct slug guess（fuzzy matching）
  4. External API（FALLBACK ONLY — 只有 brain 完全沒東西才到這步）
- **為什麼 brain first**：brain 有 relationship history, 你自己的 assessments, meeting transcripts, cross-references, timeline — 沒有任何 external API 能提供這些
- 「An agent that calls Brave Search before checking the brain is wasting money and giving worse answers.」
- 連「simple questions」也要先查 brain（< 100ms for keyword search, no cost）
- **實作觀察**：光把規則寫進 CLAUDE.md 不夠 — agent 在 context window 龐大時會 attention drift，跳過非核心指令。CLI 工具（`memory recall`）比 CLAUDE.md 規則更可靠，因為是顯式 tool call 而非隱式行為期望

## Key Sources

- **2026-04-12** — GBrain brain-first-lookup guide。Source: [[raw/garry-tan-gbrain-deep]]

## Implementation

### 2026-04-12 — 應用到 openab-bot auto-memory

- **做法**：加規則到 CLAUDE.md —— 回答問題前先 `grep -r` memory/ 目錄找相關記憶，不只靠 session 開頭讀的 MEMORY.md 索引。觸發條件：使用者問過去的事、提到可能有記憶的 entity、回答可能跟 feedback 衝突時。
- **簡化**：GBrain 有四層 fallback（keyword → hybrid → slug guess → external API），我們只做第一層 keyword grep。沒有 embedding、沒有 hybrid search。
- **PR**：追溯記錄在 marvin-69-jpg/agent-memory-research#1 comment
- **觀察**（2026-04-13）：在同日 session 中，被問到「研究資料讀得懂嗎」時，bot **沒有**先 grep memory/ 就直接回答。規則寫在 CLAUDE.md 但行為沒 100% 內化。可能原因：(1) 問題不像「之前怎麼做的」這類觸發條件，(2) 規則在 CLAUDE.md 太長容易被 attention 忽略。**結論：規則存在 ≠ 行為改變，需要 CLI 層面的強制觸發。**

### 2026-04-13 — `memory recall` CLI：搜尋範圍擴展到 wiki

- **做法**：新增 `memory recall <query>` subcommand，同時搜尋 memory/ 和 wiki/。按 keyword 頻率排序，輸出 compiled truth 摘要。把 brain-first lookup 從「只 grep memory/」擴展到「查整個 brain（memory + wiki）」。
- **PR**：marvin-69-jpg/agent-memory-research#12
- **觀察**：剛實作，待後續 session 觀察是否被使用

### 2026-04-13 — UserPromptSubmit Hook：每則訊息注入提醒

- **做法**：在 `~/.claude/settings.json` 加 `UserPromptSubmit` hook，每次使用者送訊息時自動注入 `additionalContext`，提醒 agent 先查 brain
- **機制**：hook 輸出 JSON 的 `hookSpecificOutput.additionalContext`，Claude Code 會把內容注入 agent 的 context，等同於每次都有「先查 brain」的 system-level 提醒
- **與 CLAUDE.md 規則的差異**：CLAUDE.md 規則在 context window 長了之後容易被 attention drift 忽略；hook 每次都重新注入，不受 window 位置影響
- **預期效果**：brain-first lookup 100% 執行率（從 benchmark 的 75% → 100%）
- **觀察**：待下次 benchmark 驗證

## Related

[[gbrain]] [[hybrid-search]] [[brain-agent-loop]] [[compounding-memory]]
