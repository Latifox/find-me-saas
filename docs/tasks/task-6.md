# Task 6 — Distribution: npx installer, slash commands, autonomous mode, hooks

**Origin:** user request on 2026-09-06 — add slash commands (one per job), an `npx` installer, an autonomous mode, installation docs, and hooks.
**Agent:** none assigned.
**Scope:** `bin/`, `package.json`, `.claude/skills/` (command definitions), `.claude/hooks/`, `.claude/settings.json`, `tests/`, `README.md`, `CONTRIBUTING.md`, `.gitignore`.

## Problem statement

FindMeSaaS currently installs by cloning the repository and talking to the agent in prose. That works, but it puts three barriers in front of a new user: they must clone a whole repo rather than add capability to a project they already have, they must remember what to say instead of discovering commands, and nothing enforces the output contract at the moment output is written. There is also no way to run the pipeline end to end without supervising each step.

## Verified platform formats

Fetched from the official documentation during planning, not assumed:

- **Commands** are `.claude/skills/<name>/SKILL.md`; the directory name becomes the command. Frontmatter supports `name`, `description`, `argument-hint`, `arguments`, `allowed-tools`, `disable-model-invocation`, `model`. Arguments interpolate as `$ARGUMENTS`, `$0`/`$1`/`$2`, or named via the `arguments` array. `${CLAUDE_PROJECT_DIR}` resolves the project root. Namespacing by arbitrary subdirectory is **not** available; command names are flat, so names must be chosen to avoid collision.
- **Hooks** live under a `hooks` key in `.claude/settings.json`, shaped as `{ EventName: [ { matcher, hooks: [ { type, command, ... } ] } ] }`. Command hooks receive the event JSON on **stdin** and use `${CLAUDE_PROJECT_DIR}` for paths. On `SessionStart`, plain stdout at exit 0 is added to Claude's context. On `PostToolUse`, exit 2 does not block (the tool already ran) but surfaces stderr to Claude, which is the correct mechanism for "you wrote an invalid file, fix it".

## Requirements

- R1 MUST add an npm package with a `bin` entry so `npx find-me-saas init` installs the system into an existing project directory.
- R2 The installer MUST support `--platform claude|codex|cursor|all` (default `all`), `--force` to overwrite, and `--dry-run`; MUST never overwrite an existing `memory/user_profile.md` or any `memory/ideas/` content without `--force`; and MUST print what it wrote.
- R3 The installer MUST have zero runtime dependencies and MUST work on Windows, macOS and Linux.
- R4 MUST add one slash command per job: onboarding, idea generation, full validation, fast gut check, market scan, pivot, autonomous run, idea status, and memory verification.
- R5 The autonomous command MUST run onboarding if no profile exists, generate and rank candidates, fully validate the top candidate, write the memo, run the harness, and report — without stopping to ask questions mid-run, recording any gaps instead of blocking on them.
- R6 MUST add hooks: a `SessionStart` hook that reports profile and idea status into context, and a `PostToolUse` hook that validates an idea directory whenever a file inside it is written and surfaces any contract error to Claude.
- R7 Hook scripts MUST be Python (the harness language already required), not shell, so they run on Windows without `jq` or a POSIX shell.
- R8 MUST extend `--check-specs` so the commands and hooks are enforced: every declared command directory exists with valid frontmatter, and `settings.json` registers both hooks pointing at scripts that exist.
- R9 MUST document installation and the command table in `README.md`, and explain the two kinds of `.claude/skills/` entry in `CONTRIBUTING.md`.
- R10 MUST keep every existing test green: `--check-specs` at zero errors, both live runs clean, the fixture suite at documented counts, and `--baseline` exiting zero.

## Acceptance criteria

- `node bin/cli.js init --dry-run` in a temporary directory lists the files it would write and exits 0.
- A real install into a temporary directory produces a working tree, and `python tests/validate_memory.py --check-specs` passes from inside it.
- `python tests/validate_memory.py --check-specs` exits 0 in this repository with the new assertions.
- Both hook scripts run standalone against sample stdin JSON and exit 0.
- Nine command directories exist, each with a `description` and an `argument-hint` where arguments apply.

## Dependencies

Tasks 1 to 5. Node 18+ for the installer (present: v26). Python 3.10+ for hooks and harness.
