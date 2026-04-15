---
aliases: [memory failure modes, 記憶失敗模式, failure modes]
first_seen: 2026-04-14
last_updated: 2026-04-14
tags: [memory, architecture]
---

# Memory Failure Modes

Agent memory 系統的常見失敗模式。每個記憶系統都會失敗 — 問題是怎麼失敗、失敗是否可恢復。

## Current Understanding

[[chrysb]] 從實戰中總結出 10 種 failure modes：

1. **Session amnesia** — 新 session 對之前完全無感知。最基本的失敗
2. **Entity confusion** — derivation 時混淆或合併不同 entity（同名不同人）→ 跟 [[entity-detection]] 直接相關
3. **Over-inference** — 模型把推測編碼成事實，沒有 careful prompting 就填充 plausible-sounding fabrications
4. **Derivation drift** — 連鎖 summarization 累積小誤差，最終記憶偏離實際對話。「photocopy of a photocopy」→ [[memory-staleness]] 的機制之一
5. **Retrieval misfire** — embedding 相似但語境錯誤的記憶被取回 → [[hybrid-search]] 的 limitation
6. **Stale context dominance** — 舊的、被高頻引用的記憶擠掉新的。系統不斷 surface 過時 context → [[memory-staleness]]
7. **Selective retrieval bias** — retrieval 只找到符合當前 query framing 的記憶，用不同 topic 或 register 存的記憶不可見
8. **Compaction information loss** — summary 取代 raw turns 時，specific details 消失。壓縮在最有用的資訊上是有損的
9. **Confidence without provenance** — 系統高信心地陳述「記憶」，但無法追溯到實際對話 → [[actor-aware-memory]] 的 provenance tracking 是解法之一
10. **Memory-induced bias** — 系統回應永遠被既有記憶染色。有時你想要未被染色的觀點 → [[autoreason]] 的 memory isolation 是反向策略

### 與 survey 的交叉驗證

[[raw/pengfei-du-memory-survey-2026|Pengfei Du survey]] 從學術角度識別了類似的問題：
- **Summarization drift** = derivation drift
- **Attentional dilution** = 長 context 下注意力退化
- **Self-reinforcing error** = over-inference 在 reflective memory 中的版本
- **Memory blindness** = session amnesia 在 hierarchical memory 中的版本

### Raw vs Derived 根本張力

所有 failure modes 的根源是 **raw vs derived 光譜**上的位置選擇：
- Raw 端：lossless 但 inert — session amnesia、retrieval misfire
- Derived 端：compact 但 lossy — derivation drift、compaction info loss、over-inference
- 沒有任何位置能同時避免所有 failure modes

## Key Sources

- **2026-04-12** — Chrys Bader 10 種 failure modes + 9 軸設計框架。Source: [[raw/chrysb-long-term-memory-unsolved]]
- **2026-03-08** — Pengfei Du survey 從學術角度的 failure 分析。Source: [[raw/pengfei-du-memory-survey-2026]]

## Related

[[agent-memory]] [[memory-staleness]] [[chrysb]] [[hybrid-search]] [[actor-aware-memory]] [[entity-detection]] [[autoreason]] [[compounding-memory]] [[chatgpt-memory]] [[coding-agent-memory]] [[memory-evaluation]] [[open-questions]] [[multimodal-memory]] [[neuroscience-memory]] [[synapse]]
