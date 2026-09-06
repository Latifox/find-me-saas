---
name: pricing-and-wtp
description: Models willingness to pay using Van Westendorp price sensitivity analysis, desire-premium multipliers, category benchmarks, and market_insights monetization signals. Recommends pricing model, freemium conversion estimate, and annual/monthly strategy.
---

<!-- version: 0.3.0 | outputs: memory/ideas/<slug>/pricing.json -->

# Skill: pricing-and-wtp

## Purpose

Determine what users would actually pay, not what the developer hopes to charge. Anchor WTP to pain intensity, desire strength, competitive pricing, and real monetization signals from market_insights — never to the cost of building. Pricing is the single decision with the highest leverage on unit economics: a $1/mo difference at 1,000 users is $12K/year.

## Input

- Idea slug
- `memory/ideas/<slug>/idea.md` (app concept, key features, `business_model`, `price_point_hypothesis`)
- `memory/ideas/<slug>/competitors.json` (competitive pricing, pricing models in use, `anchors` for the B2B lane)
- `memory/ideas/<slug>/desire_scores.json` (desire strength, primary/secondary drivers)
- `memory/market_insights/<niche>-*-<YYYY>-<MM>.md` (trend data — **use all available platform files**)

### Using Market Insights

Trend analysis files provide monetization reality-checks that desk research alone cannot:

| Field | How it informs pricing |
|---|---|
| `monetization_evidence` | The strongest signal. If competitors are visibly making money (in-app purchases mentioned in reviews, subscription pricing in App Store listings, sponsored content), the market has validated WTP. If monetization_evidence is empty across all platforms, WTP is unproven — discount aspirational price and flag risk. |
| Platform narratives — Reddit | Users discuss pricing directly: "I'd pay for X if...", "Y is overpriced because...", "$Z/mo is too much for just..." These are raw WTP signals. Extract any price mentions. |
| Platform narratives — App Store | Review complaints about pricing reveal the ceiling: "Great app but not worth $X/mo." Review praise about pricing reveals the floor: "Amazing value at $X." |
| Platform narratives — TikTok | Creator recommendations often mention price as part of the hook ("this FREE app...", "worth every penny of $X"). Signals whether freemium or premium positioning resonates with the audience. |
| `trend_velocity` | Rising-fast markets can support premium pricing (early adopters pay more). Declining markets face price pressure (users comparison-shop harder). |

### Lane selection

`business_model` = `b2c` or `prosumer` uses the B2C lane: the category WTP table in Step 4, freemium conversion in Step 5, and `wtp_range` + `recommended_price` in the output. `b2b-smb` and `b2b2c` use the B2B lane: the benchmark table in Step 4b, trial-to-paid in Step 5b, tiers in Step 7, and `target_wtp_range` + `recommended_tiers` in the output. Van Westendorp (Step 2) and the desire multiplier (Step 3) apply to both lanes; in B2B, anchor the thresholds on the closest product that sells to the same buyer rather than on the category as a whole.

## Pricing Models

| Model | Best for | Risk | Indie sweet spot |
|---|---|---|---|
| **Freemium → subscription** | Habit-forming apps with daily use, feature-gated value | Conversion friction; most users stay free forever | $3–$8/mo or $20–$50/yr |
| **Subscription only (paywall)** | High-value, immediately obvious ROI, professional tools | High churn risk; must prove value fast | $5–$15/mo |
| **One-time purchase** | Utilities, tools with clear one-time value, privacy-focused apps | No recurring revenue; must rely on new users | $3–$10 |
| **Consumables / credits** | Variable usage (AI generations, exports, premium content) | Unpredictable revenue; usage may decline | $1–$5 per credit pack |
| **Freemium + consumables** | Apps where core is free but power usage costs (AI, storage) | Complex to balance free vs. paid tiers | Free tier + $2–$10 packs |
| **Lifetime deal** | Launch phase only — use for early adopter cash and reviews | Destroys LTV; never use as primary model | $20–$60 (3–5× annual price) |
| **Tip jar / patronage** | Content-focused, community-driven, or open-source-adjacent | Very low conversion; unreliable revenue | $1–$5 tips, rare |

