---
name: market-scan
description: Research a market before committing to an idea - trends, competitors, size and how people actually acquire users
argument-hint: "[category] [--quick for trends only]"
---

Run the workflow in `workflows/market-deep-dive.md`.

Category: $ARGUMENTS

If the argument contains `--quick`, or the user is comparing several categories, run
the **Quick scan** section instead: trend analysis only, one or two platforms, then a
five-line summary of velocity, verdict, strongest signal, monetization evidence and
biggest risk. No competitor map, no sizing, no idea directory.

Otherwise run the full chain: trend analysis, competitor mapping, TAM/SAM/SOM, and
distribution.

Ask (or infer) the likely `business_model` before researching. It decides which
platforms are worth reading: consumer ideas point at TikTok, Reddit and the app
stores; business ideas point at web search, B2B communities and X.

Every research file ends with a `## Sources` section of real URLs, and gets a row
appended to the index in `memory/market_insights/README.md`.
