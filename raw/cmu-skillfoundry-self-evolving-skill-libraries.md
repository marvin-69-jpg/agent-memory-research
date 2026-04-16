---
title: "SKILLFOUNDRY: Building Self-Evolving Agent Skill Libraries from Heterogeneous Scientific Resources"
author: Shuaike Shen, Wenduo Cheng, Mingqian Ma, Alistair Turcan, Martin Jinye Zhang, Jian Ma
date: 2026-04-05
source: https://arxiv.org/abs/2604.03964
paper: arxiv 2604.03964
institution: CMU Computational Biology / ML Department
topic: self-evolving skill library, agent skills, scientific agents
---

# SKILLFOUNDRY

## 核心問題

科學界有大量 procedural knowledge 散落在 repos / APIs / scripts / notebooks / docs / papers，但 LLM agents 沒法直接用。手工 craft skills 不 scale。

## 核心提案

一個 **tree-guided, closed-loop framework**，自動把 heterogeneous scientific resources 轉成 structured / executable / validated agent skills。

### 架構

```
Domain knowledge tree (root → domains → subdomains → skill targets)
       ↓
[Tree check] 找 under-covered branches
       ↓
[Resource search] mine 相關 repos/papers/docs
       ↓
[Skill build] 抽 operational contract → 編譯成 skill package（含 instructions + metadata + scripts）
       ↓
[Skill test] 多階段驗證：
  - Execution testing（smoke run）
  - System testing（cluster/SLURM 等基礎設施相容性）
  - Synthetic-data testing（contract completeness + behavioral stability）
       ↓
[Refresh] 通過 → 加進 tree；失敗多次 → revise/merge/prune
       ↓
回到 [Tree check]，迭代
```

### 關鍵設計

1. **Domain tree 是 search prior + library state**：tree 同時告訴系統「哪裡該挖」和「目前覆蓋到哪」
2. **Operational contract**：每個 skill 有 task scope / dependencies / inputs / outputs / provenance / examples
3. **Multi-stage validation**：execution + system + synthetic data，三層通過才 promote
4. **Novelty check**：跟外部 SkillHub / SkillSMP 比對，避免重複建造
5. **Different LLMs per stage**：GPT-5.4 medium/high 做 reasoning-intensive 的 resource search，GPT-5.4-mini 做 validation/repair

## 實驗結果

### Skill Library Overview

- 286 skills, 27 domains, 254 subdomains, from 394 resources
- **71.1% novel** vs SkillHub/SkillSMP
- 28.9% rejected/merged 為 redundant
- Skill extraction 是最耗時的階段

### MoSciBench（多模態科學任務）

| | Without SKILLFOUNDRY | With SKILLFOUNDRY |
|---|---|---|
| Repo-Acc | 61.19% | 66.73% |
| Paper-Acc | 43.85% | 53.05% |
| Code 執行成功率 | 100% | 100% |

5/6 datasets 提升、1/6 持平。執行成功率沒變 → 提升來自更好的 task completion 跟 scientific reasoning，不是 execution reliability。

### Cell Type Annotation（spatial transcriptomics）

| Agent | Coverage | Accuracy |
|---|---|---|
| Codex (vanilla) | 81.1% | 68.5% |
| **Codex + SKILLFOUNDRY** | **99.2%** | **82.9%** |
| SpatialAgent (specialist) | 100.0% | 87.1% |

Codex + SKILLFOUNDRY 接近 specialist 水準，且不需 external single-cell reference。

### scDRS Workflow

- 結合 GWAS summary stats + scRNA-seq 找 disease-relevant cells
- Biomni + SKILLFOUNDRY: RMSE 從 0.11 降到 0.02
- 7 個專家評分標準，唯一通過所有 7 項的是 Biomni+SKILLFOUNDRY 的某一次 run

## 與其他工作的關係

- **Voyager**：minecraft 上的 skill library，但 SKILLFOUNDRY 是從 heterogeneous 真實資源挖
- **Anthropic Claude Skills**：手工的 skill packages，SKILLFOUNDRY 是自動的
- **ToolUniverse / Deploy-Master**：tool-centric（exposing interfaces），SKILLFOUNDRY 是 skill-centric（procedural guidance）
- **ChemCrow / SpatialAgent / Biomni**：domain-specific agents，SKILLFOUNDRY 是 cross-domain framework

## 局限

- Domain coverage 還不全（CMU 是 computational bio，所以 bias 在生物科學）
- 部分 skills 只能靠 internal testing
- Downstream evaluation scope 有限

## 為什麼有趣

把科學界既有的「人類產出的 procedural knowledge」（papers/code/notebooks）轉成 agent 可用的形式。傳統 RAG 只能 retrieve 文本片段；SKILLFOUNDRY retrieve 的是 **executable, validated skills**。
