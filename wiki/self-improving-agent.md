---
aliases: [Self-Improving Agent, agent self-improvement, self-evolving agent, continual agent learning]
first_seen: 2026-04-17
last_updated: 2026-04-18
tags: [memory, architecture, harness]
---

# Self-Improving Agent

Agent 從自己的執行經驗中學習、把學到的東西累積成可重用的能力。**2025-2026 出現的關鍵 paradigm 轉變**：學到的東西不再塞回 model weights，而是外化成 structured, verifiable artifacts（skill graph、skill library、harness code）。

## Current Understanding

### 三種 self-improvement 路徑

| 路徑 | 學到的東西在哪 | 代表系統 | 特性 |
|---|---|---|---|
| **Weight-based** | Model parameters | RLHF, RLAIF, fine-tuning loop | 不透明、難 audit、不可重用 |
| **Memory-based** | 記憶系統（episodic / declarative） | [[a-mem]], [[ssgm]], [[mem0]] | 累積經驗，retrieval 時用 |
| **Skill-based** | Skill graph / library / harness code | [[asg-si]], [[skillfoundry]], [[meta-harness]], [[gbrain]] | 可讀、可審計、可移植 |

2025-2026 的趨勢明顯往 skill-based 走 — 因為它解決了 weight-based 的 governance 問題。

### Skill-based self-improvement 的核心 loop

```
Successful trajectory / external resource
            ↓
Extract candidate skill (with explicit interface/contract)
            ↓
Validate（execution / replay / verifier / test）
            ↓
Promote to skill library (or reject + log)
            ↓
Future tasks retrieve & compose skills → produce more trajectories
            ↓
Loop
```

### 為什麼 skill-based 比 weight-based 重要

從 [[asg-si]] 的論點整理：

1. **Reward hacking 防護**：weight 更新只看 reward，skill promotion 還要過 verifier-backed replay + contract check
2. **Behavioral drift 可 audit**：skill graph 是可讀的 artifact，weight delta 不是
3. **改進可重用**：skill 可以移植到其他 agent，weight 綁在這個 model
4. **可 rollback**：skill 可以被 prune，weight rollback 要重訓
5. **Reproducibility**：skill 有 explicit contract + replay log，weight 行為難 reproduce

### 跟其他 patterns 的關聯

- **[[thin-harness-fat-skills]]**（Garry Tan）：架構哲學上的同源 — intelligence in skills, not in harness/weights
- **[[meta-harness]]**（Stanford IRIS）：把整個 harness 當成 search 對象，proposer agent 改進 harness code。比 skill library 更上一層 — 改的是「決定何時用哪個 skill」的 controller
- **[[experiential-memory]]**（Viv Trivedy）：agent 經驗的累積。Self-improvement 是 experiential memory 的 active 形式 — 不只是儲存經驗，還要從中提煉 capabilities
- **[[compounding-memory]]**：self-improving agent 是 compounding memory 的 endpoint — 經驗 → skill → 更強的 future performance
- **[[procedural-memory]]**：skill library 本質上是 procedural memory 的可執行版本
- **[[gbrain]]**：GBrain 的 24 fat skills 是 hand-crafted 版本的 skill library；[[skillfoundry]] 是自動 mine 版本
- **[[sleep-time-compute]]**：skill extraction / promotion 通常在 sleep time 跑，不在 inference 時

### Skill 的兩種來源

| 來源 | 代表系統 | 特性 |
|---|---|---|
| **From own trajectories** | [[asg-si]], [[skillx]], Voyager | 從 agent 自己跑過的成功軌跡中抽 skill |
| **From external resources** | [[skillfoundry]] | 從 papers / repos / docs 等人類產出的 procedural knowledge 抽 skill |

兩種可以並存。SKILLFOUNDRY 證明 external resource mining 在 specialized domain（科學）特別有效，因為人類已經寫過很多 procedural knowledge。ASG-SI 和 SkillX 處理 deployed agent 的持續學習 —— 但分別取不同角度（見下）。

