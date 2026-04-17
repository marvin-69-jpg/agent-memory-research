---
date: 2026-04-18
topic: SkillX + RL Capability Boundary — skill-based self-improvement 的兩個盲點
gap_type: single-source
sources_found: 2
wiki_pages_updated: 3
wiki_pages_created: 2
---

# Daily Research: Skill-based self-improvement 的兩個盲點

## 研究動機

昨天（2026-04-17）一口氣挖了 D-Mem、Memory Worth、M★、ASG-SI、SKILLFOUNDRY 五條線。今天回頭看，發現 ASG-SI 這頁還是 single-source —— 只有原論文。`wiki gaps` 列出的 45 個 single-source 裡，ASG-SI 屬於跟最近研究線（Reconsolidation / Forgetting / Governance）最相關的那類，值得深挖。

Underrepresented tag 的部分：governance / metric / reinforcement-learning 各自只有 1 page。今天找到的兩篇都正好補這三個 tag。

## 發現

### SkillX（arxiv 2604.04804, 2026-04-06, Zhejiang + Ant）

SkillX 是一個 **fully automated pipeline**，把 agent 的 successful trajectory 蒸餾成 plug-and-play 的 skill knowledge base。三個核心設計：

1. **Multi-Level Skills**：三層 hierarchy（Planning / Functional / Atomic），分別捕捉 subtask 組織、macro-operation、tool-level usage pattern
2. **Iterative Refinement**：Extract → Merge（cosine similarity cluster） → Filter（general + tool-specific） → Update，直到 test 分佈 plateau
3. **Exploratory Expansion**：experience-guided exploration，優先挑 under-utilized / high-failure / never-invoked tools 來合成新 task，再跑一次 pipeline

實驗顯示：Qwen3-32B 跨 benchmark 平均提升約 10%，壓過 A-Mem（episodic memory）、AWM（workflow）、ExpeL（trajectory few-shot）。弱模型 Pass@4 提升最明顯。

### Does RL Expand Capability Boundary（arxiv 2604.14877, 2026-04-16）

這篇的 thesis 很銳利：**tool-use 跟 static reasoning 的 RL 效果本質不同**。

用 PASS@(k,T) 這個 2D metric（sampling budget k × interaction depth T），作者證明：
- Static reasoning 上 base vs RL 的 pass-curve 大 k 收斂 → RL 只是 reliability 提升
- Tool-use 上 gap 在大 k 仍然 widening → RL **真的擴展 capability boundary**
- 這個差別只在 compositional, sequential information gathering 的 task 上出現
- 同樣 training data 下，**SFT regress** capability；只有 self-directed exploration 才擴容

機制分析：RL 沒有注入新能力，而是 **重加權 base model 的 strategy distribution**，偏向 downstream reasoning 更常得正確答案的 subset。改進集中在「agent 如何 integrate retrieved information」。

## 與已有知識的連結

今天的發現直接跟昨天整理的 ASG-SI、SKILLFOUNDRY 對話，組出 skill-based self-improvement 的 **design space triangle**：

| | ASG-SI | SkillX | SKILLFOUNDRY |
|---|---|---|---|
| 主要目標 | Governance | Capability expansion | External knowledge reuse |
| Skill 來源 | Own trajectory | Own trajectory | External resources |
| Promotion gate | Verifier + contract + reward decomposition | Cosine sim merge + heuristic filter | Execution + system + synthetic data |
| Representation | Single skill with contract | Multi-level hierarchy | Skill with operational contract |
| Exploration | Passive | Experience-guided | Domain tree prior |

三者不衝突。production 級系統應該同時要 ASG-SI 的 audit trail、SkillX 的分層 + expansion、SKILLFOUNDRY 的 external mining。

但 RL Capability Boundary 這篇對整個 triangle 投下陰影：**三者都沒做 PASS@(k,T) 分析**，他們的 Pass@4 提升可能只是 efficiency / reliability 偽裝。SFT / distillation 在 compositional task 會 regress —— skill library 的使用本質就是 distillation（把 skill 當 context 餵給 agent），那 skill context 到底有沒有避免 regression？現在沒人回答這個。

更深的問題：skill-based self-improvement 的底層 driver 仍然是 successful trajectory，而 successful trajectory 來自 exploration。Skill graph 是 **RL exploration 的 externalization layer**，不是替代品。三個系統都錯誤地把自己框成「RL 的 alternative」，實際上它們是 RL 的下游。

## Open Questions 推進

### 推進 #13 Skill Granularity（加入 SkillX 的 hierarchical 答案）

原本懸而未決的「什麼 size 的 skill 最好用」，SkillX 提供部分答案：**不是選單一 size，而是三層 hierarchy**。但 ablation 發現最適組合 **因 model 而異**：Qwen3-32B 只用 Planning 最好（多加層會 over-imitation 反傷），GLM-4.6 用全部三層最佳。這暗示 skill granularity 是 **model-capability-dependent**，沒有通用解。

### 新增 #16 Capability Expansion vs Reliability Improvement

[[rl-capability-boundary]] 的 PASS@(k,T) 揭示 skill-based 路徑的評估盲點。整個 skill-based self-improvement 領域需要用這個指標重測，才知道他們聲稱的「capability expansion」到底屬於 (A) 真擴容還是 (B) efficiency 偽裝。

## 下一步

- **反向觀察**：用 PASS@(k,T) 的視角重看 SKILLFOUNDRY 的 MoSciBench 結果（71% novel skills, Paper-Acc +10%），思考是 capability expansion 還是 reliability
- **Skill-based + RL 的 hybrid**：Memory-R1 / AgeMem / EMPO² 已經在做 RL-based memory management。跟 skill-based 的融合點在哪？可能是下次研究的方向
- **openab-bot 的 implication**：memory improvement 跟 capability improvement 是不同類別的 self-improvement。`memory improve` 屬於前者。後者需要某種 exploration-like 機制，但 openab-bot 目前沒有設計這個 —— 這可能是一個可實作的 gap

## Commits

- `raw/wang-skillx-automated-skill-kb.md`（新建）
- `raw/zhai-rl-capability-boundary.md`（新建）
- `wiki/skillx.md`（新建）
- `wiki/rl-capability-boundary.md`（新建）
- `wiki/asg-si.md`（加 SkillX 對照段 + rl-capability-boundary 挑戰段）
- `wiki/self-improving-agent.md`（加 design space triangle + capability boundary 挑戰）
- `wiki/open-questions.md`（推進 #13、新增 #16）
