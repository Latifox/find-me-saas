# Changelog

## Unreleased — 2026-09-06

### Added
- `tests/validate_memory.py`, `tests/schemas.json`, `tests/make_fixtures.py`, `tests/README.md`: stdlib validation harness for skill outputs and specs.
- `skills/trend-analysis/prompts/b2b-communities.md`: research prompt for business buyers (G2/Capterra, Hacker News, Indie Hackers, LinkedIn, pricing pages).
- `business_model` field (`b2c | prosumer | b2b-smb | b2b2c`) on `idea.md`; B2B rubric lanes in idea-scoring, distribution-analysis, pricing-and-wtp, cac-modeler, tam-sam-som-builder, competitor-mapper, retention-predictor, pivot-engine.
- Real rubrics for desire-evaluator, retention-predictor, weakness-detection, user-segmentation-profiler (previously TODO placeholders).
- Decision memo: Devil's Advocate section, URL Sources, profile-gaps line, idea status update to `scored`.
- idea-validation: tam-sam-som-builder step, profile-gap gate before cac-modeler, concurrency note, status lifecycle.
- `docs/` (tasks, board, handoffs, changelog, agents log) and `.ay/` planning artifacts.

### Changed
- Quick-scores from idea-generation now carry `rank_label` instead of a verdict, with competition capped at 60 until competitor-mapper runs.
- idea-scoring: "3 of 6" dimensions (was "3 of 7"), `scoring_stage` semantics, round-half-to-even stated, B2B monetization and retention rows.
- Decision memo word budget 600-900 (was 400-600, never met).
- `memory/README.md`, `memory/market_insights/README.md`: phantom files removed, index corrected, provenance and lane documented.
- `.claude/settings.json`: WebFetch allowed.
- `.gitignore`: Python caches ignored.

### Added (task 2)
- **Fast path** in `workflows/idea-validation.md`: a five-step gut check scoring demand, competition, distribution, and founder-market fit. Writes `scores.json` with `scoring_stage: fast-validation` and no decision memo.
- **Micro-pivot** in `workflows/pivot-optimization.md` and `skills/pivot-engine/SKILL.md`: the user names one variable, weakness-detection is skipped, and exactly one option is generated with `pivot_scope: micro`.
- **Slug Rule**: one variable changed updates the idea in place; two variables, a `business_model` change, or a problem change creates a new directory with `pivot_of` and sets the original to `paused` with `superseded_by`.
- **Quick scan** in `workflows/market-deep-dive.md`: trend analysis only, for choosing between categories.
- Intent-router rows for the fast path and micro-pivot in `CLAUDE.md` and `AGENTS.md`; memo version and supersede-footer rules in `skills/decision-memo/SKILL.md`.
- Harness support for all of the above plus six fixtures (`fixture-fast`, `fixture-fast-broken`, `fixture-micro`, `fixture-micro-broken`, `fixture-superseded`, `fixture-superseded-v2`, `fixture-superseded-broken`).

### Added (task 6)
- **npx installer.** `npx find-me-saas init` adds the system to any existing project, with `--dry-run`, `--platform claude|codex|cursor|all` and `--force`. Zero dependencies, Node built-ins only. User analyses under `memory/` are never overwritten, even with `--force`.
- **Nine slash commands**, one per job: `/founder-profile`, `/find-idea`, `/validate-idea`, `/gut-check`, `/market-scan`, `/pivot-idea`, `/auto-pilot`, `/idea-status`, `/verify-memory`. Each dispatches to a workflow rather than restating it.
- **Autonomous mode.** `/auto-pilot` runs onboarding, research, ranking, full validation, memo and harness without stopping to ask, recording assumptions instead of blocking, and stops early only for no market signal, insufficient dimensions, or an unfixable harness error.
- **Two hooks.** `SessionStart` reports profile and portfolio status into context; `PostToolUse` validates any idea directory that is written to and returns contract errors to the agent. Both are dependency-free Python that fails open.
- `--check-specs` now asserts all nine commands exist with matching frontmatter and that both hooks are registered and point at scripts that exist.

### Launched (task 5)
- Project branded **FindMeSaaS**, applied across `README.md`, `CLAUDE.md`, `AGENTS.md` and `skills/README.md`. No directory, skill identifier or adapter path changed.
- `LICENSE` rewritten as MIT with two copyright blocks: the upstream original work and the 2026 extensions, each stating what it covers.
- `README.md` fully rewritten for public launch: value proposition, three-platform quickstart, onboarding paths, a real abridged verdict from `memory/ideas/`, the five-run competition recalibration table, the four workflows, the consumer and business lanes, methodology with origins, the validation harness, an honest comparison against a general chatbot, and an FAQ. Every figure traces to a repository file.
- First-run onboarding reworked: runs ahead of any workflow when no profile exists, states the time cost of each path, and now captures hours per week, monthly budget, risk tolerance and target buyer. The target-buyer answer sets `preferred_business_model`, which selects the rubric lane.
- `CONTRIBUTING.md` added, covering the canonical-plus-adapters rule, the harness commands and the memory contract.
- Three new `--check-specs` assertions cover the onboarding contract and the router wiring.

### Validated (task 3)
- First live runs of the rewritten specs. `shadow-ai-discovery-for-msp` full-validated in the B2B lane at 43/100 (pivot), superseding its 53/100 candidate quick-score; `habit-tracker-climbers` full-validated in the B2C lane at 28/100 (drop) as the consumer-lane control subject.
- First execution of the `b2b-communities` research prompt, producing `memory/market_insights/shadow-ai-msp-b2b-communities-2026-09.md`.
- Profile gate closed: `time_per_week_hours`, `budget_constraint` and `risk_tolerance` captured in `memory/user_profile.md` after being flagged as blocking by four previous memos.
- Both runs pass `validate_memory.py --idea` with zero errors and zero warnings, with no improvisation language and no cross-lane field contamination.

### Changed (task 4)
- Decision memo budget raised to 700-1000 words of prose, measured to the `## Sources` heading so citations no longer compete with analysis for space. The 1200-word hard error still applies to the full body.
- `cac.json` in the B2B lane now requires `blended_ceiling_customers`, and the viability verdict states explicitly that it measures unit economics only, with channel reachability scored in `distribution-analysis`.
- Monetization scoring penalises a small market in both lanes: -5 for `niche`, -10 for `micro-niche`, mirroring the existing +5 for `large`.
- Candidate-stage competition cap tightened from 60 to 45 and extracted into `CANDIDATE_COMPETITION_CAP` so the skill and the harness cannot drift apart. Evidence: five full validations landed at 38, 45, 65, 32 and 22.
- `trend-analysis` gained a rule for a platform that returns no usable signal: write no file, record the attempted queries in the consuming skill's `inputs_missing`, lower `score_confidence`, and never substitute another platform's data.

### Fixed
- All four `(task-2)` TODO comments in `workflows/` resolved.
- Workflows no longer read files no skill produces (`user_extraction.json`, `weighted_signals.json`, `keywords.json`, `complexity.json`).
- `pivot_options.md` typo and `-deep-dive-` filename in workflows.