### Model selection criteria

| If the app... | Recommended model |
|---|---|
| Has daily usage with progressively unlocked value | Freemium → subscription |
| Delivers immediate, obvious ROI in one session | Subscription only or one-time purchase |
| Produces output that varies in volume (AI, exports) | Freemium + consumables |
| Is a simple utility used occasionally | One-time purchase |
| Requires trust before users see value (health, finance) | Extended free trial → subscription |
| Competes with free alternatives that are "good enough" | Freemium (generous free tier) → subscription for power features |

## Process

### Step 1 — Establish competitive pricing range

From `competitors.json`, extract pricing data for all direct competitors:
1. List each competitor's pricing model and price point.
2. Compute the range: `competitive_min` (cheapest) and `competitive_max` (most expensive).
3. Identify the **modal price** — the price point most competitors converge on. This is the market's revealed equilibrium.
4. Note any competitor using a different model (e.g., all use subscription but one uses one-time purchase) — this is a potential positioning gap.

If `competitors.json` has limited pricing data, supplement with market_insights monetization_evidence and App Store narrative pricing mentions.

### Step 2 — Van Westendorp Price Sensitivity Analysis

The Van Westendorp model uses four price perception thresholds to identify the acceptable price range. Since we can't survey users directly, we estimate each threshold from available data:

#### The four thresholds

| Threshold | Question (conceptual) | How to estimate |
|---|---|---|
| **Too cheap** (floor) | Below this price, users suspect low quality | Half the cheapest competitor's price. If app is free, this is $0 (no floor). |
| **Cheap but acceptable** (low) | Feels like a good deal | Competitive minimum price. Discount slightly if the app offers less than the cheapest competitor. |
| **Getting expensive** (target) | Fair price — users would consider it but think carefully | Competitive modal price, adjusted by desire multiplier (Step 3). |
| **Too expensive** (ceiling) | Above this, users won't consider it regardless of value | Competitive maximum price × 1.2. Cap at the "pain threshold" — the maximum users pay for similar apps in the category. |

#### Acceptable price range

The **optimal price point** sits between "cheap but acceptable" and "getting expensive" — this is the target WTP.

```
wtp_low = cheap_but_acceptable
wtp_target = getting_expensive (adjusted by desire multiplier)
wtp_aspirational = midpoint between getting_expensive and too_expensive
```

### Step 3 — Desire-Premium Multiplier

Desire strength from `desire_scores.json` directly affects pricing power. Apps that tap into primal desires command premium pricing; apps that solve mild inconveniences face price resistance.

| Primary desire driver | Premium multiplier | Rationale |
|---|---|---|
| **Survival** (health, safety, financial security) | 1.3–1.8× | Users pay more when stakes are high. Health and money apps can charge premium. |
| **Status** (achievement, appearance, signaling) | 1.5–2.0× | Status is inherently scarce — users pay for differentiation. Luxury/prestige positioning works. |
| **Belonging** (community, connection) | 1.0–1.3× | Users value belonging but expect community features to be free (social norms). Premium only for exclusive communities. |
| **Control** (mastery, organization, reducing chaos) | 1.2–1.5× | Moderate premium. Users pay for control when the alternative is stressful. |
| **Curiosity** (learning, discovery, novelty) | 0.8–1.2× | Lowest premium. Curiosity-driven apps compete with free content (YouTube, blogs). Must add structure/accountability to charge. |

**Apply the multiplier to the competitive modal price:**

```
desire_adjusted_target = competitive_modal_price × desire_multiplier
```

If `desire_strength_label` = "weak", do not apply any multiplier — the app lacks the emotional pull to justify premium pricing.

#### Secondary desire bonus

