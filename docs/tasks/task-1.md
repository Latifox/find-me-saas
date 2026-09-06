# Task 1 — Skill Quality Hardening (B2B lane, validation harness, spec consistency)

**Origin:** user request on 2026-09-06: "look up this project, test it, and see what improvements we can add to enhance the output and quality of this skill."
**Agent:** none assigned (orchestrator edits canonical skill specs directly).
**Scope:** `skills/`, `workflows/`, `memory/README.md`, `memory/market_insights/README.md`, `tests/`, `CLAUDE.md`, `AGENTS.md`, `.claude/settings.json`.

## Problem statement

The skill system was designed for indie B2C mobile apps. Every real run in this repo (20 ideas, 4 full validations) targeted B2B buyers (AI agencies, MSPs). The agent had to improvise: 4 of 7 dimension outputs ignore their spec schema, rubric thresholds ($5/mo WTP, ASO, TikTok) are meaningless for $199/mo SaaS, and there is no way to test whether an output conforms. Four skills that carry 45% of the final score still contain TODO placeholders instead of rubrics.

## Requirements

- R1 MUST add a validation harness that checks every `memory/ideas/*/*.json` against a schema, recomputes `scores.json` arithmetic, and checks `decision_memo.md` length. Runnable with plain Python, no dependencies.
- R2 MUST make every ```json block in `skills/*/SKILL.md` parse, and the harness MUST verify this.
- R3 MUST introduce a `business_model` field (`b2c | prosumer | b2b-smb | b2b2c`) in `idea.md` frontmatter, set at idea creation, and read by every dimension skill.
- R4 MUST add a B2B rubric lane (channels, pricing benchmarks, churn benchmarks, SOM method, review-mining sources, pivot filters) beside the existing B2C lane in: distribution-analysis, pricing-and-wtp, cac-modeler, tam-sam-som-builder, competitor-mapper, retention-predictor, pivot-engine, idea-scoring.
- R5 MUST replace TODO placeholders with real rubrics in desire-evaluator, retention-predictor, weakness-detection, user-segmentation-profiler.
- R6 MUST fix spec inconsistencies: "3 of 7 dimensions" (there are 6), phantom inputs (`user_extraction.json`, `weighted_signals.json`, `keywords.json`, `complexity.json`, `signals.json`), `pivot_options.md` typo, `-deep-dive-` filename, `signal-aggregator` reference, stale market_insights index.
- R7 MUST define `scoring_stage` semantics: candidate quick-scores get a rank label, not a pursue/test/pivot/drop verdict, and cap competition at 60 when `competitors.json` is absent (evidence: 4/4 runs dropped 20–40 pts under research).
- R8 MUST add tam-sam-som-builder to the idea-validation chain and a profile-gap gate (hours, budget, risk) before cac-modeler.
- R9 MUST require source provenance (`sources: [{url,title,accessed}]`) in competitors, pricing, market_size, distribution outputs and URL citations in the decision memo.
- R10 MUST add a "Devil's Advocate" section to the decision memo and set a realistic word budget (600–900) enforced by the harness.
- R11 MUST update idea lifecycle status (`in-validation` at entry, `scored` after memo) in the workflow.
- R12 SHOULD add a B2B research prompt (`prompts/b2b-communities.md`) covering LinkedIn, G2/Capterra, Hacker News, Indie Hackers, GitHub, Product Hunt.
- R13 SHOULD allow WebFetch in `.claude/settings.json` so source verification does not prompt every time.
- R14 SHOULD note in workflows that competitor/desire/distribution steps are independent and may run concurrently.
- R15 MAY add a `retention-predictor` D30-equivalent mapping for B2B (logo churn) so idea-scoring's retention rubric applies to both lanes.

## Acceptance criteria

- `python tests/validate_memory.py` exits 0 on a fresh B2C run and a fresh B2B run, and reports the existing 20-idea corpus with a clear list of schema failures (baseline is allowed to fail).
- `python tests/validate_memory.py --check-specs` exits 0 (all skill JSON examples parse; every file a workflow reads is produced by some skill).
- Running `idea-validation` on a B2B idea produces the 7 dimension files with no `methodology_note: "skill assumes B2C..."` style improvisation.
- No `<!-- TODO` remains in the four stub skills.

## Dependencies

None. This task does not depend on other tasks. `docs/HANDOFFS.md` and `docs/DECISIONS.md` do not exist yet.
