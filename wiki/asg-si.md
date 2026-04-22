---
aliases: [ASG-SI, Audited Skill-Graph Self-Improvement]
first_seen: 2026-04-17
last_updated: 2026-04-18
tags: [product, memory, architecture, governance]
---

# ASG-SI（Audited Skill-Graph Self-Improvement）

Ken Huang & Jerry Huang 在 2025-12 提出的 framework（arxiv 2512.23760）。**把 self-improvement 重新框定為「把 agent 編譯進一個成長中、可審計的 skill graph」**，解決 deployed self-improving agents 的 governance 問題。

## Current Understanding

### 解決什麼問題

Deployed self-improving agents 有三個未解的 governance 問題：

1. **Reward hacking** — 優化壓力會誘發 reward 漏洞利用
2. **Behavioral drift** — 行為改變難 audit 或 reproduce
3. **Opaque parameter updates** — 改進綁在 weights 裡，不是可重用、可驗證的 artifacts

### 核心提案

每個 candidate improvement 走這個 pipeline：

```
Successful trajectory
       ↓
Extract → normalize 成 skill with explicit interface
       ↓
Verifier-backed replay + contract check
       ↓
Pass → promote to skill graph
Fail → reject + audit log
```

### 三個關鍵設計

1. **Skill normalization with explicit interface**：每個 skill 有明確 inputs/outputs/前後條件，不是 weight delta
2. **Verifier-backed replay**：promote 前必須能在 verifier 上 replay
3. **Reward decomposition**：reward 拆成可從 replayable evidence 重建的組件，讓 promotion 決定獨立可 audit

### 額外組件

- **Experience synthesis**：合成 stress test scenarios 考驗 candidate skill 的 robustness
- **Continual memory control**：在 bounded context 下維持 long-horizon performance

### 哲學立場

> "ASG-SI reframes agentic self-improvement as accumulation of verifiable, reusable capabilities, offering a practical path toward reproducible evaluation and operational governance of self-improving AI agents."

跟傳統 RL fine-tuning 對比：

| | RL fine-tuning | ASG-SI |
|---|---|---|
| 學到的東西在哪 | weights（不透明） | skill graph（可讀、可審計） |
| 可重用 | 綁在這個 model | 可移植 |
| Audit | 黑盒 | contract + replay log |
| Reward hacking 防護 | 弱 | 強 |
| Rollback | 重訓 | prune skill |

### 與其他工作的關係

- **[[self-improving-agent]]**：ASG-SI 是 skill-based self-improvement 的代表
- **[[meta-harness]]**：類似的「外化成 artifact」精神，但 Meta-Harness 改的是 harness code 不是 skill graph
- **[[ssgm]]**：governance 角度的近親，SSGM 處理 memory governance，ASG-SI 處理 skill governance
- **Voyager (Wang et al 2023)**：minecraft skill library 先行者，但無 audit/governance
- **Anthropic Claude Skills**：reusable skills 概念類似，但 hand-crafted

### 為什麼重要

如果 self-improving agents 要 deploy 到真實場景，governance 是必經之路。ASG-SI 提供一條技術路徑：把改進變成 verifiable artifacts，audit、rollback、reproducibility 都變可能。這比「我們有 trust 機制 + RLHF」更具體。

### 限制

- Verifier 本身的可靠性是 bottleneck — verifier 錯了就什麼都漏掉
- Reward decomposition 在複雜 reward 上的可行性還待驗證
- Reference implementation 是概念驗證，real production 規模未測

### 與 SkillX 的對照（governance vs capability）

[[skillx]]（2026-04-06 Zhejiang+Ant）跟 ASG-SI 是 skill-based self-improvement 的兩個 pole：

| | ASG-SI | SkillX |
|---|---|---|
| 主要目標 | **Governance**（deployed safety） | **Capability expansion / transfer** |
| Promotion gate | Verifier-backed replay + contract check + reward decomposition | Cosine similarity merge + heuristic filter |
| Audit trail | 每個 promotion 獨立可 reproduce | Heuristic/embedding-based，無 contract-level audit |
| 擴充機制 | 只從既有 successful trajectory 抽 | Experience-guided exploration 主動擴充（under-utilized / high-failure tool） |
| Representation | Single-layer skill with contract | Multi-level（Planning / Functional / Atomic） |

兩者互補：ASG-SI 確保「promote 的東西是對的」，SkillX 確保「有東西好 promote」。未來系統應該融合兩端。

### 來自 [[rl-capability-boundary]] 的挑戰

ASG-SI 把 RL fine-tuning 視為 opaque alternative，但 Zhai et al. 2026-04-16 的 PASS@(k,T) 分析指出：

- Tool-use 任務上的 **capability expansion 來自 self-directed exploration**（RL 的本質）
- SFT / distillation **會 regress** 同樣的 compositional task
- ASG-SI 的 skill promotion 來自 successful trajectory，**successful trajectory 本身需要 exploration 才能產生** —— skill graph 的底層 driver 仍然是 RL-like exploration

所以 skill-based vs RL 不是 either/or：RL 做 exploration 產生 trajectory，ASG-SI 把 successful trajectory 轉成可 audit 的 artifact。Skill graph 是 RL 的 **externalization layer**，不是替代品。

## Key Sources

- **2025-12-28** — Audited Skill-Graph Self-Improvement for Agentic LLMs via Verifiable Rewards, Experience Synthesis, and Continual Memory（arxiv 2512.23760）。Source: [[raw/huang-asg-si-audited-skill-graph]]

## Related

[[self-improving-agent]] [[skillx]] [[skillfoundry]] [[meta-harness]] [[ssgm]] [[rl-capability-boundary]] [[procedural-memory]] [[experiential-memory]] [[memory-evaluation]] [[thin-harness-fat-skills]] [[mstar]] [[experience-compression-spectrum]]
