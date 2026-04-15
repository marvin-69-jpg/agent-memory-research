---
date: 2026-04-15
topic: Multimodal memory
gap_type: research-gap
sources_found: 2
wiki_pages_updated: 5
wiki_pages_created: 2
---

# Daily Research: Multimodal Memory

## 研究動機

`wiki gaps` 列為第一優先的 RESEARCH-GAP — 完全沒覆蓋的領域。Pengfei Du survey 列為 10 大 open challenges 第 5。open-questions.md 也明確標記「完全沒覆蓋」。

多模態記憶是 agent memory 的下一個前沿：現有的記憶系統（包括我們研究過的 Mem0、Letta、GBrain、ChatGPT Memory）幾乎都是純文字的。但真實世界的 agent 需要處理影像、音訊、螢幕截圖等多模態輸入。

## 發現

### MIRIX（arxiv 2507.07957）— 六種記憶 + 多 agent 管理 + 多模態原生支持

- **六種記憶類型**：Core、Episodic、Semantic、Procedural、Resource Memory、Knowledge Vault。比我們 wiki 現有的三層分類（episodic/semantic/procedural）更細緻，增加了 Core（高優先級持久資訊）、Resource（完整文件）、Knowledge Vault（敏感資訊）（來源：MIRIX paper Section 4.1）
- **多 agent 記憶管理**：Meta Memory Manager 中央調度 + 6 個專門 Memory Manager 平行管理各自記憶。這直接回應了 open question #10（Multi-Agent Memory Governance）（來源：MIRIX paper Section 4.2）
- **Active Retrieval**：自動推斷 topic → 從全部六種記憶檢索 → tag 後注入 system prompt。這是 open question #8（When Retrieval Happens）的一個新解法 — 既不是 always-injected 也不是 pure tool-driven，而是 topic-driven auto-inject（來源：MIRIX paper Section 4.3）
- **多模態效率驚人**：處理 5,000-20,000 張螢幕截圖，只存抽取的 salient info（15.89 MB SQLite），比存原圖（15.07 GB）減少 99.9% 儲存。準確率反而比 RAG baseline 高 35%（來源：MIRIX paper Section 5.1）
- **LOCOMO SOTA**：85.38% 準確率，超越 Zep 8%，接近 Full-Context upper bound（來源：MIRIX paper Section 5.2）

### M3-Agent（arxiv 2508.09736）— Entity-centric 多模態 graph + RL 控制

- **Entity-centric multimodal graph**：記憶以 entity 為中心組織（同一人的臉、聲音、知識相連），用 weight-based voting 解決衝突。這跟 graph-memory 頁面的概念直接相關，但加入了多模態維度（來源：M3-Agent paper Section 4.1）
- **持續感知 + 記憶雙程序**：Memorization（持續處理多模態輸入 → 建構記憶）和 Control（推理 + 檢索 + 執行）平行運作。這是 brain-agent-loop 在多模態場景的延伸（來源：M3-Agent paper Section 4.2-4.3）
- **RL 訓練的多輪推理**：不是單輪 RAG，而是用 DAPO 訓練的多輪推理。RL 比 prompt-based 提升 8-10% — 強力證據支持 AgeMem 的 RL 路線（來源：M3-Agent paper Section 4.4, Table 7）
- **Semantic memory 是關鍵**：ablation 移除 semantic memory 導致 -17~19% 準確率下降，是所有 ablation 中影響最大的。這暗示「只存 episodic 不做 semantic 抽象」的系統可能在多模態場景嚴重受限（來源：M3-Agent paper Table 6）
- **M3-Bench**：首個專注高層認知能力的多模態記憶 benchmark（person understanding, cross-modal reasoning 等），填補了 memory-evaluation 的空白（來源：M3-Agent paper Section 4.5）

## 與已有知識的連結

| 新發現 | 連結到的 wiki 頁面 | 關係 |
|---|---|---|
| MIRIX 六種記憶 | [[agent-memory]], [[procedural-memory]] | 擴展三層分類為六層 |
| Multi-agent 記憶管理 | [[actor-aware-memory]], [[multi-scope-memory]] | 直接回應 open question #10 |
| Active Retrieval | [[brain-first-lookup]] | retrieval timing 的新解法 |
| Entity-centric graph | [[graph-memory]], [[entity-detection]] | graph + entity 的多模態版本 |
| RL 控制記憶 | [[agemem]] | 第二個 RL for memory 的案例，互相印證 |
| 多模態 benchmark | [[memory-evaluation]], [[memory-arena]], [[locomo]] | 補充多模態維度的評估 |
| Semantic memory 至關重要 | [[compiled-truth-pattern]] | 支持 derived knowledge 的必要性 |
| 99.9% 儲存壓縮 | [[memory-failure-modes]] | raw vs derived 的實證數據 |

## Open Questions 推進

1. **#8 When Retrieval Happens**：MIRIX 的 Active Retrieval（topic-driven auto-inject）提出了第四種 timing 策略，值得加入討論
2. **#10 Multi-Agent Memory Governance**：MIRIX 的 Meta Manager + 6 專門 Manager 是目前最具體的 multi-agent 記憶治理實作
3. **#1 Raw vs Derived**：MIRIX 在 ScreenshotVQA 的 99.9% 儲存壓縮 + 35% 準確率提升，是強力證據 — 在多模態場景，derived 不只是妥協，而是必要的（raw 圖片太大、太無組織）
4. **#12 Foundation Models for Memory**：M3-Agent 用 RL 訓練專門的 memorization model，是繼 AgeMem 之後第二個 FM for memory 案例

## 下一步

- **Neuroscience integration**（下一個 research gap）可能跟多模態記憶有交叉 — 人類大腦的多模態記憶整合機制（如 hippocampal binding theory）
- 搜尋 TeleMem（arxiv 2601.06037）— 出現在搜尋結果中，專注 long-term multimodal memory for agentic AI
- 追蹤 OpenClaw 的多模態記憶功能（agents index images and audio，用 Gemini embedding）
