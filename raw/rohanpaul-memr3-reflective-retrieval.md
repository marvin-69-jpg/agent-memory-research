---
source_type: tweet
author: rohanpaul_ai
url: https://x.com/rohanpaul_ai/status/2006305580734947499
date: 2025-12-31
views: 8876
likes: 132
---

# MemR³: Memory Retrieval via Reflective Reasoning (Rohan Paul)

MemR3 = controller that helps chat-style AI agents fetch the right memories by looping.

Core insight: most "memory for agents" work fails in a boring way — the agent does 1 retrieval, gets a messy pile of old notes, and then guesses anyway.

MemR3 changes the workflow: it forces the agent to keep an explicit "what I know so far" and an explicit "what is still missing," then keeps retrieving again with better queries until the missing part is gone.

That loop matters because memory mistakes are usually not about the model being dumb — they are about pulling the wrong past info, or stopping too early with half the facts.

So instead of betting everything on 1 perfect search query, MemR3 turns memory retrieval into an iterative process, like debugging, where each round is guided by what the last round failed to find.

That is why it can plug into existing memory stores and still lift results — it is mostly fixing the control logic, not inventing a new database.

It improves LoCoMo answer scores by up to 7.29% when it wraps a basic search-then-answer memory retriever.

Because the evidence and gaps are explicit, developers can inspect why each step happened, and MemR3 can sit on top of chunk search or graph memory.

Paper: arxiv.org/abs/2512.20237
Title: "MemR³: Memory Retrieval via Reflective Reasoning for LLM Agents"
