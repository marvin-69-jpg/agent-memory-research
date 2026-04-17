---
aliases: [Meta-Harness, meta harness, automated harness optimization, harness search]
first_seen: 2026-04-16
last_updated: 2026-04-16
tags: [product, harness, architecture]
---

# Meta-Harness

Stanford IRIS Lab 的 automated harness optimization framework（arxiv 2603.28052）。用 coding agent 作為 proposer，自動搜尋最佳 model harness 設計。**同一個模型，不同 harness 可以產生 6x 性能差異** — Meta-Harness 把手動的 harness engineering 自動化。

## Current Understanding

### 核心洞察

Harness = 包裹 LLM 的外部程式，決定 store/retrieve/show 什麼。目前 harness 設計是人工迭代（inspect failures → adjust heuristics → repeat）。Meta-Harness 讓 **coding agent 自己做這個迭代**。

### Search Loop

```
Initialize harnesses → Evaluate → [Proposer inspects full history filesystem]
                                          ↓
                                   Propose k new harnesses
                                          ↓
                                   Validate + Evaluate → Log to filesystem
                                          ↓
                                   Repeat 20 iterations (~60 evaluations)
                                          ↓
                                   Return Pareto frontier
```

### 三個關鍵設計

1. **Filesystem-based full history**：每個 candidate 的完整 source code + evaluation scores + execution traces。單次 evaluation 可產生 **10M tokens** 診斷資料。Proposer 用 grep/cat 自行選擇看什麼
2. **Agentic proposer**（Claude Code + Opus 4.6）：不是固定 heuristic，是 autonomous agent 自己決定檢查什麼、修改什麼
3. **Code-space search**：直接在 code space 優化 harness 的 retrieval/memory/prompt logic，不只是 prompt tuning

### Full Traces vs Lossy Feedback

| Feedback Level | Median Acc | Best Acc |
|---|---|---|
| Scores only | 34.6% | 41.3% |
| Scores + summary | 34.9% | 38.7% |
| **Full Meta-Harness** | **50.0%** | **56.7%** |

Ablation 證明 raw traces 比 summary 好 15+ 點。**Lossy feedback 不夠做 causal reasoning** — 這呼應了 [[memory-failure-modes]] 的 compaction information loss。

### 實驗結果

| Domain | Result | Baseline |
|---|---|---|
| Text Classification (GPT-OSS-120B) | 48.6% acc, 4x fewer tokens | ACE 40.9% |
| Math Reasoning (IMO-level) | +4.7 pts avg across 5 models | No retrieval baseline |
| TerminalBench-2 (Opus 4.6) | 76.4% pass (#2 leaderboard) | Terminus-KIRA 74.7% |
| TerminalBench-2 (Haiku 4.5) | 37.6% pass (#1 all Haiku) | Goose 35.5% |

### 與 wiki 其他概念的連結

- **[[harness-engineering]]**：Meta-Harness 把人工 harness engineering 自動化。之前是 practitioner 的 craft，現在可以 search
- **[[scaffolding-lifecycle]]**：proposer 在 TerminalBench-2 實驗中自動從 aggressive rewrites → additive modifications。**自動判斷什麼該留、什麼該改** — 解決了 Aaron Levie 的「什麼時候拆 scaffolding」問題
- **[[context-rot]]**：如果 resolver 會在 90 天內 rot（Garry Tan），Meta-Harness 可以定期自動重新優化 — 是 self-healing resolver 的學術版本
- **[[mece-resolver]]**：Garry Tan 的 trigger evals + check-resolvable 是 manual verification；Meta-Harness 的 search loop 是 automated version
- **[[thin-harness-fat-skills]]**：Meta-Harness 搜尋的對象就是 harness。但它假設 harness = single-file Python program — 跟 Garry Tan 的 fat skills in markdown 架構不同
- **Memory system search**：text classification 實驗中，Meta-Harness 發現的 harnesses 包含 **memory-based context construction**（Draft Verification、Label-Primed Query）— 自動發現了 memory patterns

### 作者

- **Yoonho Lee**（Stanford IRIS Lab）— 第一作者
- **Omar Khattab**（MIT）— DSPy 創造者。從 prompt optimization（DSPy）到 harness optimization（Meta-Harness）的自然延伸
- **Chelsea Finn**（Stanford）— 指導教授。Meta-learning 專家 — Meta-Harness 就是把 meta-learning 從 weight space 搬到 harness space

### 限制

- Proposer 用 Claude Code + Opus 4.6 — 搜尋成本不低
- 假設 harness = single-file Python program — real-world harness 通常更複雜
- 60 evaluations × 可能數百 tasks = 大量 compute

### 應用到新 domain（從 repo README）

開源 framework 的設計讓使用者能把 Meta-Harness 套到自己的 domain：

1. **Onboarding flow**：把 coding assistant 指向 `ONBOARDING.md`，跟它對話會產出 `domain_spec.md` — 這份 spec 描述目標 domain 的 harness 該長什麼樣
2. **Reference examples**：`reference_examples/text_classification/` 和 `reference_examples/terminal_bench_2/` 是兩個 paper 用過的完整 case，可以對照改
3. **Proposer 替換點**：預設 proposer 是 Claude Code，要換別的 agent 改 `claude_wrapper.py`，主要 contract 是「乾淨地 log proposer interactions」— 為了讓 filesystem D 能保留全 history，proposer 必須產生可被 grep 的痕跡
4. **Quick start**：`uv sync && uv run python meta_harness.py --iterations 1` — 一次 iteration 只是 smoke test，paper 用的是 20 iterations

開源策略有意思：**framework code + 兩個 reference experiment 在 main repo，TerminalBench-2 的 production artifact 在另一個 repo**（`stanford-iris-lab/meta-harness-tbench2-artifact`）。這呼應了 Meta-Harness 的核心抽象 — framework（搜尋邏輯）和 discovered harness（搜出來的成品）是兩種不同的產物。

## Key Sources

- **2026-03-28** — Meta-Harness: End-to-End Optimization of Model Harnesses（arxiv 2603.28052）。Source: [[raw/stanford-meta-harness]]
- **2026-04-16** — github.com/stanford-iris-lab/meta-harness（repo README，操作層細節）

## Related

[[harness-engineering]] [[scaffolding-lifecycle]] [[context-rot]] [[context-engineering]] [[thin-harness-fat-skills]] [[mece-resolver]] [[agent-harness]] [[memory-failure-modes]] [[coding-agent-memory]] [[memory-evaluation]] [[session-management]] [[self-improving-agent]] [[asg-si]] [[skillfoundry]] [[mstar]]
