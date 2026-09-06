---
name: idea-scoring
description: Aggregates all dimension scores into a final idea score (0–100) and issues a verdict. Implements a multiplicative-floor algorithm with Riskiest Assumption Test (RAT). The final output of every validation workflow.
---

<!-- version: 0.5.0 | outputs: memory/ideas/<slug>/scores.json (or pivot_scores.json for pivot-rescore) -->

# Skill: idea-scoring

## Purpose

Produce a single, defensible verdict on an idea by aggregating all available dimension scores using a **multiplicative-floor algorithm** — a single catastrophic weakness kills the score, just like it kills a real startup. Includes a **Riskiest Assumption Test (RAT)** to convert the verdict into a concrete next action.

## Input

- Idea slug
- One or more of the following (uses whatever is available):
  - `memory/ideas/<slug>/idea.md`
  - `memory/ideas/<slug>/desire_scores.json`
  - `memory/ideas/<slug>/competitors.json`
  - `memory/ideas/<slug>/pricing.json`
  - `memory/ideas/<slug>/cac.json`
  - `memory/ideas/<slug>/market_size.json`
  - `memory/ideas/<slug>/distribution.json`
  - `memory/ideas/<slug>/retention.json`
- Optional: `memory/user_profile.md` (for founder-market fit)
- `memory/market_insights/<niche>-*-<YYYY>-<MM>.md` (`trend_velocity` for the Demand rubric)

### Lane selection

Read `business_model` from `idea.md` frontmatter. `b2c` and `prosumer` use the B2C rows of every rubric below; `b2b-smb` and `b2b2c` use the B2B rows. Where a rubric has only one table, it applies to both lanes. Record the lane in `scores.json` as `lane`.

### Minimum Viable Input

At least **3 of 6 dimensions** must have source data. If fewer are available, refuse to score and list what's missing. Two dimensions are **mandatory** — Demand and Distribution. Without evidence of a real problem and a path to reach users, scoring is meaningless.

## Scoring Dimensions

| Dimension | Weight | Source | What it measures |
|---|---|---|---|
| Demand | 20% | `desire_scores.json` + `idea.md` + market_insights `trend_velocity` | Real human desire + validated market signals |
| Competition | 10% | `competitors.json` | Positioning gaps and defensibility |
| Monetization | 20% | `pricing.json` + `cac.json` + `market_size.json` | Unit economics viability (LTV:CAC, WTP, market size) |
| Distribution | 20% | `distribution.json` | Organic reach, paid viability, founder edge |
| Retention | 15% | `retention.json` | Habit formation, churn risk, usage frequency |
| Founder-Market Fit | 15% | `user_profile.md` + domain overlap with idea | Builder's edge, domain expertise, distribution advantage |

## Dimension Score Mapping

Each dimension maps source data to a 0–100 sub-score using the rubrics below. When source data uses qualitative labels, apply these conversions.

### Demand (0–100)

| Condition | Score range |
|---|---|
| `desire_strength_label` = "strong" AND trend_velocity = "rising-fast" | 80–100 |
| `desire_strength_label` = "strong" OR trend_velocity = "rising" | 60–79 |
| `desire_strength_label` = "moderate" AND some signal validation | 40–59 |
| `desire_strength_label` = "weak" OR trend_velocity = "declining" | 15–39 |
| No signal data, speculation only | 0–14 |

Adjust within range: +10 if cross-platform resonance confirmed, +5 if monetization_validated is true in `idea.md`.

### Competition (0–100)

Higher = more favorable competitive landscape (counterintuitive — think of it as "opportunity score").

| Condition | Score range |
|---|---|
| `market_saturation` = "low", clear positioning gaps, no dominant incumbent | 75–100 |
| `market_saturation` = "medium", 1–2 positioning gaps identified | 50–74 |
| `market_saturation` = "high" but differentiation opportunities exist | 25–49 |
| `market_saturation` = "high", no differentiation, dominant incumbents | 0–24 |

Adjust: +10 if top competitor complaints reveal an unserved pain point. -15 if a FAANG-class player owns the category.

