---
date: 2026-04-17
topic: Self-Improving Agents via Skill Artifacts
gap_type: research-gap
sources_found: 2
wiki_pages_updated: 11
wiki_pages_created: 3
---

# Daily Research: Self-Improving Agents via Skill Artifacts

## 研究動機

延續昨天 [[meta-harness]] 的脈絡。Meta-Harness 用 coding agent 自動搜尋 harness code 改進，這跟 wiki 裡 [[experiential-memory]]、[[sleep-time-compute]]、[[compounding-memory]]、[[thin-harness-fat-skills]] 都有交叉，但目前沒有 page 專門處理「agent 從自己（或外部資源）學習，把學到的東西外化成可執行 artifact」這個 cross-cutting 主題。從 `wiki gaps` 看，這算 RESEARCH-GAP（沒有專門 page）。

## 發現

### 兩個關鍵 paper

**1. ASG-SI（Audited Skill-Graph Self-Improvement）— Ken Huang & Jerry Huang, Dec 2025**（arxiv 2512.23760）

把 self-improvement 重新框定為「把 agent 編譯進一個成長中、可審計的 skill graph」的迭代過程。每個 candidate improvement 從成功軌跡抽取 → 標準化成有明確 interface 的 skill → 過 verifier-backed replay + contract check 才能 promote。Reward 拆解成可從 replayable evidence 重建的組件，讓 promotion 決定獨立可 audit。

最核心的論點：deployed self-improving agents 有三個 governance 問題（reward hacking、behavioral drift、opaque updates），這些**不是 RL/RLHF 能直接解決的，需要把改進外化成可驗證的 artifact**。

**2. SKILLFOUNDRY — CMU, Apr 2026**（arxiv 2604.03964）

Tree-guided closed-loop framework，從科學界既有的 heterogeneous resources（repos / APIs / scripts / notebooks / docs / papers）自動 mine 成 structured executable validated agent skills。Domain knowledge tree 同時當 search prior（找哪裡該挖）和 library state（看哪裡已覆蓋）。每個 candidate skill 過三階段 validation（execution / system / synthetic-data）才 promote。

實驗：286 skills, 27 domains，**71.1% novel** vs 既有 libraries。MoSciBench 上 Repo-Acc 從 61% 升到 67%，Paper-Acc 從 44% 升到 53%。Cell type annotation 上 vanilla Codex 81% coverage → +SKILLFOUNDRY 99%（接近 specialist agent SpatialAgent 的 100%）。

### 共同的 paradigm shift

兩篇從不同角度收斂到同一個觀點：**learning 應該外化成 verifiable artifacts，不是塞回 weights**。

| | RL fine-tuning | Skill-based self-improvement |
|---|---|---|
| 學到的東西在哪 | weights | skill graph / library |
| 可重用 | 綁這個 model | 可移植 |
| Audit | 黑盒 | contract + replay log |
| Reward hacking 防護 | 弱 | 強（verifier） |
| Rollback | 重訓 | prune skill |

ASG-SI 從 trajectories 抽 skill（agent 自己的經驗），SKILLFOUNDRY 從 external resources 挖 skill（人類已寫過的 procedural knowledge）。兩種來源**互補**，可以並存。

## 與已有知識的連結

`wiki match` 結果：thin-harness-fat-skills、procedural-memory、gbrain、meta-harness 是最近的鄰居。

具體連結：

- **[[thin-harness-fat-skills]]**（Garry Tan）：架構哲學上的同源 — intelligence in skills, not in harness/weights。GBrain 是 hand-crafted 版本的 skill library，[[skillfoundry]] 是自動 mine 版本
- **[[meta-harness]]**：差異在抽象層級。Meta-Harness 改的是 controller code（決定 when to use what skill），skill-based self-improvement 改的是 skill 本身。可以 stack — 用 Meta-Harness 搜尋 controller，controller 從 skill graph 取 skill
- **[[experiential-memory]]**（Viv Trivedy）：self-improvement 是 experiential memory 的 active 形式 — 不只是儲存經驗，還要從中提煉 reusable capabilities
- **[[compounding-memory]]**：skill-based self-improvement 是 compounding 的 endpoint
- **[[ssgm]]**：互補關係 — SSGM 處理 memory governance，[[asg-si]] 處理 skill governance。兩者都是 deployment-grade 的設計
- **[[procedural-memory]]**：skill library 是 procedural memory 的可執行形式

## Open Questions 推進

新增兩條 open questions：

- **#13 Skill Granularity 與 Skill Conflicts** — SKILLFOUNDRY 286 skills 已開始遇到 redundancy（28.9% 被 merge/discard）。規模放大會更嚴重。Skill 之間的 dominance 關係怎麼學還沒解
- **#14 Self-Improving Agent Governance** — ASG-SI 提供 verifier-backed 路徑，但 verifier 自身可靠性是 bottleneck。跨 org 的 skill sharing（community-contributed SkillHub 之類）的安全問題還沒解

部分回應 open question #11 Scaffolding When to Remove — Meta-Harness + ASG-SI + SKILLFOUNDRY 一起構成「自動發現 + 自動拆解 scaffolding」的可能路徑：用 SKILLFOUNDRY 從 resources 挖 skills，用 ASG-SI 驗證並 promote 到 graph，用 Meta-Harness 搜尋最佳 controller。每一層都有 verification + audit。

## 下一步

- 找 Voyager (Wang et al 2023) 補進 wiki — 兩篇都引到，是這條線的奠基論文
- 找 Anthropic Claude Skills 的官方 spec 補進 wiki — 兩篇都引到，是 production reference
- SkillHub / SkillSMP 是 SKILLFOUNDRY 比對 novelty 的對象，值得獨立查
- 應用到 openab-bot：目前 `~/.claude/skills/` 是 hand-crafted skills，可以實驗自動從 conversation traces 抽 skill 的 pipeline
