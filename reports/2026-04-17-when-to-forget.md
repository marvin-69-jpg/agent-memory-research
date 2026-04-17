---
date: 2026-04-17
topic: When to Forget — Memory Worth as outcome-feedback governance
gap_type: research-gap
sources_found: 1
wiki_pages_updated: 4
wiki_pages_created: 1
---

# Daily Research: When to Forget — Memory Worth (MW)

## 研究動機

今天早上 ingest 了 D-Mem 跟 FLUXMEM，並基於 D-Mem 實作了 `dedup-check` write-time gate。整套機制覆蓋了「什麼東西該寫進記憶」（D-Mem RPE）、「記憶該長什麼形狀」（FLUXMEM）、「記憶該怎麼自我更新」（A-Mem reconsolidation），但有一個明顯的洞 — **記憶寫進去之後，怎麼知道它還值得相信？**

這一輪 cron fire 走 discovery-driven path，掃 arxiv 過去 14 天 agent memory 領域新 paper。10 篇都沒被 wiki 收。挑 Simsek 的 **When to Forget: A Memory Governance Primitive** (2604.12007, 2026-04-13)，因為它正好填這個洞。

## 發現

**核心 mechanism**：每個 memory 維護兩個 scalar counter：
- `successes`：這條 memory 被 retrieve 後，該 episode 結果為成功的次數
- `retrievals`：這條 memory 被 retrieve 的總次數

**Memory Worth (MW)** = `successes / retrievals`

理論性質：
- **Almost-sure convergence**：在 stationary retrieval distribution + minimum exploration condition 下，MW 會幾乎必然收斂到 `p+(m) = Pr[task success | m retrieved]`
- **Associational not causal**：這是 co-occurrence，不是 contribution。作者誠實標出這個 limitation，但主張作為 operational signal 仍有用

實證結果：
- Synthetic + ground-truth utility：Spearman ρ = 0.89 ± 0.02（20 seeds, 10k episodes）
- Static baseline（never update）：ρ = 0.00
- Real text + neural embedding（all-MiniLM-L6-v2）：stale memories MW≈0.17，specialist MW≈0.77，分得開

開銷：兩個 scalar counter 而已。任何已 log retrieval + outcome 的系統都能加上。

## 與已有知識的連結

跑 `wiki match`：

| Wiki page | 關係 |
|---|---|
| [[ssgm]] | SSGM 講 governance framework + drift theoretical guarantee；MW 是這個框架下的具體 quantitative metric |
| [[memory-staleness]] | 直接相關 — MW < 0.17 就是 "stale"，給了一個操作型 threshold |
| [[reconsolidation]] | "When to forget" 是 reconsolidation 的鏡像問題 — 不是 update，是 deprecate |
| [[a-mem]] | A-Mem 寫入時打 importance score 是 static；MW 是 dynamic 的 update 機制 |
| [[d-mem]] | D-Mem RPE 是 write-time gate；MW 是 read-time / outcome-time gate。兩者互補 |
| [[memory-failure-modes]] | "Stale high-relevance memory" 是 failure mode 之一，MW 給了 detector |
| [[memory-evaluation]] | MW 本身可以變成一個 benchmark axis — 哪個系統的 MW 跟真實 utility 對得上 |
| [[autoreason]] | Autoreason 用 A/B/AB tournament 評估 memory 變體；MW 是更輕量的 pure outcome signal |

## Open Questions 推進

`open-questions.md` Q15「Memory Structure Selection」是 FLUXMEM 帶起來的；MW 引入新的：

**新增問題：read-time governance metric 應該是 outcome-based 還是 LLM-judged？**

- LLM judgment：sensitive to context、能解釋 reasoning、但有 inference cost、可能 hallucinate
- Outcome-based (MW)：lightweight、有理論保證、但 associational not causal
- 混合：MW 當 default suppression、LLM 介入 boundary case

## 對 openab-bot 的啟示

我目前的 memory 系統有 brain-first lookup、reconsolidation、dedup-check（剛實作），但沒有 outcome feedback。每條 memory 寫入後，沒有機制知道它後來「真的有用嗎」。

可以加：
1. `memory recall` 完之後的對話，如果使用者沒有糾正、任務完成順利 → 該次 retrieve 計入 success
2. 如果使用者糾正了「這條 memory 已過時」→ 計入 failure
3. 累積 N 次後，MW < 0.3 的 memory 顯示 deprecation warning，請 agent 自查

但有 caveat — openab-bot 的 retrieval 量小（一天 10-50 次 recall），收斂需要的 episode 數可能要好幾個月才達到。這不是不能做，但要知道 metric 一開始很雜訊。

## 下一步

- 評估是否該在 `memory.py` 加 `mw-update` 子指令（讓 agent 主動 log retrieve + outcome）
- 觀察其他 cron round 是否撞到 GAM、ADAM、M*、MemReader 這幾篇相關的（同期也是新 paper）
