---
name: pivot-idea
description: Diagnose why an idea scored badly and generate evidence-backed pivots with projected scores
argument-hint: "[slug] [optional: the one variable to change]"
---

Run the workflow in `workflows/pivot-optimization.md`.

Arguments: $ARGUMENTS

**If the user named a single variable to change** (pricing, audience, channel,
platform, feature emphasis) - for example "what if I charged per client instead of
per seat" - run the **Micro-pivot** path: skip weakness detection, generate exactly
one option with `pivot_scope: micro` and `variables_changed: 1`, then re-score it.
If that named change fails the Minimum Viable Pivot Criteria, say so plainly rather
than substituting a different pivot.

**Otherwise** run the standard chain: confirm the current score, detect weaknesses
and their root causes, generate two or three options, and re-score the best one.

Apply the Slug Rule when deciding where output lands. One variable changed updates
the idea in place. Two variables, a change of `business_model`, or a change of the
core problem creates `memory/ideas/<slug>-<pivot-word>/` with `pivot_of` set, and
pauses the original with `superseded_by`.

Only `addressable_weaknesses` are pivot targets. A knowledge gap means a dimension
file is missing or thin; send it back to that research skill instead.
