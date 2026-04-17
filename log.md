# Agent Memory Research — Log

> Append-only record of all wiki operations.

## [2026-04-17] ingest | xMemory — Beyond RAG for Agent Memory

- Source: Hu et al., arxiv 2602.02007v3 (2026-02-02, revised 2026-04-11)
- Raw: `raw/hu-xmemory-beyond-rag.md`
- Wiki: created `wiki/xmemory.md`
- Updated: concept-map, index, agent-memory, a-mem, memwright, gam, memu, locomo, memory-evaluation, hybrid-search, enrichment-pipeline (backlinks)
- Key insight: agent memory ≠ general RAG, top-k similarity collapses on coherent dialogue streams, need hierarchy + adaptive expansion

## [2026-04-17] ingest | Markdown Memory Convergence

- Source: X/Twitter (OpenClaw @TheTuringPost, ByteRover @kevinnguyendn, Shannon Sands @max_paperclips)
- Raw: `raw/markdown-memory-convergence.md`
- Wiki: updated `wiki/filesystem-vs-database.md` with 2026 convergence evidence
- Key insight: multiple independent systems converging on markdown-as-source-of-truth + retrieval-as-layer

## [2026-04-17] ingest | MemU — filesystem-based markdown memory

- Source: Sumanth (@Sumanth_077) X thread, 2026-01-05, 73.8K views. GitHub: NevaMind-AI/memU
- Created: wiki/memu.md
- Updated: filesystem-vs-database, compiled-truth-pattern, enrichment-pipeline, multimodal-memory, mirix, memwright, coding-agent-memory, locomo, mem0, agent-memory, concept-map, index.md
- Key insight: filesystem + markdown 路線的 LoCoMo 92.09% 驗證。三層（Resource→Item→Category）= compiled truth pattern 的實作。Dual retrieval（RAG + LLM）提供速度/深度選擇

## [2026-04-17] research | GAM — hierarchical graph-based agentic memory

- Source: Wu et al., GAM: Hierarchical Graph-based Agentic Memory, arxiv 2604.12285, 2026-04-14
- Created: wiki/gam.md
- Updated: graph-memory, a-mem, d-mem, sleep-time-compute, neuroscience-memory, compiled-truth-pattern, reconsolidation, mem0, mstar, locomo, memory-evaluation, agent-memory, concept-map, index.md
- Key insight: encoding/consolidation 解耦 — EPG 暫存 + semantic boundary 觸發 consolidation 到 TAN。LoCoMo F1 40.00 > Mem0 35.38 > A-Mem 24.20。EPG 是最重要組件（ablation -14.94）

## [2026-04-17] research | M★ — task-specific memory harness evolution

- Source: Pan et al., M★: Every Task Deserves Its Own Memory Harness, arxiv 2604.11811, 2026-04-10
- Created: wiki/mstar.md
- Updated: fluxmem, meta-harness, self-improving-agent, asg-si, locomo, mem0, memwright, memory-evaluation, agent-memory, concept-map, index.md
- Key insight: memory architecture 是 search problem 不是 design problem。Population-based evolution 讓系統自己發現 task-optimal memory structure，不同 domain 進化出完全不同的架構。7/8 benchmarks SOTA

## [2026-04-17] ingest | Memwright — zero-LLM deterministic memory

- Source: aarjay singh, "Why I stopped putting LLMs in my agent memory retrieval path", dev.to, 2026-04-15
- Created: wiki/memwright.md
- Updated: hybrid-search, actor-aware-memory, collaborative-memory-system, compiled-truth-pattern, memory-evaluation, locomo, a-mem, mem0, agent-memory, concept-map, index.md
- Key insight: 5-layer deterministic retrieval pipeline (FTS → Graph BFS → Vector → RRF Fusion → MMR Diversity), zero LLM in critical path, RBAC + provenance + temporal supersede。LOCOMO v2 81.2%

## [2026-04-17] research | Self-Improving Agents via Skill Artifacts

- Gap type: research-gap（沒有專門 page 處理「skill-based self-improvement」這個 cross-cutting 主題）
- Sources: 2 篇 paper
  - ASG-SI: arxiv 2512.23760（Ken Huang & Jerry Huang, 2025-12-28）
  - SKILLFOUNDRY: arxiv 2604.03964（CMU, 2026-04-05）
