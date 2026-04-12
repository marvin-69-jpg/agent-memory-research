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
| Compiled truth + Timeline | GBrain, boba-wiki | boba-wiki 已實踐 ✅ | 推廣到其他 wiki |
| Brain-first lookup | GBrain | 未實作 ❌ | 回答前先查 wiki/memory |
| Entity detection | GBrain | 未實作 ❌ | 對話中自動偵測 entity 並更新 wiki |
| Sleep-time compute | GBrain, Letta | 未實作 ❌ | 背景 enrichment / consolidation |
| Memory portability | Harrison Chase | markdown-based ✅ | 維持 open format |
| Three-layer memory | GBrain | 部分（auto-memory + boba-wiki） | 明確區分 world / operational / session |

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
