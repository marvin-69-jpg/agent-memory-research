#!/usr/bin/env python3
"""
memory-selfimprove.py — Session-start self-improvement pipeline.

Designed to be run at the start of each new Claude Code session.
Combines lint + consolidation into a single actionable report.

Outputs a concise summary the agent can act on immediately:
  - Errors that need fixing NOW
  - Memories to merge, update, or remove
  - Feedback patterns ready to promote to CLAUDE.md
  - Overall health score

Usage:
  python3 tools/memory-selfimprove.py [--memory-dir PATH] [--claude-md PATH]
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from difflib import SequenceMatcher

MEMORY_DIR = Path("/home/node/.claude/projects/-home-node/memory/")
CLAUDE_MD = Path("/home/node/CLAUDE.md")
STALE_DAYS = 14
SIM_THRESHOLD = 0.6


def parse_frontmatter(text):
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


def load(d):
    mems = {}
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md") or f == "MEMORY.md":
            continue
        p = d / f
        fields, body = parse_frontmatter(p.read_text("utf-8"))
        if fields:
            mems[f] = {"fields": fields, "body": body, "mtime": datetime.fromtimestamp(p.stat().st_mtime)}
    return mems


def parse_index(d):
    idx = {}
    p = d / "MEMORY.md"
    if p.exists():
        for line in p.read_text("utf-8").splitlines():
            m = re.match(r"- \[.+?\]\((.+?)\)", line)
            if m:
                idx[m.group(1)] = True
    return idx


def run(memory_dir=MEMORY_DIR, claude_md=CLAUDE_MD):
    mems = load(memory_dir)
    index = parse_index(memory_dir)
    actions = []  # (priority, category, message)

    # --- 1. Lint: structural errors ---
    for f, m in mems.items():
        for field in ("name", "description", "type"):
            if field not in m["fields"]:
                actions.append((0, "FIX", f"{f}: missing {field}"))
        if m["fields"].get("type") not in ("user", "feedback", "project", "reference"):
            actions.append((0, "FIX", f"{f}: invalid type '{m['fields'].get('type')}'"))

    # Index sync
    for f in mems:
        if f not in index:
            actions.append((1, "FIX", f"{f}: not in MEMORY.md index"))
    for f in index:
        if f not in mems:
            actions.append((0, "FIX", f"MEMORY.md points to '{f}' but file missing"))

    # --- 2. Stale project memories ---
    cutoff = datetime.now() - timedelta(days=STALE_DAYS)
    for f, m in mems.items():
        if m["fields"].get("type") == "project" and m["mtime"] < cutoff:
            age = (datetime.now() - m["mtime"]).days
            actions.append((2, "REVIEW", f"{f}: project memory {age}d old, may be stale"))

    # --- 3. Near-duplicates ---
    flist = list(mems.keys())
    for i, f1 in enumerate(flist):
        for f2 in flist[i + 1:]:
            if mems[f1]["fields"].get("type") != mems[f2]["fields"].get("type"):
                continue
            ds = SequenceMatcher(None, mems[f1]["fields"].get("description", "").lower(),
                                mems[f2]["fields"].get("description", "").lower()).ratio()
            bs = SequenceMatcher(None, mems[f1]["body"].lower(), mems[f2]["body"].lower()).ratio()
            if ds > SIM_THRESHOLD or bs > SIM_THRESHOLD:
                actions.append((2, "MERGE", f"{f1} ↔ {f2} (desc:{ds:.0%} body:{bs:.0%})"))

    # --- 4. Promotion candidates ---
    claude_text = claude_md.read_text("utf-8").lower() if claude_md.exists() else ""
    groups = {}
    for f, m in mems.items():
        if m["fields"].get("type") != "feedback":
            continue
        topic = f.replace("feedback_", "").replace(".md", "").split("_")[0]
        groups.setdefault(topic, []).append((f, m["fields"].get("name", f)))
    for topic, files in sorted(groups.items(), key=lambda x: -len(x[1])):
        if len(files) >= 2 and topic not in claude_text:
            names = ", ".join(n for _, n in files)
            actions.append((3, "PROMOTE", f"topic '{topic}' ({len(files)} feedbacks: {names})"))

    # --- 5. Type balance ---
    types = {}
    for m in mems.values():
        t = m["fields"].get("type", "?")
        types[t] = types.get(t, 0) + 1
    if types.get("user", 0) == 0:
        actions.append((3, "NOTE", "No 'user' memories — consider storing user identity/preferences"))

    return actions, mems, types


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-dir", default=str(MEMORY_DIR))
    parser.add_argument("--claude-md", default=str(CLAUDE_MD))
    args = parser.parse_args()

    actions, mems, types = run(Path(args.memory_dir), Path(args.claude_md))

    dist = ", ".join(f"{t}:{c}" for t, c in sorted(types.items()))
    print(f"Memory: {len(mems)} files ({dist})")

    if not actions:
        print("Health: ✓ all good")
        return

    # Sort by priority
    actions.sort(key=lambda x: x[0])

    fixes = [a for a in actions if a[1] == "FIX"]
    others = [a for a in actions if a[1] != "FIX"]

    if fixes:
        print(f"\n⚠ NEEDS FIXING ({len(fixes)}):")
        for _, cat, msg in fixes:
            print(f"  {msg}")

    for cat in ("MERGE", "REVIEW", "PROMOTE", "NOTE"):
        items = [a for a in others if a[1] == cat]
        if items:
            labels = {"MERGE": "Consider merging", "REVIEW": "Review needed",
                      "PROMOTE": "Ready to promote to CLAUDE.md", "NOTE": "Notes"}
            print(f"\n{labels[cat]} ({len(items)}):")
            for _, _, msg in items:
                print(f"  {msg}")

    # Health score
    error_count = len(fixes)
    health = max(0, 100 - error_count * 20 - len(others) * 5)
    print(f"\nHealth: {health}/100")


if __name__ == "__main__":
    main()
