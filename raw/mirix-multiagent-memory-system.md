# MIRIX: Multi-Agent Memory System for LLM-Based Agents

- **Authors**: Yu Wang, Xi Chen (MIRIX AI / UCSD / NYU Stern)
- **Date**: 2025-07-10
- **Source**: https://arxiv.org/abs/2507.07957
- **Type**: arxiv paper

## Summary

MIRIX 是一個模組化的多 agent 記憶系統，專為 LLM-based agents 設計。核心創新在於：

1. **六種記憶類型**：Core、Episodic、Semantic、Procedural、Resource Memory、Knowledge Vault
2. **多 agent 架構**：Meta Memory Manager + 6 個 Memory Managers + Chat Agent，各自管理一種記憶
3. **Active Retrieval**：自動推斷 topic → 從六種記憶中檢索 → 注入 system prompt，不需要使用者顯式查詢
4. **原生多模態支持**：處理螢幕截圖等視覺資料，每 1.5 秒截圖一次，每 60 秒觸發記憶更新

## Key Results

### ScreenshotVQA（新 benchmark，多模態記憶）
- 資料集：3 名 PhD 學生的 5,000-20,000 張高解析度電腦螢幕截圖
- MIRIX 準確率 59.50%，比 RAG baseline（SigLIP@50）高 35%，比 long-context Gemini 高 410%
- 儲存只需 15.89 MB（SQLite），比 SigLIP@50（15.07 GB）減少 99.9%

### LOCOMO（文字對話記憶）
- MIRIX 達 85.38% 準確率，超越最佳 baseline（Zep, 79.09%）8%
- Multi-hop 問題表現最突出，比 baselines 高 24+ 個百分點
- 接近 Full-Context upper bound（87.52%）

## Architecture Details

### 六種記憶
1. **Core Memory**：持久高優先級資訊（agent persona + user facts），用 rewrite 機制保持精簡
2. **Episodic Memory**：時間戳事件日誌（event_type, summary, details, actor, timestamp）
3. **Semantic Memory**：抽象事實知識，獨立於時間（name, summary, details, source），樹狀結構
4. **Procedural Memory**：結構化流程（how-to, workflows, steps in JSON）
5. **Resource Memory**：完整文件、transcript、多模態檔案（title, summary, resource_type, content）
6. **Knowledge Vault**：敏感資訊安全儲存（credentials, API keys），有存取控制

### Multi-Agent Workflow
- **Meta Memory Manager**：中央調度，分析輸入 → 路由到正確的 Memory Manager
- **Memory Managers（×6）**：各自平行管理一種記憶，處理更新和檢索
- **Chat Agent**：處理自然語言互動，發起記憶搜尋，整合結果

### Active Retrieval
1. Topic Generation：收到輸入時自動推斷當前主題
2. Automated Retrieval：用主題自動從六種記憶檢索
3. Prompt Injection：檢索結果用 tag 注入 system prompt（如 `<episodic_memory>...</episodic_memory>`）
4. 支援 embedding_match、bm25_match、string_match 多種檢索方式

### 多模態處理
- React-Electron 前端 + Uvicorn 後端
- 每 1.5 秒截圖，過濾重複後每 20 張觸發記憶更新（約每 60 秒）
- 用 Gemini API streaming upload 處理多模態資料
- 只存抽取的 salient information，不存原始圖片

## 與現有系統比較

批評現有方案的限制：
- **Knowledge Graph**（Zep, Cognee）：無法處理順序事件、情緒狀態、多模態輸入
- **Flat Memory**（Letta, Mem0, ChatGPT Memory）：缺乏組合式記憶結構、多模態支持差、難以 scale
- **Latent-space Memory**：需要重新訓練 LLM，不兼容 closed-source 模型

## Vision

- Agent Memory Marketplace：個人記憶成為可交易的數位資產
- 穿戴裝置整合：AI 眼鏡、pin 等的即時記憶形成
