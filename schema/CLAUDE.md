# Agent Memory Research — Schema

This wiki is a **persistent, compounding knowledge base** about agent memory systems.
Sources are articles, papers, blog posts, and tweets from researchers and builders.
The LLM reads sources, extracts knowledge, and maintains wiki pages. Humans read via Obsidian.

## Architecture

```
raw/          ← immutable source articles (original text, never modify)
wiki/         ← LLM-maintained entity pages (the knowledge base)
index.md      ← catalog of all wiki pages + one-line summaries
log.md        ← append-only record of all operations
schema/       ← this file (rules for the LLM)
```

## Wiki Page Format

Every page in `wiki/` follows this template:

```markdown
---
aliases: [別名1, alias2]
first_seen: YYYY-MM-DD
last_updated: YYYY-MM-DD
tags: [memory, harness, architecture, retrieval, multi-agent, benchmark, people, product]
---

# Entity Name

One-paragraph summary: what this is, why it matters in the context of agent memory.

## Current Understanding

Bullet points of the latest known state of knowledge on this topic.
Update (not append) when new sources arrive.
Mark uncertainty: "as of 2026-04-12" or "unconfirmed".

## Key Sources

Reverse-chronological list. Each entry:
- **YYYY-MM-DD** — What the source says about this topic. Source: [[raw/filename]]

## Related

[[other-entity]] [[another-entity]]
```

### Naming Convention

- Filename = lowercase, hyphens for spaces: `agent-harness.md`, `memory-lock-in.md`
- Use the most commonly known name
- One concept per page. Don't merge "agent harness" and "agent memory" — make two pages and cross-link
- People get their own page if they have significant viewpoints

## Tag Taxonomy

| Tag | 用途 |
|-----|------|
| `memory` | Agent 記憶機制本身（短期/長期/工作記憶、compaction、retrieval） |
| `harness` | Agent harness / scaffolding 架構 |
| `architecture` | 系統設計、分層、模組化 |
| `retrieval` | 記憶檢索策略（RAG、embedding、reranking） |
| `multi-agent` | 多 agent 系統中的記憶共享 / 隔離 |
| `benchmark` | 評測、benchmark、實驗結果 |
| `people` | 研究者、builder、意見領袖 |
| `product` | 具體產品 / 工具 / 框架 |
| `lock-in` | 平台鎖定、開放 vs 封閉 |
| `context` | Context engineering、context window 管理 |

## Operations

### 1. Ingest

Triggered when a new source article is added to `raw/`.

**Steps:**

#### Step 1: Orient
- Read `index.md` to understand the current wiki landscape
- Read the last 5 entries of `log.md`
- Read the new raw file

#### Step 2: Extract
- Identify every concept/entity mentioned in the source:
  - Concepts (agent memory, short-term memory, compaction, context engineering...)
  - Products/tools (Claude Code, Deep Agents, Letta, LangGraph...)
  - People (Harrison Chase, Sarah Wooders, Andrej Karpathy...)
  - Organizations (Anthropic, LangChain, OpenAI...)
  - Patterns/techniques (memory-as-harness, stateful API, encrypted compaction...)
- For each entity, note what the source says about it

#### Step 2.5: Match (CLI)
- Run `wiki match` with extracted entities to find related pages:
  ```bash
  cd /home/node/agent-memory-research && export PATH="/home/node/.local/bin:$PATH" && uv run python3 tools/wiki.py match <keyword1> <keyword2> ...
  ```
- CLI returns ranked list of related pages with scores
- Use this instead of manually scanning `index.md` — scales to hundreds of pages

#### Step 3: Plan
- Using match results + extracted entities:
  - **Exists (match score > 0)** → will update (load the page)
  - **Doesn't exist** → will create (use template above)
- Identify cross-links between entities
- Identify contradictions with existing pages
- **Micro-source gate**: if source is < 500 words (single tweet, short post), only update existing pages — don't create new concept pages for thin content
- Write out the plan before executing

