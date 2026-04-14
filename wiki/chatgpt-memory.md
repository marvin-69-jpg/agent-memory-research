---
aliases: [ChatGPT Memory, OpenAI Memory, ChatGPT 記憶]
first_seen: 2026-04-14
last_updated: 2026-04-14
tags: [product, memory]
---

# ChatGPT Memory

OpenAI 的消費者端記憶系統。經逆向工程揭示：**沒有 vector DB、沒有 RAG** — 是四層靜態注入架構，設計哲學是 speed over completeness。

## Current Understanding

### 四層架構（Manthan Gupta 逆向工程）

| 層 | 內容 | 持久性 | Token 成本 |
|---|---|---|---|
| Session Metadata | 裝置、timezone、subscription、usage patterns | Ephemeral（每 session 注入一次） | 低 |
| User Memory | 顯式儲存的 facts（名字、偏好、目標），~10k tokens | Persistent | 每次都注入 |
| Recent Conversations Summary | 過去對話 titles + user message snippets，~15 條 | Persistent | 每次都注入 |
| Current Session | 完整對話 sliding window，token-based rolloff | Session-only | 隨對話增長 |

### 設計決策分析

- **不用 RAG 的原因**：pre-computed 摘要直接注入，跳過 embedding/search/retrieval 延遲。犧牲詳細度換速度
- **只摘要 user messages**：Recent Conversations Summary 不包含 assistant 回應 — 是興趣地圖，不是完整記錄
- **Token budget 管理**：session 增長時舊訊息 roll off，但 memory facts 和對話摘要保留 — 長期 context 比短期對話優先

### 用 Chrys Bader 9 軸框架分析

| 軸 | ChatGPT 的選擇 |
|---|---|
| 1. What gets stored | Derived（user messages 摘要）+ raw facts |
| 2. When derivation | Pre-computed（async，非 real-time） |
| 3. Write trigger | 使用者說「記住」或模型自動偵測 + 隱性同意 |
| 4. Where stored | OpenAI server（不透明） |
| 5. Retrieval | 無 retrieval — 全量注入 |
| 6. Post-retrieval | 無（不需要，因為沒有 retrieval） |
| 7. When retrieval | Always-injected — [[chrysb]] 指出此模式 "pollutes context with irrelevant history" |
| 8. Who curates | Main model + user（user 可看/編輯/刪除） |
| 9. Forgetting | User 手動刪除 + Temporary Chat 模式 |

### Charles Packer（MemGPT 作者）的批評

- ChatGPT memory 是**黑盒** — 不透明地操作 context window，可能降低下限
- 「saves stupid memories that pollute the context window」
- 使用者已經靠「開新 chat = 新 session」手動管理 context，memory feature 反而破壞這個 muscle memory
- 解法：讓使用者看到哪些 chunks 被拉進 context、透過哪種 mechanism

### 與其他消費者產品比較

| 產品 | Memory 觸發 | 更新頻率 | 透明度 |
|---|---|---|---|
| ChatGPT | 自動 + 手動 | 滾動 | 可看 stored facts |
| Claude | 明確 tool 呼叫 | ~每 24hr re-summarize | CLAUDE.md + memory/ 可讀寫 |
| Gemini | Premium 自動 | — | Temporary chats 模式 |
| Grok | 自動 | — | 一鍵刪除 |

## Key Sources

- **2025-12-09** — Manthan Gupta 逆向工程 ChatGPT Memory 四層架構。Source: [[raw/manthan-gupta-chatgpt-memory-reverse-engineered]]
- **2025-08-28** — Yohei Nakajima 消費者端 memory 比較。Source: [[raw/yohei-nakajima-rise-of-ai-memory]]

## Related

[[agent-memory]] [[memory-lock-in]] [[chrysb]] [[memory-failure-modes]] [[coding-agent-memory]] [[yohei-nakajima]]
