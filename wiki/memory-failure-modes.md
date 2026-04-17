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

### SSGM 的 Reconsolidation Failure Taxonomy

[[ssgm]]（arxiv 2603.11768）從 evolving memory 的角度識別了七種失敗：

1. **Semantic drift** — 記憶語意在反覆 rewrite 中漂移
2. **Procedural drift** — 操作記憶偏離正確步驟
3. **Goal drift** — agent 目標記憶被逐步修改
4. **Memory hallucination** — 記憶系統產生不存在的「回憶」（≈ over-inference）
5. **Temporal obsolescence** — 記憶過時但未標記（≈ stale context dominance）
6. **Memory poisoning** — 惡意注入假記憶
7. **Privacy leakage** — 記憶洩漏私人資訊

前三種是 [[reconsolidation]] 特有的 — 只有當記憶可改寫時才會出現 drift。這表示 reconsolidation 帶來新能力的同時也帶來新的 failure surface。

### Raw vs Derived 根本張力

所有 failure modes 的根源是 **raw vs derived 光譜**上的位置選擇：
- Raw 端：lossless 但 inert — session amnesia、retrieval misfire
- Derived 端：compact 但 lossy — derivation drift、compaction info loss、over-inference
- 沒有任何位置能同時避免所有 failure modes

### Bad Compact（Thariq）

Thariq（Claude Code team）指出 **compaction information loss** 的一個具體機制：

> **Due to context rot, the model is at its least intelligent point when compacting.**

典型案例：autocompact 在長 debugging session 後觸發，把 investigation 壓縮成 summary。下一個 turn 使用者說「fix that other warning in bar.ts」— 但因為壓縮時的主題是 debugging，那個 warning 已經被 drop。

**關鍵洞察**：壓縮品質 = 壓縮時的 model IQ × 壓縮者是否能預測未來 query 方向。兩個條件都不滿足時就是 bad compact。

**解法光譜**：
- `/rewind`：lossless 裁剪，只要還沒 compact 就優先用
- `/compact focus on X, drop Y`：proactive + steered，趁 model 還清醒時帶著 intent 壓縮
- `/clear` + manual brief：使用者自己寫關鍵資訊，最高控制力
- Subagent：隔離大量中間 output，只讓 conclusion 回到父 context

詳見 [[session-management]]。

## Key Sources

- **2026-04-16** — Thariq (Claude Code): bad compact 的機制（context rot × unpredictable next query）。Source: [[raw/thariq-claude-code-session-management]]
- **2026-04-12** — Chrys Bader 10 種 failure modes + 9 軸設計框架。Source: [[raw/chrysb-long-term-memory-unsolved]]
- **2026-03-08** — Pengfei Du survey 從學術角度的 failure 分析。Source: [[raw/pengfei-du-memory-survey-2026]]

## Related

[[agent-memory]] [[memory-staleness]] [[memory-consistency]] [[chrysb]] [[hybrid-search]] [[actor-aware-memory]] [[entity-detection]] [[autoreason]] [[compounding-memory]] [[chatgpt-memory]] [[coding-agent-memory]] [[memory-evaluation]] [[open-questions]] [[multimodal-memory]] [[neuroscience-memory]] [[synapse]] [[reconsolidation]] [[a-mem]] [[ssgm]] [[meta-harness]] [[session-management]] [[context-rot]] [[d-mem]] [[memory-worth]]