**Candidate-stage prior cap.** When `competitors.json` does not exist (idea-generation quick-scores), competition is an estimate from trend narrative only. Cap it at **45** and set `competition_prior_capped: true`. Evidence from this repo: in five consecutive full validations the competition score fell 20-40 points once real competitor research was done (88 to 38, 85 to 45, 85 to 65, 62 to 32, 55 to 22). Four of those five landed below 45 and the median was 38, so a cap of 45 remains an upper bound rather than a prediction while removing most of the unearned optimism. The cap was 60 from task 1 until task 4. Treat candidate-stage competition as an upper bound, and say so when presenting.

### Monetization (0–100)

**B2C lane** (`b2c`, `prosumer`) — from `pricing.json` + `cac.json` + `market_size.json`:

| Condition | Score range |
|---|---|
| LTV:CAC ≥ 3:1 on at least 2 channels, WTP target ≥ $5/mo, viable SOM | 80–100 |
| LTV:CAC ≥ 3:1 on 1 channel, WTP target ≥ $3/mo | 60–79 |
| LTV:CAC ≥ 2:1, WTP target $1–$3/mo, marginal unit economics | 35–59 |
| LTV:CAC < 2:1 OR viability_verdict = "not-viable" | 10–34 |
| No pricing data or CAC data | 0–9 (flag as missing) |

Adjust: +10 if `freemium_conversion_estimate` > 5%. +5 if market_size_verdict = "large", -5 if "niche", -10 if "micro-niche".

**B2B lane** (`b2b-smb`, `b2b2c`) — from `pricing.json` (`recommended_tiers`, `anchors`) + `cac.json` (`ltv_cases`, `cac_by_channel_b2b`) + `market_size.json`:

| Condition | Score range |
|---|---|
| LTV:CAC ≥ 3:1 on at least 2 channels in the base case, payback ≤ 6 months on the recommended channel, AND a validated price anchor (a named product charging the same buyer at a comparable price) | 80–100 |
| LTV:CAC ≥ 3:1 on 1 channel, payback ≤ 9 months, price anchor exists | 60–79 |
| LTV:CAC ≥ 2:1 on the best channel, OR payback 9–12 months, OR no price anchor (the revealed price is a gap between two clusters) | 35–59 |
| LTV:CAC < 2:1 in the base case, OR pessimistic-case LTV:CAC < 1:1 on every channel, OR revealed price is $0 (free incumbents, nobody charges) | 10–34 |
| No pricing data or CAC data | 0–9 (flag as missing) |

Adjust: +5 if `trial_to_paid_estimate` ≥ 20% (heuristic: self-serve B2B trial-to-paid benchmarks cluster at 15–25%). +5 if an expansion mechanism exists (per-client or per-seat overage, rebilling). -10 if the pessimistic LTV case drops the recommended channel below 3:1. +5 if market_size_verdict = "large", -5 if "niche", -10 if "micro-niche".

The market-size penalty was added in task 4. The rubric previously rewarded a large market with no symmetric penalty for a tiny one, which let a business with sound ratios and a $33,600 year-one SOM score in the middle of the band.

### Distribution (0–100)

| Condition | Score range |
|---|---|
| `distribution_verdict` = "strong", viral_loop_exists = true | 80–100 |
| `distribution_verdict` = "strong" OR (organic_reach = "high" + creator_economy_fit = "high") | 60–79 |
| `distribution_verdict` = "moderate", at least one viable organic channel | 40–59 |
| `distribution_verdict` = "weak", paid-only path | 15–39 |
| No viable channel identified | 0–14 |

Adjust: +10 if founder has existing audience or distribution edge (from `user_profile.md`).

### Retention (0–100)

| Condition | Score range |
|---|---|
| `retention_verdict` = "sticky", D30 ≥ 20%, habit_formation_score ≥ 4 | 80–100 |
| `retention_verdict` = "sticky" OR D30 ≥ 15% | 60–79 |
| `retention_verdict` = "moderate", D30 ≥ 8% | 40–59 |
| `retention_verdict` = "disposable" OR D30 < 8% | 15–39 |
| `churn_risk` = "high" AND no habit loop | 0–14 |

Adjust (B2C lane): +5 if natural_usage_frequency is daily. -10 if weekly-or-less with no external trigger.