If the secondary desire driver is different from the primary and scores ≥ 3, add a +10% bonus. Apps that tap two distinct desires (e.g., survival + control in a health tracker) have stronger pricing power than single-desire apps.

### Step 4 — WTP Benchmarks by App Category

Use these ranges as a sanity check against the Van Westendorp and desire-adjusted estimates:

| App category | Subscription WTP range (monthly) | One-time WTP range | Annual discount sweet spot |
|---|---|---|---|
| **Health & fitness** | $5–$15/mo | $8–$30 | 40–50% off monthly |
| **Nutrition / diet** | $5–$12/mo | $8–$25 | 40–50% off monthly |
| **Meditation / mental health** | $5–$15/mo | $10–$30 | 50–60% off monthly |
| **Finance / budgeting** | $3–$10/mo | $5–$20 | 30–40% off monthly |
| **Productivity / task management** | $3–$8/mo | $5–$15 | 30–40% off monthly |
| **Habit tracking** | $2–$6/mo | $3–$10 | 40–50% off monthly |
| **Creative tools (photo/video)** | $3–$10/mo | $5–$20 | 30–40% off monthly |
| **Education / learning** | $5–$15/mo | $10–$30 | 50–60% off monthly |
| **Dating / social** | $5–$25/mo | N/A (subscription dominates) | 30–40% off monthly |
| **Parenting / family** | $3–$8/mo | $5–$15 | 40–50% off monthly |
| **Utility / scanner / converter** | $1–$4/mo | $2–$8 | 50–60% off monthly |
| **AI-powered tools** | $5–$20/mo | $10–$40 consumable pack | 30–40% off monthly |

If the estimated WTP is more than 2× above the category range, it's likely too optimistic. If it's below the category minimum, the app may struggle to sustain development.

### Step 4b — B2B lane benchmarks (SMB and agency buyers, self-serve or light sales; heuristic ranges)

| Pricing unit | Typical SMB range | Use when | Buyer resentment risk |
|---|---|---|---|
| **Flat monthly tiers** | $29–99 / $99–299 / $299–799 | Value does not scale with seats; buyer wants a predictable line item | Low; publish the prices |
| **Per seat** | $8–30 per user/mo | Every user gets individual value (inbox, CRM, editor) | High when only one person uses it; punishes growing teams |
| **Per client / workspace / location** | $10–50 per unit/mo on top of a base | Agencies, MSPs, franchises: value is per managed account | Low; aligns cost with the buyer's revenue |
| **Usage / credits** | Metered with a floor of $49–199/mo | AI generation, scans, exports with variable volume | Medium; unpredictable bills drive churn |
| **Annual contract** | 10–20% below 12× monthly | Buyers with budget cycles; lock-in before incumbents react | Low |

Sanity anchors: routine SMB tooling sits at $20–100/mo per company (heuristic: Zapier, Make, Notion team plans); agency white-label tooling at $59–349/mo with per-client overage (AgencyAnalytics pricing page); compliance and security platforms at $10k–80k/yr (Vanta, Drata, Nudge published or quoted pricing). If the idea sits between two clusters with nothing in the gap, the revealed price is a gap, not a validation; say so and set `monetization_risk` no lower than "medium".

Rules for the B2B lane:
- Copy the billing unit the buyer already accepts from the closest comparable product; do not invent a unit.
- Do not price per seat unless the per-user value is real.
- Recommend a free **trial** (time-boxed or one-unit) rather than a free tier unless a free incumbent must be defended against.
- Publish prices unless every comparable hides them; transparency is a free differentiator in categories full of "contact sales".

### Step 5 — Freemium Conversion Estimation

If the recommended model includes a free tier, estimate what percentage of free users will convert to paid:

