---
name: idea-validation
trigger: "User has a specific app idea and wants it validated"
entry_condition: "User has stated a concrete idea"
exit_output: "memory/ideas/<slug>/decision_memo.md"
---

# Workflow: Idea Validation

## Startup Announcement

When this workflow is triggered, **immediately** say this before doing anything else:

> **🔍 Starting: Idea Validation**
> I'll run a full validation on your idea across demand, competition, monetization, distribution, retention, and founder fit — and give you a scored verdict with a concrete next step.

Then proceed to step 1.

## Trigger

User expresses one of:
- "Validate my idea: [description]"
- "I want to build [idea] — is it worth it?"
- "Score this idea for me"
- Resuming after idea-generation selected a candidate

**Fast path triggers.** Run the fast path instead of the full chain when the user says "gut check", "quick check", "fast", "is this worth a proper look?", or asks to screen several ideas at once. When the request is ambiguous, run the full chain — it is the default. Never run the fast path after the user has asked for a decision memo.

## Entry Conditions

0. Create `memory/ideas/<slug>/idea.md` with the raw idea description before starting the chain. Frontmatter must include `idea_slug`, `status: in-validation`, `created_at`, and **`business_model`** (`b2c | prosumer | b2b-smb | b2b2c`). If the user has not said who pays, ask one question: "Who pays for this: consumers with their own card, or a business?" Also record `buyer:` (one line) and `price_point_hypothesis:` when stated. `business_model` selects the rubric lane in every dimension skill (see `memory/README.md`).
   - If the idea came from idea-generation, `idea.md` already exists: set `status: in-validation` and confirm `business_model` is filled.
1. Idea slug = kebab-case derived from idea name (max 40 chars).
2. If `memory/user_profile.md` is missing the chain still runs: founder-market fit defaults to 50 and distribution/cac skip tier adjustments. Say so in the memo.

## Skill Chain

Steps 2, 3 and 5 read only `idea.md` and market_insights and do not depend on each other. An orchestrator that can run skills concurrently may run those three in parallel, each writing its own file. Steps 4, 6, 7, 8, 9 and 10 consume earlier outputs and run in order.

