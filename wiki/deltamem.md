---
aliases: [DeltaMem, RL memory management]
first_seen: 2026-04-17
last_updated: 2026-04-17
tags: [product, memory, reinforcement-learning]
---

# DeltaMem

Zhang et al. 提出的 agentic memory management system（arxiv 2604.01560, ICML 投稿, 2026-04-02）。核心主張：**memory management 應該是 single agent end-to-end 任務 + RL 強化**，不是多個 agent 各負責一部分。

## Current Understanding

### 為什麼不用 Multi-Agent

現有系統（如 Mem0 的 multi-agent pipeline）把記憶操作分給不同 agent：一個負責提取、一個負責更新、一個負責刪除。作者發現這些 pipeline fragile — information loss across agents，且不同場景下表現不穩。

DeltaMem 的做法：**一個 agent 看完整個 memory state + 新對話，直接輸出所有操作**（ADD / UPDATE / DELETE / NOOP）。

### Memory-based Levenshtein Distance

RL 的 reward 不用向量相似度，而用 **factual keyword coverage**：每條 target memory 有一組事實關鍵字，reward = 預測記憶覆蓋了多少。這跟 [[memory-worth]] 的 outcome-based evaluation 有相同直覺 — 不要用 proxy metric（vector distance），要用 ground truth（factual correctness）。

### 結果

| Benchmark | DeltaMem-8B-RL | 比較 |
|---|---|---|
| LoCoMo | SOTA | beats all product-level baselines |
| PersonaMem Overall | **63.61** | beats Memobase, Zep, Mem0 |
| Memory Extraction | **80.65** | training-free: 68.02 |
| New-Ideas | **40.14** | training-free: 24.73 (+62%) |
| Recall-Facts | **76.47** | 不遺忘核心事實 |

### 核心 Insight

**Updating 是最難的記憶操作**。很多系統 extraction 做得好但 updating 差（如 LightMem）。原因是 updating 需要同時判斷「舊記憶哪裡過時」和「新資訊哪些值得保留」。RL 讓 agent 在反覆嘗試中學會平衡 extraction 和 updating。

### 跟其他系統的連結

| 連結 | 說明 |
|---|---|
| [[agemem]] | 也用 RL 訓練 memory management，但 AgeMem 是訓練 agent 決定「何時存」，DeltaMem 是訓練整個 CRUD pipeline |
| [[memory-worth]] | 都主張不用 proxy metric。MW 用 outcome-based 兩計數器，DeltaMem 用 keyword coverage |
| [[mem0]] | DeltaMem 建在 Mem0 backend 之上，是 Mem0 的「如果換成 RL 會怎樣」實驗 |
| [[memory-failure-modes]] | DeltaMem 的 RL 可能是解 failure mode #5（update vs overwrite 混淆）的方向 |

## For Agent Memory Research

- **我們的 memory management 完全是 rule-based** — entity detection 觸發存入、dedup-check 防重複、reconsolidation 觸發更新。沒有任何學習機制
- **DeltaMem 暗示 RL 可以改善 updating 品質** — 我們的 reconsolidation 是 heuristic-based（人寫的規則），如果有 outcome feedback 也許能更好
- **但我們沒有 training infrastructure** — DeltaMem 需要 GPU 跑 GRPO，我們跑在 k8s pod 裡沒有 GPU

## Key Sources

- **2026-04-02** — Zhang et al., arxiv 2604.01560v1, ICML. Source: [[raw/zhang-deltamem-rl-memory]]

## Related

[[agemem]] [[memory-worth]] [[mem0]] [[agent-memory]] [[memory-failure-modes]] [[locomo]] [[empo2]] [[mem1]] [[memory-r1]]