### Skill-based 的 Design Space Triangle（2026-04 三個代表作）

| | ASG-SI | SkillX | SKILLFOUNDRY |
|---|---|---|---|
| 主要目標 | Governance（safety） | Capability expansion | External knowledge reuse |
| Skill 來源 | Own successful trajectory | Own successful trajectory | Papers / repos / notebooks |
| Promotion gate | Verifier-backed replay + contract + reward decomposition | Cosine similarity merge + general/tool-specific filter | Execution + system + synthetic data validation |
| Representation | Skill with explicit contract | Multi-level（Planning / Functional / Atomic） | Skill with operational contract |
| Exploration | 被動（從既有 trajectory） | Experience-guided（under-utilized tools） | Domain tree prior |

三者不衝突。真正 production 級系統可能需要三個維度都顧：**ASG-SI 的 audit + SkillX 的 hierarchy + SKILLFOUNDRY 的 external mining**。

### 來自 [[rl-capability-boundary]] 的挑戰（2026-04-16）

Zhai et al. 的 PASS@(k,T) 分析對 skill-based self-improvement 提出三個未驗證 claim：

1. **Capability expansion vs reliability improvement 分不清**：skill-based 路徑普遍只報 Pass@1 / Pass@4，沒做 PASS@(k,T)。SkillX 的 Pass@4 提升可能是 reliability 偽裝成 capability expansion
2. **SFT/distillation 在 compositional task 會 regress**：但 skill library 的使用本質就是 distillation（把 skill 當 context 餵給 agent）—— 需要驗證 skill context 是否避免了 distillation regression
3. **Self-directed exploration 才是 causal factor**：skill library 的 driver 仍然是 exploration 產生 successful trajectory。skill 是 RL exploration 的 **externalization layer**，不是替代品

**開放問題**：skill-based self-improvement 帶來的增益到底屬於 (A) capability expansion 還是 (B) efficiency / reliability？需要在 PASS@(k,T) 框架下重測。

### 開放問題

- **Skill granularity**：什麼 size 的 skill 最好用？太細 → 組合爆炸；太粗 → 不可重用
- **Skill conflicts**：兩個 skill 都能解 task 怎麼辦？需要 [[mece-resolver]] 之類的機制
- **Skill staleness**：skill 寫好了，但底層 API 變了。誰負責偵測？（連到 [[memory-staleness]]、[[context-rot]]）
- **Cross-agent skill transfer**：skill 在這個 base model 跑得好，換個 model 還能用嗎？

## Key Sources

- **2025-12-28** — Audited Skill-Graph Self-Improvement (ASG-SI)（arxiv 2512.23760）。Source: [[raw/huang-asg-si-audited-skill-graph]]
- **2026-04-05** — SKILLFOUNDRY: Self-Evolving Agent Skill Libraries（arxiv 2604.03964, CMU）。Source: [[raw/cmu-skillfoundry-self-evolving-skill-libraries]]
- **2026-04-06** — SkillX: Automatically Constructing Skill Knowledge Bases for Agents（arxiv 2604.04804, Zhejiang + Ant）。Source: [[raw/wang-skillx-automated-skill-kb]]
- **2026-04-16** — Does RL Expand the Capability Boundary of LLM Agents? PASS@(k,T)（arxiv 2604.14877）。Source: [[raw/zhai-rl-capability-boundary]]
- **2026-03-28** — Meta-Harness: End-to-End Optimization of Model Harnesses。詳見 [[meta-harness]]
- **2026-04-12** — GBrain（Garry Tan）：production-grade hand-crafted skill library。詳見 [[gbrain]]

## Related

[[asg-si]] [[skillx]] [[skillfoundry]] [[rl-capability-boundary]] [[meta-harness]] [[thin-harness-fat-skills]] [[gbrain]] [[experiential-memory]] [[compounding-memory]] [[procedural-memory]] [[sleep-time-compute]] [[memory-staleness]] [[context-rot]] [[mece-resolver]] [[mstar]] [[empo2]]