**B2B lane.** `retention.json` carries `d30_equivalent` (derived from `monthly_churn_estimate`; see retention-predictor) so the bands above apply unchanged. Sanity anchors for the mapping (heuristic): monthly logo churn ≤ 3% maps to d30_equivalent ≥ 64 and "sticky"; 3–6% maps to 28–64 and "moderate"; above 6% maps below 28 and "disposable". The daily-frequency adjustment does not apply; instead +5 if an external recurring trigger exists (report cycle, audit, renewal, client onboarding) and -10 if usage is event-only with no calendar trigger.

### Founder-Market Fit (0–100)

| Condition | Score range |
|---|---|
| Strong domain match in `strong_domains`, distribution advantages align, builder/growth tier | 75–100 |
| Moderate domain overlap OR builder tier with adjacent experience | 50–74 |
| Beginner tier but high motivation and time commitment (≥ 20 hrs/wk) | 30–49 |
| No domain overlap, beginner tier, low time commitment | 0–29 |

Adjust: +10 if `inner_circle_domains` in `user_profile.md` includes the idea's buyer (a design partner or first customer one call away). For B2B ideas this is the single strongest founder-fit signal. -10 if the idea requires a regulated or licensed competence the founder lacks (legal, medical, financial advice).

If `user_profile.md` is unavailable, default to 50 (neutral) and flag as missing.

## Scoring Algorithm

### Step 1 — Compute dimension sub-scores

Apply the mapping rubrics above. Record each as `d_i` (0–100).

### Step 2 — Apply floor penalty (the "Killer Dimension" rule)

Any dimension scoring below **25** is a potential startup killer. Apply this penalty:

```
floor_penalty = 1.0
for each dimension d_i:
    if d_i < 25:
        floor_penalty *= (d_i / 25)
```

This multiplicative penalty means a single catastrophic weakness (score 0–10) can halve or destroy the final score, regardless of how strong other dimensions are. This reflects startup reality: brilliant distribution cannot save a product nobody wants.

### Step 3 — Compute weighted base score

```
weights = {
    demand: 0.20,
    competition: 0.10,
    monetization: 0.20,
    distribution: 0.20,
    retention: 0.15,
    founder_market_fit: 0.15
}

base_score = sum(d_i * w_i for each dimension)
```

### Step 4 — Apply floor penalty and missing-input discount

```
missing_discount = available_dimensions / total_dimensions
adjusted_score = base_score * floor_penalty * missing_discount
final_score = round(clamp(adjusted_score, 0, 100))
```

