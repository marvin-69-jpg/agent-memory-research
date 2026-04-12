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
- **觀察**：首次跑在 22 個記憶上全 pass，表示之前的寫入品質不錯。下一步是排 cron 定期跑，或在 entity-detection 收尾時自動跑。

### memory-consolidate.py + memory-selfimprove.py（Phase 2 — 2026-04-12）

Phase 1 的 lint 只檢查格式。Phase 2 加入**語意層分析**：

- **`tools/memory-consolidate.py`** — 深度分析，找出：
  - 近似重複（description/body 相似度 > 60%）→ 建議合併
  - feedback 主題群聚（同 topic 2+ 條且 CLAUDE.md 沒涵蓋）→ 建議升級
  - 過時 project 記憶 → 建議 review/刪除
  - 缺失的 cross-reference → 建議補連結
- **`tools/memory-selfimprove.py`** — 整合 lint + consolidate 成一個簡潔報告，設計給 session 啟動時跑
  - 輸出分 FIX（當場修）/ MERGE / REVIEW / PROMOTE / NOTE
  - 附 health score（0-100）

**關鍵決策**：不做自動修改,只輸出報告讓 agent 判斷。原因：
- 合併記憶需要理解語意,script 只能找候選
- promote feedback 到 CLAUDE.md 需要判斷是否真的穩定
- 刪除過時記憶需要確認是否真的不再需要

**觸發方式**：寫進 CLAUDE.md + auto-memory,每個新 session 開始時自動跑。不是真的 cron,但效果一樣 — 每次對話記憶系統都比上次好。

**首次跑結果**（22 memories）：
- 1 個 PROMOTE：pepe topic（2 feedbacks）可考慮升級
- 1 個 NOTE：缺 user 類型記憶
- Health: 90/100

### 預計的後續 Phase

- **Phase 3**：自動執行 — 對 FIX 類問題直接修,不只是報告
- **Phase 4**：feedback → CLAUDE.md 回流的自動化 PR

## Related

[[context-constitution]] [[letta]] [[gbrain]] [[compounding-memory]] [[brain-agent-loop]]
