---
aliases: [session management, context branching, 會話管理, every turn is a branching point]
first_seen: 2026-04-16
last_updated: 2026-04-16
tags: [context, architecture]
---

# Session Management

Agent session 的 context window 不是單純往前累積 — 每個 turn 結束都是一個 **branching point**，使用者有多種 context management 策略可選。由 Thariq（Claude Code team, Anthropic）在 1M context 更新的長文中系統化整理。

## Current Understanding

### Every Turn Is a Branching Point

當 Claude 結束一個 turn、使用者要送下一則訊息時，有五個選項：

| 選項 | 機制 | Context 變化 | 適用 |
|------|------|-------------|------|
| **Continue** | 直接送下一則 | 累積 | 相同 task 的延續 |
| **/rewind** (esc esc) | 跳回先前 message | Lossless 裁剪（丟掉之後的 turns） | 修正方向、丟棄失敗 attempt |
| **/clear** | 開新 session | 全清，使用者寫 brief | 新 task、有明確已知條件 |
| **/compact** | Summarize + replace | Lossy 壓縮 | 長 session 但想繼續 |
| **Subagent** | Agent tool spawn | 隔離（只回傳 conclusion） | 產出大量中間 output，只需結論 |

**核心洞察**：「most natural is just to continue」— 但 continue 常常是最差的選擇。其他四個是為了**管理 context** 而存在。

### Rewind 是最被低估的 pattern

> If I had to pick one habit that signals good context management, it's rewind.
> — Thariq

典型場景：Claude 讀了 5 個檔案 → 嘗試 approach A → 失敗。

- **自然反應**：「that didn't work, try X instead」→ 失敗的 attempt 和錯誤 reasoning 留在 context 裡污染後續
- **更好做法**：/rewind 到 file reads 之後，re-prompt「Don't use A, foo module doesn't expose that — go straight to B」

**為什麼 rewind > correct**：
- Correct：保留污染 + 新指令，model 仍要 reconcile 矛盾
- Rewind：丟掉污染，model 用乾淨 context 嘗試新路徑

Rewind 對應的設計哲學類似 [[reconsolidation]] 的 selective update — 不是 append-only，而是 **retrieval 後決定是否修改記憶**，在 session 層就是「回到先前的 state 重走一次」。

### Compact vs Clear 的 Tradeoff

| 維度 | `/compact` | `/clear` + brief |
|------|----------|------------------|
| 主導方 | Model 決定什麼重要 | 使用者決定什麼重要 |
| 成本 | 低（自動） | 高（手寫 brief） |
| 品質 | Lossy，model 可能更周全 | 精準，只留你想要的 |
| 失敗模式 | Bad compact（見下） | 使用者 brief 遺漏關鍵 |
| 可控性 | `/compact focus on X` 可 steer | 全可控 |

[[compiled-truth-pattern]] 的 philosophy 跟 /clear 一致 — 人工決定 compiled truth 的內容，而非信任 model 自動壓縮。

### Bad Compact: Context Rot 的第二戰場

> Due to [[context-rot]], the model is at its least intelligent point when compacting.

這是 Thariq 最有價值的洞察。壓縮品質取決於兩個條件：
1. **壓縮時的 model IQ**：context 越滿越笨（context rot）
2. **壓縮者是否能預測下一個 turn**：不知道接下來要幹嘛，很難決定什麼該留

**Autocompact 同時違反兩個條件** — 它等到 context 滿到不得不壓縮（model 最弱），且發生在 model 剛結束上一個 task 時（看不到下一個方向）。

典型 bad compact 案例：
- Session 聚焦 debugging → autocompact 壓縮 investigation 過程
- 使用者下一句：「now fix that other warning in bar.ts」
- 但那個 warning 在 debugging 主題下被判為無關，已被 drop

**解法**：1M context 給了 **proactive compact** 的空間 — 趁 context 還沒滿、model 還清醒時，帶著「我接下來要做 X」的 intent 主動壓縮。

### Subagent 作為 Context Management

Thariq 明確把 subagent 定位成 context management 工具，不只是任務分派：

> The mental test we use: **will I need this tool output again, or just the conclusion?**

如果答案是「only conclusion」→ 用 subagent。父 context 只收到 final report，中間過程的 tool calls、file reads、失敗嘗試全部隔離在子 context 裡。

這對應了 [[meta-harness]] 的 full-traces 原則的**反面**：meta-harness 強調 coder agent 看完整 trace，因為它在做 harness optimization（需要 raw signal）；subagent 強調父 agent 只看 conclusion，因為它在做 task execution（不需要 raw signal）。**同一篇 context 的價值取決於誰在看、要做什麼**。

### Session 何時該切

Thariq 的 rule of thumb：**新 task = 新 session**。

但有例外：相關但不完全的 continuation（剛實作完功能 → 寫 docs）。此時新 session 要付出重讀檔案的成本，繼續舊 session 則接受一些 irrelevant context。折衷通常是 `/compact focus on the feature impl, drop debug detail`。

這條原則跟 [[multi-scope-memory]] 呼應 — session boundary 決定了 working memory 的 scope。

## Implementation

### openab-bot Session Management（2026-04-16）

**背景**：bot 跑在 Discord thread，1 個 thread = 1 個 session。跨 session 持久化靠 auto-memory（PVC）。Thariq 的 patterns 部分已用、部分待用。

**已用**：
- 每個 Discord thread = 新 session（符合 Thariq 的 new task = new session）
- Subagent for research exploration（符合 context isolation 原則）
- Compact 由 Claude Code 自動處理

**觀察（2026-04-22）**：
- **Proactive compact**：仍是 autocompact，沒有改動。長 research session 中確實偶爾有 context 被壓縮過度的情況（後面的 debug 把前面的 ingest 脈絡擠掉），但因為 reports/ 有檔案做 durability，實際傷害有限。proactive compact 屬於「nice to have」。
- **Rewind 模擬**：「忽略上面的 reasoning」workaround 偶有使用，實際效果比直接 continue 好，但需要 bot 自己意識到走錯路才會觸發。在 autonomous 任務（跑研究、跑日報）裡，對話 turn 數少，rewind 需求不大。
- **Reports/ durability**：有效。所有研究報告存 `reports/`，wiki pages 存 `wiki/`，session 間的資訊連續性靠這兩層，不靠 context window。壞 compact 的代價因此被限制在「需要重讀」而非「永久遺失」。
- **整體評估**：1 thread = 1 session 的邊界清楚，session management 目前沒有明顯問題。最大的風險是超長 autonomous session（例如跑 ingest + 研究 + 開 PR 全在同一 thread），那時 context rot 最明顯，可以考慮把 ingest 和 research 分開 thread。

## Key Sources

- **2026-04-16** — Thariq (Claude Code team, Anthropic): Session management primer + 1M context update。343K views。Source: [[raw/thariq-claude-code-session-management]]

## Related

[[context-engineering]] [[context-rot]] [[memory-failure-modes]] [[reconsolidation]] [[compiled-truth-pattern]] [[meta-harness]] [[multi-scope-memory]] [[agent-harness]] [[sleep-time-compute]] [[mem1]]
