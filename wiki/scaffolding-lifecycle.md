---
aliases: [scaffolding lifecycle, scaffolding removal, brutally unsentimental architecture, 鷹架生命週期]
first_seen: 2026-04-13
last_updated: 2026-04-13
tags: [harness, architecture]
---

# Scaffolding Lifecycle

Agent scaffolding 不是永久建設 — 它有生命週期。模型變強時，之前的 scaffolding 變成不必要的限制，必須拆掉。

## Current Understanding

- **Aaron Levie（Box CEO, 109.7K views）的 loop**：
  1. 在 LLM 周圍建系統確保特定 task 做好
  2. Model 能力大幅提升，很多系統變得 redundant 甚至 harmful
  3. 移除舊 scaffolding 來獲得新 model 的性能提升
  4. 新能力解鎖更難的問題
  5. 回到步驟 1
- **Box Agent 的實際經驗**：
  - 設計到發布之間必須多次 evolve harness 組件
  - 為 data finding 和 chunking 做的 mitigations，在模型變好後反而**降低品質**或**過度擬合**特定場景
  - 核心教訓：**不要對你已建的技術產生感情（don't become nostalgic）**
- **與 Garry Tan thin harness 的對比**：
  - Garry Tan：harness 一開始就該 thin，intelligence 放 skills
  - Levie：不管一開始多厚，模型變強時都要 ruthlessly jettison
  - 兩者互補：thin harness 是起點，lifecycle awareness 是持續維護
- **NLAH 的回應**：Natural-Language Agent Harnesses 讓 harness 變成可 ablate 的模組 — 更容易測試哪個 scaffolding 還有用、哪個該拆
- **與我們的實踐**：openab-bot 的 behavior benchmark 可以量化測試每個 rule/hook 的效果。如果某個 hook 變得不需要（因為模型自己就會做），benchmark 會顯示它是 redundant
- **[[context-rot]]**：scaffolding 不只因為模型變強而需要拆，也因為**系統演化而自然腐敗**。Garry Tan 的 resolver 在 90 天內從完美退化為歷史文件 — 需要 check-resolvable + trigger evals 持續維護
- **[[meta-harness]]（Stanford, 2026）**：把 scaffolding lifecycle 自動化。Proposer agent 自動判斷什麼該留、什麼該改。TerminalBench-2 實驗中觀察到 proposer 從 aggressive rewrites → additive modifications — **自動學會了 Levie 的 "don't become nostalgic" 原則**
- **Autoreason 的微觀版本**：[[autoreason]] 的 bloat/prune oscillation 是同一個 pattern 在單次 task 層面的體現 — AB（synthesis）系統性增加複雜度，B（adversarial revision）系統性刪減。當模型夠強（Haiku 4.5 transition point），refinement 增益消失 — 跟 Levie 的「模型變強 scaffolding 要拆」一致

## Key Sources

- **2026-04-03** — Aaron Levie: brutally unsentimental architecture loop（109.7K views）。Source: [[raw/aaron-levie-unsentimental-architecture]]

## Related

[[agent-harness]] [[harness-engineering]] [[thin-harness-fat-skills]] [[context-engineering]] [[autoreason]] [[aaron-levie]] [[context-rot]] [[mece-resolver]] [[garry-tan]] [[meta-harness]]
