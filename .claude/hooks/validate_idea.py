#!/usr/bin/env python3
"""PostToolUse hook: validate an idea the moment a file inside it is written.

Registered in ``.claude/settings.json`` for ``Write`` and ``Edit``. Claude Code
sends the event JSON on stdin, including ``tool_input.file_path``.

If the written file sits inside ``memory/ideas/<slug>/`` this runs the project's
own harness for that idea. On a contract violation it writes the errors to stderr
and exits 2. On PostToolUse exit 2 does not block anything, because the write has
already happened; it surfaces stderr to Claude, which is exactly what is wanted
here: the agent is told which contract it broke while it still has the context to
fix it.

Note on rule 10: stderr is this script's documented interface with Claude Code.

Fails open. Anything unexpected exits 0 in silence rather than interrupting work.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

# .claude/hooks/validate_idea.py -> project root is three levels up.
ROOT = Path(__file__).resolve().parent.parent.parent
HARNESS = ROOT / "tests" / "validate_memory.py"
TIMEOUT_SECONDS = 25
MAX_REPORTED_ERRORS = 12


def read_event() -> dict:
    """Return the hook event JSON from stdin, or an empty dict if unreadable."""
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def idea_slug_for(file_path: str) -> str | None:
    """Return the idea slug when file_path is inside memory/ideas/<slug>/, else None."""
    if not file_path:
        return None
    try:
        parts = Path(file_path).resolve().relative_to(ROOT).parts
    except (ValueError, OSError):
        # Outside the project, or an unresolvable path. Not our concern.
        return None
    if len(parts) >= 3 and parts[0] == "memory" and parts[1] == "ideas":
        return parts[2]
    return None


def main() -> int:
    """Validate the touched idea; exit 2 with errors on stderr if it fails."""
    event = read_event()
    tool_input = event.get("tool_input") or {}
    slug = idea_slug_for(tool_input.get("file_path", ""))
    if slug is None or not HARNESS.is_file():
        return 0
    if not (ROOT / "memory" / "ideas" / slug).is_dir():
        return 0

    try:
        result = subprocess.run(
            [sys.executable, "-B", str(HARNESS), "--idea", slug],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=str(ROOT),
        )
    except (subprocess.TimeoutExpired, OSError):
        # A slow or unavailable harness is not the agent's problem to solve now.
        return 0

    if result.returncode == 0:
        return 0

    errors = [line for line in result.stdout.splitlines() if line.startswith("ERROR")]
    if not errors:
        return 0

    print(
        f"FindMeSaaS contract check failed for idea '{slug}'. "
        f"Fix these before continuing:",
        file=sys.stderr,
    )
    for line in errors[:MAX_REPORTED_ERRORS]:
        print(f"  {line}", file=sys.stderr)
    if len(errors) > MAX_REPORTED_ERRORS:
        print(f"  ... and {len(errors) - MAX_REPORTED_ERRORS} more.", file=sys.stderr)
    print(
        f"  Run: python tests/validate_memory.py --idea {slug}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # noqa: BLE001 - a hook must never break the session
        sys.exit(0)
