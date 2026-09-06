---
name: gut-check
description: Three-minute screen on four dimensions - can rule an idea out, never rules one in
argument-hint: "[idea description]"
---

Run the **Fast path** section of `workflows/idea-validation.md`, not the full chain.

Idea: $ARGUMENTS

Five steps: one trend platform, competitor mapping in light mode, desire, distribution,
then scoring at `scoring_stage: fast-validation`. Monetization and retention are left
`null` deliberately.

Write no decision memo. Present the gut-check summary inline: score and verdict, the
strongest dimension with its evidence, the weakest with its evidence, the riskiest
assumption, and this sentence verbatim:

> This is a gut check on four dimensions - it did not examine whether anyone will pay
> or whether they will stay.

The idea keeps `status: in-validation`. Only a full validation earns `scored`.

Because two of six dimensions are missing, the arithmetic makes `pursue` unreachable.
A fast `drop` is trustworthy; a fast `test` means "worth the full chain", never "worth
building". Offer `/validate-idea <slug>` at the end.
