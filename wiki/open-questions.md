---
aliases: [open questions, 未解問題, open problems]
first_seen: 2026-04-14
last_updated: 2026-04-17
tags: [memory, architecture]
---

# Open Questions

研究中遇到的未解決問題和核心張力。按重要性排序。

## Tier 1: Fundamental — 可能無法完全解決

### 1. Raw vs Derived：所有記憶系統的根本 trade-off

> "There are no solutions. There are only trade-offs." — Thomas Sowell

所有記憶系統都在 raw（lossless but inert）和 derived（compact but lossy）之間選位置。兩端都不行。Raw 沒有組織、連結、優先級。Derived 會 drift — photocopy of a photocopy。

**為什麼可能無解**：完美保存和完美解釋是矛盾的。壓縮必然有損，但不壓縮就淹沒在資料中。

**現有策略**：GBrain 的 [[compiled-truth-pattern]]（rewrite compiled + append-only timeline）是目前最好的妥協 — raw 和 derived 共存，但需要有東西觸發 rewrite。

Sources: [[chrysb]], [[memory-failure-modes]]

### 2. Evaluation Paradox：怎麼證明記憶系統有效？

驗證需要 ground truth，但真實長期對話的 ground truth 超過任何 context window，也超過人能標註的範圍。任何用來評估的 judge 都有跟被評估系統一樣的 limitation。

**為什麼可能無解**：評估者本身受限於它要評估的東西。synthetic data 在長度上失去 coherence，real data 無法 annotate。

**現有方向**：[[memory-arena]] 從 recall → agentic tasks 提升了層級。Pengfei Du 提出 four-layer metric stack。但都只是近似。

Sources: [[chrysb]], [[memory-evaluation]]

### 3. Compounding vs Forgetting：越記越聰明 vs 遺忘是 feature

[[compounding-memory]] 的核心假設：每次互動累積知識，agent 越用越好。但 [[autoreason]] 證明某些場景下，刻意切斷記憶（memory isolation）反而獲得更好結果 — 遺忘防止 authorship bias。

[[memory-staleness]] 也挑戰 compounding：naive append 最終導致 catastrophic failure。

**核心張力**：什麼時候該記、什麼時候該忘、什麼時候該假裝不知道？

**現有策略**：Mem0 selective pipeline（ADD/UPDATE/DELETE/NOOP）、AgeMem 用 RL 學、autoreason 直接切斷。沒有統一答案。

Sources: [[compounding-memory]], [[autoreason]], [[memory-staleness]], [[agemem]]

---

## Tier 2: Hard but Approachable — 有人在做但還沒做好

### 4. Memory Staleness Detection

高頻 retrieve 的記憶過時後變成 confidently wrong。三種機制：
- **外在事實改變**：使用者換公司
- **Derivation drift**：連鎖 summarization 累積誤差
- **Stale context dominance**：舊記憶擠掉新記憶

**Pengfei Du survey 排名**：10 大 open challenges 第 4（"learned selective forgetting"）。

**為什麼難**：寫入時不知道什麼會過時，刪除時不知道什麼還有用。Forgetting propagation 需要 provenance tracking。

Sources: [[memory-staleness]], [[chrysb]]

### 5. Forgetting Propagation

刪除 raw turns 不會刪除衍生的 summaries。Graph 中刪除 source 留下 orphaned facts。真正的 forgetting 需要 provenance tracking + cascade delete，或定期 re-derive（昂貴）。

Sources: [[chrysb]], [[graph-memory]], [[actor-aware-memory]]

### 6. Cross-Session Coherence

Agent 跨 session 保持一致行為和記憶。[[memory-arena]] 的核心測試目標。大多數系統在單 session 內表現尚可，跨 session 立刻退化。

Sources: [[memory-evaluation]], [[memory-arena]]

### 7. Causally Grounded Retrieval

超越語意相似性（semantic similarity），基於因果關係做 retrieval。「為什麼使用者提到 X」比「X 跟什麼語意相似」更有用。

**Pengfei Du survey 排名**：10 大 open challenges 第 2。

Sources: [[raw/pengfei-du-memory-survey-2026]]

### 8. When Retrieval Happens：三難困境

三種 retrieval timing 各有致命缺陷：
- **Always-injected**：pollutes context with irrelevant history
- **Hook-driven**：expensive，model "performs memory rather than has it"
- **Tool-driven**：model doesn't know what it doesn't know，often fails to fetch when it should

**我們的經驗**：openab-bot 用 hook-driven（UserPromptSubmit hook 注入提醒）+ tool-driven（brain-first lookup 規則）的混合。Hook 解決了 100% enforcement 但代價是每則訊息都注入。

Sources: [[chrysb]], [[brain-first-lookup]]

### 10. Multi-Agent Memory Consistency & Governance

