# Task 5 — Public launch: branding, README, licence, and first-run onboarding

**Origin:** user request on 2026-09-06, to prepare the project for a public GitHub launch under Latif Abderrahmane's maintainership, with a branded name, a marketing-grade README, a replaced licence, and a first-run onboarding that asks the right questions.
**Agent:** none assigned.
**Scope:** root documentation (`README.md`, `LICENSE`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`), `skills/README.md`, `skills/user-background-interviewer/`, `workflows/idea-generation.md`, `tests/`.

## Problem statement

Four tasks have substantially rebuilt this system: a B2B rubric lane, a validation harness with fixtures, three shortcut workflows, a pivot lineage rule, and two live validations proving it works on real research. None of that is visible from outside. The README still describes the pre-task-1 system, credits none of the new capability, and points at the upstream repository. The first-run experience also lags the system: the interview never asks the three constraints (hours, budget, risk tolerance) that four separate decision memos flagged as blocking, and never asks who the user wants to sell to, which now selects the rubric lane in every dimension skill.

## Licensing constraint (must be respected)

This working copy originates from `github.com/MaxKmet/idea-validation-agents`, whose `LICENSE` is MIT with copyright held by MaxKmet, and whose initial commit created the core skill system. MIT requires the copyright notice to be retained in all copies and substantial portions. The licence therefore **cannot** be replaced with one naming only Latif Abderrahmane. The task delivers the rebrand with attribution intact: both copyright lines in `LICENSE`, and a short credit line in the README. Latif's authorship of the substantial extensions is stated prominently and accurately.

## Requirements

- R1 MUST replace `LICENSE` with an MIT licence retaining MaxKmet's original copyright line and adding a copyright line for Latif Abderrahmane covering the 2026 extensions.
- R2 MUST replace `README.md` with a launch-quality document covering: the branded name and one-line value proposition, a no-setup quickstart for Claude Code, Codex and Cursor, the four workflows, the two business-model lanes, the scoring methodology, the validation harness, a real worked example drawn from an actual run in `memory/ideas/`, what gets saved, an honest comparison against asking a general chatbot, an FAQ, credits, and licence.
- R3 MUST NOT contain invented metrics, fabricated testimonials, fake star or user counts, or claimed endorsements. Every number in the README must trace to a file in this repository or a cited public source.
- R4 MUST adopt the branded name chosen at the approval gate across `README.md`, `CLAUDE.md`, `AGENTS.md` and `skills/README.md`, without renaming any directory or skill identifier, so nothing in the harness or the adapters breaks.
- R5 MUST rework first-run onboarding in `skills/user-background-interviewer/SKILL.md` so that it: triggers on any workflow when `memory/user_profile.md` is absent rather than only in idea generation; captures the three constraints (hours per week, monthly budget, risk tolerance) in the full and fast paths; captures a target-buyer preference that maps to `business_model`; and states the time cost of each path up front.
- R6 MUST route first-run onboarding from the intent routers in `CLAUDE.md` and `AGENTS.md`, and reference it from `workflows/idea-generation.md`.
- R7 MUST add a `CONTRIBUTING.md` covering how to add or edit a skill, the canonical-plus-adapters rule, and the requirement to run the harness.
- R8 MUST extend `--check-specs` so the new onboarding contract is enforced: the interviewer skill asks for constraints and target buyer, and the routers reference onboarding.
- R9 MUST keep every existing test green: `--check-specs` at zero errors, both live runs at zero errors and zero warnings, the fixture suite at its documented counts, and `--baseline` exiting zero.

## Acceptance criteria

- `python tests/validate_memory.py --check-specs` exits 0 with the new assertions.
- `LICENSE` contains both copyright lines.
- `README.md` contains no metric that cannot be traced to a repository file or a cited source.
- `grep -rn "MaxKmet" README.md LICENSE` returns the credit and copyright lines.
- Both live idea runs and the fixture suite are unchanged.

## Dependencies

Tasks 1 to 4 (all DONE). The worked example in the README depends on the task-3 runs existing in `memory/ideas/`.
