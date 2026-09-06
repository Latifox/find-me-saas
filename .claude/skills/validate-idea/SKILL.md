---
name: validate-idea
description: Run the full ten-step validation on one idea and write a decision memo with a verdict, an experiment and kill criteria
argument-hint: "[idea description, or an existing slug]"
---

Run the workflow in `workflows/idea-validation.md` end to end.

Idea: $ARGUMENTS

Entry conditions:

- If `memory/user_profile.md` does not exist, run first-run onboarding first.
- If the argument names an existing slug in `memory/ideas/`, validate that one.
  Otherwise create `memory/ideas/<slug>/idea.md` from the description.
- The frontmatter must carry `business_model`. If who pays is not obvious, ask one
  question: consumers with their own card, or a business? Then set `status: in-validation`.

Follow all ten steps. Do not shortcut the research: every competitor price, market
size and channel cost needs a real source URL recorded in the file that uses it.

Before presenting the memo:

1. Run `python tests/validate_memory.py --idea <slug>` and fix every ERROR.
2. Set `status: scored` and `validated_at` in `idea.md`.

Present the memo in full. If the verdict is pivot or drop, offer `/pivot-idea <slug>`.
