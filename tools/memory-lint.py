#!/usr/bin/env python3
"""
memory-lint.py — Sleep-time memory quality checker.

Scans the auto-memory directory and reports issues:
  1. Frontmatter problems (missing/invalid fields)
  2. MEMORY.md ↔ file sync (orphans, missing pointers)
  3. feedback/project memories missing Why/How to apply
  4. Stale project memories (older than 14 days)
  5. Duplicate or near-duplicate memories
  6. Type distribution summary

Usage:
  python3 tools/memory-lint.py [--memory-dir PATH] [--fix]

Default memory dir: /home/node/.claude/projects/-home-node/memory/
"""

import argparse
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from difflib import SequenceMatcher

VALID_TYPES = {"user", "feedback", "project", "reference"}
REQUIRED_FIELDS = {"name", "description", "type"}
STALE_DAYS = 14


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    """Parse YAML-ish frontmatter. Returns (fields_dict, body) or (None, text)."""
    if not text.startswith("---"):
        return None, text
    end = text.find("---", 3)
    if end == -1:
        return None, text
    fm_text = text[3:end].strip()
    fields = {}
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fields[key.strip()] = val.strip()
    body = text[end + 3:].strip()
    return fields, body


def parse_memory_md(path: Path) -> dict[str, str]:
    """Parse MEMORY.md, return {filename: title} mapping."""
    entries = {}
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    for line in text.splitlines():
        m = re.match(r"- \[(.+?)\]\((.+?)\)", line)
        if m:
            title, filename = m.group(1), m.group(2)
            entries[filename] = title
    return entries


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def lint(memory_dir: Path) -> list[dict]:
    """Run all lint checks. Returns list of {file, severity, message}."""
    issues = []

    def warn(file: str, msg: str, severity: str = "warning"):
        issues.append({"file": file, "severity": severity, "message": msg})

    # --- Load all memory files ---
    md_files = sorted(
        f for f in os.listdir(memory_dir)
        if f.endswith(".md") and f != "MEMORY.md"
    )

    memories = {}  # filename -> {fields, body, mtime}
    for fname in md_files:
        fpath = memory_dir / fname
        text = fpath.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(text)
        stat = fpath.stat()
        memories[fname] = {
            "fields": fields,
            "body": body,
            "mtime": datetime.fromtimestamp(stat.st_mtime),
        }

    # --- Load MEMORY.md index ---
    index = parse_memory_md(memory_dir / "MEMORY.md")

    # === Check 1: Frontmatter validity ===
    for fname, mem in memories.items():
        if mem["fields"] is None:
            warn(fname, "Missing frontmatter (no --- block)", "error")
            continue
        for field in REQUIRED_FIELDS:
            if field not in mem["fields"]:
                warn(fname, f"Missing required field: {field}", "error")
        if "type" in mem["fields"] and mem["fields"]["type"] not in VALID_TYPES:
            warn(fname, f"Invalid type: '{mem['fields']['type']}' (valid: {VALID_TYPES})", "error")

    # === Check 2: MEMORY.md sync ===
    for fname in md_files:
        if fname not in index:
            warn(fname, "File exists but no entry in MEMORY.md", "warning")
    for fname in index:
        if fname not in memories:
            warn("MEMORY.md", f"Points to '{fname}' but file doesn't exist", "error")

    # === Check 3: feedback/project should have Why/How ===
    for fname, mem in memories.items():
        if mem["fields"] is None:
            continue
        mtype = mem["fields"].get("type", "")
        if mtype in ("feedback", "project"):
            body = mem["body"]
            if "**Why:**" not in body and "**Why**" not in body:
                warn(fname, f"{mtype} memory missing **Why:** section", "info")
            if "**How to apply:**" not in body and "**How to apply**" not in body:
                warn(fname, f"{mtype} memory missing **How to apply:** section", "info")

    # === Check 4: Stale project memories ===
    cutoff = datetime.now() - timedelta(days=STALE_DAYS)
    for fname, mem in memories.items():
        if mem["fields"] is None:
            continue
        if mem["fields"].get("type") == "project" and mem["mtime"] < cutoff:
            age = (datetime.now() - mem["mtime"]).days
            warn(fname, f"Project memory is {age} days old — may be stale", "warning")

    # === Check 5: Near-duplicate detection ===
    fnames = [f for f in memories if memories[f]["fields"] is not None]
    for i, f1 in enumerate(fnames):
        for f2 in fnames[i + 1:]:
            desc1 = memories[f1]["fields"].get("description", "")
            desc2 = memories[f2]["fields"].get("description", "")
            sim = similarity(desc1, desc2)
            if sim > 0.7:
                warn(f1, f"Similar to {f2} (similarity: {sim:.0%})", "warning")

    return issues


def print_report(issues: list[dict], memories: dict, memory_dir: Path):
    """Print human-readable lint report."""
    # --- Summary ---
    type_counts = {}
    for mem in memories.values():
        if mem["fields"]:
            t = mem["fields"].get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1

    print("=" * 60)
    print("  Memory Lint Report")
    print("=" * 60)
    print(f"\n  Directory: {memory_dir}")
    print(f"  Total files: {len(memories)}")
    print(f"  Distribution: {', '.join(f'{t}: {c}' for t, c in sorted(type_counts.items()))}")
    print()

    if not issues:
        print("  ✓ No issues found.")
        print()
        return

    # --- Issues by severity ---
    for sev in ("error", "warning", "info"):
        sev_issues = [i for i in issues if i["severity"] == sev]
        if not sev_issues:
            continue
        icon = {"error": "✗", "warning": "△", "info": "·"}[sev]
        print(f"  {sev.upper()} ({len(sev_issues)})")
        print(f"  {'─' * 50}")
        for issue in sev_issues:
            print(f"  {icon} {issue['file']}: {issue['message']}")
        print()

    errors = sum(1 for i in issues if i["severity"] == "error")
    warnings = sum(1 for i in issues if i["severity"] == "warning")
    infos = sum(1 for i in issues if i["severity"] == "info")
    print(f"  Total: {errors} errors, {warnings} warnings, {infos} info")
    print()


def main():
    parser = argparse.ArgumentParser(description="Lint auto-memory files")
    parser.add_argument(
        "--memory-dir",
        default="/home/node/.claude/projects/-home-node/memory/",
        help="Path to memory directory",
    )
    args = parser.parse_args()

    memory_dir = Path(args.memory_dir)
    if not memory_dir.exists():
        print(f"Error: {memory_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    issues = lint(memory_dir)

    # Build memories dict for report
    memories = {}
    for fname in os.listdir(memory_dir):
        if fname.endswith(".md") and fname != "MEMORY.md":
            fpath = memory_dir / fname
            text = fpath.read_text(encoding="utf-8")
            fields, body = parse_frontmatter(text)
            memories[fname] = {"fields": fields, "body": body, "mtime": datetime.fromtimestamp(fpath.stat().st_mtime)}

    print_report(issues, memories, memory_dir)

    errors = sum(1 for i in issues if i["severity"] == "error")
    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()
