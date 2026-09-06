---
name: weakness-detection
description: Analyzes idea-scoring output to identify the weakest dimensions, root causes of low scores, and probable failure modes if the idea were pursued as-is.
---

<!-- version: 0.2.0 | outputs: memory/ideas/<slug>/weaknesses.json -->

# Skill: weakness-detection

## Purpose

Before triggering the pivot engine, understand WHY dimensions are weak. A low distribution score might mean "no viral loop" (fixable) or "fundamentally wrong category for organic growth" (structural). Surface the root cause, not just the symptom.

## Input

- Idea slug
- `memory/ideas/<slug>/scores.json` (required)
- `memory/ideas/<slug>/idea.md` (`business_model`)
- All available dimension files in `memory/ideas/<slug>/`
- `memory/market_insights/<niche>-*-<YYYY>-<MM>.md` (to tell a knowledge gap from a real weakness)

## Weakness Classification

| Root Cause Type | Description | Fix Type |
|---|---|---|
| Structural | Inherent to the idea, can't be pivoted away | Drop or major pivot |
| Situational | Weak due to user's current constraints | Fixable (more time, budget) |
| Knowledge gap | Weak because data is missing | Run more research |
| Addressable | Weak but has a clear fix | Targeted pivot |

## Weak Threshold

A dimension is **weak** when its score is below 40, or when it is the lowest-scoring dimension and below 55. Any dimension below 25 (a killer dimension in idea-scoring) is weak and automatically **critical**. Missing dimensions (null) are weak with `root_cause_type: knowledge-gap`.

## Severity Matrix

| `overall_weakness_severity` | Condition |
|---|---|
| **fatal** | Any structural weakness below 25, OR two or more structural weaknesses below 40, OR Demand and Distribution both weak |
| **major** | One structural weakness below 40, OR two or more addressable/situational weaknesses below 40, OR one killer dimension that is addressable |
| **minor** | Everything else: weaknesses are addressable, situational, or knowledge gaps, and none is below 25 |

## Failure Mode Library

Use these as starting points for `failure_mode`; make each specific to the idea and cite the score that predicts it.

| Dimension | Typical B2C failure mode | Typical B2B failure mode |
|---|---|---|
| Demand | Launch gets installs from curiosity, D7 collapses because the problem was interesting, not painful | Buyers agree the problem is coming, nobody has it yet; the product is 18 months early and cancels at first renewal |
| Competition | Incumbent with 100K ratings adds the differentiating feature in one release | Funded adjacent vendor already owns the buyer relationship and ships the module in a quarter |
| Monetization | Free tier is good enough; conversion stays under 2% and revenue never covers acquisition | Revealed price is $0 (free tools, checklists); the buyer never forms a budget line |
| Distribution | The only working channel (one creator, one subreddit) exhausts at a few thousand installs | Warm network exhausts at 20-30 customers and SEO or partnerships never ramp before runway ends |
| Retention | No external trigger; the habit never forms and D30 sits under 5% | Customer business mortality: the buyer churns because the buyer fails, regardless of product |
| Founder-Market Fit | Founder cannot produce content in the channel the category requires | Founder has no access to the buyer and the sale needs a relationship they do not have |

## Process

1. Load `scores.json` and identify weak dimensions with the threshold above.
2. For each weak dimension, read its source file and write a one-paragraph root cause. Name the specific value that produced the low score (a ratio, a churn figure, a competitor, a missing channel).
3. Classify the root cause: **structural** (inherent to the idea; changing it changes the idea), **situational** (the founder's current constraints: time, budget, audience), **knowledge-gap** (the file is missing or rests on one source), **addressable** (a clear fix exists that changes one variable).
4. Describe the failure mode if the idea proceeds unchanged, using the library as a starting point.
5. Sort weaknesses into `critical_weaknesses` (structural, or any dimension below 25) and `addressable_weaknesses` (addressable or situational).
6. Assign `overall_weakness_severity` from the matrix and write the file.

## Output

Write to `memory/ideas/<slug>/weaknesses.json`:

```json
{
  "idea_slug": "",
  "detected_at": "YYYY-MM-DD",
  "weak_threshold_applied": "score < 40, or lowest dimension < 55",
  "weak_dimensions": [
    {
      "dimension": "",
      "score": 0,
      "root_cause_type": "structural | situational | knowledge-gap | addressable",
      "root_cause_description": "",
      "failure_mode": "",
      "source_value_cited": ""
    }
  ],
  "critical_weaknesses": [],
  "addressable_weaknesses": [],
  "knowledge_gaps": [],
  "overall_weakness_severity": "fatal | major | minor",
  "severity_rationale": ""
}
```

## Notes

- pivot-engine only generates options for `addressable_weaknesses`; `knowledge_gaps` are sent back to the relevant research skill instead of being pivoted around.
- When `overall_weakness_severity` is fatal, say so plainly when presenting; the honest output of this skill is sometimes "no pivot can fix this".
