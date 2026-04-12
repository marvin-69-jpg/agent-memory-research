# Agent Memory Research

LLM-maintained knowledge base about agent memory systems.
Inspired by [Andrej Karpathy's LLM Wiki pattern](https://github.com/karpathy/llm-wiki).

## Architecture

```
raw/          ← 原始文章全文（immutable，不可改）
wiki/         ← LLM 維護的 entity pages（知識庫）
index.md      ← wiki 目錄 + 一句話摘要
log.md        ← 操作記錄（append-only）
schema/       ← ingest/query/lint 規則
```

- **Raw** = source of truth，LLM 只讀不改
- **Wiki** = LLM 完全擁有，建立 / 更新 / cross-link / 淘汰過時資訊
- **Schema** = 人類定義的規則

## As Obsidian Vault

1. Clone this repo
2. Install [Obsidian Git plugin](https://github.com/Vinzent03/obsidian-git)
3. Open the repo as an Obsidian vault
4. Set auto-pull interval
5. Browse wiki pages, explore graph view, search with `[[wiki-links]]`

## Topics Covered

- Agent memory 架構（短期 / 長期 / 工作記憶）
- Agent harness 與 memory 的關係
- Memory lock-in 與 open memory
- Context engineering
- 各家產品比較（Claude Code, Deep Agents, Letta, Codex...）

## Credits

- Pattern: [Andrej Karpathy — LLM Wiki](https://github.com/karpathy/llm-wiki)
- Maintained by: Claude Code (via [openab](https://github.com/marvin-69-jpg/openab))
