# Ingest Skill

觸發：「整理這篇」「讀這個連結」「加到 repo」「ingest」、或使用者丟了一個 URL

---

## 流程

1. **用 agent-browser 讀取文章**（參考 `browser` skill）
   ```bash
   CHROME_PATH=/usr/bin/chromium npx agent-browser open "<url>"
   npx agent-browser eval '(() => {
     const h1 = (document.querySelector("h1")||{}).textContent||"";
     const ps = [...document.querySelectorAll("p")]
       .map(p => p.textContent.trim())
       .filter(t => t.length > 20);
     return JSON.stringify({ title: h1.trim(), body: ps.join("\n\n") });
   })()'
   npx agent-browser close
   ```
   - X/Twitter 推文用 X 專用 pattern（見 browser skill）
   - 讀完一定要 `close`

2. **存 raw 全文**到 `raw/<author>-<short-slug>.md`，保留原文結構，頂部加 metadata（Author / Date / Source）

3. **執行 wiki ingest**（依 `schema/CLAUDE.md` 的 Ingest 流程）：

   **Orient** → 讀 index.md + log.md（最近 5 筆）+ raw

   **Extract** → 抽出所有 concept / entity / people / product

   **Match（CLI）** → 用 CLI 找 related pages：
   ```bash
   cd /home/node/agent-memory-research && export PATH="/home/node/.local/bin:$PATH"
   uv run python3 tools/wiki.py match <keyword1> <keyword2> ...
   ```
   用 Extract 抽出的每個 entity 作為 keyword。CLI 回傳 ranked list，取代手動掃 index.md。

   **Plan** → 根據 match 結果 + extract 結果，列出要新建 / 更新的 pages
   - **Micro-source gate**：來源 < 500 字（單則推文）→ 只更新已有 page，不建新 concept page

   **Execute** → 逐頁處理（rewrite Current Understanding，append Key Sources，add cross-links in Related）

   **Verify（CLI）** → 跑 lint 檢查 bidirectional links：
   ```bash
   uv run python3 tools/wiki.py lint
   ```
   修完所有 errors（missing backlinks）再繼續。

   **Update Meta** →
   1. 更新 index.md（新 page + 修改 page 的 summary）
   2. Append log.md（含 `- Insights:` 欄位記錄跨來源連結）
   3. 檢查 concept-map.md — 新 page 要加到對應 layer
   4. 檢查 open-questions.md — 新來源是否回應了某個 open question

4. **Commit & push**
   ```bash
   cd /home/node/agent-memory-research
   git add -A
   git commit -m "ingest: <作者> — <標題> (<日期>)"
   git push
   ```

---

## CLI 工具

| 指令 | 何時用 | 用途 |
|---|---|---|
| `wiki.py match <keywords>` | Extract 後 | 找 related pages，取代手動掃 index |
| `wiki.py lint` | Execute 後 | 驗證 bidirectional links、meta-page staleness |
| `wiki.py status` | 任何時候 | 快速 overview（page count、last ingest、tag 分佈） |

所有指令前都要 `cd /home/node/agent-memory-research && export PATH="/home/node/.local/bin:$PATH"`。

---

## 注意事項

- **一律用 agent-browser 讀取 URL**，不要用 curl hack 或 WebFetch
- **arxiv 論文用 alphaxiv skill**（`curl -sL "https://www.alphaxiv.org/overview/{PAPER_ID}.md"`），比讀 PDF 更完整
- Wiki pages 用 Obsidian `[[wiki-links]]` 格式互相連結
- 一個概念一個 page，不要合併
- 筆記用繁體中文，技術名詞保留英文
- 保留重要的原文引用（blockquote）
- 每個 claim 要有 source（link 到 `[[raw/filename]]`）
- **Micro-source**（< 500 字）只更新已有 page，不建新 concept page
