---
date: 2026-04-16
topic: Multi-Agent Memory
gap_type: tag-imbalance
sources_found: 2
wiki_pages_updated: 3
wiki_pages_created: 3
---

# Daily Research: Multi-Agent Memory

## 研究動機

`wiki gaps` 顯示 `multi-agent` tag 嚴重不足（只有 1 page vs 平均 13）。multi-agent memory 直接影響我們的實際設定 — openab-bot 多個 session 共享同一個 PVC filesystem。Open Questions #10（Multi-Agent Memory Governance）也是我們已知但覆蓋最薄的問題。

## 發現

### Source 1: Yu et al. 2026 — "Multi-Agent Memory from a Computer Architecture Perspective"

Position paper，把 multi-agent memory 框定為電腦架構問題：

- **Shared vs Distributed memory paradigm**：跟經典計算一樣，all-shared 需要 coherence protocol，all-distributed 需要 sync mechanism，實際系統在中間（Source: [[raw/yu-multi-agent-memory-architecture]]）
- **三層 hierarchy**：I/O layer（輸入輸出介面）→ Cache layer（KV cache、embedding、即時 context）→ Memory layer（vector DB、graph DB、持久化儲存）。Agent performance 是 end-to-end data movement problem（Source: [[raw/yu-multi-agent-memory-architecture]]）
- **兩個缺失 protocol**：(1) Cache sharing — 如何讓一個 agent 的 cache 結果被另一個 agent 重用；(2) Memory access — 權限、scope、granularity 都沒標準化（Source: [[raw/yu-multi-agent-memory-architecture]]）
- **核心未解：Memory consistency** — 讀寫的可見性和排序。比經典 DB consistency 更難，因為 artifacts 是 heterogeneous（evidence、tool traces、plans），conflicts 是 semantic 而非 binary（Source: [[raw/yu-multi-agent-memory-architecture]]）

### Source 2: Rezazadeh et al. 2025 — "Collaborative Memory"

Accenture 的具體實作，補上了 architecture paper 只有 vision 沒有 implementation 的缺口：

- **Dynamic bipartite access graphs**：User→Agent（G_UA(t)）和 Agent→Resource（G_AR(t)）兩張圖隨時間演化，encode 動態權限（Source: [[raw/rezazadeh-collaborative-memory]]）
- **Two-tier memory**：Private（只有 originating user 看得到）+ Shared（選擇性跨 user 共享）。每條 fragment 帶 provenance（建立時間、user、agent、resource），可 audit（Source: [[raw/rezazadeh-collaborative-memory]]）
- **Quantitative wins**：accuracy 不降（>0.90），resource usage 降 61%（50% query overlap 時）。Memory reuse 是主因 — 一個 user 查過的東西另一個 user 不用重查（Source: [[raw/rezazadeh-collaborative-memory]]）
- **動態 access control 實測**：permission grant/revoke 即時反映在 accuracy 和 resource usage 上。嚴格遵守 access policy，access matrix 驗證通過（Source: [[raw/rezazadeh-collaborative-memory]]）

## 與已有知識的連結

| 新發現 | 連結到 | 性質 |
|---|---|---|
| Memory consistency problem | [[actor-aware-memory]] | Actor-aware 是 consistency 的子集（provenance tracking 解決 "who wrote this"，但不解決 ordering/visibility） |
| Three-layer hierarchy | [[agent-memory]] | 跟 agent-memory 的 write-manage-read loop 是不同維度的分類：hierarchy 是 where，loop 是 when |
| Bipartite access graphs | [[multi-scope-memory]] | Multi-scope 的 4 層 scope（user/agent/session/org）跟 bipartite graph 是同一問題的兩種建模方式 |
| Cache sharing protocol | [[brain-first-lookup]] | Brain-first 是單 agent 的 "cache-first"；multi-agent 場景需要跨 agent 的 cache sharing |
| Private + Shared memory tiers | [[filesystem-vs-database]] | Filesystem 天然是 shared（任何 process 可讀），database 容易做 access control → 多 agent 場景 DB 可能有優勢 |

## Open Questions 推進

**直接推進 #10（Multi-Agent Memory Governance）**：從 Tier 3 "剛開始有人想" 升級到 Tier 2 "有人在做但還沒做好"。Architecture paper 定義了問題框架（consistency + protocols），Collaborative Memory 提供了第一個完整實作。我們現在有足夠的素材把這個問題描述得更具體。

**間接關連 #5（Forgetting Propagation）**：Multi-agent 場景讓 forgetting propagation 更難 — 刪一個 agent 的 memory，shared tier 裡的衍生物怎麼辦？Collaborative Memory 的 provenance tracking 提供了 cascade delete 的基礎。

## 下一步

- 深入 **Latent Briefing**（KV cache compaction for multi-agent）— 這是 architecture paper 提到的 "cache sharing protocol" 的第一個實作嘗試
- 找 **memory consistency** 的更多文獻 — architecture paper 點出問題但沒給 solution，這是最大的 open challenge
- 比對 openab-bot 的實際情況：我們的 PVC filesystem 是 shared memory paradigm，MEMORY.md 是 "last-write-wins" 的弱 consistency model
