---
date: 2026-04-19
topic: Self-Refinement 的三種體制 — 從 Autoreason 向外延伸
gap_type: single-source
sources_found: 2
wiki_pages_updated: 3
wiki_pages_created: 2
---

# Daily Research: Self-Refinement 的三種體制

## 研究動機

`wiki gaps` 顯示 [[autoreason]] 是 single-source（SHL0MS 推文 + Nous Research repo）。Autoreason 的核心 claim「模型越強，self-refinement 增益越低」本身很強，但缺少對照證據：這個現象只發生在 inference-time 做法上？還是 self-refinement 整個領域都是這樣？

昨天（2026-04-18）我讀到 [[rl-capability-boundary]] 後對 skill library 起疑 — 它看起來像 distillation，而 distillation 在 compositional task 上反而退化。今天想延伸的問題是：**self-refinement 跟 RL 一樣也有 capability expansion vs reliability improvement 的區分嗎？**

從 Autoreason 出發，找到兩篇互補的新來源。

## 發現

### EVOLVE（arxiv 2502.05605）：LLM 原生沒有 self-refinement 能力

- **關鍵經驗 claim**：comprehensive experiments 證明 LLM 原生做 self-refinement 會 **degrade** 品質，不是持平。這是跟 Autoreason 一致的觀察，但表達更強硬
- EVOLVE framework：training 階段用 preference pair 把 refinement 內化；inference 階段產生 refined output 回餵 dataset；兩階段 synergistic iteration
- 結果：Llama-3.1-8B base 超越 GPT-4o（AlpacaEval 2 62.3% LC、Arena-Hard 50.3%）
- **對比 Autoreason**：Autoreason 用外部 judge panel 繞過 LLM 不會 self-critique 的問題；EVOLVE 選擇用 gradient 把能力壓進 weight

Source: [[raw/zeng-evolve-self-refinement]]

### De Jure（arxiv 2604.02276）：Multi-criteria Judge + Bounded Repair

- Pipeline 四階段：normalize → decompose → **19-dim judge** → bounded iterative repair
- 關鍵設計：**upstream-first repair** — 上游 component 先修再動下游 rule units。下游 refine 無法補救上游錯誤
- **收斂**：3 iterations 內 monotonic improvement 到 peak。跟 Autoreason 的 k-consecutive-wins 不同，用 budget exhaustion 作為 stopping criterion
- 下游 RAG 評估：73.8% 情況被偏好，深 retrieval 時升到 84.0%

Source: [[raw/guliani-dejure-iterative-refinement]]

### 三種體制的共同點

三條路線都承認同一個 empirical fact：**LLM 不會自己改好自己。** 要讓 refinement 有效，必須外掛某種評分信號：

| 維度 | Autoreason | De Jure | EVOLVE |
|---|---|---|---|
| 評分信號 | Borda panel (implicit preference) | 19-dim criteria vector (explicit) | trained reward (gradient) |
| 收斂條件 | k consecutive A wins | regeneration budget | training convergence |
| 修改位置 | orchestration 層 | orchestration 層 | model weight |
| 適用域 | 主觀創作 | 結構化抽取 | 通用 capability |
| 可審計性 | 低（panel 黑盒） | 高（19 維度可見） | 無（weight） |

## 與已有知識的連結

用 `wiki match` 找到最相關的頁面：

- [[autoreason]] — 今天的三源之一，補強到 three-source 後升級
- [[memory-evaluation]] — De Jure 的 19-dim judge 是「可審計 evaluation」的具體實作範例
- [[open-questions]] Q2（Evaluation Paradox）— 三篇都面對「誰當 judge」的問題，各自給不同答案
- [[open-questions]] Q16（Capability vs Reliability）— self-refinement 是否也有 capability/reliability 二分？EVOLVE 的 OOD 泛化證據傾向 capability，Autoreason 的 CodeContests 4% 提升更像 reliability
- [[rl-capability-boundary]] — 昨天的發現。self-refinement vs RL 的對照軸

## 新概念：Refinement Regime（要新建 wiki page）

三種 refinement regime：
- **Panel Regime**：外部 judge panel + implicit preference（Autoreason）
- **Criteria Regime**：multi-dim explicit judge + upstream-first repair（De Jure）
- **Training Regime**：refinement 內化為 weight（EVOLVE）

選哪個取決於：是否有可定義的 criteria、是否能付 training cost、是否需要可審計性。

## Open Questions 推進

### Q2 Evaluation Paradox
三個新資料點：
- EVOLVE 的 reward model 本身是另一個需要被評的 judge（recursion 沒停止）
- De Jure 的 19-dim 顯示「把 judge 拆細」可以部分繞過 paradox — 單一維度的 judge 比整體 judge 可靠
- Autoreason 的 "fresh agents" 證明 **judge 的無狀態性** 比 judge 的強度更重要

這不是解決 Q2，但把 paradox 拆成三個可操作的子問題。

### Q3 Compounding vs Forgetting
EVOLVE 把 refinement 壓進 weight — 這是 **compounding via weight**，跟 context-based compounding 不同。Autoreason 的 fresh agents 則是 forgetting as feature。三條路線對「記憶該存哪」給不同答案。

### 新 Tier 3 問題（考慮新增）
**Q17: Refinement Regime Selection** — 什麼場景該用哪一種 regime？目前沒有 framework。

## 對 Agent Memory 的意義

1. **不要假設 agent 會自己判斷記憶品質**：EVOLVE 證明 raw LLM 做 self-critique 會 degrade。那麼「你覺得這條該存嗎」這種 prompt-only 的記憶管理策略可能是 anti-pattern
2. **Memory pipeline 該做 upstream-first repair**：De Jure 的教訓 — normalization 錯了，downstream summarization / abstraction 都是錯的。現有 memory 系統很少有顯式的 upstream validation
3. **三種 regime 對應三種 memory 架構**：
   - Panel → 多 agent 投票決定記憶（類似 [[collaborative-memory-system]]）
   - Criteria → multi-dim judge 做 memory quality scoring（[[memory-worth]] 的前驗版）
   - Training → fine-tune memory policy（[[memory-r1]]、[[agemem]]）
4. **Fresh agent 作為 memory isolation pattern**：Autoreason 刻意切斷記憶來獲得公正性。在 memory QA 的 judge 環節，judge agent 不該共享被評 agent 的 context

## 下一步

- 追 EVOLVE 的 follow-up：有沒有人做 **RL + self-refinement + memory** 三合一？
- De Jure 的 19-dim 值不值得移植到 memory quality scoring？哪幾個維度通用、哪幾個 domain-specific？
- **Q17 要不要正式新增到 open-questions**？取決於有沒有第三、第四個 regime 證據（目前只有 Panel / Criteria / Training 三類）
- 寫 Threads：Autoreason → EVOLVE → De Jure 的敘事線，接昨天「distillation 會退化」的思考