```
1. trend-analysis
   ↓ reads: topic and business_model from memory/ideas/<slug>/idea.md; existing memory/market_insights/ files for the niche
   ↓ condition: recommend the platform set by business_model (b2c/prosumer: TikTok + Reddit + Apps + Web Search; b2b-smb/b2b2c: Web Search + B2B communities + X/Twitter). Skip a platform whose fresh file already exists.
   ↓ writes: memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md (one file per platform)
   → present: Share the top 3 trend signals found, trend velocity, and overall verdict (hot/warm/cool/cold). Full analysis at memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md

2. competitor-mapper
   ↓ reads: memory/ideas/<slug>/idea.md, memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md (one file per platform)
   ↓ writes: memory/ideas/<slug>/competitors.json
   → present: List the top 3 direct competitors with their pricing and top complaint, and state market saturation. Full landscape at memory/ideas/<slug>/competitors.json

3. desire-evaluator
   ↓ reads: memory/ideas/<slug>/idea.md, memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md (one file per platform)
   ↓ writes: memory/ideas/<slug>/desire_scores.json
   → present: State the primary desire driver, desire strength label, and virality potential. Full scores at memory/ideas/<slug>/desire_scores.json

4. pricing-and-wtp
   ↓ reads: memory/ideas/<slug>/idea.md, memory/ideas/<slug>/competitors.json, memory/ideas/<slug>/desire_scores.json, memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md (one file per platform)
   ↓ writes: memory/ideas/<slug>/pricing.json
   → present: State the recommended pricing model, target WTP range (or tiers), and the freemium conversion or trial-to-paid estimate. Full model at memory/ideas/<slug>/pricing.json

5. distribution-analysis
   ↓ reads: memory/user_profile.md (if present), memory/ideas/<slug>/idea.md, memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md (one file per platform), memory/ideas/<slug>/competitors.json (optional)
   ↓ writes: memory/ideas/<slug>/distribution.json
   → present: State the distribution verdict, recommended first acquisition channel, its ceiling, and whether a viral loop exists. Full analysis at memory/ideas/<slug>/distribution.json

6. tam-sam-som-builder
   ↓ reads: memory/ideas/<slug>/competitors.json, memory/ideas/<slug>/pricing.json, memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md (one file per platform)
   ↓ writes: memory/ideas/<slug>/market_size.json
   → present: State TAM, SAM, realistic SOM for year 1, the triangulation confidence, and the market size verdict. Full estimates at memory/ideas/<slug>/market_size.json

7. retention-predictor
   ↓ reads: memory/ideas/<slug>/idea.md, memory/ideas/<slug>/desire_scores.json, memory/ideas/<slug>/pricing.json (optional), memory/ideas/<slug>/competitors.json (optional)
   ↓ writes: memory/ideas/<slug>/retention.json
   → present: State the retention verdict, natural usage frequency, and top churn risk factor. Full prediction at memory/ideas/<slug>/retention.json

8. cac-modeler
   ↓ condition (profile gap gate): before running, check memory/user_profile.md for time_per_week_hours, budget_constraint and risk_tolerance. If any is missing or "unknown", ask all three in ONE message ("Roughly how many hours a week can you give this, what monthly budget for tools and ads, and how much risk are you comfortable with: low, medium, or high?") and write the answers to user_profile.md before continuing. Budget tier drives channel viability here and kill criteria in decision-memo. If the user declines, write "unknown", assume bootstrap, and say so in the memo.
   ↓ reads: memory/user_profile.md, memory/ideas/<slug>/pricing.json, memory/ideas/<slug>/retention.json, memory/ideas/<slug>/distribution.json, memory/ideas/<slug>/competitors.json (optional), memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md (one file per platform)
   ↓ writes: memory/ideas/<slug>/cac.json
   → present: State the viability verdict, LTV:CAC ratio for the recommended channel, and payback period in months. Full model at memory/ideas/<slug>/cac.json

9. idea-scoring
   ↓ reads: memory/ideas/<slug>/idea.md (business_model), memory/ideas/<slug>/competitors.json, memory/ideas/<slug>/desire_scores.json, memory/ideas/<slug>/pricing.json, memory/ideas/<slug>/distribution.json, memory/ideas/<slug>/market_size.json, memory/ideas/<slug>/retention.json, memory/ideas/<slug>/cac.json, memory/user_profile.md (if present)
   ↓ writes: memory/ideas/<slug>/scores.json (scoring_stage: full-validation)
   → present: Show the final score (X/100), verdict, top strength, and top weakness. Full breakdown at memory/ideas/<slug>/scores.json

10. decision-memo
   ↓ reads: memory/ideas/<slug>/scores.json + all dimension files + memory/user_profile.md
   ↓ writes: memory/ideas/<slug>/decision_memo.md; then updates memory/ideas/<slug>/idea.md frontmatter to `status: scored` and adds `validated_at: <YYYY-MM-DD>`
   → present: Share the complete decision memo in full. File also saved at memory/ideas/<slug>/decision_memo.md
```

## State Flow

| Step | Reads | Writes |
|---|---|---|
| trend-analysis | `idea.md` (topic, business_model) | `market_insights/<niche>-<platform>-<YYYY>-<MM>.md` |
| competitor-mapper | `idea.md`, market_insights | `competitors.json` |
| desire-evaluator | `idea.md`, market_insights | `desire_scores.json` |
| pricing-and-wtp | `idea.md`, `competitors.json`, `desire_scores.json`, market_insights | `pricing.json` |
| distribution-analysis | `user_profile.md`, `idea.md`, market_insights, `competitors.json` (opt) | `distribution.json` |
| tam-sam-som-builder | `competitors.json`, `pricing.json`, market_insights | `market_size.json` |
| retention-predictor | `idea.md`, `desire_scores.json`, `pricing.json` (opt), `competitors.json` (opt) | `retention.json` |
| cac-modeler | `user_profile.md`, `pricing.json`, `retention.json`, `distribution.json`, `competitors.json` (opt), market_insights | `cac.json` |
| idea-scoring | `idea.md`, `competitors.json`, `desire_scores.json`, `pricing.json`, `distribution.json`, `market_size.json`, `retention.json`, `cac.json`, `user_profile.md` (opt) | `scores.json` |
| decision-memo | `scores.json` + all dimension files + `user_profile.md` | `decision_memo.md`, `idea.md` (status) |