`round` is round-half-to-even (Python's `round`): 72.5 becomes 72, 73.5 becomes 74. `tests/validate_memory.py` recomputes every value above with the same rule and fails the file if any differs.

The missing-input discount ensures that ideas scored on only 3 of 6 dimensions can never reach the "pursue" tier without completing more analysis.

### Step 5 — Determine confidence level

| Available dimensions | Confidence |
|---|---|
| 6 of 6 | high |
| 4–5 of 6 | medium |
| 3 of 6 (minimum) | low |

A skill may lower confidence below this table (for example when source data is stale or a dimension rests on a single source) but never raise it.

### Step 6 — Issue verdict

| Score | Verdict | Meaning |
|---|---|---|
| 75–100 | **pursue** | Strong across dimensions. Build an MVP. |
| 55–74 | **test** | Promising but unproven. Run the RAT experiment first. |
| 35–54 | **pivot** | Structural weakness. Use pivot-engine to explore alternatives. |
| 0–34 | **drop** | Fatal flaws. Move to next idea. |

## Scoring Stages

`scores.json` always carries `scoring_stage`. The stage decides whether the output is a verdict or a ranking.

| Stage | When | Output field | Rules |
|---|---|---|---|
| `candidate-quick-score` | idea-generation step 5: only `idea.md` and market_insights exist | `rank_label` (no `verdict`) | Competition capped at 60 with `competition_prior_capped: true`. Retention is `null`. `missing_discount` applies as usual. `rank_label` is read from the **undiscounted** `base_score`: ≥ 65 `strong-candidate`, 50–64 `candidate`, < 50 `weak-candidate`. RAT is optional; `reason` on strengths and weaknesses is still required. |
| `fast-validation` | idea-validation **fast path**: only `desire_scores.json`, `competitors.json` (light) and `distribution.json` exist | `verdict` | Scores exactly four dimensions — demand, competition, distribution, founder-market fit. Monetization and retention are `null`, so `missing_discount` is 4/6 and `pursue` is arithmetically unreachable (it would need a base score above 112). RAT required. `score_confidence` is at most medium. Every presentation of this score must say it is a gut check and name the two dimensions that were not examined. |
| `full-validation` | idea-validation step 9: all dimension files exist | `verdict` | Verdict from the threshold table below. RAT required. `dimension_rationale` required: one paragraph per dimension naming the source-file value that placed it in its band. |
| `pivot-rescore` | pivot-optimization step 4 | `verdict` + `pivot_id` | Written to `pivot_scores.json`. Dimensions adjusted per the `scoring_simulation` in `pivot_options.json`. |

Why quick-scores get no verdict: with one or two dimensions missing, the missing-input discount pushes every candidate into the 45–54 band, and labelling all of them "pivot" tells the user nothing. Rank labels compare candidates with each other; verdicts compare a fully validated idea against the build threshold.

Why fast-validation does get one: the four dimensions it scores include both mandatory ones (demand and distribution), and the discount already caps the ceiling. The verdict is honest as long as its two blind spots — whether anyone pays and whether they stay — are named every time the score is shown. A fast verdict of `drop` is trustworthy; a fast verdict of `test` means "worth the full chain", not "worth building".

## Riskiest Assumption Test (RAT)

Every idea rests on assumptions. The RAT identifies the single assumption that, if wrong, kills the idea — and designs the cheapest possible experiment to test it before building anything.

### RAT Identification Process

1. **List all assumptions** embedded in the idea (drawn from dimension scores and source data):
   - Demand: "People actually have this problem and will seek a solution"
   - Monetization: "Users will pay $X/mo for this"
   - Distribution: "We can reach users via [channel] at acceptable cost"
   - Retention: "Users will come back [frequency]"
   - Competition: "Our differentiator matters to users"
   - Founder fit: "I can build this with my current skills/resources" (using user_profile.md if available)

2. **Rank by two axes** (each 1–5):
   - **Criticality**: If wrong, how dead is the idea? (5 = instant kill)
   - **Uncertainty**: How little evidence do we have? (5 = pure speculation)

3. **RAT = assumption with highest (criticality × uncertainty)**. Ties broken by criticality.

### RAT Experiment Design

For the identified RAT, design an experiment following these constraints:

| Constraint | Requirement |
|---|---|
| Time to run | ≤ 2 weeks |
| Cost to run | ≤ $100 (indie budget) |
| Signal type | Behavioral (what people DO, not what they SAY) |
| Sample size | Minimum credible: 30 responses or 100 landing page visitors |

#### Experiment types by assumption category

| Assumption category | Experiment template |
|---|---|
| Demand exists | Landing page with email capture. Pass: ≥ 10% signup rate from ≥ 100 targeted visitors. |
| WTP is real | Landing page with price shown + "buy" button (payment step). Pass: ≥ 3% click-to-buy from ≥ 100 visitors. |
| Distribution works | Run 1 channel for 7 days (e.g., 5 TikToks, 10 Reddit posts, ASO test). Pass: CAC below modeled threshold. |
| Retention holds | Concierge MVP or manual-ops version with 10–30 users for 14 days. Pass: ≥ 3 return sessions per user. |
| Differentiator matters | Show competitor + your concept side-by-side to 30 target users. Pass: ≥ 60% prefer your concept. |

### Pass/Fail Threshold

Define the threshold **before** running the experiment. The threshold is written into `scores.json` so it can be evaluated later. Thresholds must be:
- **Specific**: a number, not "good engagement"
- **Time-bound**: measured within the experiment window
- **Binary**: pass or fail, no "sort of passed"

## Process (step by step)

1. Read `idea.md` frontmatter: `business_model` selects the rubric lane. Load all available dimension files from `memory/ideas/<slug>/`; their presence decides `scoring_stage` (see Scoring Stages). The orchestrator states the stage when invoking the fast path or a pivot re-score; otherwise infer it from which files exist.
2. Check minimum viable input (≥ 3 dimensions, including Demand and Distribution). If not met, refuse and list missing inputs. At candidate stage, apply the competition prior cap.
3. Map each dimension's source data to a 0–100 sub-score using the rubrics.
4. Compute `floor_penalty` from any sub-scores below 25.
5. Compute `base_score` using weighted sum.
6. Apply `floor_penalty` and `missing_discount` to get `final_score`.
7. Determine `score_confidence`.
8. Issue `verdict` from threshold table.
9. Identify `top_strengths` (top 2 dimensions) and `top_weaknesses` (bottom 2 dimensions), each with a one-sentence `reason` that cites a concrete value from the source file (a ratio, a price, a churn figure, a named competitor), never an adjective.
10. Run RAT identification: list assumptions, score criticality × uncertainty, select the riskiest.
11. Design RAT experiment with pass/fail threshold.
12. If this is a pivot re-score, write to `pivot_scores.json` instead with `scoring_stage: pivot-rescore` and `pivot_id`.
13. Run `python tests/validate_memory.py --idea <slug>` if a shell is available and fix any ERROR line before presenting.

## Output

Write to `memory/ideas/<slug>/scores.json` (or `pivot_scores.json` for re-scores). The block below shows every field; `verdict`, `riskiest_assumption_test` and `dimension_rationale` appear only for `full-validation` and `pivot-rescore`, while `rank_label` and `competition_prior_capped` appear only for `candidate-quick-score`. Extra explanatory fields (`verdict_note`, `score_movement`, comparisons to sibling ideas) are welcome.

```json
{
  "idea_slug": "",
  "scored_at": "YYYY-MM-DD",
  "scoring_stage": "candidate-quick-score | full-validation | pivot-rescore",
  "lane": "b2c | b2b",
  "dimension_scores": {
    "demand": 0,
    "competition": 0,
    "monetization": 0,
    "distribution": 0,
    "retention": null,
    "founder_market_fit": 0
  },
  "dimension_rationale": {
    "demand": "",
    "competition": "",
    "monetization": "",
    "distribution": "",
    "retention": "",
    "founder_market_fit": ""
  },
  "competition_prior_capped": false,
  "weights_applied": {
    "demand": 0.20,
    "competition": 0.10,
    "monetization": 0.20,
    "distribution": 0.20,
    "retention": 0.15,
    "founder_market_fit": 0.15
  },
  "floor_penalty": 1.0,
  "base_score": 0,
  "missing_discount": 1.0,
  "final_score": 0,
  "rank_label": "strong-candidate | candidate | weak-candidate",
  "verdict": "pursue | test | pivot | drop",
  "score_confidence": "high | medium | low",
  "missing_inputs": [],
  "sources_checked": 0,
  "top_strengths": [
    { "dimension": "", "score": 0, "reason": "" }
  ],
  "top_weaknesses": [
    { "dimension": "", "score": 0, "reason": "" }
  ],
  "killer_dimensions": [],
  "riskiest_assumption_test": {
    "assumption": "",
    "category": "demand | monetization | distribution | retention | competition | founder_fit",
    "criticality": 0,
    "uncertainty": 0,
    "rat_score": 0,
    "experiment": {
      "type": "",
      "description": "",
      "duration": "",
      "estimated_cost": "",
      "pass_threshold": "",
      "fail_action": "pivot | drop | re-test with different channel"
    },
    "all_assumptions_ranked": [
      { "assumption": "", "criticality": 0, "uncertainty": 0, "rat_score": 0 }
    ]
  }
}
```

`sources_checked` is the count of distinct URLs across the `sources` arrays of the dimension files read. It is a transparency number for the memo, not a score input.

## Notes

- **Re-scoring pivots**: When scoring a pivot variant from `pivot_options.json`, write output to `memory/ideas/<slug>/pivot_scores.json`. Include a `pivot_id` field referencing the option.
- **Score decay**: If source data is older than 90 days (check `analyzed_at` or file timestamps), apply a 10% confidence penalty and flag stale inputs.
- **Geometric vs. additive**: The floor penalty provides multiplicative dynamics (one zero kills the score) while the weighted sum provides interpretable dimension contributions. This hybrid outperforms pure additive (hides fatal flaws) and pure geometric (too punishing for moderate weaknesses).
