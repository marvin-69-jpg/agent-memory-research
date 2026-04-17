---
url: https://arxiv.org/abs/2604.04804
alphaxiv: https://www.alphaxiv.org/overview/2604.04804
arxiv_id: 2604.04804
title: "SkillX: Automatically Constructing Skill Knowledge Bases for Agents"
authors: Chenxi Wang, Zhuoyun Yu, Runnan Fang, Shuofei Qiao, Kexin Cao, Guozhou Zheng, Shumin Deng (Zhejiang University); Xin Xie, Wuguannan Yao, Xiang Qi, Peng Zhang (Ant Digital Technologies, Ant Group)
date: 2026-04-06
fetched: 2026-04-18
---

# SkillX: Automatically Constructing Skill Knowledge Bases for Agents

## 摘要重點

SkillX 是一個 **fully automated framework**，把成功 trajectory 蒸餾成 plug-and-play 的 skill knowledge base。三個核心 innovations：Multi-Level Skills Design、Iterative Skills Refinement、Exploratory Skills Expansion。

## 動機

Prevailing self-evolving agent paradigms 有四個 bottleneck：

1. **Isolated learning**：agents 各自重複發現類似 behavior
2. **Weak generalization**：experience 轉移到新 task 差
3. **Model capability bottleneck**：experience 被 exploration agent 的能力上限卡住
4. **Representation problem**：raw trajectories / insights / workflows 都無法同時做到 transferable + efficient retrieval + directly executable
5. 現有 skill 系統（如 Claude Skills）需要 long-context processing 和 progressive disclosure，demand 太重

## Multi-Level Skills Design（三層）

| 層級 | 內容 | 抽取方式 |
|---|---|---|
| **Planning Skills (S_plan)** | 高層 subtask 組織、順序、依賴、分支 | 壓縮 trajectory 成 ordered steps，濾掉 exploration/backtracking，summarize 冗長 feedback |
| **Functional Skills (S_func)** | Subtask 層級的 macro-operations，每個對應一個 sub-query | LLM 依 planning 中的 subtask 目標抽出，每個 skill 有 name / document / content |
| **Atomic Skills (S_atomic)** | 單個 tool spec 延伸，加上 reusable usage pattern、constraints、common failure modes | LLM 從 trajectory 蒸餾 invocation pattern + parameter config + notes |

目標：concise, composable, robust to distributional shift.

## Iterative Skills Refinement Pipeline

```
Rollout on training tasks（GLM-4.6 backbone）
       ↓
Extract multi-level skills
       ↓
Skills Merge（cosine similarity cluster → 合併 semantically similar skills）
       ↓
Skills Filter 兩階段：
  - General filter（濾掉 extraneous package dependency、idiosyncratic function def、過度封裝）
  - Tool-specific filter（跟 env tool schema 對照，reject 不存在 tool / 無效 param）
       ↓
Skills Library Update（add / modify / keep）
       ↓
直到 test 分佈 performance plateau
```

## Exploratory Skills Expansion

不是 random exploration。用 **Experience-Guided Exploration**：
- 優先挑 **under-utilized tools、high-failure-rate tools、never-invoked tools**
- 從這些 exploratory trajectory 合成新 task（Q_syn），再跑一次整個 pipeline

## 使用時的 retrieval

1. **Planning Skills Retrieval + Pseudo-Plan Rewriting**：新 task 來，retrieve 相似歷史任務的 planning skill，LLM 自行改寫成 task-specific pseudo-plan（這個 plan 只當 retrieval query，不直接注入 system prompt 避免 hallucination）
2. **Functional + Atomic Retrieve**：pseudo-plan 的每個 step 當 query 檢索 skill，去重後 LLM 做 self-filter 選最適用的

Embedding: Qwen3-Embedding-8B；backbone: GLM-4.6。

## 實驗

**Benchmarks**: BFCL-v3, AppWorld, τ²-Bench（複雜 multi-turn、tool-use、conversational）

**Models**: Qwen3-32B, Kimi-K2-Instruct-0905, GLM-4.6 (backbone for extraction)

**Baselines**: No-memory, A-Mem, AWM (modular workflows), ExpeL (few-shot trajectories)

### 主要發現

- **Qwen3-32B 獲得 ~10% 跨 benchmark 效能提升**（弱模型受益最多）
- **Multi-level skills 壓過所有 baseline**（包括 A-Mem 的 episodic memory、AWM 的 workflow、ExpeL 的 trajectory）
- **Capability boundary expansion**：weaker models 的 Pass@4 大幅提升，表示從強模型蒸餾 skill 真的能擴展能力邊界（不只是提升 reliability）
- **Execution efficiency**：減少 execution steps + input tokens

### 各層貢獻

- **Planning Skills**：一致減少 execution steps，對弱模型效果最明顯
- **Functional Skills**：最主要的效能提升來源
- **Atomic Skills**：關鍵 API 的釐清，缺了大幅掉分
- **組合最優**因 model 而異：GLM-4.6 用全部三層最佳；Qwen3-32B 只用 Planning 就夠（加其他層會 over-imitation 反傷）

### 其他觀察

- Iterative refinement 持續改善，但 limited data 下會 overfit（text-only optimization 的固有問題）
- Experience-guided expansion 遠優於 random exploration
- 對 DeepSeek-V3.2、GPT-4.1 等更強模型仍有收益

## 局限

- 假設 **stable tool schema**（schema drift 時 skill 會壞）
- 專注 tool-using scenario，不擅長無 function-call 的純對話
- Text-only iterative optimization 在 limited data 會 overfit

## 與 ASG-SI 的對照（我的觀察）

- **兩者都**：把 skill 當 first-class artifact、從 trajectory 抽、組成 library
- **ASG-SI 強調 governance**：verifier-backed replay + contract check + reward decomposition，每個 promotion 獨立 auditable
- **SkillX 強調 capability expansion**：merge + filter + iterative refine + experience-guided expansion，目的是讓 library 更 transferable 和 plug-and-play
- **SkillX 沒 audit trail**：merge 和 filter 是 heuristic/embedding-based，不是 contract-based，改進過程無法像 ASG-SI 那樣做 post-hoc reproducibility
- **ASG-SI 沒 expansion mechanism**：只從既有 trajectory 抽，沒有 proactive exploration
- **分野的本質**：deployment safety（ASG-SI）vs library growth velocity（SkillX）。這兩個目標不衝突但 engineering trade-off 不同
