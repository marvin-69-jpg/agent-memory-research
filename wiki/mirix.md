---
aliases: [MIRIX, mirix, MIRIX AI]
first_seen: 2026-04-15
last_updated: 2026-04-15
tags: [product, memory, architecture]
---

# MIRIX

模組化多 agent 記憶系統 — 六種記憶類型 + Active Retrieval + 原生多模態支持。由 MIRIX AI（UCSD / NYU Stern）開發。

## Current Understanding

- **六種記憶**（擴展傳統三分法）：Core、Episodic、Semantic、Procedural、Resource Memory、Knowledge Vault → 詳見 [[multimodal-memory]]
- **Multi-agent 架構**：Meta Memory Manager + 6 個專門 Memory Manager + Chat Agent。每個 Memory Manager 平行管理自己的記憶類型 — 目前看到最具體的 multi-agent memory governance 實作
- **Active Retrieval**：topic-driven auto-inject — 自動推斷主題 → 從全部六種記憶檢索 → tag 後注入 system prompt。retrieval timing 的第四種策略（不是 always-injected / hook-driven / tool-driven）
- **多模態效率**：處理 5,000-20,000 張螢幕截圖，只存 15.89 MB SQLite（vs 原圖 15.07 GB），99.9% 儲存壓縮
- **ScreenshotVQA benchmark**（新）：準確率 59.50%，比 RAG baseline 高 35%，比 long-context Gemini 高 410%
- **LOCOMO SOTA**：85.38%，超越 Zep（79.09%）8%，接近 Full-Context upper bound（87.52%）。Multi-hop 問題比 baselines 高 24+ 個百分點 — 因為六層結構化記憶讓 consolidated events 可以直接 retrieve，不需要 multi-step reasoning
- **Vision**：Agent Memory Marketplace（個人記憶成為數位資產）、穿戴裝置整合

### 對現有系統的批評

- Knowledge Graph（Zep, Cognee）：無法處理順序事件、情緒、多模態
- Flat Memory（Letta, Mem0, ChatGPT Memory）：缺乏組合式結構、多模態差、難 scale
- Latent-space Memory：需重新訓練 LLM，不兼容 closed-source 模型

## Key Sources

- **2025-07-10** — Yu Wang & Xi Chen: MIRIX paper (arxiv 2507.07957)。Source: [[raw/mirix-multiagent-memory-system]]

## Related

[[multimodal-memory]] [[agent-memory]] [[mem0]] [[letta]] [[actor-aware-memory]] [[multi-scope-memory]] [[graph-memory]] [[locomo]] [[memory-evaluation]] [[memory-arena]] [[brain-first-lookup]] [[procedural-memory]] [[agemem]] [[memu]]
