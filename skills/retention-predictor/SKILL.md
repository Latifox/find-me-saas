---
name: retention-predictor
description: Predicts retention potential by evaluating usage frequency, habit formation mechanics, and churn risk factors for a B2C app idea.
---

<!-- version: 0.2.0 | outputs: memory/ideas/<slug>/retention.json -->

# Skill: retention-predictor

## Purpose

Retention determines LTV. An app that churns users in week 1 can't build a business regardless of acquisition. This skill evaluates how sticky the idea is structurally — not based on feature lists, but on the underlying usage pattern and habit formation potential.

## Input

- Idea slug
- `memory/ideas/<slug>/idea.md` (app concept, `business_model`)
- `memory/ideas/<slug>/desire_scores.json` (desire strength and primary driver inform habit potential)
- Optional: `memory/ideas/<slug>/pricing.json` (pricing model affects commitment), `memory/ideas/<slug>/competitors.json` (incumbent churn signals from reviews)
- `memory/market_insights/<niche>-*-<YYYY>-<MM>.md` (usage cadence and complaint patterns)

### Lane selection

`business_model` = `b2c` or `prosumer` uses the B2C lane (D1/D7/D30 user retention). `b2b-smb` or `b2b2c` uses the B2B lane (monthly logo churn, cohort retention at month 1-2, 6 and 12). Both lanes fill `d30_equivalent` so idea-scoring can apply one rubric.

## Evaluation Factors

| Factor | High Retention Signal | Low Retention Signal |
|---|---|---|
| Usage frequency | Daily or multiple times/day | Weekly or less |
| External trigger | Clear real-world trigger (meal, workout, payday) | No natural trigger |
| Progress/reward loop | Clear progress visible over time | No feedback loop |
| Network effects | Gets better with more users | No network component |
| Data lock-in | User data accumulates | Nothing to lose by leaving |
| Habit stack | Fits into existing daily routine | Requires behavior change |

## Benchmarks

### B2C lane — D1 / D7 / D30 by category (median, heuristic ranges from public mobile-analytics reports; treat as bands, not point estimates)

| Category | D1 | D7 | D30 | Note |
|---|---|---|---|---|
| Health & fitness | 25–35% | 12–18% | 6–12% | Spikes in January, decays by March |
| Habit / lifestyle | 25–35% | 12–20% | 6–12% | Streak mechanics lift D7 more than D30 |
| Finance / budgeting | 25–35% | 15–22% | 10–18% | High trust barrier, sticky once data accumulates |
| Productivity / tools | 22–30% | 12–18% | 8–15% | Utility apps retain on need, not habit |
| Social / messaging | 30–45% | 20–30% | 15–25% | Network effects dominate |
| Education / learning | 25–35% | 10–15% | 5–10% | Motivation decay is the norm |
| Creative tools | 25–35% | 15–22% | 10–18% | Output ownership creates lock-in |
| Games (casual) | 30–40% | 10–15% | 3–8% | Disposable by design |

### B2B lane — monthly logo churn by segment (heuristic ranges from public SaaS benchmark reports)

| Segment | Monthly logo churn | Annualised | Typical driver |
|---|---|---|---|
| Very small business / solo operators, self-serve, < $100/mo | 5–8% | 45–65% | Customer business failure, card failures |
| SMB self-serve, $100–500/mo | 3–6% | 30–50% | Champion leaves, tool consolidation |
| SMB with onboarding or light sales, $500–2,000/mo | 1.5–3% | 17–30% | Value not embedded in a recurring workflow |
| Mid-market, annual contracts | 0.5–1.5% | 6–17% | Renewal-time re-evaluation |

Use the lower end when the product is embedded in a client deliverable or calendar trigger (report, audit, renewal, onboarding) and the upper end when usage is event-only.

### D30 equivalent (both lanes)

`d30_equivalent` lets idea-scoring apply its retention bands to either lane.

