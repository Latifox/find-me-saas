# Memory System

This directory is the persistent state layer shared across all platform adapters and all skills. All skill outputs are written here. All skill inputs are read from here.

## Structure

```
memory/
  user_profile.md          # User background, ICP tier, strengths, constraints
  market_insights/         # Per-niche market intelligence (one file per niche + platform + period)
    README.md              # Index and naming convention
    <niche>-<platform>-<YYYY>-<MM>.md  # e.g. nutrition-tiktok-2026-04.md
  ideas/
    <idea-slug>/           # One directory per idea evaluated
      idea.md              # Idea description, trend evidence, business_model, status (written by trend-to-product-mapper or at idea-validation entry)
      desire_scores.json   # desire-evaluator
      competitors.json     # competitor-mapper
      pricing.json         # pricing-and-wtp
      market_size.json     # tam-sam-som-builder
      distribution.json    # distribution-analysis
      retention.json       # retention-predictor
      cac.json             # cac-modeler
      scores.json          # idea-scoring (scoring_stage: candidate-quick-score | fast-validation | full-validation)
      weaknesses.json      # weakness-detection
      pivot_options.json   # pivot-engine: structured pivot data for downstream re-scoring
      pivot_report.md      # pivot-engine: human-readable pivot brief
      pivot_scores.json    # idea-scoring (scoring_stage: pivot-rescore)
      decision_memo.md     # decision-memo
```

Every file above is produced by exactly one skill. If a skill lists an input that no skill produces, that is a spec bug: run `python tests/validate_memory.py --check-specs`.

## Business model lane

`idea.md` frontmatter carries `business_model: b2c | prosumer | b2b-smb | b2b2c`. Dimension skills read it to select their rubric lane (B2C: app-store, ASO, TikTok, D30 retention; B2B: content/community/partner channels, ACV tiers, logo churn). Every dimension JSON records the lane it used in a `lane: b2c | b2b` field (`prosumer` uses the B2C pricing lane and the B2B channel lane).

## Provenance

`competitors.json`, `pricing.json`, `market_size.json`, and `distribution.json` must carry a `sources` array: `[{ "url": "https://...", "title": "", "accessed": "YYYY-MM-DD", "used_for": "" }]`. The decision memo cites URLs from these arrays under `## Sources`.

## Naming Convention

- Idea slugs: kebab-case, max 40 characters, derived from idea name
- Examples: `habit-tracker-climbers`, `nutrition-coach-glp1`, `freelance-invoice-ios`
- Market research slugs: prefix with `market-` (e.g., `market-nutrition-2026`)

## State Protocol

- **Skills WRITE** structured JSON or Markdown to their designated output files
- **Orchestrator READS** output files and provides relevant context when invoking the next skill
- Skills do NOT call each other — the orchestrator manages the chain

## Idea Lifecycle

Ideas are never deleted. Use `status` field in `idea.md` to track lifecycle:

| Status | Meaning |
|---|---|
| `candidate` | Generated but not yet validated |
| `in-validation` | Currently being analyzed |
| `scored` | Validation complete, has decision_memo |
| `active` | User is building this |
| `paused` | On hold |
| `dropped` | Decided not to pursue |

## Pivot Lineage

A pivot that changes one variable updates the idea in place. A pivot that changes two variables, the `business_model`, or the core problem becomes a new idea directory, and two frontmatter fields record the link:

| Field | Written on | Meaning |
|---|---|---|
| `pivot_of: <slug>` | the new idea | This idea came from a pivot of `<slug>`; the source directory must still exist |
| `superseded_by: <slug>` | the original idea | A pivot moved on to `<slug>`; the original's `status` must be `paused` or `dropped` |

Neither directory is ever deleted. Dimension files are not copied into the new directory: a pivot that big changes the competitive set and the channels, so they are researched again.

## Rules

1. Never delete idea directories — set `status: dropped` in idea.md instead
2. `user_profile.md` is updated incrementally — later skills append new fields
3. `market_insights/` grows over time — each new analysis is a new file, never overwrite an existing one
4. JSON files must be valid JSON (parseable by any adapter)
5. Outputs must pass `python tests/validate_memory.py --idea <slug>` (see `tests/README.md`)
