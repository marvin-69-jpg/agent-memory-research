# SYNAPSE: Empowering LLM Agents with Episodic-Semantic Memory via Spreading Activation

- **Authors**: Hanqi Jiang, Junhao Chen, Yi Pan +8 (University of Georgia + UT Knoxville + CU Boulder + NJIT)
- **Date**: 2026-01-06
- **Source**: https://arxiv.org/abs/2601.02744
- **Type**: arxiv paper

## Summary

SYNAPSE 是一個受認知科學啟發的記憶架構，用 spreading activation（擴散激活）取代靜態 vector similarity 做記憶檢索。核心是統一的 episodic-semantic graph + 認知動力學。

## Core Architecture

### Unified Episodic-Semantic Graph

有向圖 G = (V, E)，兩種節點：
- **Episodic Nodes**：每個互動 turn 一個，含文字內容、embedding、timestamp
- **Semantic Nodes**：每 5 turns 用 LLM 抽取的抽象概念（entity、preference、event）

三種邊：
- **Temporal Edges**：連接時序上相鄰的 episodic nodes
- **Abstraction Edges**：雙向連接 episodic ↔ semantic（基於 co-occurrence）
- **Association Edges**：semantic 之間的潛在相關性

### Spreading Activation（認知動力學）

受 Collins & Loftus (1975) 和 ACT-R 啟發：

1. **Initialization**：收到 query → 用 BM25 + dense retrieval 找 anchor nodes → 注入初始 activation energy
2. **Propagation with Fan Effect**：activation 沿邊傳播，被出度 dilute（fan effect, Anderson 1983）
   - Temporal edges 有 exponential time decay（ρ=0.01）
   - Semantic edges 用 cosine similarity 加權
3. **Lateral Inhibition**：高度激活的概念抑制競爭者（模擬注意力選擇）
4. **Sigmoid Activation**：非線性轉換，3 輪迭代收斂

### Triple-Signal Hybrid Retrieval

融合三個信號做最終排序：
- Semantic similarity（cosine）
- Activation score（spreading activation 結果）
- PageRank（全局結構先驗）

### Uncertainty-Aware Rejection（防幻覺）

- Confidence gating：top-ranked node 的 activation energy < threshold → 拒絕回答
- 明確驗證 prompt：強制 LLM 輸出 "Not mentioned" 如果資訊不存在

## Key Results（LoCoMo benchmark）

| Metric | SYNAPSE | Best baseline |
|---|---|---|
| Overall F1 | **40.5** | A-Mem 33.3 (+7.2) |
| Temporal reasoning | **50.1** | A-Mem 45.9 |
| Multi-hop reasoning | **35.7** | A-Mem 27.0 (+8.7) |
| Adversarial robustness | **96.6** | LoCoMo 69.2 |
| Token per query | **814** | Full-context 16,910 (**95% reduction**) |
| Cost per 1K queries | **$0.24** | Full-context $2.64 (**11x cheaper**) |

### Ablation 關鍵發現

- 移除 lateral inhibition → adversarial robustness 大幅下降
- 移除 fan effect → multi-hop 和 open-domain 下降（hub 壟斷 activation）
- 移除 node decay → temporal F1 從 50.1 → 14.2（無法區分新舊事實）
- 只用 vector → 整體退化，確認 spreading activation 的必要性

### 效率

- 95% token 減少
- 11x 成本減少
- 4x 延遲減少
- 弱 backbone 模型的增益更大（結構化 activation 補償推理能力不足）

## Neuroscience Concepts Used

| Concept | Source | 在 SYNAPSE 中的實作 |
|---|---|---|
| Spreading Activation | Collins & Loftus 1975 | 記憶檢索 = 圖上的 energy propagation |
| Fan Effect | Anderson 1983 | 出度越大 activation 越 dilute |
| Lateral Inhibition | 神經科學 | 高激活節點抑制低激活競爭者 |
| Temporal Decay | Ebbinghaus 遺忘曲線 | temporal edges 的 exponential decay |
| Pattern Completion | 海馬體 | 從部分 cue 恢復完整記憶 |

## Limitations

- Cold start：對話初期圖太稀疏
- Cognitive tunneling：lateral inhibition 可能過度抑制弱連結
- 目前只支援文字，未來要擴展到多模態
- Graph topology 品質依賴 LLM 的 entity extraction 能力
