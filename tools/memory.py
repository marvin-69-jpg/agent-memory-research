#!/usr/bin/env python3
"""
memory — Unified CLI for auto-memory management.

Subcommands:
  lint         Check memory file format and structural integrity
  consolidate  Semantic analysis: duplicates, staleness, promotion candidates
  improve      Combined lint + consolidate (designed for session startup)
  stats        Quick overview of memory distribution

Usage:
  memory lint
  memory consolidate
  memory improve
  memory stats

Global options:
  --memory-dir PATH   Memory directory (default: /home/node/.claude/projects/-home-node/memory/)
  --claude-md PATH    CLAUDE.md path for promotion checking (default: /home/node/CLAUDE.md)
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from pathlib import Path

# ── Defaults ──────────────────────────────────────────────

DEFAULT_MEMORY_DIR = Path("/home/node/.claude/projects/-home-node/memory/")
DEFAULT_CLAUDE_MD = Path("/home/node/CLAUDE.md")
VALID_TYPES = {"user", "feedback", "project", "reference"}
REQUIRED_FIELDS = {"name", "description", "type"}
STALE_DAYS = 14
SIM_THRESHOLD_LINT = 0.7
SIM_THRESHOLD_CONSOLIDATE = 0.6

# ── Shared helpers ────────────────────────────────────────


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("---", 3)
    if end == -1:
        return None, text
    fields = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fields[k.strip()] = v.strip()
    return fields, text[end + 3:].strip()


def load_memories(memory_dir: Path) -> dict:
    mems = {}
    for f in sorted(os.listdir(memory_dir)):
        if not f.endswith(".md") or f == "MEMORY.md":
            continue
        p = memory_dir / f
        text = p.read_text("utf-8")
        fields, body = parse_frontmatter(text)
        mems[f] = {
            "fields": fields,
            "body": body,
            "mtime": datetime.fromtimestamp(p.stat().st_mtime),
        }
    return mems


def parse_index(memory_dir: Path) -> dict[str, str]:
    idx = {}
    p = memory_dir / "MEMORY.md"
    if p.exists():
        for line in p.read_text("utf-8").splitlines():
            m = re.match(r"- \[(.+?)\]\((.+?)\)", line)
            if m:
                idx[m.group(2)] = m.group(1)
    return idx


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def type_dist(mems: dict) -> dict[str, int]:
    counts = {}
    for m in mems.values():
        if m["fields"]:
            t = m["fields"].get("type", "?")
            counts[t] = counts.get(t, 0) + 1
    return counts


def dist_str(counts: dict) -> str:
    return ", ".join(f"{t}:{c}" for t, c in sorted(counts.items()))


# ── lint ──────────────────────────────────────────────────


def cmd_lint(memory_dir: Path, **_):
    mems = load_memories(memory_dir)
    index = parse_index(memory_dir)
    issues = []

    def add(sev, f, msg):
        issues.append((sev, f, msg))

    # Frontmatter
    for f, m in mems.items():
        if m["fields"] is None:
            add("error", f, "missing frontmatter")
            continue
        for field in REQUIRED_FIELDS:
            if field not in m["fields"]:
                add("error", f, f"missing field: {field}")
        if "type" in m["fields"] and m["fields"]["type"] not in VALID_TYPES:
            add("error", f, f"invalid type: '{m['fields']['type']}'")

    # Index sync
    for f in mems:
        if f not in index:
            add("warn", f, "not in MEMORY.md")
    for f in index:
        if f not in mems:
            add("error", "MEMORY.md", f"dangling pointer: '{f}'")

    # Why/How for feedback/project
    for f, m in mems.items():
        if m["fields"] is None:
            continue
        t = m["fields"].get("type", "")
        if t in ("feedback", "project"):
            if "**Why:**" not in m["body"] and "**Why**" not in m["body"]:
                add("info", f, f"{t} missing **Why:**")
            if "**How to apply:**" not in m["body"] and "**How to apply**" not in m["body"]:
                add("info", f, f"{t} missing **How to apply:**")

    # Stale projects
    cutoff = datetime.now() - timedelta(days=STALE_DAYS)
    for f, m in mems.items():
        if m["fields"] and m["fields"].get("type") == "project" and m["mtime"] < cutoff:
            age = (datetime.now() - m["mtime"]).days
            add("warn", f, f"project memory {age}d old")

    # Near-duplicates
    flist = [f for f in mems if mems[f]["fields"]]
    for i, f1 in enumerate(flist):
        for f2 in flist[i + 1:]:
            d1 = mems[f1]["fields"].get("description", "")
            d2 = mems[f2]["fields"].get("description", "")
            if similarity(d1, d2) > SIM_THRESHOLD_LINT:
                add("warn", f1, f"similar to {f2}")

    # Report
    counts = type_dist(mems)
    print(f"memory lint — {len(mems)} files ({dist_str(counts)})")

    if not issues:
        print("✓ all clear")
        return 0

    for sev in ("error", "warn", "info"):
        items = [(s, f, m) for s, f, m in issues if s == sev]
        if items:
            icon = {"error": "✗", "warn": "△", "info": "·"}[sev]
            for _, f, msg in items:
                print(f"  {icon} {f}: {msg}")

    errors = sum(1 for s, _, _ in issues if s == "error")
    return 1 if errors else 0


# ── consolidate ───────────────────────────────────────────


def cmd_consolidate(memory_dir: Path, claude_md: Path, **_):
    mems = load_memories(memory_dir)
    actions = []

    # Near-duplicates (lower threshold than lint)
    flist = [f for f in mems if mems[f]["fields"]]
    for i, f1 in enumerate(flist):
        for f2 in flist[i + 1:]:
            m1, m2 = mems[f1], mems[f2]
            if m1["fields"].get("type") != m2["fields"].get("type"):
                continue
            ds = similarity(m1["fields"].get("description", ""), m2["fields"].get("description", ""))
            bs = similarity(m1["body"], m2["body"])
            if ds > SIM_THRESHOLD_CONSOLIDATE or bs > SIM_THRESHOLD_CONSOLIDATE:
                actions.append(("MERGE", f"{f1} ↔ {f2} (desc:{ds:.0%} body:{bs:.0%})"))

    # Stale projects
    cutoff = datetime.now() - timedelta(days=STALE_DAYS)
    for f, m in mems.items():
        if m["fields"] and m["fields"].get("type") == "project" and m["mtime"] < cutoff:
            age = (datetime.now() - m["mtime"]).days
            actions.append(("REVIEW", f"{f}: {age}d old — \"{m['fields'].get('name', '')}\""))

    # Promotion candidates
    claude_text = claude_md.read_text("utf-8").lower() if claude_md.exists() else ""
    groups: dict[str, list[str]] = {}
    for f, m in mems.items():
        if m["fields"] and m["fields"].get("type") == "feedback":
            topic = f.replace("feedback_", "").replace(".md", "").split("_")[0]
            groups.setdefault(topic, []).append(m["fields"].get("name", f))
    for topic, names in sorted(groups.items(), key=lambda x: -len(x[1])):
        if len(names) >= 2 and topic not in claude_text:
            actions.append(("PROMOTE", f"'{topic}' ({len(names)}): {', '.join(names)}"))

    # Cross-ref suggestions
    for i, f1 in enumerate(flist):
        m1_words = set(re.findall(r'\w{4,}', mems[f1]["fields"].get("name", "").lower()))
        for f2 in flist[i + 1:]:
            m2_body_words = set(re.findall(r'\w{4,}', mems[f2]["body"].lower()))
            m2_name_words = set(re.findall(r'\w{4,}', mems[f2]["fields"].get("name", "").lower()))
            m1_body_words = set(re.findall(r'\w{4,}', mems[f1]["body"].lower()))
            if len(m1_words & m2_body_words) >= 2 or len(m2_name_words & m1_body_words) >= 2:
                if f2 not in mems[f1]["body"] and f1 not in mems[f2]["body"]:
                    actions.append(("XREF", f"{f1} ↔ {f2}"))

    # Type balance
    counts = type_dist(mems)
    if counts.get("user", 0) == 0:
        actions.append(("NOTE", "no 'user' memories — consider storing user identity/preferences"))

    # Report
    print(f"memory consolidate — {len(mems)} files ({dist_str(counts)})")

    if not actions:
        print("✓ nothing to consolidate")
        return 0

    for cat in ("MERGE", "REVIEW", "PROMOTE", "XREF", "NOTE"):
        items = [msg for c, msg in actions if c == cat]
        if items:
            labels = {
                "MERGE": "Merge candidates",
                "REVIEW": "Review (stale)",
                "PROMOTE": "Promote to CLAUDE.md",
                "XREF": "Missing cross-refs",
                "NOTE": "Notes",
            }
            print(f"\n{labels[cat]} ({len(items)}):")
            for msg in items:
                print(f"  {msg}")

    return 0


# ── improve (lint + consolidate combined) ─────────────────


def cmd_improve(memory_dir: Path, claude_md: Path, **_):
    mems = load_memories(memory_dir)
    index = parse_index(memory_dir)
    actions = []  # (priority, category, message)

    # ── Lint checks ──
    for f, m in mems.items():
        if m["fields"] is None:
            actions.append((0, "FIX", f"{f}: missing frontmatter"))
            continue
        for field in REQUIRED_FIELDS:
            if field not in m["fields"]:
                actions.append((0, "FIX", f"{f}: missing {field}"))
        if "type" in m["fields"] and m["fields"]["type"] not in VALID_TYPES:
            actions.append((0, "FIX", f"{f}: invalid type '{m['fields']['type']}'"))

    for f in mems:
        if f not in index:
            actions.append((1, "FIX", f"{f}: not in MEMORY.md"))
    for f in index:
        if f not in mems:
            actions.append((0, "FIX", f"MEMORY.md → '{f}' missing"))

    # ── Consolidation checks ──
    cutoff = datetime.now() - timedelta(days=STALE_DAYS)
    for f, m in mems.items():
        if m["fields"] and m["fields"].get("type") == "project" and m["mtime"] < cutoff:
            age = (datetime.now() - m["mtime"]).days
            actions.append((2, "REVIEW", f"{f}: {age}d old"))

    flist = [f for f in mems if mems[f]["fields"]]
    for i, f1 in enumerate(flist):
        for f2 in flist[i + 1:]:
            m1, m2 = mems[f1], mems[f2]
            if m1["fields"].get("type") != m2["fields"].get("type"):
                continue
            ds = similarity(m1["fields"].get("description", ""), m2["fields"].get("description", ""))
            bs = similarity(m1["body"], m2["body"])
            if ds > SIM_THRESHOLD_CONSOLIDATE or bs > SIM_THRESHOLD_CONSOLIDATE:
                actions.append((2, "MERGE", f"{f1} ↔ {f2} ({ds:.0%}/{bs:.0%})"))

    claude_text = claude_md.read_text("utf-8").lower() if claude_md.exists() else ""
    groups: dict[str, list[str]] = {}
    for f, m in mems.items():
        if m["fields"] and m["fields"].get("type") == "feedback":
            topic = f.replace("feedback_", "").replace(".md", "").split("_")[0]
            groups.setdefault(topic, []).append(m["fields"].get("name", f))
    for topic, names in sorted(groups.items(), key=lambda x: -len(x[1])):
        if len(names) >= 2 and topic not in claude_text:
            actions.append((3, "PROMOTE", f"'{topic}' ({len(names)}): {', '.join(names)}"))

    counts = type_dist(mems)
    if counts.get("user", 0) == 0:
        actions.append((3, "NOTE", "no 'user' memories"))

    # ── Report ──
    print(f"Memory: {len(mems)} files ({dist_str(counts)})")

    if not actions:
        print("Health: ✓ all good")
        return 0

    actions.sort(key=lambda x: x[0])

    for cat in ("FIX", "MERGE", "REVIEW", "PROMOTE", "NOTE"):
        items = [msg for _, c, msg in actions if c == cat]
        if items:
            labels = {
                "FIX": "⚠ Fix now",
                "MERGE": "Consider merging",
                "REVIEW": "Review needed",
                "PROMOTE": "Ready to promote",
                "NOTE": "Notes",
            }
            print(f"\n{labels[cat]} ({len(items)}):")
            for msg in items:
                print(f"  {msg}")

    fixes = sum(1 for _, c, _ in actions if c == "FIX")
    health = max(0, 100 - fixes * 20 - (len(actions) - fixes) * 5)
    print(f"\nHealth: {health}/100")
    return 1 if fixes else 0


# ── stats ─────────────────────────────────────────────────


def cmd_stats(memory_dir: Path, **_):
    mems = load_memories(memory_dir)
    counts = type_dist(mems)

    print(f"Total: {len(mems)} memories")
    print()
    for t in ("user", "feedback", "project", "reference"):
        c = counts.get(t, 0)
        bar = "█" * c
        print(f"  {t:12s} {c:3d}  {bar}")

    # Oldest / newest
    if mems:
        oldest = min(mems.items(), key=lambda x: x[1]["mtime"])
        newest = max(mems.items(), key=lambda x: x[1]["mtime"])
        print(f"\n  oldest: {oldest[0]} ({oldest[1]['mtime'].strftime('%Y-%m-%d')})")
        print(f"  newest: {newest[0]} ({newest[1]['mtime'].strftime('%Y-%m-%d')})")

    return 0


# ── Main ──────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="memory",
        description="Auto-memory management CLI",
    )
    parser.add_argument("--memory-dir", default=str(DEFAULT_MEMORY_DIR))
    parser.add_argument("--claude-md", default=str(DEFAULT_CLAUDE_MD))

    sub = parser.add_subparsers(dest="command")
    sub.add_parser("lint", help="Check format and structural integrity")
    sub.add_parser("consolidate", help="Semantic analysis: duplicates, staleness, promotions")
    sub.add_parser("improve", help="Combined lint + consolidate (session startup)")
    sub.add_parser("stats", help="Quick memory distribution overview")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    kwargs = {"memory_dir": Path(args.memory_dir), "claude_md": Path(args.claude_md)}
    cmds = {"lint": cmd_lint, "consolidate": cmd_consolidate, "improve": cmd_improve, "stats": cmd_stats}
    sys.exit(cmds[args.command](**kwargs))


if __name__ == "__main__":
    main()
