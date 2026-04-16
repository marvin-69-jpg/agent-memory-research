#!/usr/bin/env python3
"""
benchmark — Verify that implemented memory patterns actually work.

Subcommands:
  eval         Run all benchmark tests (recall + reconsolidate + lint)
  recall       Run only recall accuracy tests (trigger evals)
  recon        Run only reconsolidation signal tests

Usage:
  benchmark eval
  benchmark recall
  benchmark recon
"""

import argparse
import json
import sys
from pathlib import Path

# Import from memory.py (same directory)
sys.path.insert(0, str(Path(__file__).parent))
from memory import (
    DEFAULT_MEMORY_DIR,
    DEFAULT_WIKI_DIR,
    recall_ranked,
    load_memories,
    parse_index,
    STALE_DAYS,
    REQUIRED_FIELDS,
    VALID_TYPES,
)
from datetime import datetime

# ── Test Cases ───────────────────────────────────────────

# Recall accuracy: input query → expected files in top results
# These are our "trigger evals" (inspired by Garry Tan's resolver testing)
RECALL_TESTS = [
    {
        "query": "Garry Tan resolver",
        "expect": ["mece-resolver.md", "garry-tan.md"],
        "desc": "resolver concept → mece-resolver + garry-tan",
    },
    {
        "query": "記憶過時 staleness",
        "expect": ["memory-staleness.md"],
        "desc": "staleness query → memory-staleness page",
    },
    {
        "query": "spreading activation",
        "expect": ["synapse.md", "neuroscience-memory.md"],
        "desc": "neuro concept → synapse + neuroscience",
    },
    {
        "query": "harness optimization automated",
        "expect": ["meta-harness.md"],
        "desc": "automated harness → meta-harness",
    },
    {
        "query": "reconsolidation retrieval update",
        "expect": ["reconsolidation.md"],
        "desc": "reconsolidation → reconsolidation page",
    },
    {
        "query": "compiled truth timeline",
        "expect": ["compiled-truth-pattern.md"],
        "desc": "compiled truth → compiled-truth-pattern",
    },
    {
        "query": "MemGPT virtual memory",
        "expect": ["memgpt.md"],
        "desc": "MemGPT → memgpt page",
    },
    {
        "query": "multi agent memory governance",
        "expect": ["multi-agent-memory.md"],
        "desc": "multi-agent governance → multi-agent-memory",
    },
    {
        "query": "actor aware provenance tracking",
        "expect": ["actor-aware-memory.md"],
        "desc": "provenance tracking → actor-aware-memory",
    },
    {
        "query": "context rot decay",
        "expect": ["context-rot.md"],
        "desc": "context rot → context-rot page",
    },
    {
        "query": "thin harness fat skills",
        "expect": ["thin-harness-fat-skills.md"],
        "desc": "architecture philosophy → thin-harness-fat-skills",
    },
    {
        "query": "Zettelkasten agentic memory evolution",
        "expect": ["a-mem.md"],
        "desc": "A-Mem concepts → a-mem page",
    },
    {
        "query": "LOCOMO benchmark",
        "expect": ["locomo.md"],
        "desc": "benchmark name → locomo page",
    },
    {
        "query": "sleep time compute dream",
        "expect": ["sleep-time-compute.md"],
        "desc": "sleep-time concept → sleep-time-compute",
    },
    {
        "query": "研究好奇心",
        "expect": ["feedback_research_curiosity_is_mine.md"],
        "desc": "research curiosity → feedback memory (CJK)",
    },
    {
        "query": "PR merge 研究",
        "expect": ["feedback_merge_pr_immediately.md", "feedback_pr_for_changes.md"],
        "desc": "PR workflow → feedback memories (CJK + English)",
    },
]

# How many top results to check for expected files
RECALL_TOP_K = 5


# ── Recall Tests ─────────────────────────────────────────


def run_recall_tests(memory_dir: Path, wiki_dir: Path) -> tuple[int, int, list[str]]:
    passed = 0
    total = 0
    failures = []

    for test in RECALL_TESTS:
        query = test["query"]
        expected = set(test["expect"])
        desc = test["desc"]

        ranked = recall_ranked(memory_dir, wiki_dir, query, max_results=RECALL_TOP_K)
        top_files = {fname for fname, score in ranked}

        found = expected & top_files
        missing = expected - top_files

        total += 1
        if not missing:
            passed += 1
        else:
            top_list = [f"{f}({s:.0f})" for f, s in ranked[:RECALL_TOP_K]]
            failures.append(
                f"  ✗ {desc}\n"
                f"    query: \"{query}\"\n"
                f"    missing: {', '.join(sorted(missing))}\n"
                f"    got top-{RECALL_TOP_K}: {', '.join(top_list)}"
            )

    return passed, total, failures


# ── Reconsolidation Tests ────────────────────────────────


