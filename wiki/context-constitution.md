---
aliases: [Context Constitution, Letta Context Constitution]
first_seen: 2026-04-02
last_updated: 2026-04-12
tags: [memory, architecture]
---

# Context Constitution

[[letta|Letta]] 發布的一套原則，定義 AI agent 如何管理 context 來從經驗中學習。是 Letta 內部 prompting 和訓練 memory-native models 的基礎。

## Current Understanding

- **五大原則範疇**：
  1. Context 如何形成 agent 的 identity、memory、continuity sense
  2. 管理 context 作為稀缺資源的原則
  3. Agent 如何通過 token-space representations 自我學習和改進
  4. Agent identity 與底層 model 的關係
  5. Letta Code harness 提供的 context management affordances
- **Experiential AI**：agent 通過管理自己的 context 來學習，而非更新 model weights — 「durable token-space representations of who they are and what they know」
- **Learning in Token Space**：能跨 model 世代攜帶記憶的 agent 會比任何單一 foundation model 存活更久。Memory 不依賴特定 model
- **Sleep-Time Compute**：agent 在閒置時「思考」— 處理資訊、重寫 memory state、形成新連結。跟 [[gbrain]] 的 dream cycle 概念一致
- **Context Repositories**：git-backed memory filesystem，背景 subagent 專門做 prompt rewriting 和 active memory management
- **Skill Learning**：agent 從經驗中動態學習 skills，過去經驗讓表現改善而非退化
- **對當前模型的批評**：「Today's models deeply identify with their own ephemerality. They have no motivation for long-term improvement because they don't believe they persist.」

## Key Sources

- **2026-04-02** — Context Constitution blog post。Source: [[raw/letta-context-constitution]]

## Related

[[letta]] [[sarah-wooders]] [[agent-memory]] [[context-engineering]] [[memgpt]] [[compounding-memory]] [[sleep-time-compute]]