## Exit Output

`memory/ideas/<slug>/decision_memo.md` — the human-readable validation brief with:
- Verdict (pursue / test / pivot / drop)
- Final score
- Top 3 strengths with evidence
- Top 3 risks with evidence
- Recommended next step

If verdict is `pivot` or `drop`, offer to run `pivot-optimization` workflow.

Before presenting the memo, run `python tests/validate_memory.py --idea <slug>` when a shell is available and fix every ERROR line. The harness recomputes the score and checks each file against its contract (see `tests/README.md`).

---

### Fast path (gut check)

A five-step screen that answers "is this worth a proper look?" in roughly three minutes. It scores four dimensions and deliberately learns nothing about pricing or retention, so it can rule an idea out but never rule one in.

Entry conditions are the same as the full chain: `idea.md` with `business_model` and `status: in-validation`.

```
F1. trend-analysis
   ↓ reads: topic and business_model from memory/ideas/<slug>/idea.md; existing memory/market_insights/ files for the niche
   ↓ condition: ONE platform only — the highest-signal one for the business model (b2c/prosumer: Reddit or App Store; b2b-smb/b2b2c: Web Search). Skip entirely if a fresh file for the niche already exists.
   ↓ writes: memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md
   → present: One line — trend velocity and overall verdict.

F2. competitor-mapper (light mode)
   ↓ reads: memory/ideas/<slug>/idea.md, memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md
   ↓ condition: LIGHT MODE — find 3 direct competitors with pricing, skip review mining, skip indirect competitors and substitutes, score saturation from competitor count and incumbent dominance only. Set review_mining_summary.competitors_mined to 0 and say in saturation_rationale that saturation is provisional.
   ↓ writes: memory/ideas/<slug>/competitors.json
   → present: The three competitors, their prices, and the saturation level.

F3. desire-evaluator
   ↓ reads: memory/ideas/<slug>/idea.md, memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md
   ↓ writes: memory/ideas/<slug>/desire_scores.json
   → present: Primary desire driver and strength label.

F4. distribution-analysis
   ↓ reads: memory/user_profile.md (if present), memory/ideas/<slug>/idea.md, memory/ideas/<slug>/competitors.json, memory/market_insights/<niche>-<platform>-<YYYY>-<MM>.md
   ↓ writes: memory/ideas/<slug>/distribution.json
   → present: Distribution verdict, first channel, and its ceiling.

F5. idea-scoring
   ↓ reads: memory/ideas/<slug>/idea.md, memory/ideas/<slug>/desire_scores.json, memory/ideas/<slug>/competitors.json, memory/ideas/<slug>/distribution.json, memory/user_profile.md (if present)
   ↓ writes: memory/ideas/<slug>/scores.json with scoring_stage: fast-validation (monetization and retention null, missing_discount 4/6, RAT required, confidence at most medium)
   → present: The gut-check summary below. No decision memo is written.
```

**Fast path exit output.** An inline summary, not a file. Five lines: the score and verdict, the strongest dimension with its evidence, the weakest dimension with its evidence, the riskiest assumption, and this sentence verbatim: *"This is a gut check on four dimensions — it did not examine whether anyone will pay or whether they will stay."* Then offer the full chain, and offer `pivot-optimization` if the verdict is `pivot` or `drop`.

The idea keeps `status: in-validation` after a fast path. Only a decision memo moves it to `scored`.

## Notes

- Steps 2, 3 and 5 are independent; see the note above the skill chain.
- The fast path exists to screen, not to decide. A fast `drop` is trustworthy because demand and distribution were both examined; a fast `test` means "worth the full chain", never "worth building". Never present a fast-validation score next to a full-validation score without labelling both stages.
