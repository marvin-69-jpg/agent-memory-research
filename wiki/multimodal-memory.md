---
aliases: [multimodal memory, 多模態記憶, visual memory, audio memory]
first_seen: 2026-04-15
last_updated: 2026-04-15
tags: [memory, architecture]
---

# Multimodal Memory

Agent 記憶系統處理非文字模態（影像、音訊、影片、螢幕截圖）的能力 — 從「文字優先」到「原生多模態」的演進。

## Current Understanding

### 為什麼多模態記憶重要

現有主流記憶系統（[[mem0]]、[[letta]]、[[gbrain]]、[[chatgpt-memory]]）幾乎都是純文字的。但真實世界的 agent 需要處理：
- 螢幕截圖（桌面助手）
- 攝影機畫面（embodied agent / robot）
- 音訊（語音助手、會議記錄）
- 影片（長影片理解）

Pengfei Du survey 將多模態記憶列為 10 大 open challenges 第 5。

### MIRIX — 六種記憶 + 多 agent 管理

MIRIX（Yu Wang & Xi Chen, 2025）是目前最完整的多模態記憶架構：

**六種記憶類型**（擴展了傳統 episodic/semantic/procedural 三分法）：
1. **Core Memory** — 高優先級持久資訊（agent persona + user facts），rewrite 機制保持精簡
2. **Episodic Memory** — 時間戳事件日誌
3. **Semantic Memory** — 抽象事實知識，樹狀結構
4. **Procedural Memory** — 結構化流程（how-to, workflows）
5. **Resource Memory** — 完整文件、transcript、多模態檔案
6. **Knowledge Vault** — 敏感資訊安全儲存

**多 agent 記憶管理**：
- Meta Memory Manager 中央調度 + 6 個專門 Memory Manager 平行管理
- 這是目前看到最具體的 multi-agent memory governance 實作 → [[actor-aware-memory]]

**Active Retrieval**（retrieval timing 的第四種策略）：
- 自動推斷當前 topic → 從六種記憶檢索 → tag 後注入 system prompt
- 不是 always-injected、不是 hook-driven、不是 tool-driven，而是 **topic-driven auto-inject**
- 支援 embedding_match、bm25_match、string_match 多種方式

**多模態效率**：
- 每 1.5 秒截圖，過濾重複後每 20 張觸發記憶更新
- 只存抽取的 salient info（15.89 MB SQLite），不存原圖（15.07 GB）→ **99.9% 儲存壓縮**
- 準確率反而比 RAG baseline 高 35%（ScreenshotVQA benchmark）
- LOCOMO 達 85.38%（SOTA），超越 Zep 8%

### M3-Agent — Entity-Centric 多模態 Graph + RL

M3-Agent（ByteDance Seed, 2025）從 embodied agent 角度解決多模態記憶：

**Entity-centric multimodal graph**：
- 記憶以 entity 為中心（同一人的臉、聲音、知識相連）→ 延伸了 [[graph-memory]] 到多模態
- Weight-based voting 解決衝突資訊
- 外部工具做臉部辨識 + 說話人辨識 → 持久的 face_id / voice_id
- 跨 clip 一致追蹤角色

**雙程序架構**：
- **Memorization**：持續感知多模態輸入 → 生成 episodic + semantic 記憶
- **Control**：RL 訓練的多輪推理（DAPO 演算法），不是單輪 RAG

**Ablation 關鍵發現**：
- 移除 semantic memory → **最大的準確率下降**（-17% ~ -19%）
- 移除 character identity equivalence → -11.2%
- RL vs prompt-based → +8% ~ +10%
- 結論：derived knowledge（semantic memory）在多模態場景**不是妥協，是必要的**

**M3-Bench**：首個專注高層認知能力的多模態記憶 benchmark — person understanding、cross-modal reasoning、multi-hop reasoning

### Raw vs Derived 在多模態場景的新意義

多模態場景讓 [[memory-failure-modes|raw vs derived 張力]] 更加尖銳：
- Raw 影像/影片太大（GB 級）、太無組織 → 不存 raw 是**效能必要**，不只是設計選擇
- MIRIX 的 99.9% 壓縮 + 35% 準確率提升證明：well-designed derived > brute-force raw
- 但 derived 仍會 drift — M3-Agent 用 weight-based voting 緩解，MIRIX 用結構化六層分離緩解

### 開放問題

1. **Fine-grained visual memory**：M3-Agent 的 hard cases 包括精確提取微小視覺細節和空間推理
2. **跨模態 identity binding**：如何穩定地將臉、聲音、文字描述綁定為同一 entity
3. **多模態 forgetting**：刪除一段影片記憶時，衍生的文字 summary 怎麼辦？比純文字的 forgetting propagation 更複雜
4. **Privacy**：螢幕截圖記憶引發嚴重隱私問題 — 比文字記憶更敏感

## Key Sources

- **2025-07-10** — MIRIX: 六種記憶 + 多 agent 管理 + Active Retrieval + ScreenshotVQA benchmark。Source: [[raw/mirix-multiagent-memory-system]]
- **2025-08** — M3-Agent: Entity-centric multimodal graph + RL 控制 + M3-Bench。Source: [[raw/m3-agent-multimodal-long-term-memory]]

## Related

[[agent-memory]] [[graph-memory]] [[procedural-memory]] [[experiential-memory]] [[actor-aware-memory]] [[multi-scope-memory]] [[memory-evaluation]] [[memory-failure-modes]] [[agemem]] [[mem0]] [[locomo]] [[memory-arena]] [[entity-detection]] [[brain-first-lookup]] [[compiled-truth-pattern]] [[open-questions]] [[mirix]] [[memu]]
