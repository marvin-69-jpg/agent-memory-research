---
date: 2026-04-17
topic: Memwright — zero-LLM deterministic agent memory
gap_type: single-source
sources_found: 1
wiki_pages_updated: 9
wiki_pages_created: 1
---

# Daily Research: Memwright — zero-LLM deterministic agent memory

## 研究動機

`wiki gaps` 標出 governance tag 只有 1 page（memory-worth），想延伸 governance 主題。搜到 aarjay singh 4/15 在 dev.to 發的「Why I stopped putting LLMs in my agent memory retrieval path」，直接攻擊目前主流 LLM-in-the-loop retrieval 的可靠性問題。

## 發現

**核心主張：memory 是 infrastructure，不是 prompt engineering。**

- **zero LLM in retrieval critical path** — embedding 只在 write time 算一次（local all-MiniLM-L6-v2），recall 是純數學 + graph traversal。理由四個：non-determinism（同 query 不同結果）、latency（500-2000ms per call）、cost（50x in planner/executor loop）、untestable（無法寫 unit test）
- **5-layer pipeline**：Tag FTS → Graph BFS (depth 2) → Vector cosine → RRF (k=60) + PageRank + confidence decay → MMR (λ=0.7) diversity。每層是 pure function，607 test cases
- **Multi-agent 是 first-class**：6 RBAC roles、row-level namespace isolation、provenance chain（source_id + content hash + timestamp + agent role）、per-agent token budgets + write quotas
- **Temporal correctness**：never overwrite, supersede。valid_from/valid_to window，recall(as_of=...) 回放任意時間點
- **LOCOMO v2 81.2%**：OpenAI 52.9%、Mem0 66.9%、Letta 74%、Zep ~75%、MemMachine 84.9%
- 6 種 backend（SQLite/Postgres/ArangoDB/AWS/Azure/GCP）同 API

## 與已有知識的連結

- **vs [[a-mem]]**：A-Mem 用 LLM 做 write-time evolution（memory enrichment），Memwright 連 retrieval 都不用 LLM。兩者解不同問題：A-Mem 解 organization rot，Memwright 解 determinism + testability
- **vs [[hybrid-search]]**：GBrain 用 LLM 做 multi-query expansion → Memwright 完全拿掉 LLM，改用 graph BFS expansion 補語意覆蓋。Memwright 多了 PageRank weighting
- **vs [[actor-aware-memory]] / [[collaborative-memory-system]]**：provenance chain 和 RBAC 跟這兩者同源思想，但 Memwright 是 schema-level enforce，不靠 application code
- **vs [[compiled-truth-pattern]]**：temporal supersede = compiled truth + timeline 的 schema 化。valid_from/valid_to 直接解 memory-staleness 的 silent overwrite 問題
- **[[memory-evaluation]]**：deterministic retrieval 使 fixture-based unit test 成為可能 → 一致性是正確性的必要條件

## Open Questions 推進

推進了 #5（Memory Evaluation Paradox）的一個子問題：「如何驗證 retrieval 品質？」Memwright 的答案不是解 ground truth 問題，而是先保證 determinism → 至少可以測 consistency。

也推進了 #7（Multi-Agent Memory）的 governance 面向：6 RBAC roles + per-agent quotas 是目前最具體的 multi-agent memory access control 實作之一。

## 下一步

- 研究 HN discussion (#47773981) 看 community 的反應和 critique
- 比較 Memwright 跟 [[synapse]] 的 retrieval pipeline（synapse 用 spreading activation，也是 non-LLM）
- 深入 temporal correctness 在 regulated domain 的需求（金融、醫療的 audit trail）
