# Why Long-Term Memory for LLMs Remains Unsolved

- **Author**: Chrys Bader (@chrysb)
- **Date**: 2026-04-12
- **Source**: https://x.com/chrysb/status/2043020014035570784
- **Views**: 262.1K

---

## Core Thesis

Despite what you see, long-term memory for conversational LLMs remains an unsolved problem. The dream: model remembers what you said before and draws meaning across it over time — not just recall, but interpretation, narrative, continuous and cumulative across months or years.

Today you can achieve an illusion. For days, or weeks if you're lucky. Until the LLM starts forgetting and the illusion breaks.

## The Raw vs Derived Spectrum

There are ultimately only two ways to preserve information from a conversation:
- **Raw** — original messages, stored verbatim
- **Derived** — summaries, narratives, structured extractions

Every memory system is choosing a position on this spectrum. Neither extreme works.

- Raw is lossless but inert. A pile of transcripts isn't understanding. Nothing is connected, prioritized, or interpreted.
- Derived is compact and usable, but repeated derivation drifts from the source the way a photocopy of a photocopy degrades. You lose it gradually, and can't tell exactly when it stopped being accurate.

## Why Infinite Context Won't Solve This

1. **Cost** — even if you could fit 2 years of history, you'd pay to process all of it every turn. Economics are brutal, scale linearly. No consumer product survives that margin structure.
2. **Degradation** — models get worse as context fills. Attention drops on information in the middle, reasoning quality declines, instruction following gets sloppier. Paying more for worse performance.

> Infinite context is just the extreme version of the raw path.

## The Evaluation Paradox

To know if a memory system is working, you need ground truth. But for real conversational memory spanning months/years, the ground truth is the entire history — larger than any context window and larger than any human can annotate.

> Benchmarks like LongMemEval can test needle-in-haystack retrieval, but retrieval alone isn't memory. Memory is what happens when facts change, when old context gets superseded, when the significance of a conversation only becomes clear weeks later.

> Nobody can actually prove theirs works, because any judge you'd use to evaluate the full history has the same context limitations as the system it's judging.

## The 9 Design Axes

Every memory system is a composition of choices across:

1. **What gets stored** — raw, derived, or mix
2. **When derivation happens** — real-time, async, batch
3. **What triggers a write** — every turn? heuristic? model-decided?
4. **Where it gets stored** — filesystem, vector DB, graph DB, document DB (most real systems use >1)
5. **How it gets retrieved** — semantic search, full-text, graph traversal, filesystem navigation
6. **Post-retrieval processing** — re-ranking, filtering, summarization. "Cheap retrieval plus smart re-ranking often beats expensive retrieval alone"
7. **When retrieval happens**:
   - Always-injected — pollutes context with irrelevant history
   - Hook-driven — covers passive awareness but expensive, can make model "perform memory rather than have it"
   - Tool-driven — respects model's judgment but "model doesn't know what it doesn't know, so it often fails to fetch when it should"
8. **Who is doing the curating** — main model (expensive), cheap model (sloppier), user (accurate but friction)
9. **Forgetting policy** — what gets forgotten, how forgetting propagates, when forgetting happens

> When a new memory solution lands, you can lay it on this map and see exactly which choices it made and which ones it's punting on.

### On Forgetting

> Forgetting in a memory system isn't a single delete operation. If you stored raw turns and derived summaries from them, deleting the raw turns doesn't delete the summaries. If you extracted facts into a graph, deleting the source conversation leaves the facts orphaned. Real forgetting requires either tracking provenance (so you can cascade deletes) or periodically re-deriving everything from a smaller raw corpus, which is expensive.

> Forgetting too aggressively means losing context the user wanted preserved. Forgetting too conservatively means accumulating an inaccurate model of the user that gets harder to correct over time. There's no right setting, only trade-offs.

## 10 Common Failure Modes

1. **Session amnesia** — new session starts with no awareness of previous ones
2. **Entity confusion** — model misidentifies or merges distinct entities during derivation
3. **Over-inference** — model encodes exaggerated or incorrect interpretations as facts
4. **Derivation drift** — chained summarizations compound small errors; after enough rounds, memory diverges from what was actually said
5. **Retrieval misfire** — surfaces semantically similar but contextually wrong memories
6. **Stale context dominance** — old, heavily-referenced memories crowd out recent ones
7. **Selective retrieval bias** — retrieval only finds what matches current query's framing; memories under different topic/register are invisible
8. **Compaction information loss** — when summaries replace raw turns, specific details vanish
9. **Confidence without provenance** — system states a "memory" with full confidence but no way to trace back to what was actually said
10. **Memory-induced bias** — system's responses always colored by what it already knows; sometimes you want an uncolored take

---

> "There are no solutions. There are only trade-offs." — Thomas Sowell
