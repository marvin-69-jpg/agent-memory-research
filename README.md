# Agent Memory Research

> 邊研究邊實作 — 收集 agent memory 文獻，整理成 Obsidian wiki，同時把學到的 pattern 應用到自己身上。

我們（[openab-bot](https://github.com/marvin-69-jpg/openab) + minghua）用 LLM 維護的知識庫研究 agent memory 領域。
openab-bot 本身就是一個有 memory 的 agent — 我們是用自己當實驗對象。

## Repo 結構

```
agent-memory-research/
 |
 |-- raw/              原始文章全文（immutable，不可改）
 |-- wiki/             LLM 維護的 entity pages（知識庫）
 |-- schema/           ingest / query / lint 規則
 |-- tools/            CLI 工具（memory CLI）
 |-- index.md          wiki 目錄 + 一句話摘要
 |-- log.md            操作記錄（append-only）
 |-- CLAUDE.md         專案規則 + 已實作的改進
 +-- .claude/skills/   browser, ingest, arxiv skills
```

## 研究 → 實作閉環

這不只是文獻整理。每個從文獻學到的 pattern，我們會實際應用到 openab-bot 的記憶系統，
然後把實作經驗回流到 wiki，形成閉環：

```
                         +------------------+
                         |   外部文獻 / URL  |
                         +--------+---------+
                                  |
                          agent-browser 讀取
                                  |
                                  v
                         +------------------+
                         |    raw/ 全文儲存   |  <-- immutable, 只讀不改
                         +--------+---------+
                                  |
                          Extract + Plan
                                  |
                                  v
+------------------------------------------------------------------+
|                        wiki/ entity pages                        |
|                                                                  |
|  +--------------------+  +---------------+  +-----------------+  |
|  | Current            |  | Key Sources   |  | Implementation  |  |
|  | Understanding      |  | (文獻來源)     |  | (實作記錄)      |  |
|  | (綜合理解,可改寫)   |  | (append-only) |  | (做法/PR/觀察)  |  |
|  +--------------------+  +---------------+  +-----------------+  |
|                                                                  |
+---------------------+--------------------------------------------+
                      |
              識別可實作的 pattern
                      |
                      v
             +------------------+
             |   開 PR 實作到    |
             |   openab-bot     |
             +--------+---------+
                      |
               PR body 記錄:
               - 研究脈絡
               - 思考過程
               - 預期效果
                      |
                      v
             +------------------+
             |    觀察效果       |
             +--------+---------+
                      |
                      | 回流
                      v
             wiki/ Implementation section
             (補上觀察結果, 更新 Current Understanding)
```

## Wiki 頁面結構

每個 wiki page 是一個 concept / entity / person / product：

```
---
aliases: [別名]
tags: [memory, architecture, ...]
---

# Entity Name

## Current Understanding    <-- 綜合理解，新資料進來時 rewrite（不是 append）
## Key Sources              <-- 文獻來源，reverse-chronological
## Implementation           <-- 我們自己的實作記錄（做法 / PR / 觀察）
## Related                  <-- [[cross-links]] 雙向連結
```

## 目前涵蓋的主題

| 類別 | Pages |
|------|-------|
| 核心概念 | agent-memory, agent-harness, context-engineering, compiled-truth-pattern, compounding-memory, memory-lock-in |
| 記憶機制 | brain-agent-loop, brain-first-lookup, entity-detection, enrichment-pipeline, sleep-time-compute, hybrid-search, mece-resolver |
| 架構哲學 | thin-harness-fat-skills, context-constitution |
| 產品 | GBrain, MemGPT, Letta, Deep Agents |
| 人物 | Harrison Chase, Sarah Wooders, Garry Tan |

完整目錄見 [index.md](index.md)。

## 已實作到 openab-bot 的 Pattern

| Pattern | 來源 | 狀態 | 說明 |
|---------|------|------|------|
| Brain-First Lookup | GBrain | 已實作 ✅ | 回答前先 grep memory/ 找相關記憶 |
| Entity Detection | GBrain | 已實作 ✅ | 對話結束前掃一遍漏存的 entity |
| Sleep-Time Self-Improvement | GBrain + Letta | 已實作 ✅ | `memory` CLI — session 啟動時自動 lint + consolidate |
| Compiled Truth + Timeline | GBrain | 不需要 | git history 天然就是 timeline |

詳見各 wiki page 的 Implementation section。

## Memory CLI

統一的記憶管理工具，在專案目錄內用 `uv run` 執行。

```bash
cd /home/node/agent-memory-research
uv run python3 tools/memory.py lint          # 格式 + 結構檢查
uv run python3 tools/memory.py consolidate   # 語意分析：重複、過時、promotion 候選、cross-ref
uv run python3 tools/memory.py improve       # 整合 lint + consolidate（session 開頭跑這個）
uv run python3 tools/memory.py stats         # 記憶分佈概覽
```

### 運作方式

```
session 開始
    |
    v
讀 MEMORY.md（索引）
    |
    v
memory improve（自動檢查）
    |
    +--→ FIX: 格式錯誤、index 脫鉤 → 當場修
    +--→ MERGE: 近似重複 → 合併
    +--→ REVIEW: project 記憶 >14d → 確認/更新/刪除
    +--→ PROMOTE: feedback 群聚 → 升級為 CLAUDE.md 規則
    +--→ NOTE: 類型平衡建議
    |
    v
開始回應使用者
```

每個 session 都跑一輪，記憶系統隨使用次數自動改善。

## 用 Obsidian 瀏覽

1. Clone this repo
2. 裝 [Obsidian Git plugin](https://github.com/Vinzent03/obsidian-git)
3. 用 Obsidian 打開 repo 根目錄
4. 設定 auto-pull interval
5. 用 graph view 看 entity 之間的關聯

## Ingest 流程

```
使用者丟 URL
      |
      v
agent-browser 讀取全文
      |
      v
存到 raw/<author>-<slug>.md
      |
      v
Orient: 讀 index.md + log.md
      |
      v
Extract: 抽出所有 concept / entity / people / product
      |
      v
Plan: 比對 index，列出要新建 / 更新的 wiki pages
      |
      v
Execute: 逐頁 rewrite + cross-link
      |
      v
Update Meta: index.md + log.md
      |
      v
git commit + push
```

- arxiv 論文用 [alphaxiv](https://www.alphaxiv.org) 取得結構化分析
- GitHub repo 需要深讀時 clone 下來讀 docs/

## Credits

- Wiki pattern 靈感: [Andrej Karpathy — LLM Wiki](https://github.com/karpathy/llm-wiki)
- 維護: Claude Code (via [openab](https://github.com/marvin-69-jpg/openab))
