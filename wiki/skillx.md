---
aliases: [SkillX]
first_seen: 2026-04-18
last_updated: 2026-04-18
tags: [product, memory, architecture]
---

# SkillX

Zhejiang University + Ant Digital Technologies 2026-04-06 提出的 framework（arxiv 2604.04804）。**Fully automated pipeline，把成功 trajectory 蒸餾成 plug-and-play 的 multi-level skill knowledge base**。

## Current Understanding

### 解決什麼問題

2025-2026 prevailing self-evolving agent 的四個 bottleneck：

1. **Isolated learning**：各 agent 重複發現類似 behavior
2. **Weak generalization**：experience 轉移差
3. **Model capability bottleneck**：experience 被 exploration agent 自身能力卡住
4. **Representation problem**：raw trajectories / insights / workflows 都無法同時 transferable + efficiently retrievable + directly executable

Claude Skills / 既有 skill 系統又需要 long-context processing 和 progressive disclosure，demand 太重。

### Multi-Level Skills（三層設計）

| 層級 | 內容 |
|---|---|
| **Planning Skills** | 高層 subtask 組織、順序、依賴、分支（ordered steps，濾掉 exploration/backtracking） |
| **Functional Skills** | Subtask 層級 macro-operation，每個對應一個 sub-query（name / document / content） |
| **Atomic Skills** | Tool spec 延伸：reusable usage pattern、constraints、common failure modes |

### 三個核心 innovation

1. **Multi-level skills design**：三層 hierarchy 做到 concise + composable + robust to distributional shift
2. **Iterative refinement**：Extract → Merge（cosine sim cluster）→ Filter（general + tool-specific）→ Update；直到 test 分佈 plateau
3. **Exploratory expansion**：experience-guided exploration，優先挑 under-utilized / high-failure / never-invoked tools，合成新 task 重跑 pipeline

### 實驗結果

**Benchmarks**: BFCL-v3、AppWorld、τ²-Bench

**亮點**：
- Qwen3-32B（弱模型）跨 benchmark ~10% 提升
- 壓過 A-Mem（episodic）、AWM（workflow）、ExpeL（trajectory few-shot）—— 表示 multi-level hierarchy 比 monolithic representation 更有效
- 弱模型的 Pass@4 大幅提升，暗示從強模型蒸餾 skill 可以擴展 capability boundary
- 同時降低 execution steps 和 input tokens（不只 performance，還 efficiency）

### 各層貢獻

- **Planning Skills**：跨模型都減少 execution steps，弱模型受益最大
- **Functional Skills**：最主要的效能來源
- **Atomic Skills**：關鍵 API 釐清，缺了大幅掉分
- **Over-imitation trap**：弱模型加太多層會反傷（Qwen3-32B 只用 Planning 就夠）

### 與 ASG-SI 的對照（兩種 skill-based 路徑）

| | ASG-SI | SkillX |
|---|---|---|
| 主要目標 | Governance（deployed safety） | Capability expansion / transfer |
| Promotion gate | Verifier-backed replay + contract check + reward decomposition | Cosine similarity merge + heuristic filter |
| Audit trail | 每個 promotion 獨立可 reproduce | Heuristic/embedding-based，無 contract-level audit |
| 擴充機制 | 只從既有 trajectory 抽 | Experience-guided exploration 主動擴充 |
| 設計哲學 | Deployment safety first | Library growth velocity first |

兩者不衝突但 engineering trade-off 不同。ASG-SI 把 skill library 當 regulated artifact，SkillX 當 growing asset。

### 與 SKILLFOUNDRY 的對照

| | SKILLFOUNDRY | SkillX |
|---|---|---|
| Skill 來源 | Papers / repos / notebooks（external human-written resources） | Agent 自己的成功 trajectory |
| Validation | Execution + system + synthetic data（三階段） | General filter + tool-specific filter |
| Exploration prior | Domain knowledge tree | Experience-guided（under-utilized tools） |
| Novelty check | 跟外部 SkillHub / SkillSMP 比對 | 內部 cosine sim dedup |
| 領域 | Scientific computing（biased 到 computational bio） | General tool-use agents |

三者（ASG-SI / SKILLFOUNDRY / SkillX）呈現 skill-based self-improvement 的 **Design space triangle**：governance-first / external-resource-first / trajectory-first。

### 與 Does RL Expand 的張力

[[rl-capability-boundary]]（Zhai et al. 2026-04-16）指出：**只有 self-directed exploration（RL）** 能擴展 tool-use agent 的 capability boundary；SFT / distillation 在 compositional task 上會 regress。

SkillX 的「從強模型蒸餾給弱模型 → Pass@4 提升」看起來擴展了 capability，但：
- SkillX 只報 Pass@1 / Pass@4，沒做 PASS@(k,T) 分析
- 無法排除「表面看似 capability expansion，實際只是 efficiency improvement」
- 這是 skill-based self-improvement 的一個**未驗證 claim**

### 局限

- 假設 **stable tool schema**（schema drift 時 skill 會壞，連到 [[memory-staleness]]）
- 專注 tool-use scenario，不擅長純對話
- Text-only iterative optimization 在 limited data 會 overfit
- Over-imitation trap：小模型塞太多層 skill 反而傷害表現

### 為什麼有趣

- **Provides the "capability expansion" side of the skill-based coin**：配合 ASG-SI 的 governance 面，組出完整 picture
- **三層粒度設計**是 [[self-improving-agent]] 的 "skill granularity" 問題（[[open-questions]] #13）的具體回答 —— 不是單一 size，而是分層
- **Experience-guided exploration** 解決 [[bitter-lesson-search]] 提的 search prior 問題：under-utilized / high-failure tool 就是 skill library 的缺口 signal

## Key Sources

- **2026-04-06** — SkillX: Automatically Constructing Skill Knowledge Bases for Agents（arxiv 2604.04804, Zhejiang University + Ant Digital Technologies）。Source: [[raw/wang-skillx-automated-skill-kb]]

## Related

[[self-improving-agent]] [[asg-si]] [[skillfoundry]] [[procedural-memory]] [[experiential-memory]] [[bitter-lesson-search]] [[memory-staleness]] [[rl-capability-boundary]] [[thin-harness-fat-skills]] [[gbrain]]
