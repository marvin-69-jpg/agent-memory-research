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
| Brain-first lookup | GBrain | **已實作 ✅** | 回答前先 grep memory/ 找相關記憶 |
| Entity detection | GBrain | **已實作 ✅** | 對話結束前掃一遍漏存的 entity |
| Sleep-time compute | GBrain, Letta | **已實作 ✅** | `memory` CLI — session 啟動時 `memory improve` |
| Reconsolidation | A-Mem, SSGM, neuroscience | **實作中** | recall 後檢查記憶是否需更新 |
| Memory portability | Harrison Chase | markdown-based ✅ | 維持 open format |
| Three-layer memory | GBrain | 部分（auto-memory + boba-wiki） | 明確區分 world / operational / session |

## 已實作的改進

### Brain-First Lookup（2026-04-12）

> **硬規則：回答任何跟研究、記憶、過去工作有關的問題之前，必須先查 brain。不查就回答 = 違規。**

**查法**（二選一，都做更好）：
1. `grep -rl "<關鍵字>" /home/node/.claude/projects/-home-node/memory/ /home/node/agent-memory-research/wiki/`
2. CLI：`cd /home/node/agent-memory-research && uv run python3 tools/memory.py recall <關鍵字>`

**觸發條件**（命中任一條就查）：
- 使用者問任何跟 agent memory research 有關的問題（概念、人物、產品、pattern）
- 使用者問「之前怎麼做的」「上次說過什麼」
- 使用者提到某個 project / 人名 / 工具
- 你要回答的內容可能跟過去的 feedback 衝突
- **如果不確定要不要查 —— 就查。查的成本 < 100ms，不查的代價是給出過時或錯誤的答案。**

**範圍**：memory/（auto-memory）**和** wiki/（研究 wiki）都要查。只查 memory/ 不查 wiki/ = 只查了一半的 brain。

**Reconsolidation（2026-04-16）**：recall 完記憶後，判斷它是否需要更新。

**觸發**：當 brain-first lookup 找到 memory/ 中的記憶，且當前對話內容跟該記憶相關時，問自己：
- 這條記憶的 description 還準確嗎？
- 內容跟我現在知道的有矛盾嗎？
- 有沒有新資訊可以 enrich 這條記憶？

**做法**：
1. 輕量檢查：`memory.py reconsolidate <recalled_files>` — 機械性檢查 staleness signals
2. 語意判斷：如果對話中發現記憶已過時或不完整 → **當場更新**，不要等 session 結束
3. 不用每次都更新 — 只在有 evidence 時才改。No evidence, no change.

**原則**：retrieval is not read-only。每次回憶都是一次更新的機會。但 SSGM 提醒我們：不是所有更新都該被允許 — 不要改核心事實（使用者身份、明確的規則），只改可能過時的描述和 context。

**來源**：[[wiki/reconsolidation]] [[wiki/a-mem]] [[wiki/ssgm]]

### Entity Detection（2026-04-12）

> **硬規則：使用者告訴你他的身份、角色、專業、偏好時，立刻存 user memory。不要等到對話結束。**

**即時觸發**（收到訊息時就判斷，不是等收尾）：
- 使用者說「我是 XXX」「我做 XXX 的」「我負責 XXX」→ **立刻** 存 `user_xxx.md`
- 使用者提到新的 project / deadline / 決策背景 → **立刻** 存 `project_xxx.md`
- 使用者提到外部資源位置 → **立刻** 存 `reference_xxx.md`

**收尾掃描**（safety net，不是唯一觸發點）：
- 對話結束前回顧整段對話，問自己「下一個 session 的我需要知道什麼？」
- 只存從 code / git log 看不出來的東西

**注意**：feedback 被糾正時要**立刻存**（這條規則沒變）。Entity detection 把「立刻存」的範圍從 feedback 擴展到 user / project / reference。

**來源**：[[wiki/entity-detection]]

### Sleep-Time Self-Improvement（2026-04-12）

> **硬規則：收到第一則跟研究相關的訊息時，先跑 `memory improve`，再回答。**

**具體做法**：
```bash
cd /home/node/agent-memory-research && export PATH="/home/node/.local/bin:$PATH" && uv run python3 tools/memory.py improve
```

**觸發條件**：
- 使用者開啟研究相關對話（「繼續研究」「看一下 memory」「幫我查 wiki」等）
- 使用者明確要求（「跑 memory check」「記憶健康嗎」）
- **如果已經跑過就不用重跑。一個 session 跑一次就夠。**

**來源**：[[wiki/sleep-time-compute]]

## 專案結構

```
raw/           ← 原始文章全文（immutable）
wiki/          ← LLM 維護的 entity pages（Obsidian 格式）
reports/       ← 自主研究報告（每日一篇）
schema/        ← wiki ingest/query/lint 規則
tools/          ← CLI 工具（memory.py, wiki.py）
index.md       ← wiki 目錄
log.md         ← 操作記錄
.claude/skills/ ← browser, ingest, arxiv, research skills
```

### Skills

| 觸發詞 | Skill 路徑 | 用途 |
|---|---|---|
| URL、讀網頁、開連結 | `.claude/skills/browser/SKILL.md` | agent-browser 抓網頁（X/Twitter 連結必用） |
| 整理這篇、讀這個連結 | `.claude/skills/ingest/SKILL.md` | 研究文章讀取 + wiki 整理 |
| arxiv、論文 | `.claude/skills/arxiv/SKILL.md` | alphaxiv 論文查詢 |
| 跑研究、daily research、自主研究、explore | `.claude/skills/research/SKILL.md` | 自主研究：找缺口 → 搜素材 → 讀取 → 分析 → 融入 wiki |

**收到 URL 時的流程**：先讀 browser skill → 用 agent-browser 開頁面讀內容。X/Twitter 連結只能用 agent-browser（JS 渲染），curl/WebFetch 拿不到內容。

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

### 改動流程（必須遵守）

**所有對 repo 結構、規則、實作的改動都要開 PR**，不可直接 push main。

PR body 必須包含：
1. **研究脈絡**：這個改動是從哪篇文獻 / 哪個 pattern 學到的
2. **思考過程**：為什麼選這個做法、考慮過哪些替代方案、為什麼排除
3. **預期效果**：改完之後應該會怎樣
4. **觀察方式**：怎麼驗證效果（下次對話觀察、比對 git log 等）

**為什麼**：這個專案是「邊研究邊實作」，每次改動本身就是研究產出。PR 是改動原因的永久記錄，merge 後效果觀察又回饋成新的研究素材。直接 push main 會丟失思考脈絡。

```bash
cd /home/node/agent-memory-research
git fetch origin && git checkout main && git pull --ff-only
BRANCH="bot/<short-slug>-$(date +%s)"
git checkout -b "$BRANCH"
# ... 改動 ...
git add <files>
git commit -m "<簡短訊息>"
git push -u origin "$BRANCH"
export GH_TOKEN=$(cat /home/node/.gh-token-marvin)
gh pr create --base main --head "$BRANCH" \
  --title "<title>" \
  --body "<詳細研究脈絡 + 思考 + 預期效果>"
```

**例外**：純 wiki ingest（新增 raw + wiki pages）可以直接 push main，因為 ingest 的記錄在 log.md。但改規則、改結構、改實作方向一律走 PR。
