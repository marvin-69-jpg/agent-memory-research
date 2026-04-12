# GBrain — Deep Dive (Supplementary Docs)

**Author**: Garry Tan (@garrytan)
**Source**: https://github.com/garrytan/gbrain (cloned and read docs/)
**Date**: 2026 (repo active, skillpack v0.7.0)

This file supplements [[raw/garry-tan-gbrain]] with content from docs/ and skills/ that the README doesn't cover.

---

## 1. Thin Harness, Fat Skills (docs/ethos/THIN_HARNESS_FAT_SKILLS.md)

Garry Tan 的核心架構哲學，基於 YC Spring 2026 演講。

### 五個定義

1. **Skill File** — 可重用的 markdown procedure，教 model HOW to do something。Skill 像 method call，接受參數，同一個 skill 用不同參數產出完全不同能力。「Markdown is actually code — a more perfect encapsulation of capability than rigid source code.」

2. **Harness** — 跑 LLM 的程式，只做四件事：run model in loop, read/write files, manage context, enforce safety。That's the "thin."
   - Anti-pattern: fat harness with 40+ tool definitions 吃掉半個 context window
   - 正確做法：Playwright CLI 200ms vs Chrome MCP 15s = 75x faster

3. **Resolver** — Context 的 routing table。Task type X 出現時，自動載入 document Y。
   - Garry 的 CLAUDE.md 曾經 20,000 行，模型 attention degraded
   - 修正：改成 200 行 pointer，resolver 在需要時載入正確文件
   - Claude Code 內建 resolver：每個 skill 的 description 就是 resolver

4. **Latent vs. Deterministic** — 每個步驟要放對邊
   - Latent space = intelligence（判斷、合成、pattern recognition）
   - Deterministic = trust（SQL、code、數字，same input same output）
   - 最糟：把 deterministic 問題塞進 latent space（800 人座位分配用 LLM）

5. **Diarization** — Model 讀所有關於一個主題的資料，寫出結構化 profile。「Read 50 documents, produce 1 page of judgment.」No SQL query or RAG pipeline produces this.

### 三層架構

```
Fat skills (top)     — markdown procedures, 90% of value
Thin CLI harness     — ~200 lines, JSON in text out
Your app (bottom)    — QueryDB, ReadDoc, Search, deterministic foundation
```

Push intelligence UP into skills. Push execution DOWN into deterministic tooling. Keep the harness THIN.

### 自我學習系統

YC Startup School 案例（Chase Center, July 2026, 6,000 founders）：
- `/enrich-founder` skill 每晚 2am cron 跑 6,000 profiles
- Diarization 抓「SAYS vs ACTUALLY BUILDING」差異
- `/match-breakout`, `/match-lunch`, `/match-live` — 同一 skill 三種 invocation
- `/improve` skill 讀 NPS survey，自動改寫 matching rules 寫回 skill file
- 結果：「OK」ratings 從 12% 降到 4%

### 關鍵引言

「The bottleneck is never the model's intelligence. The bottleneck is whether the model understands your schema.」

「Every skill I write is a permanent upgrade. It never degrades. It never forgets. It runs at 3 AM while I sleep. And when the next model drops, every skill instantly gets better.」

---

## 2. Brain-Agent Loop (docs/guides/brain-agent-loop.md)

### The Loop

```
Signal → DETECT entities (async sub-agent) → READ brain first → RESPOND with context → WRITE brain pages → SYNC index
```

### Two Invariants
1. Every READ improves the response
2. Every WRITE improves future reads

### Key Rules
- Read BEFORE responding, not after
- Don't skip the write step（「later」means never）
- Sync after every write batch
- External APIs are fallback, not primary

---

## 3. Brain-First Lookup (docs/guides/brain-first-lookup.md)

```
1. Keyword search (fast, no embeddings needed)
2. Hybrid search (needs embeddings, semantic matches)
3. Direct slug guess
4. External API (FALLBACK ONLY)
```

「An agent that calls Brave Search before checking the brain is wasting money and giving worse answers.」

Brain has: relationship history, your own assessments, meeting transcripts, cross-references, timeline. No external API provides this.

---

## 4. Entity Detection (docs/guides/entity-detection.md)