#### Step 4: Execute
For each page to update:
1. Read the full page
2. **Rewrite** "Current Understanding" to integrate new info (don't append — synthesize)
3. **Append** to "Key Sources" (reverse-chronological)
4. **Add cross-links** in "Related" (bidirectional)
5. **Handle contradictions**: update and note the change
6. Update `last_updated` in frontmatter

For new pages:
1. Create using the template
2. Fill in all sections
3. Add cross-links to related existing pages
4. Go to those related pages and add backlinks

#### Step 4.5: Verify (CLI)
- Run `wiki lint` to check bidirectional links:
  ```bash
  cd /home/node/agent-memory-research && export PATH="/home/node/.local/bin:$PATH" && uv run python3 tools/wiki.py lint
  ```
- Fix all errors (missing backlinks in Related sections) before continuing
- Check warnings (concept-map/open-questions staleness)

#### Step 5: Update Meta
1. **index.md**: add new pages, update summaries for modified pages
2. **log.md**: append one entry:
   ```
   ## [YYYY-MM-DD] ingest | <source title>
   - Source: raw/<filename>
   - Created: page1.md, page2.md
   - Updated: page3.md, page4.md
   - New cross-links: page1 ↔ page3
   - Insights: <cross-source insights — connections discovered during this ingest>
   ```
3. **concept-map.md**: if new pages were created, add them to the appropriate layer/section
4. **open-questions.md**: if the new source addresses any open question, update it

### 2. Query

When asked a question:
1. Read `index.md` to find relevant pages
2. Read those pages
3. Synthesize an answer with `[[citations]]`
4. If the answer produces a valuable new synthesis, save it as a new wiki page

### 3. Lint (CLI)

Use the wiki CLI for health checks:
```bash
cd /home/node/agent-memory-research && export PATH="/home/node/.local/bin:$PATH" && uv run python3 tools/wiki.py lint
```

Checks: bidirectional links in Related, orphan pages, dangling links, index sync, concept-map/open-questions staleness, frontmatter fields.

Other useful commands:
```bash
uv run python3 tools/wiki.py status    # quick overview
uv run python3 tools/wiki.py match <keywords>  # find related pages
```

## Wiki Page Format — Implementation Section

當一個 wiki concept 被實際應用到 openab-bot 時，在該 wiki page 加上 `## Implementation` section（放在 Key Sources 和 Related 之間）。

```markdown
## Implementation

### <日期> — <簡短描述>

- **做法**：具體怎麼實作的（簡化了什麼、改了什麼）
- **PR**：marvin-69-jpg/agent-memory-research#<number>
- **觀察**：（實作後的效果，持續補充）
```

**規則**：
- 一個 concept 可以有多次 implementation（不同階段的嘗試）
- 每次 implementation 對應一個 PR
- 「觀察」欄在實作當下可以先寫「待觀察」，後續 session 發現效果時回來補
- 觀察結果如果產生新的 insight，可以反過來更新 Current Understanding

**這形成研究閉環**：

```
外部文獻 → raw/ → wiki（Current Understanding）→ 識別 pattern → 實作（PR）
                        ↑                                           ↓
                        └──────── Implementation section ───────────┘
                                  （效果觀察回流更新理解）
```

## Rules

1. **Never modify raw files.** Raw sources are immutable.
2. **Always rewrite, never just append.** Wiki pages should read as coherent documents, not logs.
3. **Every claim needs a source.** Link to `[[raw/filename]]` or external URL.
4. **Bidirectional links.** If A references B, B must reference A in Related.
5. **Use `[[wiki-links]]`** for internal references (Obsidian format).
6. **One concept per page.** If in doubt, split and cross-link.
7. **Write in Traditional Chinese** (technical terms keep English).
8. **Frontmatter is mandatory.**
9. **Update index.md on every operation.**
10. **Log every operation.** No silent changes.
11. **Use agent-browser to read URLs.** Never curl hack or WebFetch.
12. **Implementation 回流**。實作了某個 concept 就更新該 wiki page 的 Implementation section。
13. **Micro-source gate.** < 500 字的來源（單則推文、短 post）= micro-source。Ingest 時只更新已有 page，不為薄內容建新 concept page。
14. **Verify before commit.** Execute 後跑 `wiki lint`，修完 errors 才進 Step 5。
