# AI Meets Brain: A Unified Survey on Memory Systems from Cognitive Neuroscience to Autonomous Agents

- **Authors**: Jiafeng Liang, Hao Li, Chang Li +12 (Harbin Institute of Technology, Fudan, PKU, NUS)
- **Date**: 2025-12-29
- **Source**: https://arxiv.org/abs/2512.23343
- **Type**: arxiv survey paper

## Summary

跨學科 survey，系統性連結 cognitive neuroscience 和 LLM agent 的記憶系統。400+ 引用，涵蓋記憶定義、分類、儲存、管理生命週期、benchmark、安全性。

## 核心架構：Neuroscience ↔ AI 對照

### 記憶分類

| 維度 | Cognitive Neuroscience | AI Agent |
|---|---|---|
| 短期 | 感覺暫存，4-9 items，秒級 | Context window，inside-trail |
| 長期 - Episodic | 個人經歷，有時空 context（mental time travel） | 互動軌跡，sequential，含工具使用記錄 |
| 長期 - Semantic | 事實知識，脫離獲取情境 | 知識庫，entity/concept/rules |

Agent 記憶的雙維度分類：
- **Nature-based**：Episodic（how-to，經驗）vs Semantic（what-is，知識）
- **Scope-based**：Inside-trail（單次軌跡）vs Cross-trail（跨軌跡，可泛化）

### 記憶儲存

| 維度 | Brain | Agent |
|---|---|---|
| 位置 | 短期：感覺-前額頂網路；長期：海馬體（索引）+ 新皮質（儲存） | Context window（inside-trail）；Memory bank（external，persistent） |
| 格式 | 持續神經活動、突觸權重、cognitive maps | Text、Graph、Parameters、Latent representation |

**Cognitive Maps**（認知地圖）：大腦用抽象地圖組織知識、概念、經驗 → 對應 agent 的 knowledge graph

### 記憶管理生命週期

| 階段 | Brain | Agent |
|---|---|---|
| 形成 | Encoding → Consolidation（海馬體 replay）→ Integration | Flat extraction / Hierarchical / Generative |
| 更新 | 由 prediction error 觸發，Reconsolidation | Inside-trail（filter/summarize）；Cross-trail（selective retain/forget，RL） |
| 檢索 | Cue-driven pattern completion，是 transformative process | Similarity-based / Multi-factor（recency, importance, reward） |
| 應用 | 引導行為 | Contextual augmentation / Parameter internalization |

**關鍵 neuroscience insight**：
- **Reconsolidation**：檢索本身會修改記憶 → agent 的 retrieval 也應該 update 記憶
- **Prediction error 驅動更新**：只在預期和現實不符時更新 → 對應 selective update
- **Hippocampal replay**：睡眠時重播記憶做 consolidation → 對應 sleep-time compute

### 記憶效用（Agent 記憶的三大用途）

1. **突破 context window 限制**：virtual context、gist memory、task-structure folding
2. **建構長期個人化 profile**：從互動中提煉 traits → 偏好對齊
3. **驅動經驗推理**：strategic guidance（reflection、exemplar、guideline retrieval）+ procedural solidification（skill library、trajectory distillation）

### Benchmark

分兩類：
- **Semantic-oriented**：評估內部記憶狀態（LoCoMo, MemBench, HaluMem）
- **Episodic-oriented**：評估領域任務表現（WebChoreArena, ToolBench, ScienceWorld）
- 評估屬性：Fidelity、Dynamics、Generalization

### 記憶安全

- **攻擊**：Extraction-based（隱私洩漏）、Poisoning-based（注入惡意資料、植入後門）
- **防禦**：Retrieval-based（異常偵測淨化）、Response-based（多 agent review、MCTS）、Privacy-based（隔離私有記憶、匿名化）

### 未來方向

1. **Multimodal memory**：跨模態整合（語意退化、時間對齊、計算效率問題）
2. **Agent skills**：模組化、可組合、可轉移的技能（類比遊戲裝備）→ 技能生態系統
