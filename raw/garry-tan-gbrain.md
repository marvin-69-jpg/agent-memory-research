# GBrain

**Author**: Garry Tan (@garrytan)
**Date**: 2026 (repo active)
**Source**: https://github.com/garrytan/gbrain

---

Your AI agent is smart but it doesn't know anything about your life. GBrain fixes that. Meetings, emails, tweets, calendar events, voice calls, original ideas... all of it flows into a searchable knowledge base that your agent reads before every response and writes to after every conversation. The agent gets smarter every day.

~30 minutes to a fully working brain. Your agent does the work. Database ready in 2 seconds (PGLite, no server). Schema, import, embeddings, and integrations take 15-30 minutes depending on brain size. You just answer questions about API keys.

Requires a frontier model. Tested with Claude Opus 4.6 and GPT-5.4 Thinking. Likely to break with smaller models.

## Architecture

```
┌──────────────────┐    ┌───────────────┐    ┌──────────────────┐
│   Brain Repo     │    │    GBrain     │    │    AI Agent      │
│   (git)          │    │  (retrieval)  │    │  (read/write)    │
│                  │    │               │    │                  │
│  markdown files  │───>│  Postgres +   │<──>│  skills define   │
│  = source of     │    │  pgvector     │    │  HOW to use the  │
│    truth         │    │               │    │  brain           │
│                  │<───│  hybrid       │    │                  │
│  human can       │    │  search       │    │  entity detect   │
│  always read     │    │  (vector +    │    │  enrich          │
│  & edit          │    │   keyword +   │    │  ingest          │
│                  │    │   RRF)        │    │  brief           │
└──────────────────┘    └───────────────┘    └──────────────────┘
```

The repo is the system of record. GBrain is the retrieval layer. The agent reads and writes through both. Human always wins — you can edit any markdown file directly and gbrain sync picks up the changes.

## The Compounding Thesis

Most tools help you find things. GBrain makes you smarter over time.

Signal arrives (meeting, email, tweet, link)
  → Agent detects entities (people, companies, ideas)
  → READ: check the brain first (gbrain search, gbrain get)
  → Respond with full context
  → WRITE: update brain pages with new information
  → Sync: gbrain indexes changes for next query

Every cycle through this loop adds knowledge. The agent enriches a person page after a meeting. Next time that person comes up, the agent already has context. You never start from zero.

An agent without this loop answers from stale context. An agent with it gets smarter every conversation. The difference compounds daily.

## The Knowledge Model

Every page in the brain follows the compiled truth + timeline pattern:

```markdown
---
type: concept
title: Do Things That Don't Scale
tags: [startups, growth, pg-essay]
---

Paul Graham's argument that startups should do unscalable things early on.
[compiled truth above the separator]

---

- 2013-07-01: Published on paulgraham.com
- 2024-11-15: Referenced in batch W25 kickoff talk
[timeline below, append-only]
```

Above the --- separator: compiled truth. Your current best understanding. Gets rewritten when new evidence changes the picture. Below: timeline. Append-only evidence trail. Never edited, only added to.

The compiled truth is the answer. The timeline is the proof.

## How Search Works

- Multi-query expansion (Claude Haiku)
- Vector search (HNSW cosine, text-embedding-3-large)
- Keyword search (tsvector + ts_rank)
- RRF Fusion: score = sum(1/(60 + rank))
- 4-Layer Dedup: best chunk per page, cosine similarity > 0.85, type diversity (60% cap), per-page chunk cap
- Stale alerts (compiled truth older than latest timeline)

## Three-Layer Memory Model

| Layer | What it stores | How to query |
|-------|---------------|--------------|
| gbrain | People, companies, meetings, ideas, media | gbrain search, gbrain query, gbrain get |
| Agent memory | Preferences, decisions, operational config | memory_search |
| Session context | Current conversation | (automatic) |

## Database Schema (10 tables)

- pages (slug, type, title, compiled_truth, timeline, frontmatter JSONB, search_vector, content_hash)
- content_chunks (page_id, chunk_text, chunk_source, embedding vector 1536-dim)
- links (from_page_id, to_page_id, link_type)
- tags (page_id + tag)
- timeline_entries (page_id, date, source, summary, detail)
- page_versions (compiled_truth, frontmatter, snapshot_at)
- raw_data (page_id, source, data JSONB)
- files (page_slug, storage_path, content_hash, mime_type)
- ingest_log
- config

## Chunking Strategies

1. **Recursive** (timeline, bulk import): 5-level delimiter hierarchy, 300-word chunks, 50-word overlap
2. **Semantic** (compiled truth): Embed sentences, cosine similarities, Savitzky-Golay smoothing for topic boundaries
3. **LLM-guided** (high-value content): Pre-split 128-word candidates, Claude Haiku identifies topic shifts

## Integrations

| Recipe | What It Does |
|--------|-------------|
| Voice-to-Brain | Phone calls → brain pages (Twilio + OpenAI Realtime) |
| Email-to-Brain | Gmail → entity pages |
| X-to-Brain | Twitter → brain pages |
| Calendar-to-Brain | Google Calendar → searchable daily pages |
| Meeting Sync | Circleback transcripts → brain pages |

## Skills (fat markdown files)

| Skill | What it does |
|-------|-------------|
| ingest | Ingest meetings, docs, articles. Rewrite compiled truth, append timeline |
| query | 3-layer search with synthesis and citations |
| maintain | Periodic health: contradictions, stale pages, orphans, dead links |
| enrich | Enrich pages from external APIs |
| briefing | Daily briefing with meeting prep |
| migrate | Migration from Obsidian, Notion, Logseq, plain markdown |

## Scale

- Real deployment: 10,000+ markdown files, 3,000+ people dossiers, 13 years calendar data, 280+ meeting transcripts, 300+ captured ideas
- Storage for 7,500 pages: ~750MB total in Postgres
- Embedding cost: ~$4-5 for 7,500 pages (OpenAI text-embedding-3-large)
- PGLite for local, Supabase Pro ($25/mo) for production

## Key Quotes

"An agent without this loop answers from stale context. An agent with it gets smarter every conversation. The difference compounds daily."

"The compiled truth is the answer. The timeline is the proof."

"The agent runs while I sleep. The dream cycle scans every conversation, enriches missing entities, fixes broken citations, and consolidates memory. I wake up and the brain is smarter than when I went to sleep."

## Author Background

Garry Tan is CEO of Y Combinator. Built GBrain for personal use with OpenClaw/Hermes agents, grew to 10,000+ files organically.
