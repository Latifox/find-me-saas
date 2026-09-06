---
name: idea-status
description: Portfolio view - every idea you have analysed, its score, verdict and what is still missing
argument-hint: "[optional slug for a single idea]"
---

Read `memory/ideas/` and report the portfolio. Do not run any analysis.

Filter: $ARGUMENTS

For every idea directory, read `idea.md` frontmatter and `scores.json` if present,
then produce a table ordered by score descending:

| Idea | Model | Stage | Score | Verdict | Status | Missing |
|---|---|---|---|---|---|---|

- **Stage** is `scoring_stage`: candidate-quick-score, fast-validation or full-validation.
- **Verdict** is the verdict for a full validation, or the rank label for a quick score.
  Never show a verdict for a quick score.
- **Missing** is the count of dimension files not yet written, from `missing_inputs`.

Then call out, in prose:

- Ideas with dimension files but no `decision_memo.md` - started and abandoned.
- Ideas still at `status: candidate` whose scores came from a capped competition
  prior, so their ranking is provisional.
- Any idea whose `superseded_by` points at a pivot, with where it went.

Finish with one recommendation: which idea deserves the next hour, and why. If a
single slug was given, skip the table and give the full picture for that one idea.
