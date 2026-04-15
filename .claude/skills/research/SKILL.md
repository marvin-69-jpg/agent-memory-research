# Daily Research Skill

觸發：「跑研究」「daily research」「自主研究」「研究報告」「找新素材」「explore」

---

## 概述

自主研究 loop：從 wiki 缺口出發，搜尋新素材，讀取分析，寫報告，融入 wiki 資料循環。每次研究選一個主題，不跟過去重複。

---

## 流程

### Step 0: 環境準備

```bash
cd /home/node/agent-memory-research
export PATH="/home/node/.local/bin:$PATH"
```

### Step 1: Discover — 找缺口

```bash
uv run python3 tools/wiki.py gaps
```

CLI 回傳 ranked gaps（research-gap > single-source > tag-imbalance > stale），以及建議的 top 3 主題。

**選題規則**：
- 優先選 `RESEARCH-GAP`（完全沒覆蓋的領域）
- 其次選 `SINGLE-SOURCE`（只有一個來源、需要更多證據的概念）
- CLI 已排除過去研究過的主題（讀 `reports/` 的 frontmatter）
- 不要自己發明主題 — 從 CLI 建議中選

確認選題後，記下主題名稱和 gap 類型。

### Step 2: Search — 搜尋素材

用 WebSearch 搜尋 2-3 篇相關來源：

```
優先順序：
1. X/Twitter（搜 agent memory 相關的有影響力的人的貼文）
2. GitHub repo（README、docs）
3. Blog posts / 技術文章
4. arxiv 論文（用 alphaxiv skill）
```

**搜尋關鍵字**：用選定主題 + 相關的 wiki 概念名稱組合搜尋。
例如主題是 "multimodal memory"，搜 `"agent multimodal memory" site:x.com` 或 `"multimodal memory" AI agent`。

**篩選標準**：
- 來源要有實質內容（不是純轉推、不是廣告）
- 優先選有數據或具體實作的
- 2-3 篇就好，不要貪多

### Step 3: Read — 讀取來源

用 **browser skill** 讀取每篇來源：

```bash
CHROME_PATH=/usr/bin/chromium npx agent-browser open "<url>"
# 讀取內容（參考 browser skill 的 pattern）
npx agent-browser close
```

- X/Twitter 連結必須用 agent-browser
- arxiv 用 alphaxiv skill
- 每篇存 raw：`raw/<author>-<short-slug>.md`

### Step 4: Analyze — 寫研究報告

存到 `reports/YYYY-MM-DD-<topic-slug>.md`：

```markdown
---
date: YYYY-MM-DD
topic: <主題名稱>
gap_type: research-gap | single-source | tag-imbalance | stale
sources_found: <數字>
wiki_pages_updated: <數字>
wiki_pages_created: <數字>
---

# Daily Research: <主題名稱>

## 研究動機
為什麼選這個主題。來自 `wiki gaps` 的哪個缺口。

## 發現
從新來源學到的重點（bullet points，每個 claim 附來源）。

## 與已有知識的連結
跟 wiki 裡哪些現有概念有交叉。用 `wiki match` 確認：
```bash
uv run python3 tools/wiki.py match <keywords from findings>
```

## Open Questions 推進
這次研究是否回答或推進了 open-questions.md 裡的某個問題。

## 下一步
未來可以深入的方向（給下次研究參考）。
```

報告長度：500-1000 字。重點是 actionable insights，不是長論文。

### Step 5: Ingest — 融入 wiki

照 **ingest skill** 的流程，把新來源融入 wiki：

1. 存 raw（Step 3 已做）
2. `wiki match` 找 related pages
3. 更新/新建 wiki pages
4. `wiki lint` 驗證
5. 更新 index.md、log.md、concept-map.md（如需要）、open-questions.md（如推進了某個問題）

### Step 6: Commit & 回報

```bash
git add -A
git commit -m "research: <topic> — <一句話摘要>"
git push
```

完成後在 Discord 回報：
- 研究主題
- 找到幾篇來源
- 更新/新建了哪些 wiki pages
- 是否推進了某個 open question
- 報告路徑

---

## CLI 工具

| 指令 | 何時用 |
|---|---|
| `wiki.py gaps` | Step 1 — 找研究缺口和建議主題 |
| `wiki.py research-log` | 任何時候 — 看過去研究了什麼（防重複） |
| `wiki.py match <keywords>` | Step 4 — 確認新發現跟哪些 wiki 概念相關 |
| `wiki.py lint` | Step 5 — ingest 後驗證 |

---

## 注意事項

- **不要重複研究**：`wiki gaps` 已排除 `reports/` 裡的主題，但也要自己判斷是否真的是新方向
- **不要貪多**：一次研究一個主題、讀 2-3 篇來源就好
- **報告是給人看的**：繁體中文，技術名詞保留英文，簡潔有料
- **來源品質 > 數量**：寧可一篇好來源也不要三篇水文
- **一律用 agent-browser 讀 URL**
- **直接 push main**（研究報告不需要 PR，跟 ingest 一樣）
