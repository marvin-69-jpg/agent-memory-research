# I Reverse Engineered ChatGPT's Memory System

- **Author**: Manthan Gupta (@godofprompt)
- **Date**: 2025-12-09
- **Source**: https://manthanguptaa.in/posts/chatgpt_memory/
- **Type**: Blog (reverse engineering through conversation, not official docs)

---

## Core Finding

ChatGPT's memory system is far simpler than expected. **No vector databases. No RAG over conversation history.** Four distinct layers of static injection.

## ChatGPT Context Structure

Every message receives:

```
[0] System Instructions
[1] Developer Instructions
[2] Session Metadata (ephemeral)
[3] User Memory (long-term facts)
[4] Recent Conversations Summary (past chats)
[5] Current Session Messages (this chat)
[6] Your latest message
```

## Layer 2: Session Metadata (Ephemeral)

Injected once at session start, not stored permanently:
- Device type, browser, user agent
- Rough location/timezone
- Subscription level
- Usage patterns and activity frequency
- Recent model usage distribution (gpt-5 49%, gpt-4o 17%, etc.)
- Screen size, dark mode, JS enabled
- Session duration

## Layer 3: User Memory (Persistent)

Dedicated tool for storing/deleting stable long-term facts. Author had 33 stored facts.

Stored only when:
1. User says "remember this"
2. Model detects fact fitting OpenAI criteria (name, job, preferences) + implicit consent

Injected into **every future prompt** as separate block. ~10k token limit.

## Layer 4: Recent Conversations Summary (Persistent)

**Most surprising finding**: expected RAG, found lightweight digest instead.

Format: `<Timestamp>: <Chat Title> |||| user message snippet ||||`

Key observations:
- **Only summarizes user messages**, not assistant responses
- ~15 summaries available
- Loose map of recent interests, not detailed context
- Pre-computed and injected directly

**Why not RAG?** Speed over completeness. Pre-computed summaries avoid embedding/search/retrieval latency. Trades detailed context for efficiency.

## Layer 5: Current Session (Sliding Window)

- Token-based cap (not message count)
- Older messages roll off, but memory facts + conversation summaries remain
- Everything passed verbatim

## Design Philosophy

> "Not everything needs to be 'memory' in the traditional sense. Sometimes a simpler, more curated approach outperforms complex retrieval systems."

Trade-off: **sacrifices detailed historical context for speed and efficiency**.
