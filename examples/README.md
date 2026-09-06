# Two real runs. Neither idea survived.

These are complete, unedited outputs from FindMeSaaS. Nothing here was written for the README. Both analyses were produced by running the workflow, doing live web research, and letting the scoring algorithm reach whatever verdict it reached.

Both ideas got a no.

That is the point of showing them. A validation tool that agrees with you is a very expensive way to feel good.

---

## What happened

| | **Shadow AI for MSPs** | **Habit tracker for climbers** |
|---|---|---|
| Who pays | Managed service providers reselling to SMB clients | Recreational climbers, consumer subscription |
| Verdict | **PIVOT — 43/100** | **DROP — 28/100** |
| Killed by | Competition, 22/100 | Monetization, 22/100 |
| Sources checked | 15 | 10 |
| Research files | 1 | 1 |
| Memo length | 829 words | 837 words |
| Test experiment designed | 14 days, under $50 | 14 days, under $30 |

Both scores were pulled down by the same mechanism. Any dimension below 25 multiplies the final score, so one fatal flaw cannot be averaged away. In both runs that multiplier was 0.88, and in both runs it was the difference between a comfortable-looking number and an honest one.

### Score breakdown

| Dimension | Weight | Shadow AI | Habit tracker |
|---|---|---|---|
| Demand | 20% | 64 | 42 |
| Competition | 10% | **22** | 32 |
| Monetization | 20% | 55 | **22** |
| Distribution | 20% | 32 | 26 |
| Retention | 15% | 48 | 42 |
| Founder-market fit | 15% | 58 | 30 |
| | | **43 final** | **28 final** |

---

## Start here

Read the two decision memos first. Each is about 830 words and takes three minutes.

- **[Shadow AI for MSPs](memory/ideas/shadow-ai-discovery-for-msp/decision_memo.md)** — a genuinely good market the founder cannot reach
- **[Habit tracker for climbers](memory/ideas/habit-tracker-climbers/decision_memo.md)** — a problem the audience never actually complained about

Then open `scores.json` in either folder to see how the number was built, and any dimension file to see the evidence underneath it.

---

## The two findings worth your time

### One: the competitor nobody thinks to look for

The shadow-AI idea rested on a real and well-documented gap. Enterprise tools start around $25,000 to $40,000 a year. The most down-market credible vendor still charges a $750 monthly floor. A sixty-seat company cannot buy any of them. The gap was priced, sourced and true.

Then research found that **Microsoft bundles Purview into M365 Business Premium**. For any Microsoft-native client, adequate discovery now arrives inside a licence they already pay for. The competitor was not another startup. It was a line item the buyer had already bought.

Competition fell from an estimated 55 to a researched 22, and the whole idea went with it.

### Two: the premise the audience never stated

The climbing idea assumed climbers know what training to do and fail to do it consistently. Reasonable. Plausible. Probably true of the person who thought of it.

Research read the actual complaints about the three leading climbing training apps. Climbers ask for force-gauge integration, automated periodization, in-workout grade logging, and shorter sessions. **Nobody complains about failing to keep habits.** Meanwhile the category's authority brand gives away a hundred structured workouts for free.

Two searches. The premise was gone before any pricing work happened.

---

## The system corrected itself, on the record

Competition is the dimension that moves most when assumption meets research. Across five full validations in this project it fell every single time:

| Idea | Estimated | Researched | Drop |
|---|---|---|---|
| Automation security scanner | 88 | 38 | −50 |
| Delivery provenance attestation | 85 | 45 | −40 |
| Agent governance layer | 85 | 65 | −20 |
| GEO category panel | 62 | 32 | −30 |
| Shadow AI for MSPs | 55 | 22 | −33 |

So the scoring rules changed. Unresearched competition estimates are now capped at 45 and labelled as an upper bound rather than a score. The reasoning is written down in [`docs/HANDOFFS.md`](../docs/HANDOFFS.md).

---

## Don't take any of this on trust

These examples pass the project's own test suite. Run it:

```bash
python tests/validate_memory.py --memory examples/memory
```

```
SUMMARY checked=20 errors=0 warnings=0
```

That check re-computes every score from its dimension values, verifies the floor penalty and the missing-data discount, confirms each verdict matches the threshold table, checks every file against its contract, and requires each memo to carry its sections, sit inside its word budget, and cite at least three working URLs.

If any number in these examples had been adjusted by hand, that command would fail.

---

## What is in each folder

Ten files per idea. The memo is the one you read; the rest is the evidence it rests on.

| File | What it holds |
|---|---|
| `idea.md` | The idea, who pays, the price hypothesis, and the trend evidence behind it |
| `desire_scores.json` | Five human desires scored 1–5, with a reason for each |
| `competitors.json` | Direct, indirect, substitute and emerging competitors, positioning gaps, saturation scored on five factors, and every source URL |
| `pricing.json` | Van Westendorp thresholds, price anchors, recommended tiers or range, conversion estimate |
| `market_size.json` | TAM, SAM and SOM from triangulated methods, with the reality checks that fired |
| `distribution.json` | Channels ranked with cost and ceiling, viral coefficient, founder edge |
| `retention.json` | Predicted retention, churn factors by severity, retention levers |
| `cac.json` | Lifetime value, cost per channel, payback, and the ceiling the business hits |
| `scores.json` | The arithmetic, the rationale per dimension, and the riskiest assumption with its experiment |
| `decision_memo.md` | Verdict, strengths, risks, the experiment, a pre-mortem, a devil's advocate section, kill criteria, sources |

Plus the research each one used, in [`market_insights/`](memory/market_insights/), with a full source list at the bottom of every file.

---

## The bit most tools skip

Every memo argues against its own verdict before it closes. From the shadow-AI run:

> **Devil's Advocate**
>
> 1. The demand data is the strongest in this project and I am discounting it on channel grounds. Businesses have been built into worse markets with better hustle.
> 2. Two competitors withholding rate cards may mean no traction, not ownership.
> 3. Bundling has been survived before. Defender did not kill endpoint security; it killed the weak and pushed the rest up-market.
>
> Each objection argues the market is attackable. None argues that you can reach it at 15 hours a week with no channel.

And every verdict ends with something to do about it, not just a number. Both runs designed a two-week experiment costing under $50, with a numeric pass threshold set before the test rather than after.

---

## One honest caveat

The climbing idea was chosen deliberately as a control subject, to exercise the consumer scoring path end to end. Its own memo says so at the top. It is included because a drop verdict on a spec test is still a real demonstration of the consumer rubrics working, and hiding it would be exactly the kind of selective presentation this project exists to argue against.

---

**[← Back to FindMeSaaS](../README.md)** · Want your own? Clone the repo and say *"validate my idea: ..."*