- B2C: `d30_equivalent = predicted_retention.d30` (percent).
- B2B: `d30_equivalent = clamp(1 - 12 × monthly_churn_estimate, 0, 1) × 100`. Examples: 3%/mo → 64; 5%/mo → 40; 8%/mo → 4. This is a mapping heuristic, not a measurement; say so in `retention_score_reasoning`.

## Churn Risk Rubric

Score each factor high / medium / low with a sentence of evidence. Count the highs:

| High-severity factors | `churn_risk` |
|---|---|
| 0 | low |
| 1–2 | medium |
| 3+ (or any factor the founder cannot influence, such as customer business mortality, rated high) | high |

Factor library: no external trigger; value decays as the user succeeds (the clean-report paradox); free alternative is good enough; onboarding requires data the user does not have; single-champion dependency; customer business mortality (B2B); seasonal demand cliff; incumbent can add the feature; pricing indexed to a metric that shrinks when the customer struggles.

## Retention Verdict

| Lane | sticky | moderate | disposable |
|---|---|---|---|
| B2C | D30 ≥ 15% with a daily or triggered loop | D30 8–14% | D30 < 8% or no trigger |
| B2B | monthly churn ≤ 3% with a calendar or deliverable trigger | 3–6% | > 6% or event-only usage |

## Process

1. Read `idea.md` and select the lane from `business_model`.
2. Estimate natural usage frequency from the problem cadence (daily tooth-brushing vs. annual tax filing) and name the external trigger(s) that cue usage. If none exists, say "none" and treat it as a high-severity churn factor.
3. Score habit formation 1–5 across the six factors in the table above (each factor scored 0/0.5/1, sum rounded, minimum 1). Cite `desire_scores.json`: Survival and Control primary drivers add 0.5; a Status driver with a recurring judgement moment adds 0.5 in the B2B lane.
4. Predict retention from the benchmark table for the closest category or segment, adjusted by habit score (±1 band) and by competitor review signals when `competitors.json` exists.
5. Compute `d30_equivalent`.
6. Score churn-risk factors, count highs, assign `churn_risk`, and name the single `top_churn_risk_factor`.
7. List 3–5 `retention_levers`, each with impact and detail; include at least one lever that addresses the top churn risk.
8. Assign `retention_verdict` from the table, write `retention_score` (0–100 per idea-scoring's retention bands) with reasoning, and write the file.

## Output

Write to `memory/ideas/<slug>/retention.json`:

```json
{
  "idea_slug": "",
  "predicted_at": "YYYY-MM-DD",
  "lane": "b2c | b2b",
  "natural_usage_frequency": "multiple daily | daily | weekly | monthly | infrequent | event-driven",
  "usage_frequency_rationale": "",
  "external_trigger": "",
  "habit_formation_score": 0,
  "habit_formation_rationale": "",
  "predicted_retention": {
    "d1": null,
    "d7": null,
    "d30": null,
    "m1_to_m2": null,
    "m6": null,
    "m12": null,
    "monthly_churn_estimate": null,
    "benchmark_used": ""
  },
  "d30_equivalent": 0,
  "churn_risk_factors": [
    { "factor": "", "severity": "high | medium | low", "detail": "" }
  ],
  "top_churn_risk_factor": "",
  "retention_levers": [
    { "lever": "", "impact": "very-high | high | medium | low | structural", "detail": "" }
  ],
  "churn_risk": "low | medium | high",
  "retention_verdict": "sticky | moderate | disposable",
  "retention_score": 0,
  "retention_score_reasoning": "",
  "inputs_used": [],
  "inputs_missing": []
}
```

Fill the `predicted_retention` keys for the active lane and leave the others `null`.

## Notes

- `retention_score` is the number idea-scoring copies into its retention dimension; keep the reasoning tied to the band table in idea-scoring so the two files agree.
- cac-modeler reads `monthly_churn_estimate` (B2B) or `d30` (B2C) for lifespan. If this file is missing, cac-modeler falls back to category medians and LTV confidence drops to medium at best.
