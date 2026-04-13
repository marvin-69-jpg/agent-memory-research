# Autoreason: Self-Refinement That Knows When to Stop

- **Author**: SHL0MS + Hermes Agent (Nous Research)
- **Date**: 2026-04-12
- **Source**: https://x.com/shl0ms/status/2043415274196435325 + https://github.com/NousResearch/autoreason
- **Views**: 208.6K

---

## Core Problem

Iterative self-refinement fails for three structural reasons:
- **Prompt bias**: models hallucinate flaws when asked to critique
- **Scope creep**: outputs expand unchecked each pass
- **Lack of restraint**: models never say "no changes needed"

Additional failure modes:
- **Sycophancy**: "make this better" → "make this more of what it already is"
- **Overcriticism**: critique instruction interpreted as instruction to change — saying "this is fine" feels like task failure
- **Overcompromise**: synthesize two perspectives → mushy average, hedging everything
- **Authorship bias**: agent that wrote version A defends it even while "incorporating feedback"
- **Scope drift**: each iteration adds hedging, caveats, complexity — bloats away from task
- **Context collapse**: (ACE, Zhang et al. ICLR 2026)

## Method: A/B/AB Tournament

```
Task Prompt → Incumbent A
                  ↓
        ┌─── Critic (fresh agent) ───→ Critique
        │
        ├─── Author B (fresh agent) ──→ Revision (B)
        │
        └─── Synthesizer (fresh) ─────→ Synthesis (AB)
                  ↓
          Judge Panel (3 fresh agents, Borda count)
                  ↓
              Winner → new A  (or converge if A wins k=2 times)
```

- **A** = conservatism: current version is fine, changes made things worse
- **B** = adversarial editing: critique found real problems, revision fixes them
- **AB** = objectivity: both versions got some things right, synthesis keeps the best of each
- **"Do nothing" is always a first-class option** — A can win

### Key Design Choices

1. **Fresh isolated agents per role per pass** — no shared context → prevents authorship bias
2. **Blind evaluation** — judges don't know which version is which
3. **Borda count** — ranked choice voting across judge panel
4. **Conservative tiebreak** — incumbent wins ties → favors stability over churn
5. **Convergence at k consecutive A wins** — knows when to stop

## Key Results

| Finding | Detail |
|---------|--------|
| **42/42 perfect sweep** | Haiku 3.5 + autoreason scored perfect Borda across 3 tasks; all baselines *degraded* below single-pass |
| **77% vs 73%** | Sonnet 4.6 on 150 CodeContests problems (private-test), autoreason vs single-pass |
| **40% vs 31%** | Haiku 3.5 autoreason vs best-of-6 sampling at matched compute (150 problems) |
| **Haiku 4.5: transition point** | At 60% private accuracy, autoreason's held-out gains vanish — the generation-evaluation gap has closed |
| **Code scaling curve** | Haiku 3.5 (40%) → Haiku 4.5 (60%) → Sonnet 4 (64%) → Sonnet 4.6 (77%) private-test with autoreason |
| **Refinement destroys weak models** | Critique-and-revise reduced Haiku 3.5 outputs by 59–70% in word count over 15 passes |
| **7 judges → 3× faster convergence** | Than 3 judges; 1 judge is noisy and slow |

## Bloat/Prune Oscillation

Structural finding from 26-pass experiment:
- **Phase 1 (1–5)**: Rapid improvement, B and AB win easily
- **Phase 2 (6–16)**: Quality plateau, A starts surviving on close calls
- **Phase 3 (17–26)**: B re-emerges to prune bloat that AB added → stable oscillation

> "AB systematically adds complexity. B systematically prunes it. When the task is ambiguous about scope, these two forces create a stable oscillation rather than a stable equilibrium. This isn't a bug — it's a real signal that the task itself is underdetermined along the scope dimension."

5-way baseline comparison (7-judge blind panel):
- autoreason 35/35 Borda, 7/7 first place unanimous
- conservative 21
- improve_this 18
- harsh_critic 18
- critique_and_revise 13

## Meta-Recursive: The Paper Was Written With Autoreason

- Paper itself was refined using autoreason (Opus 4.6)
- The research-paper-writing skill was developed *during* the writing process
- Used Hermes Agent by Nous Research as the co-author agent

## Technical Details

- All experiments: claude-sonnet-4-20250514 (temp=0.8 author, temp=0.3 judge)
- Paper revision: claude-opus-4-6 (temp=0.7 author, temp=0.2 judge)
- 3-judge panel for experiments, 7-judge for final baselines
- ~160 LLM calls per 26-pass run (~2.5 min/pass)
- Code experiments: 150 CodeContests problems × 3 strategies × 4 model tiers

## Related Work (cited in paper)

- Karpathy's AutoResearch — inspiration, objective domains
- SlopCodeBench (Orlanski et al. 2026) — prompting doesn't fix code sycophancy
- ACE context collapse (Zhang et al. ICLR 2026)
- LLM Council — multi-agent evaluation
