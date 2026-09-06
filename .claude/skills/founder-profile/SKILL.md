---
name: founder-profile
description: Create or refresh your builder profile - the background, constraints and target buyer that every other command scores against
argument-hint: "[full | short | browse | skip]"
---

Run first-run onboarding from `skills/user-background-interviewer/SKILL.md`.

$ARGUMENTS

If the user named a path (full, short, browse, skip), go straight to it. Otherwise
show the opening message and let them choose.

If `memory/user_profile.md` already exists, do not overwrite it silently. Present
the existing profile summary and offer to keep it, update it, or add interest
domains, exactly as Step 0 of that skill describes.

Whichever path runs, four things must end up in the profile because every other
command depends on them:

- **technical level** - filters ideas to what this person can build
- **domain, audience and inner circle** - drives founder-market fit and warm channels
- **constraints**: hours per week, monthly budget, risk tolerance
- **target buyer** - sets `preferred_business_model`, which selects the B2C or B2B
  rubric lane in eight downstream skills

The browse and skip paths leave constraints unknown. That is allowed, but say so,
and record them in `profile_gaps` so later commands know to ask.

Finish by confirming what was captured and naming the gaps, then suggest
`/find-idea` if they have no idea yet or `/validate-idea` if they do.
