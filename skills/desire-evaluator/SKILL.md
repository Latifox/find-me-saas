---
name: desire-evaluator
description: Scores the strength of core human desire motivations (survival, status, belonging, control, curiosity) for a given app idea to predict user pull and retention potential.
---

<!-- version: 0.2.0 | outputs: memory/ideas/<slug>/desire_scores.json -->

# Skill: desire-evaluator

## Purpose

Apps that tap into primal human desires outperform apps that only solve functional problems. This skill scores how strongly an app idea connects to core motivational drivers, which predicts organic virality, retention, and pricing power.

## Input

- Idea slug
- `memory/ideas/<slug>/idea.md` (app concept, emotional trigger, audience vocabulary, `business_model`)
- `memory/market_insights/<niche>-*-<YYYY>-<MM>.md` (pain language, complaint patterns; use all available platform files)
- Reference: `memory/extra-context/core-human-desires.md` (what drives core human desires)

## Desire Dimensions

| Dimension | Description | Example App |
|---|---|---|
| Survival | Health, safety, financial security | Calorie tracker, budgeting app |
| Status | Looking good, achieving, winning | Fitness leaderboard, portfolio tracker |
| Belonging | Community, connection, not being alone | Group savings, running clubs |
| Control | Mastery, autonomy, reducing chaos | Task manager, habit tracker |
| Curiosity | Learning, discovery, novelty | Language app, quiz game |

## Scoring Rubric

Score each desire 1–5 by answering its three diagnostic questions. Each "yes" backed by evidence from `idea.md` or market_insights is one point above the base of 1; two yes answers give 3, three give 4; award 5 only when all three are yes AND the audience's own vocabulary names the desire (a hashtag, a recurring complaint, a search query).

| Desire | Q1 — Is it the reason the user opens the app? | Q2 — Is failing to satisfy it painful or costly? | Q3 — Does the app make progress visible? |
|---|---|---|---|
| **Survival** | Does the user believe health, money, or safety is at stake? | Is the cost of inaction concrete (weight, debt, symptoms, fines)? | Can the user see risk going down (a number, a streak, a report)? |
| **Status** | Would the user show the output to someone else? | Is there a moment of public judgement (a review, a client question, a leaderboard)? | Does the app produce a visible artefact of competence? |
| **Belonging** | Is the app better with other specific people in it? | Does leaving mean losing a group, not just a tool? | Are others' activity or presence visible? |
| **Control** | Is the trigger a feeling of chaos, backlog, or not knowing? | Does the mess have a real cost (missed deadline, lost client, forgotten task)? | Does the app show a state of "everything is handled"? |
| **Curiosity** | Does the user come for something new each session? | Is missing out on the new thing felt as a loss? | Is there a discovery loop that resets (feed, puzzle, lesson)? |

Anchors: 1 = the desire is absent or incidental; 3 = present but not the reason to buy; 5 = the desire is what the audience says out loud about the problem.

### B2B lane

When `business_model` is `b2b-smb` or `b2b2c`, the buyer is a business but the desires still belong to a person: the owner, operator, or manager who signs. Map the five desires this way and score them for that person:

| Desire | B2B reading |
|---|---|
| Survival | Business survival: losing a client, a fine, an outage, a failed audit, cash flow |
| Status | Professional credibility in front of a client, boss, auditor, or peer; looking like a real vendor |
| Belonging | Membership of a practitioner community or partner ecosystem; "everyone in my niche uses X" |
| Control | Legibility of operations: knowing what is running, who approved it, what it costs |
| Curiosity | Weak in B2B; score above 2 only for research, data, or discovery products |

### Proceed Threshold

- If at least one desire scores ≥ 4: `desire_strength_label` is "strong" when the weighted mean (primary ×2, secondary ×1, rest ×0.5) is ≥ 3.5, else "moderate".
- If no desire scores ≥ 3: `desire_strength_label` is "weak", flag high churn risk in `notes`, and say so when presenting. Downstream, pricing applies no desire premium and retention treats habit formation as unlikely.
- `virality_potential`: "high" when Status or Belonging is the primary driver and scores 5; "medium" when either scores ≥ 4 or Curiosity scores 5; else "low".

## Process

1. Read `idea.md` (problem, emotional trigger, audience vocabulary, business model) and the market_insights narratives for the audience's own words.
2. Score each desire 1–5 with the rubric, writing a one-sentence rationale per desire that cites the evidence (a quote, a hashtag, a complaint pattern, a stated cost).
3. Identify the primary and secondary drivers (highest two; break ties toward the one the audience names).
4. Compute `desire_strength` as the weighted mean above and assign the label.
5. Assign `virality_potential`.
6. In `notes`, state how the primary desire behaves commercially: is it continuous or episodic, does it convert to revenue or cost for the buyer, and what re-triggers it. This paragraph is what retention-predictor and pricing-and-wtp read.

## Output

Write to `memory/ideas/<slug>/desire_scores.json`:

```json
{
  "idea_slug": "",
  "evaluated_at": "YYYY-MM-DD",
  "lane": "b2c | b2b",
  "scores": {
    "survival": 0,
    "status": 0,
    "belonging": 0,
    "control": 0,
    "curiosity": 0
  },
  "score_rationale": {
    "survival": "",
    "status": "",
    "belonging": "",
    "control": "",
    "curiosity": ""
  },
  "primary_driver": "",
  "secondary_driver": "",
  "desire_strength": 0,
  "desire_strength_label": "strong | moderate | weak",
  "virality_potential": "high | medium | low",
  "notes": ""
}
```

## Notes

- retention-predictor reads `primary_driver`, `desire_strength_label` and `notes`: Survival and Control drivers raise habit-formation potential; a Status driver with a recurring external judgement moment (client review, audit) is the strongest B2B retention signal; Curiosity alone predicts novelty churn.
- pricing-and-wtp reads `primary_driver` for the desire-premium multiplier and applies none when the label is "weak".
