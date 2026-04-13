# Brutally Unsentimental Architecture

- **Author**: Aaron Levie (@levie, Box CEO)
- **Date**: 2026-04-03
- **Source**: https://x.com/levie/status/2039931799414194621
- **Views**: 109.7K
- **Type**: Tweet

---

One of the biggest lessons thus far in building AI agents is you have to be brutally unsentimental in your architecture.

The models get better and better at handling things you previously built scaffolding for, you need to ruthlessly jettison your prior tech to get those new performance gains.

The rough loop of building AI agents looks something like:

1. Build a bunch of systems around the LLM to ensure that the agent can solve specific tasks very well
2. The model capabilities dramatically improve, rendering many of those systems redundant or even harmful
3. Remove prior scaffolding to get the new performance gains from the agent
4. New capabilities emerge in the models that let you solve a new set of much harder problems
5. Go back to step 1

For instance, in our new Box Agent, from the moment we designed the original architecture to the ultimate release, we had to evolve multiple components of agent harness simply because some parts were creating unnecessary constraints for the agents as models improved.

The models continued to get insanely good at more complex reasoning, improvements in using search and other tools, writing code on the fly for new capabilities, improving context window performance for accuracy, and more.

Many of the mitigations we put in place for the Box Agent (like to appropriately find data that users were looking for, or ways of chunking text to deal with context window limitations), eventually meant we got lower quality results or meant we were overfitting for specific use-cases, as soon as the models got better.

The main lesson is always make sure you're taking advantage of the frontier capabilities and don't become nostalgic around the tech you've already built.
