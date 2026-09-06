# Task 2 — Workflow Paths: fast-path validation, micro-pivot, pivot slug rule, quick market scan

**Origin:** backlog from task 1 (four `<!-- TODO (task-2) -->` comments in `workflows/`), user request `/go task 2` on 2026-09-06.
**Agent:** none assigned (orchestrator edits canonical specs and the harness).
**Scope:** `workflows/`, `skills/idea-scoring`, `skills/pivot-engine`, `skills/decision-memo`, `memory/README.md`, `tests/`, `CLAUDE.md`, `AGENTS.md`.

## Problem statement

Every validation today is the full 10-step chain (~15 minutes with web research) and every pivot is the full 4-step chain. Users who want a 3-minute gut check, or who want to test "what if I charge per client instead of per seat", have no sanctioned path, so the orchestrator improvises and the harness cannot check the result. The workflows also never say when a pivot becomes a new idea, so pivots overwrite the original's files.

## Requirements

- R1 MUST add a **fast-path validation** to `workflows/idea-validation.md`: trend-analysis on one platform, competitor-mapper in light mode (3 direct competitors, no review mining), desire-evaluator, distribution-analysis, then idea-scoring with `scoring_stage: fast-validation`. No memo; an inline gut-check summary and an offer to complete the full chain.
- R2 MUST define `fast-validation` in `skills/idea-scoring`: four dimensions (demand, competition, distribution, founder-market fit), verdict issued from the standard table with the missing-input discount (4/6) applied, RAT required, `score_confidence` at most medium, and a mandatory sentence that the score is a gut check.
- R3 MUST add a **micro-pivot** path to `workflows/pivot-optimization.md`: the user names one variable (pricing, audience, channel, platform, feature emphasis); weakness-detection is skipped; pivot-engine generates exactly one option with `pivot_scope: micro`; idea-scoring re-scores it to `pivot_scores.json`.
- R4 MUST define the **slug rule** in `skills/pivot-engine` and `workflows/pivot-optimization.md`: a pivot that changes one variable updates the idea in place (`pivot_scores.json`, memo version note); a pivot that changes two variables, the `business_model`, or the core problem creates a new idea directory `<slug>-<pivot-word>` whose `idea.md` carries `pivot_of: <old-slug>`, and the old `idea.md` gets `status: paused` and `superseded_by: <new-slug>`.
- R5 MUST document `pivot_of` and `superseded_by` (idea.md frontmatter) and the `fast-validation` stage in `memory/README.md`.
- R6 MUST add a **quick scan** option to `workflows/market-deep-dive.md`: trend-analysis only (one or two platforms), no competitor map or sizing, and a stated exit output.
- R7 MUST extend the harness: `scoring_stage` enum gains `fast-validation` (verdict + RAT required, at most 4 scored dimensions, confidence not high); `pivot_options.json` schema gains `pivot_scope` (`micro | standard`) and requires exactly one option when micro; `idea.md` accepts `pivot_of` and `superseded_by`, and a `superseded_by` idea must have status `paused` or `dropped`; `--check-specs` asserts the fast path, micro-pivot, slug rule, and quick scan sections exist and that no `(task-2)` TODO remains.
- R8 MUST add fixtures for a fast-validation run, a micro pivot_options.json with pivot_scores.json, and a superseded idea, with expected pass results, and one broken micro pivot (two options) with an expected failure.
- R9 MUST remove the four `(task-2)` TODO comments by resolving them.
- R10 SHOULD add the fast path and micro-pivot triggers to the intent routers in `CLAUDE.md` and `AGENTS.md`.
- R11 SHOULD have `decision-memo` state the memo version rule for in-place pivots (`_v2 — re-scored after <pivot>_`) and the pointer rule for new-slug pivots (old memo gets a one-line "superseded by" footer).

## Out of scope (task 3 backlog)

Live web-research validation runs (one B2B, one B2C) against the task-1 specs. They are the acceptance test for task 1 and need a session with web access.

## Acceptance criteria

- `python tests/validate_memory.py --check-specs` exits 0 with the new assertions.
- Fixtures: fast-validation idea, micro-pivot idea, superseded idea exit 0; broken micro pivot exits 1.
- `grep -rn "task-2" workflows skills` returns nothing.

## Dependencies

Task 1 (DONE). `docs/DECISIONS.md` does not exist.
