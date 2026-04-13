---
aliases: [autoreason, A/B/AB tournament, self-refinement]
first_seen: 2026-04-14
last_updated: 2026-04-14
tags: [product, architecture]
---

# Autoreason

Nous Research 發表的 iterative self-refinement 方法，解決 LLM 在主觀領域反覆修改時的結構性失敗（sycophancy、overcriticism、authorship bias、scope drift）。受 Karpathy AutoResearch 啟發，延伸到沒有 objective metric 的領域。

## Current Understanding

- **核心機制**：A/B/AB Tournament
  - A = incumbent（現有版本，"do nothing" 選項）
  - B = adversarial revision（根據 critique 修改）
  - AB = synthesis（取兩者最佳元素）
  - 三者由 **fresh isolated agents**（無共享 context）blind 評比
  - Borda count 投票 + conservative tiebreak（平手 incumbent 贏）
  - A 連贏 k 次 → 收斂（知道何時該停）
- **"Do nothing" is first-class** — 讓模型能說「不需要改」，打破 overcriticism 循環
- **Fresh agents per role per pass** — 刻意不給 context history，防止 authorship bias。這是一種 **memory isolation by design**，跟 [[actor-aware-memory]] 的 inference cascade 問題反向處理：不是追蹤記憶來源，而是直接切斷記憶
- **Bloat/Prune Oscillation** — AB 系統性增加複雜度、B 系統性刪減。當 task 的 scope 未定義時，兩股力量形成穩定震盪而非穩定均衡。這跟 [[scaffolding-lifecycle]] 的 build/remove 循環在更微觀層面呼應
- **Results**：
  - Haiku 3.5 + autoreason 42/42 完美 Borda，所有 baseline 退化到比 single-pass 差
  - Sonnet 4.6 CodeContests: 77% vs 73% single-pass
  - Haiku 3.5: 40% vs 31% best-of-6（matched compute）
  - **Transition point**：Haiku 4.5 在 60% accuracy 時 autoreason 增益消失 — generation-evaluation gap 已關閉
- **Meta-recursive**：論文本身用 autoreason + Opus 4.6 寫成。寫論文過程中開發了 research-paper-writing skill → [[procedural-memory]] 的實例
- **Scaling insight**：模型越強，self-refinement 的邊際收益越低。當模型夠強到一次生成就接近最佳，iterative refinement 的開銷不再值得 → 跟 [[scaffolding-lifecycle]] 的「模型變強 scaffolding 要拆」完全一致

## For Agent Memory Research

- **Memory isolation as feature** — autoreason 刻意不讓 agent 記住之前的 pass，用「失憶」來獲得公正性。這挑戰了 [[compounding-memory]] 的「越記越聰明」假設 — 有些場景下，遺忘是 feature
- **Convergence = knowing when to stop updating** — 跟 [[memory-staleness]] 的問題相關：什麼時候該停止更新一條記憶？Autoreason 用 k consecutive wins 作為 stopping criterion
- **Judge panel as subjective fitness function** — 沒有 objective metric 時，用多個 independent evaluator 的 consensus 當作品質信號。可能適用於 memory quality evaluation

## Key Sources

- **2026-04-12** — SHL0MS 推文（208.6K views）+ GitHub repo。Source: [[raw/shl0ms-autoreason]]

## Related

[[shl0ms]] [[scaffolding-lifecycle]] [[actor-aware-memory]] [[procedural-memory]] [[thin-harness-fat-skills]] [[compounding-memory]] [[memory-staleness]] [[agent-harness]]
