---
title: "Reconsolidation: 檢索即改寫"
date: 2026-04-15
topic: reconsolidation
sources:
  - "A-Mem: Agentic Memory (arxiv 2502.12110)"
  - "SSGM: Stability and Safety Governed Memory (arxiv 2603.11768)"
pages_created:
  - wiki/reconsolidation.md
  - wiki/a-mem.md
  - wiki/ssgm.md
pages_updated:
  - wiki/compiled-truth-pattern.md
  - wiki/memory-staleness.md
  - wiki/memory-failure-modes.md
  - wiki/neuroscience-memory.md
  - wiki/agent-memory.md
  - wiki/agemem.md
---

# Reconsolidation: 檢索即改寫

## 選題動機

neuroscience-memory 頁面在 reconsolidation 段落寫道：「目前大多數系統的 retrieval 是 read-only」「理想的做法：每次 retrieve 後都更新記憶的 metadata」。這是神經科學啟發中最具實作價值但覆蓋最淺的方向。我們的 compiled-truth-pattern 已經有 rewrite 機制，但那是 manual trigger — 真正的 reconsolidation 應該是 **自動的**。

## 發現

### A-Mem（arxiv 2502.12110）— Memory Evolution

Zettelkasten 啟發的記憶系統。核心突破是 **Memory Evolution**：新記憶加入時，自動找到 top-k nearest neighbors 並更新它們的 context/keywords/tags。

這是目前最直接的 reconsolidation 實現：
- 記憶不是 immutable object，而是 living document
- 新資訊不只是「被加入」，還會「改變既有記憶」
- LoCoMo Multi-hop +144%（18.09 → 44.27），驗證 memory evolution 的價值

差異：A-Mem 是 **write-triggered**（新記憶觸發舊記憶更新），神經科學的 reconsolidation 是 **read-triggered**（檢索觸發重寫）。但效果類似 — 記憶是 mutable 的。

### SSGM（arxiv 2603.11768）— Governance for Evolving Memory

如果記憶可以被修改，怎麼防止失控？SSGM 提出 governance framework：

- **七種失敗模式**：semantic drift、procedural drift、goal drift、memory hallucination、temporal obsolescence、memory poisoning、privacy leakage
- **Write Validation Gate**：寫入前檢查是否與 core facts 衝突
- **Dual Storage**：Mutable Active Graph + Immutable Episodic Log
- **理論保證**：每 N 步 reconciliation → drift bounded to O(N·ε_step)

SSGM 的 dual storage 與 compiled-truth-pattern 高度呼應：
- Mutable Active Graph ≈ compiled truth（可改寫）
- Immutable Episodic Log ≈ timeline（append-only）

## 對 wiki 的影響

1. **新概念 reconsolidation.md**：從 neuroscience-memory 的一個段落升級為獨立頁面，因為它連接了太多東西
2. **compiled-truth-pattern 擴展**：加入 A-Mem 的 automatic evolution 和 SSGM 的 governance
3. **memory-failure-modes 擴展**：SSGM 的七種失敗模式補充了 Chrys Bader 的十種
4. **memory-staleness 擴展**：SSGM 的 Weibull decay 和 temporal obsolescence

## 對 openab-bot 的啟示

我們的 auto-memory 是 **完全 read-only retrieval** — 讀記憶不會修改記憶。最接近 reconsolidation 的是 `memory improve`（sleep-time compute），但那是 batch 的，不是 retrieval-triggered 的。

可實作的方向：
- 每次 recall 記憶後，更新 access count / freshness metadata
- 新 feedback 記憶存入時，自動掃描相關舊記憶看是否需要更新
- 這比 sleep-time 的 batch improve 更即時，但也更複雜

## 研究缺口

- Read-triggered reconsolidation（每次 retrieve 都 reconsolidate）目前沒有系統實現 — A-Mem 是 write-triggered，是間接的
- SSGM 的理論框架還沒有大規模實驗驗證
- Reconsolidation 與 forgetting 的交互作用：reconsolidate 可能反而 reinforce 該被遺忘的記憶
