#!/usr/bin/env python3
"""
memory-consolidate.py — Sleep-time memory consolidation.

Analyzes memory files and produces actionable recommendations:
  1. Merge near-duplicate memories
  2. Flag stale project memories for review/removal
  3. Identify feedback patterns stable enough to promote to CLAUDE.md
  4. Detect missing cross-references between related memories

Does NOT auto-modify files — outputs a report for the agent to act on.

Usage:
  python3 tools/memory-consolidate.py [--memory-dir PATH] [--claude-md PATH]
"""

import argparse
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from difflib import SequenceMatcher

STALE_PROJECT_DAYS = 14
SIMILARITY_THRESHOLD = 0.6  # description similarity for potential merges
PROMOTION_KEYWORD_GROUPS = [
    # Groups of keywords that indicate a coherent theme — if 3+ feedback
    # memories share a theme, the pattern is stable enough to consider promotion
]


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
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


def load_memories(memory_dir: Path) -> dict:
    memories = {}
    for fname in sorted(os.listdir(memory_dir)):
        if not fname.endswith(".md") or fname == "MEMORY.md":
            continue
        fpath = memory_dir / fname
        text = fpath.read_text(encoding="utf-8")
        fields, body = parse_frontmatter(text)
        if fields is None:
            continue
        memories[fname] = {
            "fields": fields,
            "body": body,
            "mtime": datetime.fromtimestamp(fpath.stat().st_mtime),
            "path": fpath,
        }
    return memories


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_merge_candidates(memories: dict) -> list[dict]:
    """Find pairs of memories with similar descriptions or overlapping content."""
    candidates = []
    fnames = list(memories.keys())
    for i, f1 in enumerate(fnames):
        for f2 in fnames[i + 1:]:
            m1, m2 = memories[f1], memories[f2]
            # Same type only
            if m1["fields"].get("type") != m2["fields"].get("type"):
                continue
            desc_sim = similarity(
                m1["fields"].get("description", ""),
                m2["fields"].get("description", ""),
            )
            body_sim = similarity(m1["body"], m2["body"])
            # Either description or body is very similar
            if desc_sim > SIMILARITY_THRESHOLD or body_sim > SIMILARITY_THRESHOLD:
                candidates.append({
                    "file1": f1,
                    "file2": f2,
                    "desc_similarity": desc_sim,
                    "body_similarity": body_sim,
                    "type": m1["fields"].get("type"),
                })
    return candidates


def find_stale_projects(memories: dict) -> list[dict]:
    """Find project memories that haven't been updated recently."""
    stale = []
    cutoff = datetime.now() - timedelta(days=STALE_PROJECT_DAYS)
    for fname, mem in memories.items():
        if mem["fields"].get("type") == "project" and mem["mtime"] < cutoff:
            age = (datetime.now() - mem["mtime"]).days
            stale.append({"file": fname, "age_days": age, "name": mem["fields"].get("name", "")})
    return stale


def find_promotion_candidates(memories: dict, claude_md_path: Path) -> list[dict]:
    """Find feedback clusters that could be promoted to CLAUDE.md rules.

    A feedback is promotable if:
    - There are 2+ feedback memories about the same topic area
    - The topic is not already covered in CLAUDE.md
    """
    claude_md_text = ""
    if claude_md_path and claude_md_path.exists():
        claude_md_text = claude_md_path.read_text(encoding="utf-8").lower()

    feedbacks = {
        f: m for f, m in memories.items()
        if m["fields"].get("type") == "feedback"
    }

    # Group by prefix pattern (e.g., feedback_image_*, feedback_pepe_*)
    groups: dict[str, list[str]] = {}
    for fname in feedbacks:
        # Extract topic from filename: feedback_<topic>_detail.md -> topic
        parts = fname.replace("feedback_", "").replace(".md", "").split("_")
        if parts:
            topic = parts[0]
            groups.setdefault(topic, []).append(fname)

    candidates = []
    for topic, files in groups.items():
        if len(files) >= 2:
            # Check if topic is already in CLAUDE.md
            already_covered = topic in claude_md_text
            names = [feedbacks[f]["fields"].get("name", f) for f in files]
            candidates.append({
                "topic": topic,
                "files": files,
                "names": names,
                "count": len(files),
                "already_in_claude_md": already_covered,
            })

    # Sort by count descending
    candidates.sort(key=lambda x: x["count"], reverse=True)
    return candidates