多 agent 共享記憶時的一致性、存取控制、provenance tracking、conflict resolution。Yu et al. 2026 認為這是 multi-agent memory **最大的未解問題**。

**兩個面向**：
- **Consistency**：read-time conflict handling（stale versions）+ update-time visibility/ordering（concurrent writes）。比經典 DB 難因為 artifacts 是 heterogeneous 且 conflicts 是 semantic
- **Access Control**：Collaborative Memory 2025 用 dynamic bipartite graphs + two-tier memory（private/shared）提供了第一個完整實作，resource usage 降 61%

**Pengfei Du survey 排名**：10 大 open challenges 第 6。

**為什麼升級到 Tier 2**：有了 architecture framing（Yu et al.）和第一個實作（Collaborative Memory），問題不再是 "剛開始有人想"。但 consistency model 仍然沒有 principled solution。

Sources: [[multi-agent-memory]], [[memory-consistency]], [[collaborative-memory-system]], [[actor-aware-memory]], [[multi-scope-memory]]

---

## Tier 3: Emerging — 剛開始有人想

### 9. Filesystem vs Database

File interface 讓 agent 用熟悉的工具（grep、cat）存取記憶。Database 提供 structured query、ACID、scalability。

**目前沒有明確贏家**。GBrain 用 filesystem（14,700+ files），Mem0 用 database，兩者都 production-viable。

Sources: [[filesystem-vs-database]], [[leonie]]

### 11. Scaffolding When to Remove

模型變強時，之前的 scaffolding 從「有幫助」變「有害」。但怎麼判斷？

**Aaron Levie 的經驗**：Box Agent 的 data finding mitigations 在模型進步後降低品質。只有 benchmark 能告訴你。

**我們的經驗**：behavior_benchmark.py 可以量化測試每個 rule/hook 的效果，理論上可以偵測 redundant scaffolding。

Sources: [[scaffolding-lifecycle]], [[aaron-levie]]

### 12. Foundation Models for Memory Management

專門的記憶管理 foundation model — 不是用 general LLM 做 memory operations，而是訓練 dedicated model。

**Pengfei Du survey 排名**：10 大 open challenges 第 9。AgeMem 的 RL approach 是這個方向的早期嘗試。

Sources: [[raw/pengfei-du-memory-survey-2026]], [[agemem]]

### 13. Skill Granularity 與 Skill Conflicts

Skill-based self-improvement（[[self-improving-agent]]）面臨兩個問題：

- **Granularity**：什麼 size 的 skill 最好用？太細 → 組合爆炸；太粗 → 不可重用。SKILLFOUNDRY 用「operational contract」當粒度單位，但 contract 邊界本身要怎麼決定還沒解
- **Conflicts**：兩個 skill 都能解 task 怎麼辦？需要 [[mece-resolver]] 之類的 routing 機制，但 skill 之間的 dominance 關係怎麼學？

**為什麼還沒解**：skill ecosystem 還沒夠大到讓這個問題凸顯。但 [[skillfoundry]] 286 個 skills 已經開始遇到 redundancy（28.9% 被 merge/discard），規模再大會更嚴重。

Sources: [[self-improving-agent]], [[asg-si]], [[skillfoundry]], [[mece-resolver]]

### 14. Self-Improving Agent Governance

Deployed self-improving agents 的安全與審計問題：reward hacking、behavioral drift、改進無法獨立驗證。

**[[asg-si]] 的回答**：把 self-improvement 變成 verifiable artifacts（skill graph）的 promotion 過程，每個改進有 contract + replay log。但 verifier 自身的可靠性是 bottleneck — verifier 出錯就什麼都漏。

**還沒解的**：跨 organization 的 skill sharing 怎麼確保安全？若 SkillHub 上的 community-contributed skill 嵌入惡意行為，誰負責 audit？

Sources: [[asg-si]], [[ssgm]], [[memory-evaluation]]

---

## Research Gaps in This Wiki

我們自己的覆蓋缺口：

| Gap | 狀態 | 需要什麼 |
|---|---|---|
| Production cases 太少 | **已部分解決** — ChatGPT Memory + 4 coding agents | 還缺 enterprise 深度案例 |
| Multimodal memory | **已覆蓋** — [[multimodal-memory]] + [[mirix]] | MIRIX 六層記憶 + M3-Agent entity-centric graph |
| Neuroscience integration | **已覆蓋** — [[neuroscience-memory]] + [[synapse]] | Spreading activation, Ebbinghaus decay, reconsolidation, hippocampal replay |
| Privacy & compliance | 只在 mem0 提到 | 需要獨立頁面 |
| Cost-effectiveness | **已部分解決** — Helix 提供最具體的 memory ROI 數據（2,000× 加速、100% cost reduction） | 還缺 general memory 的 cost-effectiveness，Helix 只覆蓋 error recovery |

## Related

[[concept-map]] [[agent-memory]] [[memory-failure-modes]] [[memory-evaluation]]
