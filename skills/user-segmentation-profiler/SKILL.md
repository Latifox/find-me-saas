---
name: user-segmentation-profiler
description: Classifies the user into an ICP tier (beginner/builder/growth) based on experience, constraints, and goals. Run once per user session before any workflow.
---

<!-- version: 0.2.0 | outputs: memory/user_profile.md -->

# Skill: user-segmentation-profiler

## Purpose

Classify the user into one of three ICP tiers and capture their constraints so all subsequent skills can tailor their output and recommendations appropriately.

## Input

- Conversation history or direct user answers about experience, budget, time, and goals.
- Optional: existing `memory/user_profile.md` (update if already exists)

## Process

1. Read `memory/user_profile.md`. If the interviewer already captured shipped products, time, budget, and risk tolerance, do not ask again; go to step 4.
2. Ask the missing constraint questions in **one message**, numbered, so the user can answer in one reply:

   > Three quick questions to calibrate the recommendations:
   > 1. Have you shipped a product before? If yes: how many, and did any earn revenue?
   > 2. Roughly how many hours per week can you give this, and what monthly budget (USD) for tools or ads?
   > 3. How much risk are you comfortable with: **low** (I need this to work within a few months), **medium**, or **high** (I can experiment for a year)?

3. If the user declines any part, write `"unknown"` for that field, add it to `profile_gaps`, and move on. Do not re-ask. Downstream skills treat `unknown` budget as bootstrap and `unknown` risk as low, and the decision memo lists the gaps.
4. Score against the tier rubric below. When evidence is mixed, assign the lower tier and record the caveat in `tier_rationale`; a wrong upgrade sends a founder into channels they cannot run.
5. Write `strategy_recommendations` (3–6 bullets) that follow from the tier and constraints: which channels to prefer, what budget assumptions downstream skills should use, and what pace the kill criteria should assume.
6. Merge into `memory/user_profile.md`, preserving every field the interviewer wrote.

### Tier Rubric

| Tier | Assign when | Downstream effect |
|---|---|---|
| `beginner` | No shipped product, no audience, or fewer than 5 hours/week | Channels with fast feedback only; paid off the table; effort estimates upgraded one level |
| `builder` | Shipped at least one product but no revenue, or revenue without repeatable acquisition; can build but has not sold | No adjustment; paid over $500/mo flagged risky |
| `growth` | Shipped a product that earned revenue AND demonstrates acquisition literacy (talks in CAC, LTV, conversion, channels) | Paid channels unlocked; effort estimates downgraded one level |

Marketing or growth experience alone is a `growth` **signal**, not proof; without shipped revenue assign `builder` and note "re-segment to growth if a revenue-generating product is confirmed".

### Re-segmentation Triggers

Re-run this skill (and note it in the profile) when the user reveals any of: a shipped product not previously mentioned, revenue figures, an audience of meaningful size, a change in hours or budget, or a change in whether this is a main focus or a side project.

## Output

Write to `memory/user_profile.md` (merge with existing if present):

```json
{
  "icp_tier": "beginner | builder | growth",
  "tier_rationale": "",
  "shipped_products": 0,
  "revenue_history": "none | some | repeatable | unknown",
  "budget_constraint": "low | medium | high | unknown",
  "budget_monthly_usd": null,
  "time_per_week_hours": null,
  "main_focus_or_side_project": "main | side | unknown",
  "risk_tolerance": "low | medium | high | unknown",
  "profile_gaps": [],
  "strategy_recommendations": []
}
```

## Notes

- `budget_constraint` maps to cac-modeler budget tiers: low = bootstrap, medium = lean, high = moderate or serious. `unknown` is treated as bootstrap.
- `risk_tolerance` sets the pace of kill criteria in decision-memo: low = decide within the RAT window, medium = one extra iteration, high = up to three iterations before dropping.
- The idea-validation workflow re-checks these three fields before cac-modeler (the profile gap gate) and asks them if still missing.
