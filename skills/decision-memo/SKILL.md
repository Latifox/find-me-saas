---
name: decision-memo
description: Writes a concise, human-readable decision brief summarizing the full validation analysis — including score, verdict, RAT experiment, pre-mortem, and tier-appropriate next actions. The document a founder actually acts on.
---

<!-- version: 0.5.0 | outputs: memory/ideas/<slug>/decision_memo.md (and updates memory/ideas/<slug>/idea.md status) -->

# Skill: decision-memo

## Purpose

After all analysis is complete, produce a document the user can actually act on. This is not a report — it is a **decision brief**. It surfaces the most important signals, names the riskiest assumption, and gives a concrete next action calibrated to the founder's tier. A good decision memo makes the reader feel slightly uncomfortable — that means it's honest.

## Input

- Idea slug
- `memory/ideas/<slug>/idea.md` (`business_model`, `status`; this skill updates the status)
- `memory/ideas/<slug>/scores.json` (required — includes RAT)
- `memory/ideas/<slug>/weaknesses.json` (if available)
- `memory/ideas/<slug>/pivot_options.json` (if available and verdict is "pivot")
- All other available dimension files in `memory/ideas/<slug>/`
- `memory/user_profile.md` (for tier-appropriate recommendations)

## Writing Principles

The memo must be **scannable in under 2 minutes**. Follow these rules:

1. **No hedging.** "This might work if…" is banned. State the verdict and own it.
2. **Evidence over opinion.** Every strength and risk must cite a specific data point from a dimension file (k-factor, LTV:CAC ratio, D30 retention, WTP range, etc.).
3. **Asymmetric emphasis on risks.** Humans overweight strengths and underweight risks. The memo corrects for this by giving risks more detail than strengths.
4. **One clear next action.** Not three options — one. The alternative path exists only as a contingency.
5. **Respect the founder's tier.** Don't tell a beginner to "optimize your Meta ads funnel." Don't tell a growth-tier founder to "watch some TikTok tutorials."
6. **Argue against yourself.** The Devil's Advocate section gives the three strongest reasons the verdict is wrong, each tied to a data point. Strawmen are banned: if the counterargument would not change a reasonable reader's mind, find a better one.
7. **Cite URLs, not file names.** Every strength, risk, and counterargument that rests on a fact must be traceable to a URL in the Sources section, pulled from the `sources` arrays of the dimension files. A reader a week from now must be able to re-verify.

## Formatting Constraints

| Section | Max length | Purpose |
|---|---|---|
| Verdict line | 1 sentence | Instant signal |
| Score + confidence | 1 line | Quantitative anchor |
| Validation watermark | 1–2 lines | Trust calibration (only if confidence < high) |
| Top 3 Strengths | 1 sentence each, with one data point | What's working |
| Top 3 Risks | 2 sentences each: the risk + what happens if ignored | What kills it |
| Riskiest Assumption | 3–5 sentences | The one thing to test before building anything |
| Pre-mortem | 3 bullet points | Failure imagination exercise |
| Devil's Advocate | 3 bullet points, 1–2 sentences each | The strongest case against the verdict |
| Recommended Next Step | 2–4 sentences with specifics | What to do this week |
| Kill criteria | 1–2 sentences | When to walk away |
| Alternative Path | 1–2 sentences | Plan B |
| Profile gaps | 1 line, only if constraints are unknown | What the memo could not calibrate |
| Sources | 3–10 links | Re-verification |

Total memo length: **700–1,000 words of prose**, measured from the end of the frontmatter to the `## Sources` heading. The Sources list itself is not counted, because citations should never compete with analysis for space. `tests/validate_memory.py` warns outside that band and fails above 1,200 words on the full body. If it's longer, cut the strengths before the risks.

The band was 600–900 until task 4. Seven memos written against that budget exceeded it on first draft (977, 1,024, 1,081, 1,072, 1,082 and 1,009 words), and the last needed three trim passes to comply. Ten evidence-bearing sections do not fit in 900 words; the budget was wrong, not the memos.

## Process

1. Load `scores.json` and all available dimension files.
2. Check `score_confidence`. If "low", compose a validation watermark (see below).
3. Identify the 3 highest-scoring dimensions → strengths. For each, pull one concrete data point from the source file (e.g., "k-factor estimated at 0.6" not "good viral potential").
4. Identify the 3 lowest-scoring dimensions → risks. For each, describe what goes wrong if ignored. If `weaknesses.json` exists, use its `root_cause_type` and `failure_mode` to add specificity.
5. Extract the RAT from `scores.json.riskiest_assumption_test`. Frame it as the one question to answer before writing a line of code.
6. Run a **pre-mortem**: assume the idea failed 12 months from now. Write 3 most likely causes of death based on the risk profile.
6b. Write the **Devil's Advocate**: the three strongest arguments that the verdict is wrong. For a pursue/test verdict, argue for drop; for a pivot/drop verdict, argue for building. Each argument cites a specific number or source from a dimension file. Then state in one sentence why the verdict stands anyway (or, if it does not, change the verdict and note it in `scores.json`).
6c. Collect **Sources**: the URLs from the `sources` arrays of the dimension files that back the strengths, risks, and counterarguments. Minimum three. Prefer primary pages (pricing pages, review pages, statistics tables) over articles about them.
7. Compose the recommended next step:
   - If verdict = **pursue**: the next step is to build a scoped MVP (define what "scoped" means for this idea).
   - If verdict = **test**: the next step IS the RAT experiment from `scores.json`. Restate it with concrete specifics (channel, spend, threshold, timeline).
   - If verdict = **pivot**: the next step is the recommended pivot from `pivot_options.json` (if available) or running the pivot-engine skill.
   - If verdict = **drop**: the next step is to archive and move on. Name one thing learned from the analysis that applies to future ideas.
