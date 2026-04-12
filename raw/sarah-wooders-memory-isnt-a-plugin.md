# Why Memory Isn't a Plugin (It's the Harness)

**Author**: Sarah Wooders (@sarahwooders), Letta CTO
**Date**: 2026-04-03
**Source**: https://x.com/sarahwooders/status/2040121230473457921

---

Ever since we've been working on MemGPT (now @Letta_AI), a common question @charlespacker and I have gotten is:

"how can I plug your memory system into my agent?"

To me, this question doesn't make sense. Asking to plug memory into an agent harness is like asking to plug driving into a car. Managing context, and therefore memory, is a core capability and responsibility of the agent harness. If a harness isn't managing context, what is it doing?

RAG over past session data (or processed form of it) can certainly be a plugin - but retrieval is a small part of memory. And even then, it's hard to do much better than just `grep`.

Because RAG is often branded as "memory," MemGPT has frequently been mistaken for RAG or a pluggable memory tool. But MemGPT was actually a stateful agent harness, before the term "harness" even existed. The agent's memory emerged from the tools the harness exposed for rewriting prompts and managing external state, combined with the harness's own context management.

Ultimately, the harness makes many invisible decisions that an external plugin can't control:

- How is the AGENTS.md or CLAUDE.md file loaded into context?
- How is skill metadata shown to the agents? (in the system prompt? in system messages?)
- Can the agent modify its own system instructions?
- What survives compaction, and what's lost?
- Are interactions stored and made queryable?
- How is memory metadata presented to the agent?
- How is the current working directory represented? How much filesystem information is exposed?

Different harnesses answer each of these questions differently. Your context window likely contains various context-related hints passed through system messages that you never see.

As an example: in recent analysis of Claude Code's memory system (from their leaked source code), you can see how a multi-level memory hierarchy is built directly into the harness.

Letta Code, a memory-first agent harness, takes this even further - projecting agent memory to a git-backed filesystem that can be concurrently modified by background memory subagents specializing in prompt rewriting and active memory management.

Letta's recently released Context Constitution outlines the common principles agents follow for context management, which is tightly coupled with harness design.

Ultimately, how the harness manages context and state in general is the foundation for agent memory.
