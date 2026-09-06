---
name: auto-pilot
description: Autonomous end-to-end run - onboards you if needed, finds ideas, validates the best one, and hands you a memo without stopping to ask
argument-hint: "[niche, or leave blank to use your profile]"
---

Run the whole pipeline without supervision. Announce the plan first, then execute
every stage in order without returning to the user between them.

Focus: $ARGUMENTS

**The rule that makes this autonomous:** do not stop to ask questions. Where you
would normally ask, choose the documented default, record the assumption, and keep
going. Gaps go in `inputs_missing`, `profile_gaps` and the memo's watermark; they do
not become questions. The only reasons to stop early are listed at the bottom.

Sequence:

1. **Profile.** If `memory/user_profile.md` is missing, run the fast path of
   first-run onboarding. This is the one place you may ask, because nothing
   downstream is meaningful without it, and it is five questions. If a profile
   exists, use it as-is; do not offer to update it.
2. **Research and generate.** Run `workflows/idea-generation.md` from the trend step.
   Reuse any `market_insights` file for the niche that is still fresh rather than
   re-running research.
3. **Rank.** Quick-score every candidate. Competition is capped at 45 and carries
   `competition_prior_capped: true`. Present the ranked table with rank labels.
4. **Validate the top candidate.** Run `workflows/idea-validation.md` in full on the
   highest-ranked idea. Set `business_model` from the profile's
   `preferred_business_model`; if that is `unsure`, infer it from the idea and say so.
5. **Memo.** Write the decision memo, set `status: scored` and `validated_at`.
6. **Verify.** Run `python tests/validate_memory.py --idea <slug>` and fix every
   ERROR before reporting.
7. **Report.** Give the final summary: the ranked candidates, the validated idea's
   score and verdict, the riskiest assumption with its experiment, and one line on
   what the run could not determine.

**Stop early only if:** the trend research finds no usable signal for the niche on
any platform, or scoring cannot meet minimum viable input (three dimensions
including demand and distribution), or the harness reports errors you cannot fix.
In each case say what stopped you and what you would need.

This run costs real research time and produces a full analysis. Say so before you
start, then get on with it.
