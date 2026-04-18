---
aliases: [PASS@(k,T), RL capability boundary, Does RL Expand Capability]
first_seen: 2026-04-18
last_updated: 2026-04-18
tags: [memory, architecture, rl, metric, reinforcement-learning]
---

# RL Capability Boundary (PASS@(k,T))

Zhai, Yan, Shao, Wang 2026-04-16 提出的分析（arxiv 2604.14877）。**用 PASS@(k,T) 這個 2D metric 分辨 RL 到底 expand 了 LLM agent 的 capability 還是只提升 reliability**。結論：**tool-use RL 真的擴大 capability boundary，但只有在 compositional sequential 任務上**。

## Current Understanding

### 核心問題

RL 對 LLM agent 有兩種可能效果：
- (A) **Capability expansion**：能做新的事
- (B) **Reliability improvement**：現有能力變穩

Static reasoning 既有結論是 (B)：base 跟 RL 的 pass@k curve 大 k 時收斂。本文問 tool-use 是否也如此。

### PASS@(k,T) 指標

同時變動兩個軸：
- **k**：sampling budget
- **T**：interaction depth（每次最多幾輪 tool call）

如果 RL vs base 在大 k 收斂 → 只是 efficiency（reliability）
如果在大 k 仍 widening → capability expansion

### 主要發現

**Tool-use 跟 static reasoning 結論相反**：
1. RL 的 pass-curve 拉到 base model 之上
2. Gap 在大 k 仍然 widening（不收斂）
3. Expansion 專屬於 **compositional, sequential information gathering** 任務
4. 簡單 task 上 RL 依然只是 efficiency 提升（跟 static reasoning 結論一致）

### 機制分析

- RL **重加權 base strategy distribution**，偏向 downstream reasoning 更常得正確答案的 subset
- 改進集中在「**agent 如何 integrate retrieved information**」
- 所以 RL 沒有注入新能力，而是 **surface 了 base model 已有的潛能**

### 關鍵對照：SFT 會 regress

**相同 training data** 下：
- SFT 在 compositional task 上 **regress** capability
- 只有 **self-directed exploration（RL 的本質）** 才能擴展 boundary
- 這 isolate 了 causal factor：不是 data、不是 compute、是 self-directed exploration

### 意義：reconcile 兩派

- 樂觀派（RL 擴容）：在 compositional tool-use 是對的
- 悲觀派（RL 只提升 reliability）：在 static reasoning 是對的
- 都對，task type 不同

### 跟 skill-based self-improvement 的張力

Skill-based self-improvement（[[asg-si]] [[skillx]] [[skillfoundry]]）把 RL fine-tuning 視為 opaque alternative，提議 skill graph/library 是更好的 self-improvement 路徑。

但本文指出：
- **Tool-use 的 capability expansion 來自 self-directed exploration**
- **SFT / distillation 會 regress 同樣的 compositional task**

這對 skill-based 提出三個未驗證 claim：
1. **Distillation 型 skill transfer（SkillX 的主線）能真的擴展 capability 嗎？** 還是只是 efficiency 偽裝？
2. **ASG-SI 的 skill promotion 來自 successful trajectory**，successful trajectory 本身需要 exploration 才能產生 —— skill graph 的底層 driver 仍然是 exploration
3. **Skill-based vs RL 不是 either/or**：可能需要 RL 做 exploration + skill-based 做 artifact externalization

### 對我們的啟發

openab-bot 自己的 sleep-time compute（`memory improve`）屬於 **heuristic-based self-improvement**，不是 RL。從本文看：
- 如果 task 是 static reasoning（answer existing question），heuristic 足夠
- 如果要擴展 agent 能做的事（compositional tool use），可能需要 exploration-like 的機制
- 換句話說：**memory improvement 跟 capability improvement 是不同類別的 self-improvement**

## Key Sources

- **2026-04-16** — Does RL Expand the Capability Boundary of LLM Agents? A PASS@(k,T) Analysis（arxiv 2604.14877, Zhai, Yan, Shao, Wang）。Source: [[raw/zhai-rl-capability-boundary]]

## Related

[[self-improving-agent]] [[asg-si]] [[skillx]] [[skillfoundry]] [[memory-evaluation]] [[sleep-time-compute]] [[memory-r1]] [[agemem]] [[evolve-self-refinement]] [[refinement-regime]]