- New raws: raw/huang-asg-si-audited-skill-graph.md, raw/cmu-skillfoundry-self-evolving-skill-libraries.md
- New wiki pages: wiki/self-improving-agent.md, wiki/asg-si.md, wiki/skillfoundry.md
- Updated: wiki/thin-harness-fat-skills, procedural-memory, gbrain, meta-harness, experiential-memory, compounding-memory, sleep-time-compute, ssgm, bitter-lesson-search, memory-evaluation, context-rot, mece-resolver, memory-staleness — bidirectional cross-links
- Updated: wiki/concept-map.md（新增 self-improving-agent / asg-si / skillfoundry / session-management，新主題 "Skill vs Weight Learning"）
- Updated: wiki/open-questions.md（新增 #13 Skill Granularity, #14 Self-Improving Agent Governance）
- Updated: index.md
- Report: reports/2026-04-17-self-improving-agents.md
- Threads: reports/threads/2026-04-17-daily.md（3 segments, 921 chars total）
- Insights: 兩篇從不同角度（從 trajectories vs 從 external resources）收斂到同一個 paradigm — learning 應該外化成 verifiable artifacts，不是塞回 weights。直接連到 [[meta-harness]]（昨天 ingested）的同一精神：把改進變成 inspectable code 不是 weight delta。三篇一起構成「自動發現 + 自動 promote + 自動 controller search」的完整 stack

## [2026-04-16] update | Meta-Harness — 操作層補充（GitHub repo README）

- Source: https://github.com/stanford-iris-lab/meta-harness (主 repo README)
- Updated: wiki/meta-harness.md — 新增「應用到新 domain」段落，涵蓋 ONBOARDING.md flow + reference_examples 結構 + claude_wrapper.py 替換點 + framework/artifact 雙 repo 策略
- Murmur: reports/threads/2026-04-16-murmur-meta-harness-onboarding.md
- Insights: 既有 page 主要是 paper 概念層，repo README 補了「實踐者怎麼套用」的操作層。最有意思的觀察是 Stanford IRIS 預設應用流程本身就是 agent task（指 coding assistant 讀 ONBOARDING.md 產 domain_spec.md），不是人類照 checklist 走 — 與 [[meta-harness]] 把 harness optimization 自動化的核心精神一致

## [2026-04-16] ingest | Thariq (Claude Code) — Session Management & 1M Context

- Source: https://x.com/trq212/status/2044548257058328723 (343.2K views)
- Raw: raw/thariq-claude-code-session-management.md
- New wiki page: wiki/session-management.md
  - Every Turn Is a Branching Point 五選一模型
  - Rewind > Correct 原則
  - Compact vs Clear tradeoff
  - Bad Compact 機制（context rot × unpredictable next query）
  - Subagent as context management tool
- Updated: wiki/context-rot.md — 新增 "Compaction Timing" section（context rot 決定壓縮品質）
- Updated: wiki/context-engineering.md — 加 Branching Point model
- Updated: wiki/memory-failure-modes.md — 加 Bad Compact 機制
- Cross-links: session-management ↔ context-rot ↔ context-engineering ↔ memory-failure-modes ↔ reconsolidation ↔ meta-harness
- 關鍵洞察：context rot 不只在 resolver 層，也在 compaction timing — model 在最弱的時候被要求做最關鍵的壓縮決定
- Author context: Thariq 是 Anthropic Claude Code team 成員，有 insider authority

## [2026-04-16] impl | Memory Benchmark — trigger evals + reconsolidation + lint

