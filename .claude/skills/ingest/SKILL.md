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

3. **整理成筆記**，存到 `papers/<author>-<short-slug>.md`，格式：
   ```markdown
   # 文章標題

   - **作者**: 名字（身份）
   - **日期**: YYYY-MM-DD
   - **來源**: 原始 URL

   ---

   ## 核心論點
   一句話總結

   ## 重點摘要
   分段整理，保留關鍵引用

   ## 相關連結 / 提到的工具
   表格或列表
   ```

4. **Commit & push**
   ```bash
   cd /home/node/agent-memory-research
   git add raw/<file>.md papers/<file>.md
   git commit -m "add: <作者> — <標題> (<日期>)"
   git push
   ```

---

## 注意事項

- **一律用 agent-browser 讀取 URL**，不要用 curl hack 或 WebFetch
- 筆記用繁體中文，技術名詞保留英文
- 保留重要的原文引用（blockquote）
- 如果文章提到其他文章/論文，在「相關連結」列出
- 不要把原文全文貼進來，要消化整理
