# Task 3 — Live validation runs against the new specs

**Origin:** acceptance test deferred from task 1 (sequence step 8, `[human-action]`), backlog line on `docs/BOARD.md`, user `/go` on 2026-09-06.
**Agent:** none assigned (the orchestrator runs the workflows itself).
**Scope:** `memory/ideas/<slug>/`, `memory/market_insights/`, `memory/user_profile.md`; spec files only if a defect is found.

## Problem statement

Tasks 1 and 2 rewrote the skill specs and built a harness, but every check so far has been static: string assertions and synthetic fixtures. No skill has actually been executed against the new rubrics with real research. Until a real run happens, three things are unproven: that the B2B lane produces the fields it promises without improvisation, that the B2C lane still works after the lane split, and that a real run passes the harness rather than only a fixture built to pass it.

## Requirements

- R1 MUST run the full `idea-validation` chain on one **B2B** idea with real web research, producing all eight dimension files, `scores.json` at `full-validation`, and `decision_memo.md`.
- R2 MUST run the full `idea-validation` chain on one **B2C** idea with real web research, producing the same set in the B2C lane.
- R3 MUST have both runs pass `python tests/validate_memory.py --idea <slug>` with exit 0.
- R4 MUST verify neither run contains improvisation language ("assumes B2C", "replaced with an equivalent", or a `methodology_note` explaining that a rubric did not fit).
- R5 MUST exercise the B2B lane specifically: `discovery_channel_score` in distribution, `cac_by_channel_b2b` with `ltv_cases` and `gross_margin`, `recommended_tiers` with an anchor in pricing, `icp_count` in market sizing, G2/Capterra or equivalent review sources in competitors.
- R6 MUST exercise the B2C lane specifically: `platform_advantage.aso_score_breakdown`, `creator_economy_fit`, `cac_by_channel` object form, `wtp_range` with a category benchmark, a B2C capture rate in market sizing.
- R7 MUST run the new `b2b-communities` trend prompt at least once and write a conforming `market_insights` file with a `## Sources` section.
- R8 MUST capture the profile-gap gate: ask the three constraint questions before `cac-modeler` and write the answers to `memory/user_profile.md`.
- R9 MUST record every defect found in the specs during the runs, and fix only those that block a run; anything else becomes a task-4 backlog line.
- R10 SHOULD produce memos that meet the 600-900 word budget with a Devil's Advocate section and at least three cited URLs.
- R11 SHOULD demonstrate the competition-prior correction: state how far the researched competition score moved from the capped candidate-stage prior when the B2B idea has a prior quick-score.

## Acceptance criteria

- `python tests/validate_memory.py --idea <b2b-slug>` and `--idea <b2c-slug>` both exit 0.
- `grep -rniE "assumes b2c|replaced with an equivalent" memory/ideas/<b2b-slug> memory/ideas/<b2c-slug>` returns nothing.
- Both `idea.md` files end at `status: scored` with `validated_at` set.
- At least one new `market_insights` file with `platform: b2b-communities`.
- Defects found are logged in `.ay/plans/task-3/references/defects.md`.

## Dependencies

Tasks 1 and 2 (DONE). Requires web access (WebSearch, WebFetch; both allowed in `.claude/settings.json`).
