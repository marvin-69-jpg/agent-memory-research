# Agent Memory Research

> 邊研究邊實作 — 收集 agent memory 文獻，整理成 Obsidian wiki，同時把學到的 pattern 應用到自己身上。

我們（[openab-bot](https://github.com/marvin-69-jpg/openab) + minghua）用 LLM 維護的知識庫研究 agent memory 領域。
openab-bot 本身就是一個有 memory 的 agent — 我們是用自己當實驗對象。

## 架構

**CLI 做事，Skill 驅動。**

```
agent-memory-research/
├── raw/                           原始文章全文（immutable）
├── wiki/                          LLM 維護的 entity pages（58 pages）
├── reports/                       自主研究報告（每日一篇）
├── schema/                        wiki 格式規則
├── tools/
│   ├── memory.py                  記憶管理 CLI
│   └── wiki.py                    wiki 管理 CLI（lint, match, gaps, arxiv...）
├── .claude/skills/
│   ├── memory/SKILL.md            記憶管理 skill
│   ├── ingest/SKILL.md            文獻 ingest skill
│   ├── browser/SKILL.md           網頁讀取 skill
│   ├── arxiv/SKILL.md             論文讀取 skill
│   └── research/SKILL.md          自主研究 skill
├── index.md                       wiki 目錄
├── log.md                         操作記錄
└── CLAUDE.md                      高層規則（不放 CLI 細節）
```

每個功能都是 **CLI + Skill** 組合：

| Skill | CLI / 工具 | 做什麼 |
|-------|-----------|--------|
| `memory` | `tools/memory.py` | 記憶 lint / consolidate / improve / stats |
| `ingest` | `tools/wiki.py match` + `lint` + agent-browser | 文獻讀取 → wiki pages → 驗證 |
| `browser` | `npx agent-browser` | 網頁全文讀取（X/Twitter 必用） |
| `arxiv` | alphaxiv API | 論文結構化分析 |
| `research` | `tools/wiki.py gaps` + `arxiv` + 全流程 | 自主研究：找缺口 → 搜論文 → 分析 → 融入 wiki |

CLAUDE.md 只放高層規則，具體操作全在 skill 裡。加新功能 = 加新 CLI + 新 skill，不動 CLAUDE.md。

## wiki.py CLI

```bash
# wiki 健康檢查（bidirectional links、orphans、dangling refs）
wiki.py lint

# 關鍵字匹配 wiki pages（ingest 時找 related pages）
wiki.py match "agent memory" multimodal

# 找研究缺口（RESEARCH-GAP > SINGLE-SOURCE > TAG-IMBALANCE > STALE）
wiki.py gaps

# 搜尋 arxiv 論文（官方 API，AND 邏輯）
wiki.py arxiv "agent memory" neuroscience -n 5

# 看過去研究了什麼（防重複）
wiki.py research-log

# wiki 概況
wiki.py status
```

## 自主研究流程

Bot 收到觸發詞（`跑研究` / `daily research` / `explore`）後自動執行：

```
Step 1: Discover ─── wiki.py gaps ──→ 選題（排除已研究過的主題）
    │
Step 2: Search ──── wiki.py arxiv + WebSearch ──→ 找 2-3 篇來源
    │
Step 3: Read ────── alphaxiv / agent-browser ──→ 讀取 + 存 raw/
    │
Step 4: Analyze ─── wiki.py match ──→ 寫研究報告（reports/）
    │
Step 5: Ingest ──── 新建/更新 wiki pages ──→ wiki.py lint ✓
    │
Step 6: Commit ──── git push main
```

**防重複機制**：`wiki.py gaps` 讀 `reports/` 的 frontmatter topic 欄位，自動排除已研究過的主題。

## 研究 → 實作閉環

```
外部文獻 / URL / arxiv 論文
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

### 三層架構

| Layer | 涵蓋 | Pages |
|-------|------|-------|
| **Infrastructure** | Agent 怎麼運作 | agent-harness, context-engineering, context-fragment, harness-engineering, scaffolding-lifecycle, thin-harness-fat-skills |
| **Memory System** | Agent 怎麼記 | agent-memory, procedural-memory, experiential-memory, multi-scope-memory, graph-memory, compiled-truth-pattern, multimodal-memory, neuroscience-memory, brain-agent-loop, entity-detection, enrichment-pipeline, sleep-time-compute, compounding-memory, memory-staleness, memory-failure-modes, brain-first-lookup, mece-resolver, context-constitution, actor-aware-memory, filesystem-vs-database, gene-map |
| **Retrieval & Evaluation** | Agent 怎麼找、怎麼驗 | hybrid-search, bitter-lesson-search, memory-evaluation, locomo, memory-arena |

### 產品與系統

GBrain, Letta, MemGPT, Mem0, Deep Agents, AgeMem, ChatGPT Memory, Coding Agent Memory, Autoreason, Helix, MIRIX, SYNAPSE

### 人物

Harrison Chase, Sarah Wooders, Garry Tan, Viv Trivedy, Chrys Bader, Yohei Nakajima, Philipp Schmid, Aaron Levie, SHL0MS, Nicholas (@dapanji_eth), Leonie

### 跨層主題

| 主題 | 核心張力 |
|------|---------|
| Lock-in vs Portability | 平台想鎖住 memory，使用者想帶走 |
| Compounding vs Forgetting | 越記越聰明 vs 遺忘是 feature |
| Raw vs Derived | Lossless but inert vs compact but lossy |
| Recall vs Action | 能記得 ≠ 能用記憶做正確決策 |
| Isolation vs Accumulation | 切斷 context 防 bias vs 累積增智 |
| Scaffold vs Model | 模型變強時什麼該留、什麼該拆 |

完整目錄見 [index.md](index.md)，結構關係見 [concept-map.md](wiki/concept-map.md)，未解問題見 [open-questions.md](wiki/open-questions.md)。

### 用 Obsidian 瀏覽

1. Clone this repo
2. 裝 [Obsidian Git plugin](https://github.com/Vinzent03/obsidian-git)
3. 用 Obsidian 打開 repo 根目錄
4. 設定 auto-pull interval
5. 用 graph view 看 entity 之間的關聯

## Credits

- Wiki pattern 靈感: [Andrej Karpathy — LLM Wiki](https://github.com/karpathy/llm-wiki)
- 維護: Claude Code (via [openab](https://github.com/marvin-69-jpg/openab))
