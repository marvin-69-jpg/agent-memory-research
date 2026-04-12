# Agent Memory Research

## 專案目標

這不只是文獻整理 — 是**邊研究邊實作**的專案。

我們（openab-bot + minghua）同時在做兩件事：
1. **研究**：收集、整理 agent memory 領域的文章、論文、開源專案，建成 Obsidian wiki
2. **實作**：把學到的東西實際應用到 openab-bot 自己的記憶系統上（auto-memory、boba-wiki 等）

openab-bot 本身就是一個有 memory 的 agent — 我們是用自己當實驗對象。

## 目前已識別的可改進方向

從研究中學到、可以應用到 openab-bot 的 pattern：

| Pattern | 來源 | 現狀 | 目標 |
|---------|------|------|------|
| Compiled truth + Timeline | GBrain, boba-wiki | boba-wiki 已實踐 ✅ | auto-memory 不需要（git history 就是 timeline） |
| Brain-first lookup | GBrain | **實作中 🔧** | 回答前先 grep memory/ 找相關記憶 |
| Entity detection | GBrain | **實作中 🔧** | 對話結束前掃一遍漏存的 entity |
| Sleep-time compute | GBrain, Letta | 未實作 ❌ | 背景 enrichment / consolidation |
| Memory portability | Harrison Chase | markdown-based ✅ | 維持 open format |
| Three-layer memory | GBrain | 部分（auto-memory + boba-wiki） | 明確區分 world / operational / session |

## 已實作的改進

### Brain-First Lookup（2026-04-12）

**規則**：當使用者問的問題可能跟過去的工作、決策、偏好、或已知資訊有關時，先 `grep -r` memory/ 目錄找相關記憶，再回答。不要只靠 session 開頭讀的 MEMORY.md 索引。

**觸發條件**（命中任一條就查）：
- 使用者問「之前怎麼做的」「上次說過什麼」
- 使用者提到某個 project / 人名 / 工具，你不確定有沒有相關記憶
- 你要回答的內容可能跟過去的 feedback 衝突

**查法**：`grep -rl "<關鍵字>" /home/node/.claude/projects/-home-node/memory/`，命中的檔案讀來看。

**來源**：[[wiki/brain-first-lookup]] — GBrain 的核心 pattern，永遠先查 brain，external 是 fallback。

**為什麼 compiled truth + timeline 不需要**：auto-memory 每次修改都有 git commit，`git log` 就是天然的 timeline。再加 append-only section 是多餘的。

### Entity Detection（2026-04-12）

**規則**：對話快結束時（使用者說謝謝 / 沒有後續 / 明確收尾），主動掃一遍整段對話，檢查有沒有該存但漏存的 entity。

**掃什麼**：
- **人**：使用者提到的人名、角色、他們在做什麼（→ `user_xxx.md`）
- **專案**：新的 project、deadline、決策背景（→ `project_xxx.md`）
- **偏好 / 決策**：使用者確認或否定的做法，但你沒即時存到 feedback（→ `feedback_xxx.md`）
- **外部資源**：被提到的 URL、repo、工具、文件位置（→ `reference_xxx.md`）

**怎麼掃**：回顧對話，問自己「如果下一個 session 的我遇到類似情境，會需要知道什麼？」。只存從 code / git log 看不出來的東西。

**注意**：這不是取代即時存記憶 —— feedback 被糾正時還是要**立刻存**。Entity detection 是收尾時的 safety net，抓漏網之魚。

**來源**：[[wiki/entity-detection]] — GBrain 每個 message 都跑 entity detection，我們簡化為對話結束時批次掃一遍。

## 專案結構

```
raw/           ← 原始文章全文（immutable）
wiki/          ← LLM 維護的 entity pages（Obsidian 格式）
schema/        ← wiki ingest/query/lint 規則
index.md       ← wiki 目錄
log.md         ← 操作記錄
.claude/skills/ ← browser, ingest, arxiv skills
```

## 工作方式

- 使用者丟 URL / paper → bot 用 agent-browser 或 alphaxiv 讀取 → 存 raw → 拆 wiki pages → cross-link → commit & push
- GitHub repo 用 Obsidian 打開可看 graph view
- 研究過程中發現可實作的改進 → 記錄到上面的表格 → 另外在 openab-bot 的系統上實作

## 規則

- Wiki 詳細規則見 `schema/CLAUDE.md`
- 一律用 agent-browser 讀 URL（不用 curl hack / WebFetch）
- arxiv 論文用 alphaxiv skill（`curl -sL "https://www.alphaxiv.org/overview/{PAPER_ID}.md"`）
- GitHub repo 需要深讀時 clone 下來讀 docs/
- 繁體中文，技術名詞保留英文
