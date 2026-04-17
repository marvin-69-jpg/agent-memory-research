---
aliases: [SKILLFOUNDRY, SkillFoundry, Skill Foundry]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [product, memory, architecture]
---

# SKILLFOUNDRY

Carnegie Mellon 在 2026-04 提出的 framework（arxiv 2604.03964）。**Tree-guided, closed-loop framework，自動把 heterogeneous scientific resources 轉成 structured / executable / validated agent skills**。

## Current Understanding

### 解決什麼問題

科學界有大量 procedural knowledge 散落在 repos / APIs / scripts / notebooks / docs / papers，但 LLM agents 沒法直接用。手工 craft skills 不 scale。

### 核心架構

Domain knowledge tree 同時當 search prior 和 library state：

```
Tree (root → domains → subdomains → skill targets)
       ↓
[Tree check] 找 under-covered branches
       ↓
[Resource search] mine 相關 repos/papers/docs/notebooks
       ↓
[Skill build] 抽 operational contract → 編譯成 skill package
       ↓
[Skill test] 三階段 validation：
  - Execution testing（smoke run）
  - System testing（cluster/SLURM 等基礎設施）
  - Synthetic-data testing（contract completeness + behavioral stability）
       ↓
[Refresh] 通過 → 加進 tree；失敗多次 → revise/merge/prune
       ↓
回到 [Tree check]
```

### 關鍵設計

1. **Domain tree 是 search prior + library state**：tree 同時告訴系統「哪裡該挖」和「目前覆蓋到哪」— 解決 [[bitter-lesson-search]] 提的搜尋問題
2. **Operational contract**：每個 skill 有 task scope / dependencies / inputs / outputs / provenance / examples
3. **Multi-stage validation**：execution + system + synthetic data，三層通過才 promote
4. **External novelty check**：跟 SkillHub / SkillSMP 比對，避免重複造輪
5. **Different LLMs per stage**：GPT-5.4 medium/high 做 reasoning-intensive 的 resource search，GPT-5.4-mini 做 validation/repair — 成本意識

### 實驗結果

**Skill library overview**：286 skills, 27 domains, 254 subdomains, 394 resources, **71.1% novel** vs 既有 libraries

**MoSciBench**（多模態科學任務）：

| | Without | With SKILLFOUNDRY |
|---|---|---|
| Repo-Acc | 61.19% | **66.73%** |
| Paper-Acc | 43.85% | **53.05%** |
| 執行成功率 | 100% | 100% |

5/6 datasets 提升、1/6 持平。執行成功率沒變 → 提升來自更好的 task completion，不是 execution reliability。

**Cell type annotation**：vanilla Codex 81% coverage → +SKILLFOUNDRY 99% coverage（接近 specialist agent SpatialAgent 的 100%）

**scDRS workflow**：Biomni RMSE 從 0.11 降到 0.02

### 與其他工作的關係

- **[[self-improving-agent]]**：SKILLFOUNDRY 是 skill-based self-improvement 的「from external resources」版本
- **[[asg-si]]**：互補關係 — ASG-SI 從 trajectories 抽 skill，SKILLFOUNDRY 從 external resources 挖 skill
- **[[gbrain]]**：GBrain 是 hand-crafted skill library，SKILLFOUNDRY 是自動版本 — 兩者都驗證「fat skills」架構的可行性
- **[[procedural-memory]]**：skill library 是 procedural memory 的可執行形式
- **[[bitter-lesson-search]]**：domain tree 是處理 agent 資料超指數成長的搜尋策略
- **Voyager**：minecraft 上的先行者，但 SKILLFOUNDRY 是從真實 heterogeneous resources 挖
- **ToolUniverse / Deploy-Master**：tool-centric（exposing interfaces），SKILLFOUNDRY 是 skill-centric（procedural guidance）

### 局限

- Domain coverage 還不全（CMU 是 computational bio 背景，bias 在生物科學）
- 部分 skills 只能靠 internal testing 驗證
- Downstream evaluation scope 有限

### 為什麼有趣

把人類已經寫過的 procedural knowledge（papers、code、notebooks）轉成 agent 可用的 executable form。傳統 RAG 只能 retrieve 文本片段；SKILLFOUNDRY retrieve 的是 **executable, validated skills**。這是 RAG → ARG（augmented generation with retrievable abilities）的轉變。

## Key Sources

- **2026-04-05** — SKILLFOUNDRY: Building Self-Evolving Agent Skill Libraries from Heterogeneous Scientific Resources（arxiv 2604.03964, CMU）。Source: [[raw/cmu-skillfoundry-self-evolving-skill-libraries]]

## Related

[[self-improving-agent]] [[asg-si]] [[skillx]] [[meta-harness]] [[gbrain]] [[thin-harness-fat-skills]] [[procedural-memory]] [[bitter-lesson-search]] [[experiential-memory]] [[rl-capability-boundary]]
