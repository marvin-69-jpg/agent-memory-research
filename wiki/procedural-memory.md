---
aliases: [procedural memory, 程序記憶, 技能記憶, how-to memory]
first_seen: 2026-04-13
last_updated: 2026-04-15
tags: [memory, architecture]
---

# Procedural Memory

第三種記憶類型：儲存「怎麼做」而非「發生了什麼」（episodic）或「知道什麼」（semantic）。在人類認知中對應 skills — 騎腳踏車、打字。在 AI agents 中對應學到的 workflow、tool-use pattern、process knowledge。

## Current Understanding

- **三種記憶的區分**：
  - Episodic：what happened（對話歷史、事件）
  - Semantic：what is known（事實、偏好、知識）
  - Procedural：how to do things（流程、技能、慣例）
- **實際案例**：coding assistant 學到某團隊的 PR 結構、偏好的測試 pattern、部署 workflow。這不是 user preference（「我喜歡 dark mode」），不是事實記憶（「使用者用 TypeScript」），是一個 process
- **Mem0 的實作**：`memory_type="procedural_memory"` 參數路由到不同的 extraction prompt，專注 distilling procedures 和 workflows 而非 facts 和 preferences
- **與 GBrain 的對比**：GBrain 的 thin-harness-fat-skills 架構隱含了 procedural memory — skills 本身就是 procedure 的具體化。但 GBrain 是 explicit skills（寫成 markdown），Mem0 的 procedural memory 是 extracted implicit procedures
- **與 openab-bot 的對比**：我們的 feedback memory 其實部分扮演了 procedural memory 的角色（「日報配圖要用彩蛋不要氛圍」= 一種 procedure），但沒有明確區分 type
- **Autoreason 的 emergent skill**：[[autoreason]] 的論文寫作過程中，Hermes Agent 開發了 research-paper-writing skill — procedural memory 的實際案例。Skill 是在 task 執行中浮現的，不是預先寫好的
- **Helix Gene Map — error-specific procedural memory**：[[helix]] 的 [[gene-map|Gene Map]] 是 procedural memory 的具體實作 — 記住「遇到 X 錯誤該怎麼修」。用 Q-value（RL）自動排序策略，成功的提升、失敗的降級。首次錯誤需 LLM 診斷（~2s），之後同類錯誤 1ms pattern match 修復。這是目前看到的最具體的 procedural memory production 實踐

## Key Sources

- **2026-04-14** — Helix Gene Map: error-specific procedural memory with Q-value RL ranking。Source: [[raw/nicholas-helix-self-healing-agents]]
- **2026-04-01** — Mem0 v1.0.0 引入 procedural memory API。Source: [[raw/mem0-state-of-ai-agent-memory-2026]]

## Related

[[mem0]] [[agent-memory]] [[thin-harness-fat-skills]] [[compounding-memory]] [[autoreason]] [[helix]] [[gene-map]] [[agemem]] [[coding-agent-memory]] [[shl0ms]] [[mirix]] [[multimodal-memory]] [[self-improving-agent]] [[asg-si]] [[skillfoundry]] [[empo2]] [[harrison-chase]]
