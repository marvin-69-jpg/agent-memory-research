---
aliases: [concept map, 概念地圖, architecture overview]
first_seen: 2026-04-14
last_updated: 2026-04-18
tags: [architecture]
---

# Concept Map

本 wiki 70 個頁面的結構關係。三層架構 + 跨層主題 + 人物/產品索引。

## Layer 1: Infrastructure — Agent 怎麼運作

包裹 LLM 的執行框架、context 管理、整合點。

| Page | 一句話 |
|---|---|
| [[agent-harness]] | 包裹 LLM 的執行框架，2026 成獨立學科 |
| [[context-engineering]] | Harness 管理 context 的方式決定 memory 的一切 |
| [[context-fragment]] | Context window 中每個 loaded object 是設計決策 |
| [[harness-engineering]] | Agent integration points 工程（hooks、skills、MCPs） |
| [[meta-harness]] | Automated harness optimization（Stanford, 6x 性能差異） |
| [[scaffolding-lifecycle]] | 模型變強時 scaffolding 要拆 |
| [[context-rot]] | Resolver/routing 隨時間自然衰敗 |
| [[thin-harness-fat-skills]] | Harness 是薄殼，intelligence 在 skills |
| [[session-management]] | Every turn is a branching point：continue/rewind/clear/compact/subagent |
| [[self-improving-agent]] | Skill-based self-improvement vs weight-based：學習外化成 verifiable artifacts |

## Layer 2: Memory System — Agent 怎麼記

記憶的類型、結構、生命週期、管理策略。

### 2a. 記憶類型與結構

| Page | 一句話 |
|---|---|
| [[agent-memory]] | 核心頁面：三維分類法、write–manage–read loop |
| [[procedural-memory]] | 第三種記憶：how to do things |
| [[experiential-memory]] | 跨 instances 累積的經驗記憶 |
| [[multi-scope-memory]] | 四層 scope：user / agent / session / org |
| [[graph-memory]] | Knowledge graph 記憶，relationship-based |
| [[compiled-truth-pattern]] | Compiled truth（可改寫）+ timeline（append-only） |
| [[multimodal-memory]] | 非文字模態記憶：影像、音訊、影片、螢幕截圖 |
| [[neuroscience-memory]] | 認知神經科學 ↔ agent memory 對照 |
| [[reconsolidation]] | 檢索即改寫：retrieval 不應是 read-only |

### 2b. 記憶生命週期

| Page | 一句話 |
|---|---|
| [[brain-agent-loop]] | Signal→Detect→Read→Respond→Write→Sync 核心 loop |
| [[entity-detection]] | 每個 message 自動偵測 entity |
| [[enrichment-pipeline]] | 三層 tier 分配 API 資源 |
| [[sleep-time-compute]] | 閒置時的背景記憶處理（dream cycle） |
| [[compounding-memory]] | 記憶複合成長效應，越用越聰明 |
| [[memory-staleness]] | 高 relevance 但過時的記憶，open problem |
| [[memory-failure-modes]] | 10 種常見失敗模式 + raw vs derived 根本張力 |

### 2c. 記憶管理策略

| Page | 一句話 |
|---|---|
| [[brain-first-lookup]] | 永遠先查 brain，external API 是 fallback |
| [[mece-resolver]] | 每塊知識有唯一 primary home |
| [[context-constitution]] | Letta 的原則集，定義 agent 如何管理 context |
| [[multi-agent-memory]] | Multi-agent memory 核心頁：paradigm + hierarchy + protocols |
| [[memory-consistency]] | Multi-agent memory 一致性問題 |
| [[actor-aware-memory]] | Multi-agent 記憶來源追蹤 |
| [[filesystem-vs-database]] | File interface vs DB 辯論 |
| [[gene-map]] | Q-value RL 排序的修復策略知識庫（Helix 核心概念） |
| [[ssgm]] | 記憶進化的 governance framework，drift 理論保證 |

## Layer 3: Retrieval & Evaluation — Agent 怎麼找、怎麼驗

| Page | 一句話 |
|---|---|
| [[hybrid-search]] | Vector + keyword + RRF fusion |
| [[bitter-lesson-search]] | 資料超指數成長下的搜尋挑戰 |
| [[memory-evaluation]] | Evaluation paradox + benchmark 演進 |
| [[locomo]] | 第一個 long-term memory benchmark |
| [[memory-arena]] | Agentic memory benchmark，測跨 session 行動 |
| [[xmemory]] | Beyond RAG：四層階層 + adaptive retrieval，解 collapsed retrieval 問題 |
| [[stitch]] | Contextual intent tagging，解 context-mismatched retrieval + CAME-Bench |
| [[deltamem]] | Single-agent RL memory management，PersonaMem SOTA |
| [[empo2]] | Hybrid on/off-policy RL，memory 引導 exploration 再蒸餾進 weights，ICLR 2026 |