8. Define **kill criteria**: the specific outcome that means "stop and move on." This is the inverse of the RAT pass threshold.
9. Write the alternative path — what to do if the recommended step fails or the kill criteria is met.
10. If `user_profile.md` has `unknown` or missing `time_per_week_hours`, `budget_constraint`, or `risk_tolerance`, add the one-line **Profile gaps** note after the watermark naming what the memo could not calibrate (pace of kill criteria, paid-channel viability).
11. Write the memo following the template below.
12. Update `memory/ideas/<slug>/idea.md` frontmatter: `status: scored` and `validated_at: <YYYY-MM-DD>`. Never leave a validated idea at `candidate` or `in-validation`.
13. Run `python tests/validate_memory.py --idea <slug>` if a shell is available and fix any ERROR before presenting.

### Validation Watermark

If `score_confidence` from `scores.json` is not "high", insert a watermark immediately after the score line:

| Confidence | Watermark |
|---|---|
| **medium** | "This score is based on incomplete data. {list missing dimensions}. Run these analyses before making a build/no-build decision." |
| **low** | "LOW CONFIDENCE — Only {N} of 7 dimensions scored. This verdict is directional, not conclusive. Required before acting: {list mandatory missing analyses}." |

### Pre-mortem Method

The pre-mortem is a proven debiasing technique (Klein, 2007). It forces the founder to imagine failure before committing resources.

Instructions:
1. Assume the idea launched and failed within 12 months.
2. Working backward from the risk profile and killer dimensions, write the 3 most probable causes of death.
3. Each cause must be specific and tied to a scored dimension — not generic ("ran out of money" is too vague; "CAC exceeded LTV by 4x because TikTok organic reach declined and no paid channel was viable under $500/mo" is useful).

## Output

Write to `memory/ideas/<slug>/decision_memo.md`:

```markdown
---
idea_slug: ""
verdict: "pursue | test | pivot | drop"
final_score: 0
score_confidence: "high | medium | low"
created_at: ""
---

# Decision Memo: <Idea Name>

## Verdict: <PURSUE / TEST / PIVOT / DROP>

**Score: X/100** | Confidence: <high / medium / low>

<Validation watermark — only if confidence is medium or low>

<Profile gaps: one line, only if hours / budget / risk tolerance are unknown>

---

## Why This Score

<2–3 sentences explaining what the score means in plain language. Not a recap of methodology — a statement of what the analysis revealed about this idea's viability.>

## Top 3 Strengths

1. **<Dimension>** (<score>/100): <one sentence with specific data point>
2. **<Dimension>** (<score>/100): <one sentence with specific data point>
3. **<Dimension>** (<score>/100): <one sentence with specific data point>

## Top 3 Risks

1. **<Dimension>** (<score>/100): <the risk>. <what happens if ignored — the failure mode.>
2. **<Dimension>** (<score>/100): <the risk>. <what happens if ignored — the failure mode.>
3. **<Dimension>** (<score>/100): <the risk>. <what happens if ignored — the failure mode.>

## Riskiest Assumption

The assumption most likely to kill this idea:

> "<the assumption, stated plainly>"

**Test it before building anything.** <Restate the RAT experiment: what to do, how long, how much it costs, and what "pass" looks like.>

## Pre-mortem: If This Fails in 12 Months

1. <Most likely cause of death — specific, tied to data>
2. <Second most likely cause — specific, tied to data>
3. <Third most likely cause — specific, tied to data>

## Devil's Advocate

The strongest case against this verdict:

1. <Counterargument with a specific number or source>
2. <Counterargument with a specific number or source>
3. <Counterargument with a specific number or source>

<One sentence: why the verdict stands despite these.>

---

## What To Do Now

<The one recommended next step — concrete, specific, calibrated to founder tier. Include timeline and cost if applicable.>

**Kill criteria:** <The specific outcome that means stop. e.g., "If landing page converts below 5% after 200 visitors, drop this idea.">

## If That Doesn't Work

<Alternative path — one sentence. What to do if the recommended step fails or kill criteria is met.>

## Sources

- [<title>](<url>) — <what it backs>
- [<title>](<url>) — <what it backs>
- [<title>](<url>) — <what it backs>
```

## Notes

- If the verdict is **pivot** and `pivot_options.json` exists, embed the recommended pivot in the "What To Do Now" section with enough detail to act on immediately.
- If the verdict is **drop**, the tone should be respectful but firm. Don't soften a drop verdict. The value of a good drop is the time it saves for the next idea.
- The memo should be re-generated whenever `scores.json` is updated (e.g., after an in-place pivot re-score). Append a version note at the bottom: `_v2 — re-scored after [pivot description]_`.
- When a pivot earns a new slug (see the Slug Rule in `skills/pivot-engine/SKILL.md`), do not rewrite the original memo. Append one line to it instead: `_Superseded by [<new-slug>](../<new-slug>/decision_memo.md) — <one-line reason>._` The original memo stays as the record of the decision that was made at the time.
- Fast-path runs (`scoring_stage: fast-validation`) do not get a memo. If asked for one, run the full chain first; a four-dimension score cannot support a decision brief.
- Decision memos are the primary artifact the user references after the session. Optimize for re-readability days later, not just first-read clarity.
- Tier language differs by lane. B2C beginners get channels with fast feedback (community posting, short-form video); B2B founders get the first ten conversations (who, where, what to ask) and the channel that must be ramping before the warm network exhausts.
