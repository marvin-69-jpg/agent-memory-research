#!/usr/bin/env python3
"""
recall_benchmark — Measures how well `memory recall` retrieves the right pages.

Metrics:
  Recall@K : fraction of expected pages found in top K results
  MRR      : Mean Reciprocal Rank (1/rank of first expected hit, averaged)
  Hit@K    : binary — at least one expected page in top K

Usage:
  python3 tools/recall_benchmark.py                    # run all cases
  python3 tools/recall_benchmark.py --verbose          # show per-case details
  python3 tools/recall_benchmark.py --k 5              # change K (default: 3)
  python3 tools/recall_benchmark.py --wiki-dir PATH    # override wiki dir
  python3 tools/recall_benchmark.py --memory-dir PATH  # override memory dir
"""

import argparse
import json
import sys
from pathlib import Path

# Import scoring function from memory.py
sys.path.insert(0, str(Path(__file__).parent))
from memory import recall_ranked, DEFAULT_MEMORY_DIR, DEFAULT_WIKI_DIR

# ── Test Cases ───────────────────────────────────────────
#
# Each case: query string → list of expected filenames (wiki/*.md or memory/*.md)
# "expect" means: these pages SHOULD appear in top K for this query.
# Order within expect doesn't matter.
#
# Guidelines for writing cases:
#   - Use natural language queries (how a user or agent would ask)
#   - Mix English and Chinese (our wiki is bilingual)
#   - Include both concept queries and people/product queries
#   - Each case should have 1-3 expected pages (not too many)
#   - Expected pages must actually exist in wiki/ or memory/

CASES = [
    # ── Concept queries ──
    {
        "query": "harness 和 memory 的關係",
        "expect": ["agent-harness.md", "agent-memory.md", "memory-lock-in.md"],
        "tag": "concept",
    },
    {
        "query": "context window 管理",
        "expect": ["context-engineering.md", "context-fragment.md", "memgpt.md"],
        "tag": "concept",
    },
    {
        "query": "agent 睡覺時做什麼",
        "expect": ["sleep-time-compute.md"],
        "tag": "concept",
    },
    {
        "query": "記憶越用越好 flywheel",
        "expect": ["compounding-memory.md"],
        "tag": "concept",
    },
    {
        "query": "怎麼避免被平台鎖住",
        "expect": ["memory-lock-in.md"],
        "tag": "concept",
    },
    {
        "query": "知識頁面怎麼寫 compiled truth",
        "expect": ["compiled-truth-pattern.md"],
        "tag": "concept",
    },
    {
        "query": "brain 先查再回答",
        "expect": ["brain-first-lookup.md", "brain-agent-loop.md"],
        "tag": "concept",
    },
    {
        "query": "entity 偵測 自動存記憶",
        "expect": ["entity-detection.md"],
        "tag": "concept",
    },
    {
        "query": "vector keyword 混合搜尋",
        "expect": ["hybrid-search.md"],
        "tag": "concept",
    },
    {
        "query": "每個知識放唯一位置 MECE",
        "expect": ["mece-resolver.md"],
        "tag": "concept",
    },
    {
        "query": "thin harness fat skills 架構",
        "expect": ["thin-harness-fat-skills.md"],
        "tag": "concept",
    },
    {
        "query": "context fragment loaded object",
        "expect": ["context-fragment.md", "context-engineering.md"],
        "tag": "concept",
    },
    {
        "query": "agent 經驗可以跨 instance 共享",
        "expect": ["experiential-memory.md"],
        "tag": "concept",
    },
    {
        "query": "資料量爆炸 search bitter lesson",
        "expect": ["bitter-lesson-search.md"],
        "tag": "concept",
    },
    {
        "query": "context constitution 原則",
        "expect": ["context-constitution.md", "letta.md"],
        "tag": "concept",
    },
    {
        "query": "enrichment tier API 分配",
        "expect": ["enrichment-pipeline.md"],
        "tag": "concept",
    },
    # ── People queries ──
    {
        "query": "Garry Tan 怎麼做知識管理",
        "expect": ["garry-tan.md", "gbrain.md"],
        "tag": "people",
    },
    {
        "query": "Harrison Chase 的觀點",
        "expect": ["harrison-chase.md"],
        "tag": "people",
    },
    {
        "query": "Sarah Wooders MemGPT",
        "expect": ["sarah-wooders.md", "memgpt.md"],
        "tag": "people",
    },
    {
        "query": "Viv Trivedy",
        "expect": ["viv-trivedy.md"],
        "tag": "people",
    },
    # ── Product queries ──
    {
        "query": "GBrain 14000 files",
        "expect": ["gbrain.md"],
        "tag": "product",
    },
    {
        "query": "Letta stateful agent",
        "expect": ["letta.md"],
        "tag": "product",
    },
    {
        "query": "MemGPT virtual memory OS",
        "expect": ["memgpt.md"],
        "tag": "product",
    },
    {
        "query": "Deep Agents LangChain",
        "expect": ["deep-agents.md"],
        "tag": "product",
    },
    # ── Cross-cutting queries ──
    {
        "query": "memory isn't a plugin",
        "expect": ["sarah-wooders.md", "letta.md", "agent-memory.md"],
        "tag": "cross",
    },
    {
        "query": "dream cycle enrichment 背景處理",
        "expect": ["sleep-time-compute.md", "compounding-memory.md"],
        "tag": "cross",
    },
    {
        "query": "resolver routing table context",
        "expect": ["mece-resolver.md", "thin-harness-fat-skills.md", "context-engineering.md"],
        "tag": "cross",
    },
]


