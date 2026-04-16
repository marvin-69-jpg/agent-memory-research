#!/usr/bin/env python3
"""
memory — Unified CLI for auto-memory management.

Subcommands:
  lint            Check memory file format and structural integrity
  consolidate     Semantic analysis: duplicates, staleness, promotion candidates
  improve         Combined lint + consolidate (designed for session startup)
  stats           Quick overview of memory distribution
  recall          Search across memory/ + wiki/ for a query (brain-first lookup)
  brief           Session startup briefing — compressed overview of everything the agent knows
  reconsolidate   Check recalled memories for staleness signals (retrieval-triggered update)

Usage:
  memory lint
  memory consolidate
  memory improve
  memory stats
  memory recall <query> [<query> ...]
  memory brief
  memory reconsolidate <file> [<file> ...]

Global options:
  --memory-dir PATH   Memory directory (default: /home/node/.claude/projects/-home-node/memory/)
  --claude-md PATH    CLAUDE.md path for promotion checking (default: /home/node/CLAUDE.md)
  --wiki-dir PATH     Wiki directory (default: /home/node/agent-memory-research/wiki/)
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
DEFAULT_WIKI_DIR = Path("/home/node/agent-memory-research/wiki/")
DEFAULT_WIKI_INDEX = Path("/home/node/agent-memory-research/index.md")
VALID_TYPES = {"user", "feedback", "project", "reference"}
REQUIRED_FIELDS = {"name", "description", "type"}
STALE_DAYS = 14
SIM_THRESHOLD_LINT = 0.7
SIM_THRESHOLD_CONSOLIDATE = 0.6
RECALL_MAX_HITS = 10
RECALL_CONTEXT_LINES = 2
BRIEF_MAX_WIKI_PAGES = 30

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


def cmd_improve(memory_dir: Path, claude_md: Path, wiki_dir: Path = DEFAULT_WIKI_DIR, **_):
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

    # ── Pending observations in wiki ──
    if wiki_dir.exists():
        for p in sorted(wiki_dir.glob("*.md")):
            try:
                text = p.read_text("utf-8")
            except Exception:
                continue
            if "## Implementation" not in text:
                continue
            # Find sections with pending observations
            in_impl = False
            current_heading = ""
            for line in text.splitlines():
                if line.startswith("## Implementation"):
                    in_impl = True
                    continue
                if in_impl and line.startswith("## "):
                    break
                if in_impl and line.startswith("### "):
                    current_heading = line.lstrip("# ").strip()
                if in_impl and ("待觀察" in line or "待後續" in line or "pending" in line.lower()):
                    # Get page title
                    title = p.stem
                    for tl in text.splitlines():
                        if tl.startswith("# "):
                            title = tl[2:].strip()
                            break
                    label = f"{title}"
                    if current_heading:
                        label += f" → {current_heading}"
                    actions.append((1, "OBSERVE", label))

    # ── Report ──
    print(f"Memory: {len(mems)} files ({dist_str(counts)})")

    if not actions:
        print("Health: ✓ all good")
        return 0

    actions.sort(key=lambda x: x[0])

    for cat in ("FIX", "OBSERVE", "MERGE", "REVIEW", "PROMOTE", "NOTE"):
        items = [msg for _, c, msg in actions if c == cat]
        if items:
            labels = {
                "FIX": "⚠ Fix now",
                "OBSERVE": "👁 Pending observations (wiki Implementation sections)",
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


# ── recall ────────────────────────────────────────────────


def grep_files(directory: Path, query: str, glob_pattern: str = "*.md") -> list[tuple[str, int, str]]:
    """Return list of (filepath, line_no, line_text) matching query (case-insensitive)."""
    hits = []
    q = query.lower()
    for p in sorted(directory.glob(glob_pattern)):
        if p.name.startswith("_") or p.name == "MEMORY.md":
            continue
        try:
            lines = p.read_text("utf-8").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines):
            if q in line.lower():
                hits.append((str(p.relative_to(directory.parent if directory.name == "memory" else directory.parent)), i + 1, line.strip()))
    return hits


def extract_summary(filepath: Path, max_lines: int = 5) -> str:
    """Extract the first meaningful paragraph after the heading (compiled truth)."""
    try:
        text = filepath.read_text("utf-8")
    except Exception:
        return "(unreadable)"
    lines = text.splitlines()
    # Skip frontmatter
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    # Skip title heading
    for i in range(start, len(lines)):
        if lines[i].strip().startswith("# "):
            start = i + 1
            break
    # Collect first non-empty paragraph
    result = []
    for i in range(start, len(lines)):
        line = lines[i].strip()
        if not line:
            if result:
                break
            continue
        if line.startswith("## "):
            if result:
                break
            continue
        result.append(line)
        if len(result) >= max_lines:
            break
    return " ".join(result) if result else "(empty)"


def parse_aliases(text: str) -> list[str]:
    """Extract aliases from frontmatter (YAML list: [a, b, c] or multi-line - a)."""
    fields, _ = parse_frontmatter(text)
    if not fields or "aliases" not in fields:
        return []
    raw = fields["aliases"]
    # Handle [a, b, c] format
    if raw.startswith("[") and raw.endswith("]"):
        return [a.strip().lower() for a in raw[1:-1].split(",") if a.strip()]
    # Single value
    return [raw.strip().lower()] if raw.strip() else []


def extract_numbers(text: str) -> list[float]:
    """Extract all numbers from text (handles commas: 14,700 → 14700)."""
    return [float(m.replace(",", "")) for m in re.findall(r'\d[\d,]*\.?\d*', text)]


def score_directory(directory: Path, keywords: list[str], pattern: str = "*.md", max_results: int = RECALL_MAX_HITS) -> list[tuple[Path, int]]:
    """Score files in a directory by keyword frequency + alias/filename/number boosting + IDF."""
    if not directory.exists():
        return []

    # Pre-extract numbers from query for fuzzy number matching
    query_numbers = extract_numbers(" ".join(keywords))

    # First pass: count document frequency for each keyword (IDF-like)
    all_files: list[tuple[Path, str, str]] = []  # (path, raw_text, lower_text)
    for p in sorted(directory.glob(pattern)):
        if p.name.startswith("_") or p.name == "MEMORY.md":
            continue
        try:
            raw_text = p.read_text("utf-8")
            all_files.append((p, raw_text, raw_text.lower()))
        except Exception:
            continue

    n_docs = len(all_files)
    if n_docs == 0:
        return []

    # Document frequency: how many files contain each keyword
    doc_freq: dict[str, int] = {}
    for kw in keywords:
        doc_freq[kw] = sum(1 for _, _, text in all_files if kw in text)

    # IDF weight: rare keywords matter more (log scale, min weight = 1)
    import math
    idf: dict[str, float] = {}
    for kw in keywords:
        df = doc_freq.get(kw, 0)
        idf[kw] = math.log(n_docs / (1 + df)) + 1 if df > 0 else 0

    # Second pass: score each file
    file_scores: dict[Path, float] = {}
    for p, raw_text, text in all_files:
        # Base score: keyword frequency weighted by IDF
        score = sum(text.count(kw) * idf.get(kw, 1) for kw in keywords)

        # Boost 1: Alias matching — alias hit = +15 per keyword match (strong signal)
        aliases = parse_aliases(raw_text)
        for alias in aliases:
            for kw in keywords:
                if kw in alias or alias in kw:
                    score += 15

        # Boost 2: Filename matching — filename contains keyword = +8
        fname = p.stem.lower().replace("-", " ").replace("_", " ")
        for kw in keywords:
            if kw in fname:
                score += 8

        # Boost 3: Fuzzy number matching — query number within ±10% of text number = +10
        if query_numbers:
            text_numbers = extract_numbers(text)
            for qn in query_numbers:
                for tn in text_numbers:
                    if tn > 0 and abs(qn - tn) / tn <= 0.10:
                        score += 10
                        break  # one match per query number

        if score > 0:
            file_scores[p] = score
    return sorted(file_scores.items(), key=lambda x: -x[1])[:max_results]


def tokenize_query(query: str) -> list[str]:
    """Split query into keywords, with CJK n-gram extraction for better Chinese matching.

    English words split by whitespace. CJK runs are split into 2-grams and 3-grams
    to handle unsegmented Chinese text (e.g., '睡覺時做什麼' → ['睡覺', '覺時', '時做', '做什', '什麼', '睡覺時', '覺時做', '時做什', '做什麼']).
    """
    tokens = []
    # Split into CJK runs vs non-CJK runs
    cjk_range = r'[\u4e00-\u9fff\u3400-\u4dbf]'
    parts = re.split(f'({cjk_range}+)', query.lower())
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if re.match(f'^{cjk_range}+$', part):
            # CJK: extract 2-grams and 3-grams
            for n in (2, 3):
                for i in range(len(part) - n + 1):
                    tokens.append(part[i:i+n])
        else:
            # Non-CJK: split by whitespace
            tokens.extend(w for w in part.split() if w)
    return list(dict.fromkeys(tokens))  # dedupe preserving order


def recall_ranked(memory_dir: Path, wiki_dir: Path, query: str, max_results: int = RECALL_MAX_HITS) -> list[tuple[str, int]]:
    """Return ranked list of (filename, score) across memory/ + wiki/. Used by benchmark."""
    keywords = tokenize_query(query)
    results = []
    for directory in [memory_dir, wiki_dir]:
        for p, score in score_directory(directory, keywords, max_results=max_results * 2):
            results.append((p.name, score))
    results.sort(key=lambda x: -x[1])
    return results[:max_results]


def cmd_recall(memory_dir: Path, wiki_dir: Path, query: list[str], **_):
    q = " ".join(query)
    if not q.strip():
        print("Usage: memory recall <query>")
        return 1

    keywords = tokenize_query(q)
    print(f"recall: searching for '{q}'\n")

    sections = [
        ("memory/", memory_dir, "*.md"),
        ("wiki/", wiki_dir, "*.md"),
    ]

    total_hits = 0
    shown_files = set()

    for label, directory, pattern in sections:
        ranked = score_directory(directory, keywords, pattern)
        if not ranked:
            continue
        print(f"── {label} (showing top {len(ranked)}) ──\n")

        for p, score in ranked:
            rel = p.name
            if rel in shown_files:
                continue
            shown_files.add(rel)

            # Get frontmatter info
            fm_text = p.read_text("utf-8")
            fields, _ = parse_frontmatter(fm_text)
            name = fields.get("name", "") if fields else ""
            ftype = fields.get("type", "") if fields else ""
            desc = fields.get("description", "") if fields else ""

            # For wiki pages, use the page title
            if not name:
                for line in fm_text.splitlines():
                    if line.startswith("# "):
                        name = line[2:].strip()
                        break

            summary = extract_summary(p, max_lines=3)

            header = f"  {rel}"
            if name:
                header += f"  [{name}]"
            if ftype:
                header += f"  ({ftype})"
            print(f"{header}  score={score}")
            if desc:
                print(f"    desc: {desc}")
            print(f"    >>> {summary[:200]}")
            print()
            total_hits += 1

    if total_hits == 0:
        print("(no matches)")

    return 0


# ── brief ────────────────────────────────────────────────


def cmd_brief(memory_dir: Path, wiki_dir: Path, **_):
    mems = load_memories(memory_dir)
    counts = type_dist(mems)

    print("=" * 60)
    print("  MEMORY BRIEF — What you currently know")
    print("=" * 60)

    # ── Auto-memory summary ──
    print(f"\n## Auto-Memory ({len(mems)} files)")
    print(f"   Distribution: {dist_str(counts)}\n")

    # Group by type, show name + description
    by_type: dict[str, list[tuple[str, str, str]]] = {}
    for f, m in mems.items():
        if m["fields"]:
            t = m["fields"].get("type", "?")
            name = m["fields"].get("name", f)
            desc = m["fields"].get("description", "")
            by_type.setdefault(t, []).append((f, name, desc))

    for t in ("user", "feedback", "project", "reference"):
        items = by_type.get(t, [])
        if not items:
            continue
        print(f"  [{t}] ({len(items)})")
        for f, name, desc in items:
            line = f"    - {name}"
            if desc:
                line += f" — {desc[:80]}"
            print(line)
        print()

    # ── Wiki summary ──
    wiki_index = wiki_dir.parent / "index.md" if wiki_dir.exists() else None
    if wiki_index and wiki_index.exists():
        idx_text = wiki_index.read_text("utf-8")
        # Count wiki pages
        wiki_pages = []
        raw_sources = []
        section = None
        for line in idx_text.splitlines():
            if "## Wiki Pages" in line:
                section = "wiki"
                continue
            elif "## Raw Sources" in line:
                section = "raw"
                continue
            if section == "wiki" and line.startswith("|") and "---" not in line and "Page" not in line:
                # Obsidian wiki-links use | as alias separator: [[wiki/name\|Display]]
                # This clashes with markdown table | delimiter. Use regex instead.
                wm = re.match(
                    r'\|\s*\[\[.+?\\\|(.+?)\]\]\s*\|(.+?)\|(.+?)\|(.+?)\|',
                    line
                )
                if wm:
                    display = wm.group(1).strip()
                    summary = wm.group(2).strip()
                    tags = wm.group(3).strip()
                    wiki_pages.append((display, summary, tags))
            elif section == "raw" and line.startswith("|") and "---" not in line and "Date" not in line:
                # Raw sources don't use pipe-alias wiki-links, safe to split
                rm = re.match(r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|', line)
                if rm:
                    raw_sources.append((rm.group(1).strip(), rm.group(3).strip()))

        print(f"## Research Wiki ({len(wiki_pages)} pages, {len(raw_sources)} sources)")
        print(f"   Path: {wiki_dir}\n")

        # Group wiki by tag categories
        concepts = []
        products = []
        people = []
        for display, summary, tags in wiki_pages:
            if "people" in tags:
                people.append((display, summary))
            elif "product" in tags:
                products.append((display, summary))
            else:
                concepts.append((display, summary))

        if concepts:
            print(f"  [concepts] ({len(concepts)})")
            for name, summary in concepts:
                print(f"    - {name} — {summary[:70]}")
            print()

        if products:
            print(f"  [products] ({len(products)})")
            for name, summary in products:
                print(f"    - {name} — {summary[:70]}")
            print()

        if people:
            print(f"  [people] ({len(people)})")
            for name, summary in people:
                print(f"    - {name} — {summary[:70]}")
            print()

        if raw_sources:
            print(f"  [sources] ({len(raw_sources)})")
            for date, title in raw_sources:
                print(f"    - {date}  {title[:60]}")
            print()

    # ── Implemented patterns ──
    print("## Implemented Patterns (applied to openab-bot)")
    impl_pages = []
    if wiki_dir.exists():
        for p in sorted(wiki_dir.glob("*.md")):
            try:
                text = p.read_text("utf-8")
            except Exception:
                continue
            if "## Implementation" in text:
                # Get page title
                for line in text.splitlines():
                    if line.startswith("# "):
                        impl_pages.append(line[2:].strip())
                        break
    if impl_pages:
        for name in impl_pages:
            print(f"    ✅ {name}")
    else:
        print("    (none found)")
    print()

    print("=" * 60)
    print("  Use 'memory recall <query>' to search specific topics")
    print("=" * 60)

    return 0


# ── reconsolidate ────────────────────────────────────────


def cmd_reconsolidate(memory_dir: Path, files: list[str], **_):
    """Check recalled memories for staleness signals.

    Inspired by neuroscience reconsolidation: retrieval is not read-only.
    Each time a memory is recalled, check if it needs updating.

    Signals checked:
    - Age: how long since last modified
    - Description freshness: does it still match the content
    - Body staleness: project/reference memories over STALE_DAYS
    - Content length: suspiciously short memories may need enrichment
    """
    mems = load_memories(memory_dir)
    now = datetime.now()
    suggestions = []

    for fname in files:
        # Normalize filename
        if not fname.endswith(".md"):
            fname += ".md"
        if fname not in mems:
            suggestions.append(("SKIP", fname, "file not found"))
            continue

        m = mems[fname]
        if m["fields"] is None:
            suggestions.append(("FIX", fname, "missing frontmatter — can't reconsolidate"))
            continue

        mtype = m["fields"].get("type", "")
        name = m["fields"].get("name", fname)
        desc = m["fields"].get("description", "")
        body = m["body"]
        age_days = (now - m["mtime"]).days

        # Signal 1: Age-based staleness
        if mtype == "project" and age_days > STALE_DAYS:
            suggestions.append(("STALE", fname,
                f"project memory {age_days}d old — verify '{name}' is still current"))
        elif mtype == "reference" and age_days > 60:
            suggestions.append(("CHECK", fname,
                f"reference {age_days}d old — verify resource still exists"))

        # Signal 2: Description-body drift
        # Only check ASCII words (4+ chars) to avoid CJK tokenization noise
        desc_words = set(re.findall(r'[a-zA-Z]{4,}', desc.lower()))
        body_words = set(re.findall(r'[a-zA-Z]{4,}', body.lower()))
        if desc_words and body_words:
            desc_only = desc_words - body_words
            if len(desc_only) > len(desc_words) * 0.5 and len(desc_only) >= 2:
                suggestions.append(("DRIFT", fname,
                    f"description has words not in body: {', '.join(sorted(desc_only)[:5])}"))

        # Signal 3: Thin content
        body_lines = [l for l in body.splitlines() if l.strip()]
        if len(body_lines) < 2 and mtype in ("feedback", "project"):
            suggestions.append(("THIN", fname,
                f"only {len(body_lines)} line(s) — consider enriching"))

        # Signal 4: Missing Why/How for feedback/project
        if mtype in ("feedback", "project"):
            if "**Why:**" not in body and "**Why**" not in body:
                suggestions.append(("ENRICH", fname,
                    f"{mtype} missing **Why:** — add reasoning for better edge-case judgment"))
            if "**How to apply:**" not in body and "**How to apply**" not in body:
                suggestions.append(("ENRICH", fname,
                    f"{mtype} missing **How to apply:** — add application guidance"))

    # Report
    print(f"reconsolidate — checking {len(files)} recalled memories\n")

    if not suggestions:
        print("✓ all recalled memories look fresh — no reconsolidation needed")
        return 0

    for sev in ("FIX", "STALE", "DRIFT", "CHECK", "THIN", "ENRICH", "SKIP"):
        items = [(f, msg) for s, f, msg in suggestions if s == sev]
        if not items:
            continue
        icons = {
            "FIX": "✗", "STALE": "⏰", "DRIFT": "↔",
            "CHECK": "?", "THIN": "△", "ENRICH": "＋", "SKIP": "·"
        }
        labels = {
            "FIX": "Needs fix", "STALE": "Possibly stale",
            "DRIFT": "Description-body drift", "CHECK": "Verify resource",
            "THIN": "Thin content", "ENRICH": "Missing structure",
            "SKIP": "Skipped",
        }
        print(f"{labels[sev]}:")
        for f, msg in items:
            print(f"  {icons[sev]} {f}: {msg}")
        print()

    actionable = sum(1 for s, _, _ in suggestions if s not in ("SKIP",))
    print(f"{actionable} reconsolidation suggestions — update these memories if current context confirms they're stale")
    return 0


# ── Main ──────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="memory",
        description="Auto-memory management CLI",
    )
    parser.add_argument("--memory-dir", default=str(DEFAULT_MEMORY_DIR))
    parser.add_argument("--claude-md", default=str(DEFAULT_CLAUDE_MD))
    parser.add_argument("--wiki-dir", default=str(DEFAULT_WIKI_DIR))

    sub = parser.add_subparsers(dest="command")
    sub.add_parser("lint", help="Check format and structural integrity")
    sub.add_parser("consolidate", help="Semantic analysis: duplicates, staleness, promotions")
    sub.add_parser("improve", help="Combined lint + consolidate (session startup)")
    sub.add_parser("stats", help="Quick memory distribution overview")
    p_recall = sub.add_parser("recall", help="Search memory/ + wiki/ for a query")
    p_recall.add_argument("query", nargs="+", help="Search keywords")
    sub.add_parser("brief", help="Session startup briefing — what you currently know")
    p_recon = sub.add_parser("reconsolidate", help="Check recalled memories for staleness signals")
    p_recon.add_argument("files", nargs="+", help="Memory filenames to check")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    kwargs = {
        "memory_dir": Path(args.memory_dir),
        "claude_md": Path(args.claude_md),
        "wiki_dir": Path(args.wiki_dir),
    }
    if args.command == "recall":
        kwargs["query"] = args.query
    if args.command == "reconsolidate":
        kwargs["files"] = args.files
    cmds = {
        "lint": cmd_lint,
        "consolidate": cmd_consolidate,
        "improve": cmd_improve,
        "stats": cmd_stats,
        "recall": cmd_recall,
        "brief": cmd_brief,
        "reconsolidate": cmd_reconsolidate,
    }
    sys.exit(cmds[args.command](**kwargs))


if __name__ == "__main__":
    main()
