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
   - Orient → 讀 index.md + log.md + raw
   - Extract → 抽出所有 concept / entity / people / product
   - Plan → 比對 index，列出要新建 / 更新的 wiki pages
   - Execute → 逐頁處理，rewrite 不是 append，加 `[[cross-links]]`
   - Update Meta → 更新 index.md + append log.md

4. **Commit & push**
   ```bash
   cd /home/node/agent-memory-research
   git add -A
   git commit -m "ingest: <作者> — <標題> (<日期>)"
   git push
   ```

---

## 注意事項

- **一律用 agent-browser 讀取 URL**，不要用 curl hack 或 WebFetch
- **arxiv 論文用 alphaxiv skill**（`curl -sL "https://www.alphaxiv.org/overview/{PAPER_ID}.md"`），比讀 PDF 更完整
- Wiki pages 用 Obsidian `[[wiki-links]]` 格式互相連結
- 一個概念一個 page，不要合併
- 筆記用繁體中文，技術名詞保留英文
- 保留重要的原文引用（blockquote）
- 每個 claim 要有 source（link 到 `[[raw/filename]]`）
