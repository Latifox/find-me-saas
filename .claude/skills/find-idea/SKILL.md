---
name: find-idea
description: Research a market and generate 7-10 scored idea candidates matched to your background
argument-hint: "[niche or leave blank to infer from your profile]"
---

Run the workflow in `workflows/idea-generation.md` end to end.

Niche or area of interest: $ARGUMENTS

Entry conditions:

- If `memory/user_profile.md` does not exist, run first-run onboarding first.
- If no niche was given, infer candidates from the profile and existing
  `memory/market_insights/` files, then confirm with the user before researching.

Follow the workflow's skill chain in order and present what each step's
`present` line asks for. Do not skip the trend research; ideas generated without
it are speculation.

When you present the ranked candidates, obey the scoring rules:

- Candidates carry a **rank label** (strong-candidate, candidate, weak-candidate),
  never a verdict. Do not use the words pursue, test, pivot or drop here.
- Competition is capped at 45 until `competitor-mapper` has actually run. Say so.
  In five full validations in this project it fell 20-40 points under research.

End by offering `/validate-idea <slug>` on the top candidate.