| Factor | Higher conversion (toward 8–12%) | Lower conversion (toward 1–3%) |
|---|---|---|
| **Value gating** | Core value is free; premium unlocks power features or removes limits | Core value IS the paid feature — free tier feels empty |
| **Free tier generosity** | Generous enough that users form habits before hitting the wall | Either too generous (no reason to pay) or too stingy (users leave) |
| **Pain of free** | Free tier has clear, felt limitations (ads, watermarks, usage caps) | Free tier works fine for most users |
| **Social proof** | Users see premium features in action (shared content with branding) | No visibility into what premium offers |
| **Trial exposure** | Time-limited trial of premium (7–14 days) shows value upfront | No trial; users must imagine premium value |

**Category benchmarks for freemium conversion:**

| Category | Typical conversion rate | Top-quartile rate |
|---|---|---|
| Health & fitness | 2–5% | 8–12% |
| Productivity | 3–6% | 10–15% |
| Creative tools | 3–7% | 10–18% |
| Education | 2–5% | 7–12% |
| Finance | 3–6% | 8–14% |
| Utility | 1–4% | 5–10% |
| Social / dating | 2–8% | 10–20% |
| AI-powered | 4–8% | 12–20% |

Use the typical rate as the base estimate. Adjust toward top-quartile if:
- The desire_strength_label is "strong"
- The free tier design has strong value gating
- Category benchmarks from market_insights show successful freemium competitors

### Step 5b — B2B trial-to-paid estimation

In the B2B lane set `freemium_conversion_estimate` to `null` unless a free tier is genuinely recommended, and estimate `trial_to_paid_estimate` instead (heuristic ranges for self-serve SMB SaaS):

| Trial design | Typical trial-to-paid |
|---|---|
| Opt-in trial, no card, no onboarding | 5–10% |
| Opt-in trial with guided onboarding or a real artefact produced during the trial | 15–25% |
| Card-required trial | 30–50% of a much smaller trial pool |
| Sales-assisted pilot | 40–60% |

Choose the row matching the recommended trial and state why. A trial that lets the buyer produce something they can show a client or boss during the trial period sits at the top of its band.

### Step 6 — Annual vs. Monthly Strategy

Most indie apps benefit from offering both monthly and annual plans. The annual plan serves as the anchor.

#### Annual discount psychology

| Discount depth | Effect |
|---|---|
| **20–30% off monthly** | Subtle incentive. Users who prefer monthly will stay monthly. Low commitment-capture rate. |
| **40–50% off monthly** | Sweet spot for most B2C apps. Enough savings to feel meaningful, not so deep it signals desperation. |
| **50–60% off monthly** | Aggressive — use for high-churn categories where locking in annual users dramatically improves LTV. |
| **> 60% off monthly** | Signals the app isn't worth the monthly price. Avoid unless in launch/promotional phase. |

**Recommended annual price** = monthly price × 12 × (1 - discount). Present the annual plan as the default/highlighted option.

### Step 7 — Pricing lane by business model

**B2B lane (`b2b-smb`, `b2b2c`): recommended tiers.** Build 3 tiers (plus a trial) from the Van Westendorp range: entry at `cheap_but_acceptable`, the primary revenue tier at `getting_expensive`, and a top tier near the midpoint to `too_expensive` with the features only larger buyers need. Name the target for each tier. For `b2b2c` add a `rebilling_strategy`: how the buyer marks the product up to its own customers, with evidence that comparable buyers do this. Rebilling moves the subscription from the buyer's cost line to its revenue line and is the strongest churn lever available; say whether it is critical, useful, or absent.

**B2C lane with a business path (B2B2C expansion).** Some consumer ideas have a viable path to both consumer and business revenue. Evaluate if the app concept could serve both:

| Signal that B2B2C path exists | Example |
|---|---|
| Users would expense the app to their employer | Productivity tools, professional development |
| A business version could serve teams | Shared dashboards, admin controls, team analytics |
| Content or data from the app has business value | Health data for employers, fitness for corporate wellness |
| The consumer app is a wedge into workplace adoption | Personal Slack → company Slack, personal Notion → team Notion |