## Cross-cutting Themes — 跨層主題

| 主題 | 涉及頁面 | 核心張力 |
|---|---|---|
| **Lock-in vs Portability** | [[memory-lock-in]], [[filesystem-vs-database]] | 平台想鎖住 memory，使用者想帶走 |
| **Compounding vs Forgetting** | [[compounding-memory]], [[memory-staleness]], [[autoreason]] | 越記越聰明 vs 某些場景遺忘是 feature |
| **Raw vs Derived** | [[memory-failure-modes]], [[compiled-truth-pattern]] | Lossless but inert vs compact but lossy |
| **Recall vs Action** | [[locomo]], [[memory-arena]], [[memory-evaluation]] | 能記得 ≠ 能用記憶做正確決策 |
| **Isolation vs Accumulation** | [[actor-aware-memory]], [[autoreason]], [[experiential-memory]] | 切斷 context 防 bias vs 累積 context 增智 |
| **Scaffold vs Model** | [[scaffolding-lifecycle]], [[thin-harness-fat-skills]], [[harness-engineering]] | 模型變強時什麼該留、什麼該拆 |
| **Skill vs Weight Learning** | [[self-improving-agent]], [[asg-si]], [[skillfoundry]], [[meta-harness]] | 學到的東西塞 weights 還是外化成 verifiable artifacts |

## Products & Systems

| Page | 類型 |
|---|---|
| [[gbrain]] | Garry Tan 個人知識庫，14,700+ files |
| [[letta]] | Stateful agent 先驅（前 MemGPT） |
| [[memgpt]] | 2023 開創性論文，OS virtual memory 類比 |
| [[mem0]] | Agent memory 基礎設施，ECAI 2025 |
| [[deep-agents]] | LangChain 開源 agent harness |
| [[agemem]] | RL 訓練 agent 自己學 memory management |
| [[chatgpt-memory]] | ChatGPT 四層靜態注入，no RAG |
| [[coding-agent-memory]] | Cursor/Claude Code/Windsurf/Cline 比較 |
| [[autoreason]] | A/B/AB tournament self-refinement |
| [[helix]] | Self-healing runtime，Gene Map 用 Q-value RL |
| [[mirix]] | 六種記憶 + Active Retrieval + 多模態原生支持 |
| [[synapse]] | Spreading activation 記憶檢索，LoCoMo SOTA |
| [[collaborative-memory-system]] | Multi-user memory sharing + dynamic access control |
| [[a-mem]] | Zettelkasten-inspired memory evolution |
| [[ssgm]] | 記憶進化 governance，drift 理論保證 |
| [[d-mem]] | Dopamine-gated memory routing，解 A-Mem 的 O(N²) 寫入瓶頸 |
| [[fluxmem]] | Adaptive memory structures：linear/graph/hierarchical 動態選擇 |
| [[memory-worth]] | Two-counter outcome-feedback metric，read-time / outcome-time governance gate |
| [[asg-si]] | Audited Skill-Graph Self-Improvement：governance-aware skill graph |
| [[skillfoundry]] | CMU 自動 mine heterogeneous resources 成 skill library |
| [[memwright]] | Zero-LLM-in-retrieval，5-layer deterministic pipeline，RBAC + provenance |
| [[mstar]] | Memory = executable program，population-based evolution 自動發現 task-optimal memory |
| [[gam]] | 雙層圖（EPG+TAN），encoding/consolidation 解耦，sleep-dependent consolidation 靈感 |
| [[memu]] | Filesystem-based markdown memory，三層架構，LoCoMo 92.09%，24/7 proactive agents |

## People

| Page | 身份 | 核心貢獻 |
|---|---|---|
| [[harrison-chase]] | LangChain CEO | "your harness, your memory" |
| [[sarah-wooders]] | Letta CTO | "memory isn't a plugin" |
| [[garry-tan]] | YC CEO | GBrain, thin harness fat skills |
| [[viv-trivedy]] | 研究者 | Context Fragment, Bitter Lesson |
| [[chrysb]] | Practitioner | 9 軸設計, 10 failure modes |
| [[yohei-nakajima]] | BabyAGI 創造者 | AI Memory 全景分析 |
| [[philipp-schmid]] | HuggingFace | "2026 = Agent Harnesses" |
| [[aaron-levie]] | Box CEO | Scaffolding lifecycle |
| [[shl0ms]] | Autoreason 作者 | Memory isolation by design |
| [[nicholas-dapanji]] | Helix 共同創作者 | Gene Map, self-healing agents |
| [[leonie]] | ML 技術作者 | Filesystem vs database 辯論 |

## Related

[[agent-memory]] [[agent-harness]] [[open-questions]]
