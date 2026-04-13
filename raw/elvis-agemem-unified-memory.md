# AgeMem: Unified Long-Term + Short-Term Memory via RL

- **Author**: Elvis / omarsar0 (@omarsar0, DAIR.AI founder)
- **Date**: 2026-01-12
- **Source**: https://x.com/omarsar0/status/2010712137933730234
- **Views**: 56.4K
- **Paper**: https://arxiv.org/abs/2601.01885
- **Type**: Tweet + paper summary

---

Great paper on Agentic Memory.

LLM agents need both long-term and short-term memory to handle complex tasks.

However, the default approach today treats these as separate components, each with its own heuristics, controllers, and optimization strategies.

But memory isn't two independent systems. It's one cognitive process that decides what to store, retrieve, summarize, and forget.

This new research introduces AgeMem, a unified framework that integrates long-term and short-term memory management directly into the agent's policy through tool-based actions.

Instead of relying on trigger-based rules or auxiliary memory managers, the agent learns when and how to invoke memory operations: ADD, UPDATE, DELETE for long-term storage, and RETRIEVE, SUMMARY, FILTER for context management.

It uses a three-stage progressive RL strategy:
1. First, the model learns long-term memory storage.
2. Then it masters short-term context management.
3. Finally, it coordinates both under full task settings.

To handle the fragmented experiences from memory operations, they design a step-wise GRPO (Group Relative Policy Optimization) that transforms cross-stage dependencies into learnable signals.

The results across five long-horizon benchmarks:

- On Qwen2.5-7B, AgeMem achieves 41.96 average score compared to 37.14 for Mem0, a 13% improvement.
- On Qwen3-4B, the gap widens: 54.31 vs 44.70. Adding long-term memory alone provides +10-14% gains.
- Adding RL training adds another +6%.
- The full unified system with both memory types achieves up to +21.7% improvement over no-memory baselines.

The unified memory management through learnable tool-based actions outperforms fragmented heuristic pipelines, enabling agents to adaptively decide what to remember and forget based on task demands.
