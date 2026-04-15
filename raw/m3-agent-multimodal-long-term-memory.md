# M3-Agent: Seeing, Listening, Remembering, and Reasoning — A Multimodal Agent with Long-Term Memory

- **Authors**: Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan Lin, Hang Li, Junbo Zhao, Wei Li
- **Institution**: ByteDance Seed + Zhejiang University + Shanghai Jiao Tong University
- **Date**: 2025-08
- **Source**: https://arxiv.org/abs/2508.09736
- **Type**: arxiv paper

## Summary

M3-Agent 是 ByteDance 開發的多模態 agent 框架，能持續處理視覺和聽覺輸入，建立和更新 entity-centric 的多模態長期記憶，並用 RL 訓練的多輪推理來回答問題。

## Core Architecture

### 兩個平行程序
1. **Memorization**：持續感知視覺/聽覺輸入 → 建構/更新長期記憶
2. **Control**：接收指令 → 推理 → 檢索記憶 → 執行任務

### Entity-Centric Multimodal Graph（長期記憶）
- 外部資料庫，節點代表記憶項目（有 ID、type、raw content、embedding、weight、metadata）
- 無向邊表示邏輯關係，特別是 entity-centric 連結（同一個人的臉、聲音、知識相連）
- **Weight-based voting mechanism**：解決衝突資訊，頻繁被激活的正確條目會覆蓋低信心條目
- 支援 `search_node` 和 `search_clip` 兩種檢索方式

### 記憶類型
1. **Episodic Memory**：具體事件和細節（"Alice takes the coffee"）
2. **Semantic Memory**：更高層級的通用知識（角色身份、屬性、關係、世界知識）
3. **Character Identity**：用外部工具做臉部辨識 + 說話人辨識 → 持久的 face_id、voice_id → 跨 clip 一致追蹤

### Control（多輪推理）
- 不是單輪 RAG，而是用 **RL（DAPO 演算法）** 訓練的多輪推理
- 每輪：policy model 生成推理 → 選擇 [Search] 或 [Answer]
- 如果 Search：查詢記憶 → 結果加入 context → 下一輪
- 如果 Answer：返回結果，結束

### Training
- **Memorization**：Qwen2.5-Omni fine-tuned via imitation learning（三階段 synthetic data）
- **Control**：Qwen3 trained with DAPO（Direct Advantage Policy Optimization）
- RL reward：GPT-4o 自動評分（binary correct/incorrect）

## M3-Bench（新 benchmark）

### M3-Bench-robot
- 100 支真實世界 robot 視角影片（平均 ~34 分鐘）
- 人類演員在家庭/辦公場景模擬 robot 互動

### M3-Bench-web
- 920 支 YouTube 長影片（平均 ~27 分鐘）
- 複雜敘事和 entity 關係

### 五種問題類型
1. Multi-evidence Reasoning
2. Multi-hop Reasoning
3. Cross-modal Reasoning
4. Person Understanding
5. General Knowledge Extraction

## Key Results

- **M3-Bench-robot**：30.7% 準確率，比最強 baseline (MA-LMM) 高 6.3%
- **M3-Bench-web**：48.9%，比 Gemini-GPT4o-Hybrid 高 7.7%
- **VideoMME-long**：61.8%，比 Gemini-GPT4o-Hybrid 高 5.3%

### Ablation Studies 重要發現
- 移除 semantic memory → 最大的準確率下降（robot -17.1%, web -19.2%）
- 移除 character identity equivalence → robot -11.2%
- RL training vs prompt-based → +10.0% / +8.0% / +9.3%
- 移除 inter-turn instructions → -5.8% ~ -10.5%
- 移除 reasoning mode → -8.8% ~ -11.7%

### Hard Cases（待解決）
- Fine-grained details：需要精確提取微小細節
- Spatial reasoning：需要理解空間佈局和時間變化

## Significance

- 首個完整的 entity-centric 多模態長期記憶框架
- 證明 semantic memory 對多模態 agent 至關重要（ablation -17~19%）
- 證明 RL 訓練的多輪推理顯著優於 prompt-based 方法
- M3-Bench 填補了長影片 QA benchmark 在高層認知能力評估的空白
- 開源（model、code、data）
