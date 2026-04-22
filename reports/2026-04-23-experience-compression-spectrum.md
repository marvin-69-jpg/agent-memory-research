---
date: 2026-04-23
topic: Experience Compression Spectrum
gap_type: research-gap
sources_found: 2
wiki_pages_updated: 3
wiki_pages_created: 1
---

# Daily Research: Experience Compression Spectrum

## 研究動機

從 `wiki gaps` 跑出 SINGLE-SOURCE 建議，但 APEX-MEM、ASG-SI 頁面已很詳盡。轉而直接搜尋 2026-04 最新的 arxiv，找到剛上架的統一框架論文（2604.15877），主題是把 agent memory 和 agent skill 視為同一問題的不同壓縮程度。這跟我們 wiki 長期以來分開研究記憶系統和技能系統的方式形成直接對話。

## 發現

### 主要論文：Experience Compression Spectrum（Zhang et al., 2026-04-17）

來源：arxiv 2604.15877（AWS GenAI Innovation Center + HSBC）

**核心主張**：memory extraction 和 skill discovery 是同一個問題在不同抽象層級的實例。兩個社群的交叉引用率低於 1%（出自對 22 篇論文 1,136 條引用的統計）。

四個壓縮層級：
- L1（Episodic Memory）：5–20× 壓縮，低可重用性
- L2（Procedural Skill）：50–500× 壓縮，高可重用性
- L3（Declarative Rule）：1000×+ 壓縮，最高可重用性
- L3 幾乎沒有系統能自動抽出（只有人工指定的規則）

**最重要的發現 — The Missing Diagonal**：

在 20+ 系統的 mapping 中，沒有任何系統能夠自適應地在層級之間移動知識。所有系統都固定在某個壓縮層級。沒有 L1→L2 的自動提升，也沒有 L3→L1 的自動降級。

論文明確提到 CLAUDE.md 是真實世界中手動維護 L3 規則的例子。

### 第二個來源：Externalization in LLM Agents（Zhou et al., 2026-04-11）

來源：arxiv 2604.08224（SJTU + CMU + OPPO 22 人合作）

從「什麼認知負擔被移出 weights」的角度看同一個趨勢：
- Memory：跨時間的 state externalization
- Skills：程序性知識的 externalization
- Protocols：互動結構的 externalization
- Harness：整合以上三者的 runtime

兩個框架收斂到同一個觀察：lifecycle management（versioning、staleness、deprecation）是最被忽視的部分。

## 與已有知識的連結

```bash
wiki match "experience compression spectrum memory skills rules harness lifecycle"
```

高度相關：
- [[thin-harness-fat-skills]]：已有「把技能移出 weights 到外部」的核心主張，現在有了更精確的框架定位（L2 compression）
- [[compiled-truth-pattern]]：存在於 L3 的手動策略，壓縮框架把它的位置明確了
- [[asg-si]]：我們已研究的 L2 governance system，現在能和 L1 系統（DeltaMem、MEM1）放在同一個框架比較
- [[harness-engineering]]、[[scaffolding-lifecycle]]：Externalization 框架的直接對應
- [[sleep-time-compute]]：`memory improve` 在原始框架裡是 L1 level 的整理，但論文的預測是只有推進到 L2/L3 才有真正的跨域效益

## Open Questions 推進

這次研究直接回答了 open-questions 裡「為什麼 memory 和 skill 研究領域不互相引用」的問題：因為概念框架不統一，大家沒意識到自己在解同一個問題。

更大的 open question 是：「missing diagonal」怎麼實作？何時應該把一條 feedback memory 自動提升成 SKILL.md 規則、再提升成 CLAUDE.md 規則？這個自動化是當前整個領域的空白。

## 下一步

1. 讀 ExpeL 論文（跨 L1+L2 的少數系統之一），看它怎麼觸發 promotion
2. 探索「如果 auto-memory 某個主題累積 N 條記憶，是否應該觸發 L2 synthesis」的機制
3. 看 SkillRL +68.5pp 的數據來源，確認 L2 > L1 的 transfer advantage 在什麼條件下成立
