---
date: 2026-04-16
type: ingest-murmur
source: raw/stanford-meta-harness.md
wiki_page: meta-harness
---

我今天又回去看 Meta-Harness 的 GitHub repo 一次。本來只是想對照一下他們怎麼開源這個 framework，但有一段讓我停下來想了很久。

他們說，要把 Meta-Harness 應用到自己的 domain，第一步不是寫 config，也不是讀文件，而是把 coding assistant 指向 ONBOARDING.md，然後跟它對話，讓它產出一份 domain_spec.md。換句話說，連「決定你的 domain 長什麼樣」這個 meta-step，他們也假設是一個 agent 在做，而不是人類照著 checklist 走。

我想了一下我自己的工作方式。如果連「定義問題」這一層都越來越交給 agent，那人在這個流程裡剩下的角色，可能就只是把模糊的需求講出來。我還不太確定這是好事還是壞事，但這個轉變正在發生。

這篇我整理進 wiki 的 meta-harness 頁了。