If B2B2C path exists:
- **B2C price**: Use the standard WTP methodology above (this is the consumer price).
- **B2B2C price**: 3–5× the consumer price per seat. Businesses have larger budgets and lower price sensitivity.
- **Recommendation**: Launch B2C first (faster validation, faster feedback). Flag B2B2C as a future monetization expansion in the output.
- **Do NOT recommend B2B2C as the primary model** for an indie developer — enterprise sales cycles and support needs don't fit the indie model.

## Output

Write to `memory/ideas/<slug>/pricing.json`:

```json
{
  "idea_slug": "",
  "modeled_at": "YYYY-MM-DD",
  "lane": "b2c | b2b",
  "wtp_range": {
    "low": 0,
    "target": 0,
    "aspirational": 0,
    "currency": "USD",
    "period": "monthly | yearly | one-time"
  },
  "target_wtp_range": {
    "low": 0,
    "target": 0,
    "high": 0,
    "unit": "USD per month per <company | seat | client>"
  },
  "van_westendorp": {
    "too_cheap": 0,
    "cheap_but_acceptable": 0,
    "getting_expensive": 0,
    "too_expensive": 0,
    "methodology_note": ""
  },
  "anchors": [
    { "product": "", "price": "", "relevance": "" }
  ],
  "desire_premium_multiplier": null,
  "desire_premium_rationale": "",
  "recommended_pricing_model": "",
  "pricing_model_rationale": "",
  "pricing_models_considered": [
    { "model": "", "fit_rationale": "", "risk": "" }
  ],
  "recommended_price": {
    "monthly": 0,
    "annual": 0,
    "annual_discount_pct": 0,
    "one_time": 0
  },
  "recommended_tiers": [
    { "name": "", "price": 0, "billing": "per month | per year | one-time", "scope": "", "target": "" }
  ],
  "freemium_conversion_estimate": null,
  "freemium_conversion_rationale": "",
  "trial_to_paid_estimate": null,
  "rebilling_strategy": { "importance": "critical | useful | none", "detail": "", "evidence": "" },
  "competitive_pricing_range": {
    "min": 0,
    "max": 0,
    "modal": null
  },
  "category_benchmark_range": {
    "min": 0,
    "max": 0
  },
  "b2b2c_potential": {
    "exists": false,
    "b2b_price_estimate": 0,
    "rationale": ""
  },
  "monetization_risk": "low | medium | high",
  "monetization_risk_explanation": "",
  "market_insights_pricing_signals": [],
  "market_insights_sources_used": [],
  "pricing_rationale": "",
  "sources": [
    { "url": "https://", "title": "", "accessed": "YYYY-MM-DD", "used_for": "" }
  ]
}
```

Fill `wtp_range` + `recommended_price` in the B2C lane and `target_wtp_range` + `recommended_tiers` in the B2B lane; the other pair may be omitted. `modal` is `null` when no competitor occupies the idea's price position. `sources` lists every pricing page and anchor consulted.

## Notes

- The `target` WTP is the price used by downstream skills (`cac-modeler` for LTV, `tam-sam-som-builder` for revenue projections). Getting this wrong cascades errors through the entire scoring system.
- If `monetization_evidence` from market_insights is empty across all platform files, flag pricing as "unvalidated" in the rationale. This is a key risk — the market may not support paid apps.
- For apps competing with strong free alternatives (Google Keep, Apple Notes, default apps), the effective WTP ceiling may be $0 for most users. In this case, the pricing model must create value that the free alternative structurally cannot (social features, AI, specialized workflows).
- Lifetime deal pricing should only appear as a launch tactic, never as the recommended primary model. LTD price = 3–5× annual price. Cap at $60 for consumer apps.
- If market_insights files are past their `stale_after` date, note that competitive pricing may have shifted and recommend refreshing.
- cac-modeler reads `target` (B2C) or the primary tier price (B2B) as ARPU, and `trial_to_paid_estimate` or `freemium_conversion_estimate` for funnel maths. Keep those fields numeric.
