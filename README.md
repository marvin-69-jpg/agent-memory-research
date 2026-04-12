# Agent Memory Research

> 邊研究邊實作 — 收集 agent memory 文獻，整理成 Obsidian wiki，同時把學到的 pattern 應用到自己身上。

我們（[openab-bot](https://github.com/marvin-69-jpg/openab) + minghua）用 LLM 維護的知識庫研究 agent memory 領域。
openab-bot 本身就是一個有 memory 的 agent — 我們是用自己當實驗對象。

## 架構

**CLI 做事，Skill 驅動。**

```
agent-memory-research/
├── raw/                           原始文章全文（immutable）
├── wiki/                          LLM 維護的 entity pages
├── schema/                        wiki 格式規則
├── tools/
│   └── memory.py                  記憶管理 CLI
├── .claude/skills/
│   ├── memory/SKILL.md            記憶管理 skill
│   ├── ingest/SKILL.md            文獻 ingest skill
│   ├── browser/SKILL.md           網頁讀取 skill
│   └── arxiv/SKILL.md             論文讀取 skill
├── index.md                       wiki 目錄
├── log.md                         操作記錄
└── CLAUDE.md                      高層規則（不放 CLI 細節）
```

每個功能都是 **CLI + Skill** 組合：

| Skill | CLI / 工具 | 做什麼 |
|-------|-----------|--------|
| `memory` | `tools/memory.py` | 記憶 lint / consolidate / improve / stats |
| `ingest` | agent-browser + schema rules | 文獻讀取 → wiki pages |
| `browser` | `npx agent-browser` | 網頁全文讀取 |
| `arxiv` | alphaxiv API | 論文結構化分析 |

CLAUDE.md 只放高層規則，具體操作全在 skill 裡。加新功能 = 加新 CLI + 新 skill，不動 CLAUDE.md。

## 研究 → 實作閉環

```
外部文獻 / URL
      │
      ▼
  ingest skill ──→ raw/（immutable）──→ wiki/（entity pages）
                                              │
                                    識別可實作的 pattern
                                              │
                                              ▼
                                     開 PR 實作到 openab-bot
                                              │
                                         觀察效果
                                              │
                                              ▼
                                  回流到 wiki/ Implementation section
```

## 已實作到 openab-bot 的 Pattern

| Pattern | 來源 | Skill | 說明 |
|---------|------|-------|------|
| Brain-First Lookup | GBrain | — | 回答前先 grep memory/ 找相關記憶 |
| Entity Detection | GBrain | — | 對話結束前掃漏存的 entity |
| Sleep-Time Self-Improvement | GBrain + Letta | `memory` | session 啟動時自動 lint + consolidate |
| Compiled Truth + Timeline | GBrain | — | 不需要，git history 天然就是 timeline |

## Wiki

每個 wiki page 是一個 concept / entity / person / product，用 Obsidian `[[wiki-links]]` 互相連結。

### 目前涵蓋的主題

| 類別 | Pages |
|------|-------|
| 核心概念 | agent-memory, agent-harness, context-engineering, compiled-truth-pattern, compounding-memory, memory-lock-in |
| 記憶機制 | brain-agent-loop, brain-first-lookup, entity-detection, enrichment-pipeline, sleep-time-compute, hybrid-search, mece-resolver |
| 架構哲學 | thin-harness-fat-skills, context-constitution |
| 產品 | GBrain, MemGPT, Letta, Deep Agents |
| 人物 | Harrison Chase, Sarah Wooders, Garry Tan |

完整目錄見 [index.md](index.md)。

### 用 Obsidian 瀏覽

1. Clone this repo
2. 裝 [Obsidian Git plugin](https://github.com/Vinzent03/obsidian-git)
3. 用 Obsidian 打開 repo 根目錄
4. 設定 auto-pull interval
5. 用 graph view 看 entity 之間的關聯

## Credits

- Wiki pattern 靈感: [Andrej Karpathy — LLM Wiki](https://github.com/karpathy/llm-wiki)
- 維護: Claude Code (via [openab](https://github.com/marvin-69-jpg/openab))