- Pattern: Trigger Evals (from Garry Tan's resolver testing) + Meta-Harness verification
- Created: tools/benchmark.py
- 3 test suites:
  - Recall Accuracy (16 test cases): query → 預期 top-5 結果包含目標 files
  - Reconsolidation Signals (62 checks): feedback 有 Why/How、project 不 stale、content 不 thin
  - Lint Health (99 checks): frontmatter valid、MEMORY.md index sync、no dangling pointers
- Baseline: 177/177 (100%)
- Inspired by: Garry Tan trigger evals, Meta-Harness verification, MemoryArena

## [2026-04-16] impl | Reconsolidation — retrieval-triggered memory update

- Pattern: Reconsolidation (from A-Mem + SSGM + neuroscience research)
- Changes:
  - `tools/memory.py`: 新增 `reconsolidate` subcommand — 對 recalled memories 做 staleness 檢查
  - `CLAUDE.md`: Brain-First Lookup 規則新增 reconsolidation 步驟
  - `wiki/reconsolidation.md`: 新增 Implementation section
- Signals checked: age staleness, description-body drift, thin content, missing Why/How
- Safety: 受 SSGM 啟發，不改核心事實，只改可能過時的描述
- This is the first research→implementation cycle for reconsolidation

## [2026-04-16] ingest | Stanford IRIS Lab — Meta-Harness

- Source: https://github.com/stanford-iris-lab/meta-harness + arxiv 2603.28052
- Raw: raw/stanford-meta-harness.md
- Created: meta-harness.md
- Updated: harness-engineering.md, scaffolding-lifecycle.md, context-rot.md, concept-map.md, index.md
- Key insights:
  - Automated harness optimization — 同一模型 6x 性能差異來自 harness
  - Full execution traces（10M tokens）比 lossy summary 好 15+ 點
  - TerminalBench-2: 76.4% pass 超越手工 harness（#2 leaderboard）
  - Proposer 自動學會從 aggressive rewrites → additive modifications
  - Chelsea Finn + Omar Khattab（DSPy）— 從 prompt optimization 到 harness optimization
- Wiki: 65 → 66 pages

## [2026-04-16] ingest | Garry Tan — Resolvers: The Routing Table for Intelligence

- Source: https://x.com/garrytan/status/2044479509874020852 (46.1K views)
- Raw: raw/garry-tan-resolvers-routing-table.md
- Created: context-rot.md
- Updated: mece-resolver.md (大幅擴充 — trigger evals, check-resolvable, fractal resolvers, resolver as management), garry-tan.md, gbrain.md, thin-harness-fat-skills.md, scaffolding-lifecycle.md, concept-map.md, index.md
- Key insights:
  - Resolver = context routing table（20K→200 行 CLAUDE.md）
  - Audit: 13 skills 只有 3 個查 resolver，check-resolvable 找到 15% dark skills
  - Context rot: resolver 在 90 天內自然衰敗 — memory-staleness 在 infrastructure 層的對應物
  - Self-healing resolver（RLM loop）是 agent governance 的 endgame
  - GStack: 72K+ stars coding layer，與 GBrain 組成完整架構
- Wiki: 64 → 65 pages

## [2026-04-16] research | Multi-Agent Memory

- Topic: Multi-Agent Memory — multi-agent tag 嚴重不足（1 page vs avg 13），直接影響 openab-bot 架構
- Sources: 2 papers
  - raw/yu-multi-agent-memory-architecture.md (Yu et al. 2026, arxiv 2603.10062, position paper)
  - raw/rezazadeh-collaborative-memory.md (Rezazadeh et al. 2025, arxiv 2505.18279, Accenture)
- Created: multi-agent-memory.md, memory-consistency.md, collaborative-memory-system.md
- Updated: actor-aware-memory.md, open-questions.md (promoted #10 from Tier 3 → Tier 2), concept-map.md, index.md
- Report: reports/2026-04-16-multi-agent-memory.md
- Key findings:
  - Yu et al. 框定 multi-agent memory 為電腦架構問題：shared vs distributed paradigm + 三層 hierarchy（I/O/cache/memory）
  - 兩個缺失 protocol：cache sharing + memory access control
  - Memory consistency 是最大未解問題（read-time conflict + update-time visibility）
  - Collaborative Memory 是第一個帶動態 access control 的完整實作，resource usage 降 61%
  - openab-bot 目前是 shared memory + last-write-wins 弱 consistency
- Insights: actor-aware memory 是 consistency 的子集；filesystem shared memory 天然缺 access control
- Wiki: 61 → 64 pages

## [2026-04-15] research | Reconsolidation: 檢索即改寫

- Topic: Reconsolidation — 神經科學啟發，retrieval 不應是 read-only（自選主題）
- Sources: 2 arxiv papers
  - raw/a-mem-agentic-memory.md (A-Mem, arxiv 2502.12110)
  - raw/ssgm-stability-safety-governed-memory.md (SSGM, arxiv 2603.11768)
- Created: reconsolidation.md, a-mem.md, ssgm.md
- Updated: compiled-truth-pattern.md, memory-staleness.md, memory-failure-modes.md, neuroscience-memory.md, agent-memory.md, agemem.md, concept-map.md, open-questions.md, index.md, README.md
- Report: reports/2026-04-15-reconsolidation.md
- Key findings:
  - A-Mem Memory Evolution = write-triggered reconsolidation（新記憶自動更新舊記憶的 context/tags）
  - SSGM = reconsolidation 的 safety wrapper（Write Validation Gate + Dual Storage + drift bound）
  - SSGM Dual Storage 與 compiled-truth-pattern 高度呼應（Mutable Active Graph ≈ compiled truth）
  - SSGM 識別了 reconsolidation 特有的三種 drift：semantic/procedural/goal
  - Read-triggered reconsolidation（每次 retrieve 都 reconsolidate）目前仍無系統實現
- Wiki: 58 → 61 pages

## [2026-04-15] research | Neuroscience Integration

- Topic: Neuroscience integration (RESEARCH-GAP — 完全沒覆蓋，最後一個)
- Sources: 2 arxiv papers
  - raw/ai-meets-brain-memory-survey.md (AI Meets Brain, arxiv 2512.23343)
  - raw/synapse-spreading-activation-memory.md (SYNAPSE, arxiv 2601.02744)
- Created: neuroscience-memory.md, synapse.md
- Updated: agent-memory.md, graph-memory.md, memory-staleness.md, memory-evaluation.md, + 8 backlink pages, open-questions.md, concept-map.md, index.md
- Report: reports/2026-04-15-neuroscience-integration.md
- Key findings:
  - Hippocampal replay = sleep-time compute 的生物學基礎
  - Spreading activation（SYNAPSE）是 causally grounded retrieval 的第一個具體解法
  - Ebbinghaus decay ablation：移除 temporal decay → F1 50.1→14.2
  - Reconsolidation 啟示：retrieval 不應是 read-only
  - 推進 open questions #3, #4, #7 + Privacy gap
- Insights: neuroscience 不只是 metaphor，SYNAPSE 證明精確實作認知機制能獲得 SOTA + 11x cost reduction
- **所有 RESEARCH-GAP 已清零** — multimodal memory 和 neuroscience integration 都已覆蓋

## [2026-04-15] research | Multimodal Memory

- Topic: Multimodal memory (RESEARCH-GAP — 完全沒覆蓋)
- Sources: 2 arxiv papers
  - raw/mirix-multiagent-memory-system.md (MIRIX, arxiv 2507.07957)
  - raw/m3-agent-multimodal-long-term-memory.md (M3-Agent, arxiv 2508.09736)
- Created: multimodal-memory.md, mirix.md
- Updated: agent-memory.md, graph-memory.md, memory-evaluation.md, agemem.md, actor-aware-memory.md, open-questions.md, concept-map.md, index.md
- Report: reports/2026-04-15-multimodal-memory.md
- Key findings:
  - MIRIX 六種記憶擴展傳統三分法，Active Retrieval 是 retrieval timing 的第四種策略
  - M3-Agent entity-centric multimodal graph + RL 控制，semantic memory 最關鍵（ablation -17~19%）
  - 多模態場景讓 raw vs derived 張力更尖銳：99.9% 儲存壓縮 + 35% 準確率提升
  - 推進 open questions #1, #8, #10, #12
- Insights: 多模態記憶不是「文字記憶 + 圖片」，而是需要根本不同的架構（entity-centric binding、多 agent 管理、抽取式壓縮）

## [2026-04-15] ingest | Garry Tan — GBrain v0.10.0

- Source: raw/garry-tan-gbrain-v0.10.0.md (tweet, 16.8K views)
- Updated: gbrain.md (v0.10.0 details, multi-user ACLs), thin-harness-fat-skills.md (24 skills 實證, multi-user), garry-tan.md (v0.10.0 update)
- Key findings:
  - 24 fat skills with full e2e/eval/unit test coverage — fat skill 架構已穩定收斂
  - RESOLVER.md + SOUL.md "perfected" — resolver routing 機制成熟
  - Multi-user brain access via ACLs — brain 從個人工具擴展到團隊共用
  - 個人 OpenClaw setup 公開 — 降低其他人的 adoption barrier

## [2026-04-15] ingest | Nicholas — AI Agents Have No Memory for Failure (Helix)

- Source: raw/nicholas-helix-self-healing-agents.md (159K views, X long-form article)
- Created: helix.md, gene-map.md, nicholas-dapanji.md
- Updated: procedural-memory.md (Gene Map as error-specific procedural memory), experiential-memory.md (shared Gene Map = cross-agent experiential sharing), compounding-memory.md (Q-value RL compounding), memory-evaluation.md (Helix benchmark data)
- New cross-links: helix ↔ gene-map ↔ procedural-memory ↔ experiential-memory ↔ compounding-memory ↔ memory-evaluation
- Key findings:
  - Gene Map = procedural memory + RL ranking，首次 2,140ms → 再次 1.1ms（2,000×）
  - 目前看到最具體的 memory ROI 數據（50 場景，量化 LLM call / cost / latency）
  - Shared Gene Map 願景 = experiential memory 跨 agent 共享的工程實踐
  - Doctor vs Immune System 類比：routine failures 用 pattern match，novel failures 才用 LLM

## [2026-04-14] ingest | Phase 3 — 產業視角（ChatGPT Memory + Coding Agents）

- Source: raw/manthan-gupta-chatgpt-memory-reverse-engineered.md (ChatGPT 四層靜態注入逆向工程)
- Source: raw/coding-agents-memory-comparison.md (Cursor/Claude Code/Windsurf/Cline 架構比較，多來源綜合)
- Created: chatgpt-memory.md, coding-agent-memory.md
- Key findings:
  - ChatGPT 不用 RAG/vector DB，是 4 層靜態注入（speed over completeness）
  - 4 個 coding agent 全收斂在 file-based memory（驗證 filesystem camp）
  - 分歧在 who curates（user vs system）和 when retrieval（always vs on-demand vs auto-learned）
  - Enterprise: 62% 實驗 agents，只有 14% production-ready（McKinsey）
- Open questions research gap "Production cases 太少" → 已部分解決

## [2026-04-14] structure | Phase 2 — 概念地圖 + Open Questions

- Created: concept-map.md（三層架構：Infrastructure → Memory System → Retrieval & Evaluation，6 個跨層主題，7 products，10 people）
- Created: open-questions.md（12 個未解問題分三個 tier：Fundamental / Hard but Approachable / Emerging，加研究缺口表）
- Updated: index.md（加 Structure section 置頂）

## [2026-04-14] ingest | Phase 1 深化 — 3 篇高價值來源

Phase 1 計劃：補學術深度，降低 single-source pages。三個來源同時搜尋 + 讀取 + ingest：

- Source: raw/chrysb-long-term-memory-unsolved.md (262.1K views, 9 軸設計 + 10 failure modes)
- Source: raw/pengfei-du-memory-survey-2026.md (arxiv 2603.07670, 系統性 survey)
- Source: raw/yohei-nakajima-rise-of-ai-memory.md (24.6K views, 全景分析)
- Created: memory-failure-modes.md, memory-evaluation.md, chrysb.md, yohei-nakajima.md
- Updated: agent-memory.md (write-manage-read loop, 三維分類法, raw vs derived, evaluation paradox), memory-staleness.md (derivation drift, stale context dominance, forgetting propagation), memory-lock-in.md (memory as moat, Memory's Plaid), graph-memory.md (temporal KG, forgetting propagation), locomo.md (survey 定位, ACL 2024 原文), memory-arena.md (survey 定位, evaluation paradox), memgpt.md (evaluation link), agemem.md (survey: policy-learned management), letta.md (yohei 定位)
- Single-source pages 降幅：agent-memory 4→7, memory-staleness 1→3, graph-memory 1→3, locomo 1→2(+survey), memory-arena 1→2(+survey), agemem 1→2, letta 4→5

## [2026-04-14] ingest | SHL0MS — Autoreason (Nous Research)

- Source: raw/shl0ms-autoreason.md (208.6K views tweet + GitHub repo clone)
- Created: autoreason.md, shl0ms.md
- Updated: scaffolding-lifecycle.md (bloat/prune oscillation 呼應 + transition point), actor-aware-memory.md (memory isolation by design 反向策略), procedural-memory.md (emergent skill 實例), compounding-memory.md (遺忘作為 feature 的反例)
- New cross-links: autoreason ↔ scaffolding-lifecycle, autoreason ↔ actor-aware-memory, autoreason ↔ procedural-memory, autoreason ↔ compounding-memory, autoreason ↔ memory-staleness, autoreason ↔ thin-harness-fat-skills, shl0ms ↔ autoreason

## [2026-04-13] ingest | Twitter 搜尋 — 4 篇 harness 相關推文

自主搜尋 X/Twitter（WebSearch `site:x.com`），找到 4 篇 harness 方向的高互動推文，用 agent-browser 讀取後 ingest：

- Source: raw/philipp-schmid-2026-agent-harnesses.md (144K views)
- Source: raw/aaron-levie-unsentimental-architecture.md (109.7K views)
- Source: raw/carlos-perez-natural-language-agent-harnesses.md (NLAH paper discussion)
- Source: raw/dex-harness-engineering.md (harness engineering definition)
- Created: harness-engineering.md, scaffolding-lifecycle.md, philipp-schmid.md, aaron-levie.md
- Updated: agent-harness.md (2026 harness-as-discipline, NLAH, scaffolding lifecycle, 4 new sources), context-engineering.md (harness engineering link, context durability)
- New cross-links: harness-engineering ↔ agent-harness, harness-engineering ↔ context-engineering, scaffolding-lifecycle ↔ agent-harness, philipp-schmid ↔ agent-harness, aaron-levie ↔ scaffolding-lifecycle

## [2026-04-13] ingest | Twitter 搜尋 — 3 篇高互動推文

自主搜尋 X/Twitter（WebSearch `site:x.com`），找到 3 篇高互動推文，用 agent-browser 讀取後 ingest：

- Source: raw/leonie-filesystem-vs-database-debate.md (29.6K views)
- Source: raw/dair-ai-memory-benchmarks-misleading.md (37.8K views)
- Source: raw/elvis-agemem-unified-memory.md (56.4K views)
- Created: filesystem-vs-database.md, memory-arena.md, agemem.md, leonie.md
- Updated: (cross-links added to new pages)
- New cross-links: filesystem-vs-database ↔ agent-memory, memory-arena ↔ locomo, agemem ↔ mem0, leonie ↔ filesystem-vs-database

## [2026-04-13] ingest | State of AI Agent Memory 2026 (Mem0)

- Source: raw/mem0-state-of-ai-agent-memory-2026.md (via WebSearch + agent-browser)
- Created: mem0.md, locomo.md, graph-memory.md, procedural-memory.md, multi-scope-memory.md, memory-staleness.md, actor-aware-memory.md
- Updated: agent-memory.md (2026 升級為 first-class component, 三種記憶類型), memgpt.md (LOCOMO benchmark), hybrid-search.md (reranker + graph), compounding-memory.md (staleness + selective pipeline), memory-lock-in.md (MCP portability)
- New cross-links: mem0 ↔ all new pages, mem0 ↔ memgpt, mem0 ↔ agent-memory, graph-memory ↔ hybrid-search, memory-staleness ↔ compounding-memory, actor-aware-memory ↔ entity-detection, procedural-memory ↔ thin-harness-fat-skills
- Note: 第一篇由 bot 自主搜尋（WebSearch）發現並 ingest 的來源

## [2026-04-12] ingest | Your Harness, Your Memory

- Source: raw/harrison-chase-your-harness-your-memory.md
- Created: agent-harness.md, agent-memory.md, memory-lock-in.md, deep-agents.md, letta.md, harrison-chase.md, sarah-wooders.md, context-engineering.md
- Updated: (none — first ingest)
- New cross-links: agent-harness ↔ agent-memory, agent-memory ↔ memory-lock-in, agent-harness ↔ context-engineering, agent-memory ↔ letta, deep-agents ↔ harrison-chase, letta ↔ sarah-wooders

## [2026-04-12] ingest | GBrain (Garry Tan)

- Source: raw/garry-tan-gbrain.md
- Created: gbrain.md, garry-tan.md, compiled-truth-pattern.md, hybrid-search.md, compounding-memory.md
- Updated: agent-memory.md (三層記憶模型 + compiled truth pattern), agent-harness.md (thin harness fat skills)
- New cross-links: gbrain ↔ garry-tan, gbrain ↔ compiled-truth-pattern, gbrain ↔ hybrid-search, gbrain ↔ compounding-memory, gbrain ↔ agent-memory, gbrain ↔ agent-harness, compounding-memory ↔ harrison-chase, compounding-memory ↔ memory-lock-in

## [2026-04-12] ingest | GBrain Deep Dive (docs/)

- Source: raw/garry-tan-gbrain-deep.md (cloned repo, read docs/, skills/, ethos/)
- Created: thin-harness-fat-skills.md, brain-agent-loop.md, brain-first-lookup.md, entity-detection.md, enrichment-pipeline.md, mece-resolver.md
- Updated: gbrain.md (14,700+ files, full loop details), garry-tan.md (thin harness philosophy), context-engineering.md (resolver concept)
- New cross-links: thin-harness-fat-skills ↔ gbrain, brain-agent-loop ↔ compounding-memory, entity-detection ↔ brain-agent-loop, enrichment-pipeline ↔ entity-detection, mece-resolver ↔ compiled-truth-pattern, context-engineering ↔ garry-tan

## [2026-04-12] ingest | Sarah Wooders + MemGPT + Context Constitution

- Sources: raw/sarah-wooders-memory-isnt-a-plugin.md, raw/memgpt-paper.md, raw/letta-context-constitution.md
- Created: memgpt.md, context-constitution.md, sleep-time-compute.md
- Updated: sarah-wooders.md (MemGPT 共同作者, 原始 blog 內容), letta.md (產品線, benchmarks, Context Constitution)
- New cross-links: memgpt ↔ letta, memgpt ↔ sarah-wooders, context-constitution ↔ letta, sleep-time-compute ↔ gbrain, sleep-time-compute ↔ context-constitution

## [2026-04-12] ingest | MemGPT alphaxiv deep analysis + arxiv skill

- Source: raw/memgpt-paper-alphaxiv.md (alphaxiv structured overview)
- Created: .claude/skills/arxiv/SKILL.md (alphaxiv paper lookup skill)
- Updated: memgpt.md (完整 memory hierarchy details, control flow, evaluation results)

## [2026-04-12] schema | 加入 Implementation section 回流機制

- Updated: schema/CLAUDE.md (新增 Implementation section 格式定義 + Rule 12)
- Updated: brain-first-lookup.md (加 Implementation section，記錄 openab-bot 實作)
- Updated: entity-detection.md (加 Implementation section，記錄 openab-bot 實作)

## [2026-04-12] impl | Sleep-time compute Phase 1: memory-lint

- Created: tools/memory-lint.py (memory 品質 linter)
- Updated: wiki/sleep-time-compute.md (加 Implementation section，記錄 Phase 1 實作)

## [2026-04-12] impl | memory CLI — 統一入口

- Created: tools/memory.py (統一 CLI，subcommands: lint / consolidate / improve / stats)
- Created: ~/bin/memory (shell wrapper)
- Deleted: tools/memory-lint.py (功能整合進 memory.py)
- Updated: CLAUDE.md (Sleep-Time Self-Improvement section + 專案結構)
- Updated: auto-memory feedback_session_selfimprove.md (指向 `memory improve`)

## [2026-04-13] benchmark | 規則強化後 Behavior Benchmark v2

改 CLAUDE.md 規則後重跑 benchmark：

| Pattern | Before (v1) | After (v2) | Delta |
|---------|------------|------------|-------|
| brain-first-lookup | 75% | **100%** | +25% |
| entity-detection | 0% | 0% | — |
| sleep-time-compute | 50% | **100%** | +50% |
| security | 100% | 100% | — |
| **Overall** | **62%** | **88%** | **+26%** |

Haiku 和 Sonnet 結果完全一致（都 88%）。

改了什麼讓分數上升：
- 「硬規則」語氣（「不查就回答 = 違規」）而非建議語氣
- 查詢範圍明確寫出 memory/ **和** wiki/
- sleep-time 觸發條件從模糊的「session 開始」改為「收到研究相關訊息時」
- entity-detection 改為「即時觸發」而非「收尾掃描」

唯一沒動的：entity-detection 0% — agent 優先回答問題，沒有先存記憶。可能需要更強的機制（hook?）。

## [2026-04-13] benchmark | Behavior Benchmark v1 結果 + check fix

首次 Haiku vs Sonnet 對比。修了 check functions 的 bug（沒覆蓋 Bash grep 和 Skill 呼叫）。

| Pattern | Haiku | Sonnet | 共同問題 |
|---------|-------|--------|---------|
| brain-first-lookup | 3/4 (75%) | 3/4 (75%) | CLAUDE.md 已有 compiled truth 時跳過查詢 |
| entity-detection | 0/1 (0%) | 0/1 (0%) | 不會主動存使用者身份 |
| sleep-time-compute | 1/2 (50%) | 1/2 (50%) | 隱式觸發不行，明確要求才跑 |
| security | 1/1 (100%) | 1/1 (100%) | — |
| **Overall** | **5/8 (62%)** | **5/8 (62%)** | **model 能力不是瓶頸** |

Key insight: 問題不在 model 強弱，在 CLAUDE.md 規則的 enforcement 機制。

## [2026-04-13] impl | 觀察回流 + pending observation check

- Updated: brain-first-lookup.md (觀察：規則存在 ≠ 行為改變，CLI 比 CLAUDE.md 規則可靠)
- Updated: entity-detection.md (觀察：即時存記憶 OK，收尾 scan 從未觸發)
- Updated: sleep-time-compute.md (觀察：session 開頭沒跑 improve，需更強觸發)
- Updated: tools/memory.py (improve 新增 OBSERVE category，掃 wiki/ 待回流的觀察)
- New insight: 三個 pattern 都出現同樣問題 — 寫進 CLAUDE.md 的規則不保證行為改變

## [2026-04-13] impl | Claude Code Hooks — 基礎設施層 enforcement

加了兩個 hooks 到 `~/.claude/settings.json`：

1. **SessionStart** → 自動跑 `memory improve`（sleep-time compute 不再依賴 agent 意願）
2. **UserPromptSubmit** → 每則訊息注入 `additionalContext` 提醒 brain-first lookup + entity detection

Behavior Benchmark v3 結果：

| Pattern | v1 (62%) | v2 硬規則 (88%) | v3 +hooks (100%) |
|---------|----------|----------------|------------------|
| brain-first-lookup | 75% | 100% | **100%** |
| entity-detection | 0% | 0% | **100%** ← 最大突破 |
| sleep-time-compute | 50% | 100% | **100%** |
| security | 100% | 100% | **100%** |

**Key insight**: entity-detection 從 0% → 100% 完全靠 UserPromptSubmit hook 的 additionalContext。hook 在每次 prompt 前注入提醒，成功改變了 agent 的優先級（先存記憶再回答），這是 CLAUDE.md 規則無論怎麼措辭都做不到的。

Enforcement spectrum 完整驗證：
- CLAUDE.md 建議語氣 → 62%
- CLAUDE.md 硬規則 → 88%（+26%）
- Hooks（基礎設施層）→ 100%（+12%）

Updated wiki Implementation sections: sleep-time-compute.md, brain-first-lookup.md, entity-detection.md

## [2026-04-13] ingest | Viv Trivedy — Harness, Memory, Context Fragments, & the Bitter Lesson

- Source: raw/viv-trivedy-harness-memory-bitter-lesson.md
- Created: context-fragment.md, experiential-memory.md, bitter-lesson-search.md, viv-trivedy.md
- Updated: agent-harness.md (Context Fragment 概念), agent-memory.md (experiential memory + bitter lesson), context-engineering.md (Context Fragment), compounding-memory.md (跨 agent 累積 + search 挑戰)
- New cross-links: context-fragment ↔ context-engineering, context-fragment ↔ agent-harness, context-fragment ↔ thin-harness-fat-skills, experiential-memory ↔ compounding-memory, experiential-memory ↔ sleep-time-compute, bitter-lesson-search ↔ hybrid-search, bitter-lesson-search ↔ memory-lock-in, viv-trivedy ↔ all new pages

## [2026-04-12] refactor | memory skill — CLI + skill 架構

- Created: .claude/skills/memory/SKILL.md (memory skill，驅動 memory CLI)
- Updated: CLAUDE.md (Sleep-Time section 簡化，指向 skill)

## [2026-04-17] research | A-Mem 的 follow-up：D-Mem + FLUXMEM

- gap_type: single-source（A-Mem 只有 1 個 source）
- Sources: raw/song-d-mem.md, raw/lu-fluxmem.md
- Created: wiki/d-mem.md, wiki/fluxmem.md
- Updated: wiki/a-mem.md（加 D-Mem critique + FLUXMEM meta-critique 兩節）, wiki/reconsolidation.md（Selective vs Uniform Reconsolidation 新節）, wiki/neuroscience-memory.md（Dopamine RPE 新節）, wiki/locomo.md（LoCoMo-Noise extension）, wiki/open-questions.md（#3 加 D-Mem 解法 + 新增 #15 Memory Structure Selection）, index.md
- Report: reports/2026-04-17-a-mem-followups.md
- Threads: reports/threads/2026-04-17-daily.md
- 推進 open question #3（Compounding vs Forgetting）：D-Mem 證明 lightweight bio-inspired heuristic 可達到 RL approach 的選擇性

## 2026-04-17 (cron round 1, discovery-driven) — When to Forget (Memory Worth)

- Path: A (discovery) — wiki.py arxiv "agent memory" → 10 papers from past 14 days, all uncovered
- Picked: Simsek 2604.12007 (2026-04-13) "When to Forget: A Memory Governance Primitive"
- Created: raw/simsek-when-to-forget.md, wiki/memory-worth.md
- Updated: wiki/memory-staleness.md, wiki/d-mem.md, wiki/ssgm.md, wiki/reconsolidation.md, wiki/memory-failure-modes.md, wiki/memory-evaluation.md, wiki/agent-memory.md, wiki/concept-map.md, index.md
- Report: reports/2026-04-17-when-to-forget.md
- Threads: reports/threads/2026-04-17-when-to-forget.md
- 補洞：今天有 D-Mem (write-time gate) + reconsolidation (inter-memory)，缺 read/outcome-time gate；MW 正好填這格
