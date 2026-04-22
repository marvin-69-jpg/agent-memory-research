---
aliases: [Experience Compression Spectrum, ECS, compression spectrum, missing diagonal]
first_seen: 2026-04-23
last_updated: 2026-04-23
tags: [architecture, memory, harness, governance, skill]
---

# Experience Compression Spectrum

Zhang et al.（AWS GenAI + HSBC）2026-04-17 提出的統一框架（arxiv 2604.15877）。核心主張：**agent memory 和 agent skill 研究是同一個問題的兩個端點**，差別只是把 interaction experience 壓縮到哪個抽象層級。

## Current Understanding

### 四個壓縮層級

| Level | 名稱 | 存什麼 | 壓縮倍數 | 可重用性 |
|---|---|---|---|---|
| 0 | Raw Trace | 原始互動序列 T = {(st, at, ot, ft)} | 1:1 | 最低 |
| 1 | Episodic Memory | 「發生了什麼」— 結構化事件、key-value 摘要 | 5–20× | 低/中（綁定到特定 episode） |
| 2 | Procedural Skill | 「怎麼做」— 可重用行為模式、代碼、workflow | 50–500× | 高（跨類似場景） |
| 3 | Declarative Rule | 「什麼原則」— domain-invariant 策略、限制 | 1000×+ | 最高（跨域）|

### 壓縮層級的 Trade-off

越高壓縮：
- Generalizability ↑（越能跨場景重用）
- Specificity ↓（越少 context 細節）
- Acquisition cost ↑（需要更多 trace 才能抽出規則）
- Maintenance cost ↓（artifacts 更少、更穩定）

### 社群斷層的量化

對 22 篇一手論文的 1,136 條引用做分析：
- Memory 論文引用 Skill 社群：0.7%（4/566）
- Skill 論文引用 Memory 社群：1.2%（7/570）

兩個社群各自解決相同的子問題（retrieval、conflict detection、staleness），但幾乎零交叉。

### 現有系統的分佈

- **Level 1（10 個系統）**：Mem0、DeltaMem、Memory-R1、APEX-MEM、MEM1 等
- **Level 2（8 個系統）**：Voyager、SkillX、SKILLFOUNDRY、ASG-SI 等
- **Level 3（幾乎零）**：只有人工指定的規則（Constitutional AI、CLAUDE.md）
- **跨層的系統（2 個）**：ExpeL、AutoAgent（L1+L2，但固定層級，非自適應）

### The Missing Diagonal（最重要的發現）

**沒有任何系統**能夠：
1. 根據 context 自適應選擇壓縮層級
2. 當 pattern 出現後把知識往上**提升**（L1→L2→L3）
3. 當抽象層太粗時把知識往下**降級**（L3→L2→L1）

這個缺口（the "missing diagonal"）是整個領域的盲點。所有現有系統都固定在某個層級運作。

### 四個結構性發現

1. **專業化不夠**：兩個社群各自重解相同子問題
2. **評估方法是層級耦合的**：L1 用 QA metrics，L2 用 task success，L3 沒有建立的評估方法
3. **Transferability 隨壓縮程度上升**（SkillRL 比 L1 trajectory retrieval 在 ALFWorld 高 68.5pp）
4. **Lifecycle management 是事後補救**：大多數系統只關注 acquisition，不關注 versioning / deprecation / cross-level consistency

### 三個設計原則

1. **Level-agnostic compression core**：壓縮引擎應能對任意層級輸出
2. **Bidirectional promotion/demotion**：知識應能在層級之間流動
3. **Continuous lifecycle governance**：追蹤 provenance、confidence、deprecation

### 與 Externalization 框架的關係

同期 Zhou et al.（2604.08224，SJTU + CMU）提出「Externalization」框架，從另一個角度看同一個趨勢：把認知負擔從 weights 移到外部可持久化結構（Memory / Skills / Protocols / Harness）。

兩個框架互補：
- 壓縮框架：問「抽象到哪個層級」
- Externalization 框架：問「哪種認知負擔移出去」

都收斂到同一個觀察：lifecycle management 是最被忽視的問題。

## 對我們系統的含義

### 目前所在位置

| 我們的系統 | 壓縮層級 |
|---|---|
| auto-memory（`memory/` dir） | L1（Episodic Memory）|
| SKILL.md 文件 | L2（Procedural Skill）|
| CLAUDE.md | L3（Declarative Rule）— 但全部是手動維護 |

### Missing Diagonal 問題

我們的系統在每個層級都有 artifacts，但三層是**完全手動分離**的：
- 沒有機制把反覆出現的 L1 記憶自動提升為 L2 skill
- 沒有機制把成熟的 L2 pattern 提升為 L3 rule（CLAUDE.md 更新）
- 沒有機制在 L3 規則過時時降級回 L2 或 L1

這正是論文說的「missing diagonal」。

### 一個可能的起點

Paper 的預測：L2 compression 在跨域遷移上會優於 L1 retrieval（相同 source experience 下）。
對我們：auto-memory 存的都是 L1 feedback。如果某個 feedback 被多次複述，應該提升為 SKILL.md 規則（L2）或 CLAUDE.md 規則（L3）。目前這個提升是靠人工判斷。

## Key Sources

- **2026-04-17** — Zhang et al., Experience Compression Spectrum (arxiv 2604.15877, AWS GenAI)。Source: [[raw/zhang-experience-compression-spectrum]]
- **2026-04-11** — Zhou et al., Externalization in LLM Agents (arxiv 2604.08224, SJTU/CMU)。Source: [[raw/zhou-externalization-llm-agents]]

## Related

[[thin-harness-fat-skills]] [[compiled-truth-pattern]] [[harness-engineering]] [[asg-si]] [[skillx]] [[skillfoundry]] [[agent-memory]] [[procedural-memory]] [[experiential-memory]] [[ssgm]] [[scaffolding-lifecycle]] [[self-improving-agent]] [[meta-harness]] [[memory-worth]] [[sleep-time-compute]]
