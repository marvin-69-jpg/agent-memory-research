---
aliases: [sleep-time compute, dream cycle, background memory processing]
first_seen: 2026-04-12
last_updated: 2026-04-12
tags: [memory, architecture]
---

# Sleep-Time Compute

Agent 在閒置時進行的背景記憶處理 — 重寫 memory state、enrichment、consolidation。在不同系統中有不同名稱但概念一致。

## Current Understanding

- **Letta 的 sleep-time compute**：讓 model 在 downtime「思考」，處理資訊、形成新連結、重寫 memory state。是 scaling AI capabilities 的新方式
- **GBrain 的 dream cycle**：agent 在使用者睡覺時自動跑 enrichment、修 citation、consolidate memory。「I wake up and the brain is smarter than when I went to sleep.」
  - 實作：20+ cron jobs 跑在不同時段（nightly enrichment, weekly lint, etc.）
- **共同點**：
  - 利用 agent 閒置時間做非即時工作
  - 記憶的品質在背景持續提升
  - 使用者不需要主動觸發
- 這個概念跟人類睡眠中的記憶 consolidation 有類比 — 白天收集的資訊在睡眠中被整合到長期記憶

## Key Sources

- **2026-04-02** — Letta Context Constitution 提出 sleep-time compute。Source: [[raw/letta-context-constitution]]
- **2026-04-12** — GBrain 的 dream cycle 實作。Source: [[raw/garry-tan-gbrain-deep]]

## Implementation

### memory-lint.py（Phase 1 — 2026-04-12）

Sleep-time compute 最簡單的起步：定期 lint 記憶品質。

- **位置**：`tools/memory-lint.py`
- **檢查項目**：
  - Frontmatter 欄位完整性（name/description/type 必填）
  - type 值合法性（user/feedback/project/reference）
  - MEMORY.md ↔ 實際檔案同步（孤兒檔、斷連 pointer）
  - feedback/project 缺少 Why/How to apply
  - project 記憶超過 14 天未更新（可能過時）
  - 近似重複偵測（description 相似度 > 70%）
- **跑法**：`uv run python3 tools/memory-lint.py [--memory-dir PATH]`
- **觀察**（2026-04-13）：首次跑在 22 個記憶上全 pass。但後續 session（04-13）**沒有在 session 開頭跑 `memory improve`**，儘管 CLAUDE.md 和 feedback memory 都有寫這條規則。原因同 brain-first-lookup：規則存在 ≠ 行為改變。MEMORY.md 的 feedback 被 Claude Code 自動注入 context，但 agent 不一定會遵守裡面的每條指令。**結論：session 開頭的 self-improvement 需要更強的觸發機制（如 hook），或在 `memory brief` 裡整合 improve 輸出。**

### SessionStart Hook（Phase 1.5 — 2026-04-13）

CLAUDE.md 規則和 feedback memory 都沒能讓 agent 在 session 開頭跑 `memory improve`。改用基礎設施層面的 enforcement：

- **做法**：在 `~/.claude/settings.json` 加 `SessionStart` hook，自動執行 `uv run python3 tools/memory.py improve`
- **機制**：Claude Code 在 session 建立時觸發 hook，不依賴 agent 的意願或 attention
- **預期效果**：sleep-time compute 100% 執行率（從 benchmark 的 50% → 100%）
- **觀察**：待下次 benchmark 驗證

### 預計的後續 Phase

- **Phase 2**：memory consolidation — 合併重複記憶、更新過時 project 記憶
- **Phase 3**：feedback → CLAUDE.md 回流 — 穩定 pattern 升級為正式規則
- **Phase 4**：cross-link enrichment — 掃記憶之間該互相引用但沒有的

## Related

[[context-constitution]] [[letta]] [[gbrain]] [[compounding-memory]] [[brain-agent-loop]]