# ── Metrics ──────────────────────────────────────────────


def recall_at_k(ranked_names: list[str], expected: list[str], k: int) -> float:
    """Fraction of expected pages found in top K."""
    top_k = set(ranked_names[:k])
    found = sum(1 for e in expected if e in top_k)
    return found / len(expected)


def mrr(ranked_names: list[str], expected: list[str]) -> float:
    """Mean Reciprocal Rank — 1/rank of first expected hit."""
    for i, name in enumerate(ranked_names):
        if name in expected:
            return 1.0 / (i + 1)
    return 0.0


def hit_at_k(ranked_names: list[str], expected: list[str], k: int) -> bool:
    """At least one expected page in top K."""
    top_k = set(ranked_names[:k])
    return any(e in top_k for e in expected)


# ── Main ─────────────────────────────────────────────────


def run_benchmark(memory_dir: Path, wiki_dir: Path, k: int, verbose: bool) -> dict:
    results = []

    for case in CASES:
        query = case["query"]
        expected = case["expect"]
        tag = case.get("tag", "")

        ranked = recall_ranked(memory_dir, wiki_dir, query, max_results=k * 2)
        ranked_names = [name for name, _score in ranked]

        r_at_k = recall_at_k(ranked_names, expected, k)
        case_mrr = mrr(ranked_names, expected)
        case_hit = hit_at_k(ranked_names, expected, k)

        result = {
            "query": query,
            "tag": tag,
            "expected": expected,
            "top_k": ranked_names[:k],
            "recall@k": r_at_k,
            "mrr": case_mrr,
            "hit@k": case_hit,
        }
        results.append(result)

        if verbose:
            status = "✓" if case_hit else "✗"
            print(f"  {status} [{tag:8s}] R@{k}={r_at_k:.0%} MRR={case_mrr:.2f}  {query}")
            if not case_hit or r_at_k < 1.0:
                missing = [e for e in expected if e not in set(ranked_names[:k])]
                if missing:
                    print(f"           missing: {', '.join(missing)}")
                print(f"           got:     {', '.join(ranked_names[:k])}")

    # Aggregate
    n = len(results)
    avg_recall = sum(r["recall@k"] for r in results) / n
    avg_mrr = sum(r["mrr"] for r in results) / n
    hit_rate = sum(1 for r in results if r["hit@k"]) / n

    # Per-tag breakdown
    tags = sorted(set(r["tag"] for r in results))
    tag_stats = {}
    for tag in tags:
        tag_results = [r for r in results if r["tag"] == tag]
        tn = len(tag_results)
        tag_stats[tag] = {
            "count": tn,
            "recall@k": sum(r["recall@k"] for r in tag_results) / tn,
            "mrr": sum(r["mrr"] for r in tag_results) / tn,
            "hit_rate": sum(1 for r in tag_results if r["hit@k"]) / tn,
        }

    return {
        "k": k,
        "cases": n,
        "recall@k": avg_recall,
        "mrr": avg_mrr,
        "hit_rate": hit_rate,
        "by_tag": tag_stats,
        "details": results,
    }


def main():
    parser = argparse.ArgumentParser(prog="recall_benchmark")
    parser.add_argument("--k", type=int, default=3, help="Top-K for metrics (default: 3)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show per-case details")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--memory-dir", default=str(DEFAULT_MEMORY_DIR))
    parser.add_argument("--wiki-dir", default=str(DEFAULT_WIKI_DIR))
    args = parser.parse_args()

    memory_dir = Path(args.memory_dir)
    wiki_dir = Path(args.wiki_dir)

    print(f"Recall Benchmark — K={args.k}, {len(CASES)} cases")
    print(f"  memory: {memory_dir}")
    print(f"  wiki:   {wiki_dir}")
    print("=" * 60)

    if args.verbose:
        print()

    stats = run_benchmark(memory_dir, wiki_dir, args.k, args.verbose)

    if args.json:
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return

    print()
    print(f"{'Metric':<20s} {'Score':>8s}")
    print("-" * 30)
    print(f"{'Recall@' + str(args.k):<20s} {stats['recall@k']:>7.0%}")
    print(f"{'MRR':<20s} {stats['mrr']:>7.2f}")
    print(f"{'Hit Rate@' + str(args.k):<20s} {stats['hit_rate']:>7.0%}")
    print()

    print(f"{'Tag':<12s} {'N':>4s} {'R@K':>6s} {'MRR':>6s} {'Hit%':>6s}")
    print("-" * 38)
    for tag, ts in sorted(stats["by_tag"].items()):
        print(f"{tag:<12s} {ts['count']:>4d} {ts['recall@k']:>5.0%} {ts['mrr']:>6.2f} {ts['hit_rate']:>5.0%}")

    # Failures
    failures = [r for r in stats["details"] if not r["hit@k"]]
    if failures:
        print(f"\nFailed cases ({len(failures)}):")
        for r in failures:
            print(f"  ✗ {r['query']}")
            print(f"    expected: {', '.join(r['expected'])}")
            print(f"    got:      {', '.join(r['top_k'])}")

    # Exit code: 0 if hit rate >= 80%, 1 otherwise
    sys.exit(0 if stats["hit_rate"] >= 0.8 else 1)


if __name__ == "__main__":
    main()