- Spawn lightweight sub-agent on EVERY inbound message（async, don't block response）
- Use Sonnet, not Opus（entity detection is pattern matching, not deep reasoning）
- Detect: original thinking FIRST（highest priority）, then entity mentions
- Filing rules: originals/ for user's own ideas, concepts/ for world concepts, people/companies/ for entities
- **Iron Law of Back-Linking**: every entity mention MUST create back-link FROM entity page TO source
- Dedup before creating: always `gbrain search` first
- Don't create stubs — if you create a page, make it good

---

## 5. Enrichment Pipeline (docs/guides/enrichment-pipeline.md)

### Three Tiers

| Tier | API Calls | For | Sources |
|------|-----------|-----|---------|
| Tier 1 | 10-15 | Key people, inner circle | Brain + web + Twitter + LinkedIn + research + funding + meetings + contacts |
| Tier 2 | 3-5 | Notable people | Brain + web + social + cross-reference |
| Tier 3 | 1-2 | Minor mentions | Brain + social lookup |

### Key Rules
- Store raw API data separately（auditable, re-processable）
- Never overwrite human-written assessments
- Don't re-enrich same page more than once per week
- X/Twitter is the most underrated data source
- Cross-references are NOT optional

### Person Page Sections
Executive Summary, State, What They Believe, What They're Building, What Motivates Them, Assessment, Trajectory, Relationship, Contact, Timeline

「Facts are table stakes. TEXTURE is the value.」

---

## 6. Brain vs Memory vs Session (docs/guides/brain-vs-memory.md)

| Layer | Stores | Route to |
|-------|--------|----------|
| GBrain | World knowledge: people, companies, deals, meetings, concepts | `gbrain search/get` |
| Agent memory | Operational state: preferences, decisions, tool config | `memory_search` |
| Session | Current conversation | automatic |

### Key Rules
- Don't store people in agent memory（Pedro's email preference is a fact about Pedro → GBrain）
- Don't store user preferences in GBrain（bullet point formatting → agent memory）
- User's synthesis of external ideas → GBrain originals/（the synthesis IS original）
- Agent memory doesn't survive resets on some platforms → critical world knowledge MUST be in GBrain

---

## 7. Recommended Schema (docs/GBRAIN_RECOMMENDED_SCHEMA.md)

### Three Founding Principles

1. **Every piece of knowledge has a primary home (MECE directories)** — decision tree, no duplicates. Every directory has a README.md resolver. Top-level RESOLVER.md is the master decision tree. Agent MUST read resolver before creating any page.

2. **Compiled Truth + Timeline (two-layer pages)** — above the line is synthesis (rewritten), below is evidence (append-only). 「The synthesis is pre-computed. Unlike RAG, where the LLM re-derives knowledge from scratch every query, your brain has already done the work.」

3. **Enrichment fires on every signal** — every pipeline automatically triggers enrichment on every entity it touches. 「The brain grows as a side effect of normal operations, not as a separate task you remember to do.」

### Four Database Primitives
1. Entity registry（canonical ID, aliases, external IDs）
2. Event ledger（immutable events with provenance）
3. Fact store（structured claims with source, confidence, timestamp — contradictions are data, not bugs）
4. Relationship graph（typed edges, enables graph queries）

### Directory Structure (MECE)
people/, companies/, deals/, meetings/, projects/, ideas/, concepts/, writing/, programs/, org/, civic/, media/, personal/, household/, hiring/, sources/, prompts/, inbox/, archive/

### Key Insight
「Knowledge management has failed for 30 years because maintenance falls on humans. LLM agents change the equation — they don't get bored, don't forget to update cross-references, and can touch 50 files in one pass.」

---

## 8. Markdown Skills as Recipes (docs/ethos/MARKDOWN_SKILLS_AS_RECIPES.md)

「Homebrew for Personal AI」— GBrain distributes recipes (markdown), not artifacts (binaries). Agent reads the recipe and builds a native implementation. No dependency hell, no version conflicts.

Distribution: build feature → GBrain captures recipe → push to repo → someone else's agent pulls recipe and implements it.

### Scale
- Real deployment: 14,700+ brain files, 40+ skills, 20+ cron jobs
- The memex vision realized: Vannevar Bush imagined a device where an individual stores everything. GBrain is that device, except the memex builds itself.
