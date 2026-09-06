# Task 4 — Spec fixes from the live runs

**Origin:** four defects logged during the task-3 live validations. Full evidence in `.ay/plans/task-3/references/defects.md`.
**Agent:** none assigned.
**Scope:** `skills/decision-memo`, `skills/cac-modeler`, `skills/idea-scoring`, `skills/trend-analysis`, `tests/`.

## Problem statement

Two live validations passed the harness cleanly, so nothing here is broken. Four rubric and budget issues surfaced that make the outputs harder to trust or harder to write, and each has evidence from a real run rather than from inspection.

## Requirements

- R1 MUST raise the decision-memo word budget from 600-900 to 700-1000, and make the harness exclude the `## Sources` section from its word count so the spec and the checker measure the same thing. Evidence: seven memos across two tasks all exceeded 900 on first draft (977, 1024, 1081, 1072, 1082, 1009), and the last needed three trim passes to comply.
- R2 MUST add a `blended_ceiling_customers` field to the cac-modeler output and state in the viability section that the verdict measures unit economics only, with channel reachability scored in distribution-analysis. Evidence: the B2B run returned `viability_verdict: "viable"` for a business whose qualifying channels cap at roughly 25-35 customers.
- R3 MUST add a market-size penalty to both monetization lane tables in idea-scoring: -5 when `market_size_verdict` is `niche`, -10 when `micro-niche`, mirroring the existing +5 for `large`.
- R4 MUST add guidance to trend-analysis for a platform that returns no usable signal: do not write a file, record the attempted queries in the consuming skill's `inputs_missing`, and lower `score_confidence`. Evidence: the B2C run's Reddit queries returned academic literature rather than community threads.
- R5 SHOULD reconsider the candidate-stage competition cap. Five consecutive validations have dropped competition 20-40 points under research (88→38, 85→45, 85→65, 62→32, 55→22); the current cap of 60 is generous against that record.
- R6 MUST keep the fixture suite passing at its current counts and `--check-specs` at zero errors.

## Acceptance criteria

- `python tests/validate_memory.py --check-specs` exits 0.
- Both task-3 runs still pass `--idea` with zero errors after the harness word-count change.
- Fixture suite unchanged unless a fixture is deliberately updated for a new field, in which case the expected counts in `tests/README.md` are updated in the same commit.

## Dependencies

Task 3 (DONE).