def find_missing_crossrefs(memories: dict) -> list[dict]:
    """Find memories that mention each other's topics but don't cross-reference."""
    suggestions = []
    fnames = list(memories.keys())
    for i, f1 in enumerate(fnames):
        m1_name = memories[f1]["fields"].get("name", "").lower()
        m1_words = set(re.findall(r'\w{4,}', m1_name))  # words >= 4 chars
        for f2 in fnames[i + 1:]:
            m2_body = memories[f2]["body"].lower()
            m2_name = memories[f2]["fields"].get("name", "").lower()
            m2_words = set(re.findall(r'\w{4,}', m2_name))
            m1_body = memories[f1]["body"].lower()
            # Check if f1's name keywords appear in f2's body (or vice versa)
            f1_in_f2 = len(m1_words & set(re.findall(r'\w{4,}', m2_body))) >= 2
            f2_in_f1 = len(m2_words & set(re.findall(r'\w{4,}', m1_body))) >= 2
            if f1_in_f2 or f2_in_f1:
                # Check if they already reference each other
                if f2 not in memories[f1]["body"] and f1 not in memories[f2]["body"]:
                    suggestions.append({"file1": f1, "file2": f2})
    return suggestions


def print_report(
    merge_candidates,
    stale_projects,
    promotion_candidates,
    crossref_suggestions,
    memories,
    memory_dir,
):
    print("=" * 60)
    print("  Memory Consolidation Report")
    print("=" * 60)
    print(f"\n  Directory: {memory_dir}")
    print(f"  Total memories: {len(memories)}")

    type_counts = {}
    for m in memories.values():
        t = m["fields"].get("type", "?")
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"  Distribution: {', '.join(f'{t}: {c}' for t, c in sorted(type_counts.items()))}")

    has_anything = any([merge_candidates, stale_projects, promotion_candidates, crossref_suggestions])

    if not has_anything:
        print("\n  ✓ No consolidation actions needed.")
        print()
        return

    # --- Merge candidates ---
    if merge_candidates:
        print(f"\n  MERGE CANDIDATES ({len(merge_candidates)})")
        print(f"  {'─' * 50}")
        for c in merge_candidates:
            print(f"  • {c['file1']} ↔ {c['file2']}")
            print(f"    desc similarity: {c['desc_similarity']:.0%}, body similarity: {c['body_similarity']:.0%}")
        print()

    # --- Stale projects ---
    if stale_projects:
        print(f"\n  STALE PROJECT MEMORIES ({len(stale_projects)})")
        print(f"  {'─' * 50}")
        for s in stale_projects:
            print(f"  • {s['file']} — {s['age_days']} days old — \"{s['name']}\"")
        print()

    # --- Promotion candidates ---
    if promotion_candidates:
        promotable = [c for c in promotion_candidates if not c["already_in_claude_md"]]
        if promotable:
            print(f"\n  FEEDBACK → CLAUDE.MD PROMOTION CANDIDATES ({len(promotable)})")
            print(f"  {'─' * 50}")
            for c in promotable:
                print(f"  • topic: \"{c['topic']}\" ({c['count']} memories)")
                for name in c["names"]:
                    print(f"    - {name}")
            print()

        already = [c for c in promotion_candidates if c["already_in_claude_md"]]
        if already:
            print(f"\n  FEEDBACK CLUSTERS ALREADY IN CLAUDE.MD ({len(already)})")
            print(f"  {'─' * 50}")
            for c in already:
                print(f"  • topic: \"{c['topic']}\" ({c['count']} memories) — already covered")
            print()

    # --- Cross-ref suggestions ---
    if crossref_suggestions:
        print(f"\n  CROSS-REFERENCE SUGGESTIONS ({len(crossref_suggestions)})")
        print(f"  {'─' * 50}")
        for s in crossref_suggestions:
            print(f"  • {s['file1']} ↔ {s['file2']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Memory consolidation analysis")
    parser.add_argument(
        "--memory-dir",
        default="/home/node/.claude/projects/-home-node/memory/",
    )
    parser.add_argument(
        "--claude-md",
        default="/home/node/CLAUDE.md",
        help="Path to CLAUDE.md for promotion checking",
    )
    args = parser.parse_args()

    memory_dir = Path(args.memory_dir)
    claude_md = Path(args.claude_md)
    if not memory_dir.exists():
        print(f"Error: {memory_dir} does not exist", file=sys.stderr)
        sys.exit(1)

    memories = load_memories(memory_dir)
    merge_candidates = find_merge_candidates(memories)
    stale_projects = find_stale_projects(memories)
    promotion_candidates = find_promotion_candidates(memories, claude_md)
    crossref_suggestions = find_missing_crossrefs(memories)

    print_report(
        merge_candidates, stale_projects, promotion_candidates,
        crossref_suggestions, memories, memory_dir,
    )


if __name__ == "__main__":
    main()