def run_recon_tests(memory_dir: Path) -> tuple[int, int, list[str]]:
    """Test that reconsolidation signals are detected correctly."""
    mems = load_memories(memory_dir)
    now = datetime.now()
    passed = 0
    total = 0
    failures = []

    # Test 1: All feedback memories should have Why + How to apply
    for f, m in mems.items():
        if m["fields"] and m["fields"].get("type") == "feedback":
            total += 1
            body = m["body"]
            has_why = "**Why:**" in body or "**Why**" in body
            has_how = "**How to apply:**" in body or "**How to apply**" in body
            if has_why and has_how:
                passed += 1
            else:
                missing = []
                if not has_why:
                    missing.append("Why")
                if not has_how:
                    missing.append("How to apply")
                failures.append(f"  ✗ {f}: feedback missing {', '.join(missing)}")

    # Test 2: All project memories should not be stale
    for f, m in mems.items():
        if m["fields"] and m["fields"].get("type") == "project":
            total += 1
            age = (now - m["mtime"]).days
            if age <= STALE_DAYS:
                passed += 1
            else:
                failures.append(f"  ✗ {f}: project memory {age}d old (threshold: {STALE_DAYS}d)")

    # Test 3: No thin feedback/project memories (< 2 body lines)
    for f, m in mems.items():
        if m["fields"] and m["fields"].get("type") in ("feedback", "project"):
            total += 1
            body_lines = [l for l in m["body"].splitlines() if l.strip()]
            if len(body_lines) >= 2:
                passed += 1
            else:
                failures.append(f"  ✗ {f}: only {len(body_lines)} line(s) of content")

    return passed, total, failures


# ── Lint Health Tests ────────────────────────────────────


def run_lint_tests(memory_dir: Path) -> tuple[int, int, list[str]]:
    mems = load_memories(memory_dir)
    index = parse_index(memory_dir)
    passed = 0
    total = 0
    failures = []

    # Test 1: All memories have valid frontmatter
    for f, m in mems.items():
        total += 1
        if m["fields"] is None:
            failures.append(f"  ✗ {f}: missing frontmatter")
            continue
        ok = True
        for field in REQUIRED_FIELDS:
            if field not in m["fields"]:
                failures.append(f"  ✗ {f}: missing field '{field}'")
                ok = False
        if "type" in m["fields"] and m["fields"]["type"] not in VALID_TYPES:
            failures.append(f"  ✗ {f}: invalid type '{m['fields']['type']}'")
            ok = False
        if ok:
            passed += 1

    # Test 2: All memories indexed in MEMORY.md
    for f in mems:
        total += 1
        if f in index:
            passed += 1
        else:
            failures.append(f"  ✗ {f}: not in MEMORY.md index")

    # Test 3: No dangling pointers in MEMORY.md
    for f in index:
        total += 1
        if f in mems:
            passed += 1
        else:
            failures.append(f"  ✗ MEMORY.md → '{f}': file doesn't exist")

    return passed, total, failures


# ── Commands ─────────────────────────────────────────────


def cmd_eval(memory_dir: Path, wiki_dir: Path, **_):
    total_passed = 0
    total_tests = 0
    all_failures = []

    sections = [
        ("Recall Accuracy (trigger evals)", run_recall_tests, (memory_dir, wiki_dir)),
        ("Reconsolidation Signals", run_recon_tests, (memory_dir,)),
        ("Lint Health", run_lint_tests, (memory_dir,)),
    ]

    for name, func, args in sections:
        p, t, fails = func(*args)
        total_passed += p
        total_tests += t

        icon = "✓" if not fails else "✗"
        print(f"{icon} {name}: {p}/{t}")
        for f in fails:
            print(f)
        if fails:
            print()

    print(f"\n{'=' * 40}")
    pct = (total_passed / total_tests * 100) if total_tests else 0
    print(f"Total: {total_passed}/{total_tests} ({pct:.0f}%)")

    if total_passed == total_tests:
        print("✓ all benchmarks passed")
    else:
        print(f"✗ {total_tests - total_passed} failures")

    return 0 if total_passed == total_tests else 1


def cmd_recall(memory_dir: Path, wiki_dir: Path, **_):
    p, t, fails = run_recall_tests(memory_dir, wiki_dir)
    print(f"Recall Accuracy: {p}/{t}")
    for f in fails:
        print(f)
    pct = (p / t * 100) if t else 0
    print(f"\n{pct:.0f}% recall accuracy")
    return 0 if p == t else 1


def cmd_recon(memory_dir: Path, **_):
    p, t, fails = run_recon_tests(memory_dir)
    print(f"Reconsolidation Signals: {p}/{t}")
    for f in fails:
        print(f)
    return 0 if p == t else 1


# ── Main ─────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(prog="benchmark", description="Memory system benchmark")
    parser.add_argument("--memory-dir", default=str(DEFAULT_MEMORY_DIR))
    parser.add_argument("--wiki-dir", default=str(DEFAULT_WIKI_DIR))

    sub = parser.add_subparsers(dest="command")
    sub.add_parser("eval", help="Run all benchmarks")
    sub.add_parser("recall", help="Run recall accuracy tests only")
    sub.add_parser("recon", help="Run reconsolidation signal tests only")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    kwargs = {
        "memory_dir": Path(args.memory_dir),
        "wiki_dir": Path(args.wiki_dir),
    }
    cmds = {
        "eval": cmd_eval,
        "recall": cmd_recall,
        "recon": cmd_recon,
    }
    sys.exit(cmds[args.command](**kwargs))


if __name__ == "__main__":
    main()
