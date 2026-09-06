#!/usr/bin/env python3
"""SessionStart hook: tell Claude where this project stands before it answers.

Registered in ``.claude/settings.json`` for the ``startup`` and ``resume``
matchers. Claude Code sends the event JSON on stdin; on exit 0 whatever this
script writes to stdout is appended to Claude's context for the session.

The output answers three questions the agent would otherwise have to discover by
reading files: does a founder profile exist, what ideas are already in memory,
and is any of them half-finished.

Note on rule 10 (no print in production code): stdout is this script's documented
interface with Claude Code, not debugging output.

Fails open. Any unexpected error exits 0 in silence, because a broken hook must
never stop a session from starting.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# .claude/hooks/session_start.py -> project root is three levels up.
ROOT = Path(__file__).resolve().parent.parent.parent
MAX_LISTED = 5


def read_event() -> dict:
    """Return the hook event JSON from stdin, or an empty dict if unreadable."""
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def frontmatter_value(text: str, key: str) -> str | None:
    """Return a scalar frontmatter value, or None when the key is absent."""
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.M)
    return match.group(1).strip().strip("\"'") if match else None


def describe_ideas() -> tuple[list[str], list[str]]:
    """Return (summary lines per idea, slugs that look unfinished)."""
    ideas_dir = ROOT / "memory" / "ideas"
    if not ideas_dir.is_dir():
        return [], []

    summaries: list[str] = []
    unfinished: list[str] = []
    for path in sorted(p for p in ideas_dir.iterdir() if p.is_dir()):
        idea_md = path / "idea.md"
        if not idea_md.is_file():
            continue
        text = idea_md.read_text(encoding="utf-8-sig", errors="replace")
        status = frontmatter_value(text, "status") or "unknown"
        model = frontmatter_value(text, "business_model") or "unset"

        score = ""
        scores_file = path / "scores.json"
        if scores_file.is_file():
            try:
                doc = json.loads(scores_file.read_text(encoding="utf-8-sig"))
                verdict = doc.get("verdict") or doc.get("rank_label") or ""
                score = f"{doc.get('final_score', '?')}/100 {verdict}".strip()
            except (json.JSONDecodeError, OSError):
                score = "unreadable scores.json"

        summaries.append(f"  {path.name} [{status}, {model}] {score}".rstrip())

        dimension_files = list(path.glob("*.json"))
        if len(dimension_files) >= 3 and not (path / "decision_memo.md").is_file():
            unfinished.append(path.name)
    return summaries, unfinished


def main() -> int:
    """Print a short project status block for Claude, then exit 0."""
    read_event()  # Consume stdin so the caller never blocks on a full pipe.

    lines = ["FindMeSaaS status"]

    profile = ROOT / "memory" / "user_profile.md"
    if profile.is_file():
        text = profile.read_text(encoding="utf-8-sig", errors="replace")
        gaps = [f for f in ("budget_constraint", "risk_tolerance", "time_per_week_hours")
                if f'"{f}": "unknown"' in text or f'"{f}": null' in text]
        if gaps:
            lines.append(f"  Profile exists but these are unset: {', '.join(gaps)}. "
                         "Ask for them before any CAC or kill-criteria work.")
        else:
            lines.append("  Founder profile is present and complete.")
    else:
        lines.append("  No founder profile yet. Run first-run onboarding "
                     "(skills/user-background-interviewer) before any workflow.")

    summaries, unfinished = describe_ideas()
    if summaries:
        lines.append(f"  {len(summaries)} idea(s) in memory:")
        lines.extend(summaries[:MAX_LISTED])
        if len(summaries) > MAX_LISTED:
            lines.append(f"  ... and {len(summaries) - MAX_LISTED} more.")
    else:
        lines.append("  No ideas analysed yet.")

    if unfinished:
        lines.append("  Unfinished (dimension files but no decision memo): "
                     + ", ".join(unfinished[:MAX_LISTED]))

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001 - a hook must never break a session
        sys.exit(0)
