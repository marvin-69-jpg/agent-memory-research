---
aliases: [Helix, helix-agent, self-healing runtime, gene map runtime]
first_seen: 2026-04-15
last_updated: 2026-04-15
tags: [product, memory, architecture]
---

# Helix

開源 self-healing runtime，能 wrap 任何 async function 並自動修復錯誤。核心創新是 **Gene Map** — 用強化學習（Q-value）排序的修復策略知識庫，讓 agent 對已見過的錯誤在 1ms 內免 LLM 修復。

## Current Understanding

- **定位**：不是 agent framework，是 **agent infrastructure** — 解決「agent 不斷踩同樣的坑卻學不會」的問題
- **核心概念 — [[gene-map|Gene Map]]**：每次修復都存入本地知識庫，附帶 Q-value 分數。成功策略提升、失敗策略降級。知識庫隨每次失敗變得更聰明
- **6 階段 repair pipeline**：
  1. **Perceive** — 分類錯誤（type、platform、context）
  2. **Construct** — 生成候選修復方案（retry with backoff、refresh token、adjust params、split request）
  3. **Evaluate** — 對每個候選方案評分（成功率、成本、安全性）
  4. **Commit** — 執行最高分的修復
  5. **Verify** — 確認是否成功，結果回饋
  6. **Gene Map** — 儲存修復策略並更新 Q-value
- **效能數據**（50 個 agentic payment 錯誤場景）：
  - 首次遇到新錯誤：2,140ms，1 LLM call
  - 再次遇到同錯誤：**1.1ms，0 LLM call，0 成本** — 2,000× 加速
- **三種模式**：observe（監控）、auto（修復+重試）、full（重構執行）
- **用法**：三行 code — `import { wrap }` → `const safe = wrap(fn, { mode: 'auto' })` → `await safe(args)`
- **Doctor vs Immune System 類比**：即使模型持續進步，routine failures 用 1ms pattern match 解決比每次呼叫 LLM 更有效率 — 就像人有免疫系統不代表不需要醫生，但感冒不需要去看診
- **實測亮點**：x402 payment agent 在 Base 上遇到 Uniswap swap revert（bare "execution reverted"），5 個 frontier LLM（含 GPT-5.4）都無法正確分類，Helix 在 50ms 內 pattern-match 到 `slippage_too_tight` 並修復
- **願景 — shared Gene Map**：所有 agent 的失敗經驗匯成集體免疫系統。你的 agent 遇到的錯誤可能已被萬個其他 agent 解決
- **GitHub**: adrianhihi/helix，npm / PyPI / Docker 都有

### 與 agent memory 研究的關聯

- Helix 的 Gene Map 是一種 **error-specific [[procedural-memory]]** — 不記事實或偏好，專門記「遇到 X 錯誤該怎麼修」
- Q-value 排序 = 一種 [[compounding-memory]] 機制 — 每次失敗都讓知識庫更強
- Shared Gene Map 願景 = [[experiential-memory]] 的跨 agent 共享 — 正好對應 Viv Trivedy 的「agent 經驗可以 fork/duplicate」論點
- 「fix once, immune forever」跟 [[brain-first-lookup]] 精神一致 — 先查已知解法，沒有才呼叫 LLM

## Key Sources

- **2026-04-14** — Nicholas & Adrian 發表 Helix，附 50 場景 benchmark 數據。Source: [[raw/nicholas-helix-self-healing-agents]]

## Related

[[gene-map]] [[procedural-memory]] [[compounding-memory]] [[experiential-memory]] [[brain-first-lookup]] [[nicholas-dapanji]] [[memory-evaluation]]
