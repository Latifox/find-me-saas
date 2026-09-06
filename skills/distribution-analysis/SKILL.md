---
name: distribution-analysis
description: Evaluates organic reach potential, paid feasibility, platform distribution advantages, creator economy fit, and founder edge for a B2C app idea. Includes viral coefficient estimation, ASO scoring rubric, and tier-adjusted verdicts.
---

<!-- version: 0.3.0 | outputs: memory/ideas/<slug>/distribution.json -->

# Skill: distribution-analysis

## Purpose

Distribution is the most underestimated factor in indie app success. A mediocre product with great distribution beats a great product with no distribution. This skill evaluates all realistic paths to users and adapts its verdict to the founder's tier — a channel that works for a growth-stage operator can be a trap for a beginner.

## Input

- Idea slug
- `memory/user_profile.md` (ICP tier, distribution advantages, inner-circle buyers, budget constraint)
- `memory/ideas/<slug>/idea.md` (app concept, key features, differentiator, `business_model`)
- Optional: `memory/ideas/<slug>/competitors.json` (competitor distribution signals)

## Distribution Dimensions

| Dimension | Questions to Answer |
|---|---|
| Organic reach | Can this spread without paid spend? Is there a viral loop? What's the estimated viral coefficient? |
| Paid feasibility | Can paid ads break even at indie scale? What's the minimum viable budget? |
| Platform advantage | Is there an ASO moat? App Store featured potential? Category competitiveness? |
| Creator economy fit | Can influencers or creators promote this authentically? Does the app produce shareable output? |
| User's distribution edge | Does the user have an existing audience, community, or channel expertise? |

## Process

### Lane selection

`business_model` = `b2c` uses the ASO rubric (Step 2a) and creator fit (Step 3a). `prosumer`, `b2b-smb`, and `b2b2c` use discovery-channel scoring (Step 2b) and advocacy fit (Step 3b). Steps 1, 4, 5 and 6 apply to both lanes; the B2B additions inside them are marked. Record the lane in the output and fill only that lane's scoring block.

### Step 1 — Viral Coefficient Estimation

The viral coefficient (k-factor) predicts whether an app can grow organically through user referrals. Estimate k = i × c where:

- **i** = average number of invitations/shares per user
- **c** = conversion rate of each invitation

#### Viral loop identification

Evaluate the app concept against these loop types:

| Loop type | Description | Typical k-factor | Example |
|---|---|---|---|
| Inherent | Product is useless alone, requires inviting others | 0.5–1.5 | Multiplayer games, shared lists |
| Collaborative | Better with others but works solo | 0.2–0.6 | Workout trackers with friends, shared budgets |
| Word-of-mouth | Users talk about it because it's remarkable | 0.1–0.4 | Apps that produce "wow" output (AI art, unique insights) |
| Incentivized | Users get a reward for referring | 0.1–0.3 | Referral credits, unlocked features |
| Content-as-distribution | App output is inherently shareable on social platforms | 0.3–0.8 | Photo editors with watermarks, personality quizzes, wrapped/recap screens |
| None | No natural reason to share | 0.0–0.05 | Utility apps (calculators, timers) |

#### Estimation rubric

1. Identify which loop type(s) apply to the app concept.
2. Estimate **i** (invitations per user) — consider: does the core UX prompt sharing? How often? To how many people?
3. Estimate **c** (conversion per invitation) — consider: how compelling is the share artifact? Does the recipient need the app to view it?
4. Compute k = i × c.
5. Classify:

| k-factor | Classification |
|---|---|
| k ≥ 0.7 | **Viral growth engine** — organic growth is a primary acquisition channel |
| 0.3 ≤ k < 0.7 | **Viral assist** — referrals supplement other channels meaningfully |
| 0.1 ≤ k < 0.3 | **Marginal virality** — some word-of-mouth, not a growth driver |
| k < 0.1 | **Non-viral** — growth depends entirely on other channels |

> k ≥ 1.0 means every user brings in at least one more user on average — true exponential growth. This is rare for indie apps; be skeptical of estimates above 0.8 unless the app has an inherent or content-as-distribution loop.

In the B2B lane add the loop type **B2B2B exposure**: the buyer's own customers see a branded artefact (a portal, a report, a badge) and some of them are buyers. Typical k 0.1–0.3; treat it as a CAC reducer, never as growth.

### Step 2a — ASO Potential Scoring (B2C lane)

App Store Optimization is the highest-leverage free channel for indie developers. Score ASO opportunity on a 3-tier rubric:

#### ASO scoring rubric

| Factor | High (3 pts) | Medium (2 pts) | Low (1 pt) |
|---|---|---|---|
| **Category competition** | Niche category, top 10 achievable with <500 ratings | Moderate category, top 50 achievable | Saturated category, dominated by incumbents with 100K+ ratings |
| **Keyword opportunity** | High-volume keywords with low-rated top results (< 4.2 stars, < 1K ratings) | Keywords exist but top results are solid (4.5+ stars) | All relevant keywords dominated by well-known brands |
| **Search intent match** | Users actively search for this exact solution (tool/utility intent) | Users search for the category but not this specific angle | Discovery-dependent — users don't know they want this |
| **Review velocity potential** | App has natural prompt moments for asking reviews (completed task, achievement) | Some prompt moments but not in core loop | No natural review prompt; must interrupt to ask |
| **Visual differentiation** | App icon and screenshots can stand out (unique aesthetic, bold output previews) | Decent but similar to competitors | Looks like every other app in the category |

**ASO score**: Sum of all factors (5–15 points).

| Total | ASO opportunity |
|---|---|
| 12–15 | **high** — ASO should be primary acquisition channel |
| 8–11 | **medium** — ASO is viable but won't be the sole driver |
| 5–7 | **low** — ASO alone won't generate meaningful installs |

#### Featured potential checklist

An app has App Store featured potential if it meets **3+ of these 5 criteria**:

1. Uses a newly released Apple/Google platform feature (widgets, Live Activities, visionOS, AI APIs)
2. Has exceptional design quality (would look good in an editorial story)
3. Serves an underrepresented audience or emerging cultural moment
4. Has a clear positive-impact or wellness angle
5. Is a premium/indie app (Apple editorially favors paid apps and small teams)

### Step 2b — Discovery Channel Scoring (B2B lane)

Business buyers are found through search intent, comparison content, communities, and referrals rather than an app store. Score the same five-factor, 5–15 point shape so idea-scoring can treat the result like ASO:

| Factor | High (3 pts) | Medium (2 pts) | Low (1 pt) |
|---|---|---|---|
| **Category competition** | Buyer-specific terms are unclaimed; incumbents sell to a different buyer | Generic category terms are contested but the buyer-specific angle is open | Funded vendors with content teams own every relevant query |
| **Keyword opportunity** | High-intent queries exist ("X for agencies", "X vs Y", "X alternative") with weak or no targeted pages | Queries exist but top results are solid | No searchable intent; demand must be created |
| **Search intent match** | The buyer searches for this when the trigger fires (audit, client request, renewal) | The buyer searches the category, not this angle | The buyer does not know to search; education required first |
| **Advocacy prompt potential** | A natural moment exists when the buyer's client or boss praises the output (report delivered, audit passed) | Some positive moments, not in the core loop | Nothing the buyer would show anyone |
| **Differentiation visibility** | The position fits in one sentence no competitor can claim ("governance your agency can bill for") | Distinct but needs explanation | Looks like every other tool in the category |

Total 12–15 = **high** (content and search should be the primary channel after the warm network), 8–11 = **medium**, 5–7 = **low** (channel must be relationships, partnerships, or outbound).

### Step 3a — Creator Economy Fit Assessment (B2C lane)

Evaluate whether influencers and creators can authentically promote the app. Not all apps are "creator-friendly" — forcing influencer marketing on a utility app wastes money.

#### Creator fit criteria

| Factor | Score: High | Score: Medium | Score: Low |
|---|---|---|---|
| **Content generation** | App produces visual or shareable output that IS the content (before/after, results, transformations) | App experience is interesting to narrate/demonstrate | App is invisible — nothing to show on camera |
| **Audience alignment** | Clear niche creator communities already talk about this problem space | Adjacent creator communities exist | No creator community maps to this product |
| **Demo-ability** | Can be demonstrated in a 30–60 second clip with visible value | Needs 2–3 minute explanation to convey value | Requires hands-on usage over days to appreciate |
| **Authenticity** | Creator would genuinely use the app (not just shill for money) | Creator could plausibly use it occasionally | Feels forced — creator has no real use case |
| **Affiliate/monetization fit** | App has a price point that supports affiliate commissions ($5+/mo or $20+ one-time) | Freemium with conversion — harder to attribute | Free app with no monetization — no creator incentive |

**Scoring**: Count High/Medium/Low across all 5 factors.
- **high fit**: 3+ factors scored High
- **medium fit**: 2 factors High, or 3+ Medium
- **low fit**: 2+ factors Low, or no factors High

### Step 3b — Advocacy Fit (B2B lane)

Replace creators with the people who recommend tools to this buyer: community moderators, consultants, integration partners, and the buyer's own peers.

| Factor | High | Medium | Low |
|---|---|---|---|
| **Shareable artefact** | The product produces something the buyer sends to a client, boss, or auditor with the vendor visible | Output is internal but demonstrable | Nothing leaves the buyer's screen |
| **Community presence** | Active operator communities discuss this problem weekly (subreddits, Slack, HN, IH) | Adjacent communities exist | No community maps to the buyer |
| **Partner pull** | Adjacent tools list partners and co-market; an integration is a listing | Partnerships possible but relationship-gated | No ecosystem |
| **Practitioner credibility** | Founder is visibly one of the buyers (same stack, same job) | Founder is adjacent | Founder is an outsider to the buyer |
| **Referral economics** | ACV supports a referral or affiliate incentive (≥ $100/mo) | Marginal | Too cheap to reward referrals |

Scoring: **high** = 3+ factors High; **medium** = 2 High or 3+ Medium; **low** otherwise.

### Step 4 — Paid Channel Feasibility

Assess whether paid acquisition can work within indie budget constraints. In the B2B lane the relevant paid channels are LinkedIn (title and firmographic targeting; needs ACV ≥ $150/mo) and Google search (needs high-intent queries with CPC under about $10); Meta and TikTok paid are excluded.

| Budget tier | Monthly ad spend | Viable paid strategies |
|---|---|---|
| **Micro** (< $200/mo) | Testing only | One platform, 2–3 ad creatives, learn CPM/CPI before scaling. Not a primary channel. |
| **Light** (< $500/mo) | Targeted campaigns | One platform with lookalike audiences. Can work if CPI < $2 and LTV > $6. |
| **Moderate** (< $2000/mo) | Real optimization | Multi-creative testing, retargeting. Viable if LTV:CAC > 3:1 on at least one platform. |

If `budget_constraint` from user profile is "low", cap paid feasibility at "marginal" regardless of other factors — the user cannot sustain the learning curve of paid acquisition.

### Step 5 — Founder Distribution Edge

Cross-reference `user_profile.md` to identify whether the founder has a pre-existing distribution advantage:

| Advantage type | Impact |
|---|---|
| Existing audience (newsletter, social, YouTube) | Direct launch channel — reduces cold-start risk significantly |
| Community membership (active in relevant subreddits, Discord, forums) | Warm audience for validation and early adopters |
| Content creation skills (video, writing, design) | Can execute organic content channels without outsourcing |
| Technical SEO / ASO experience | Can capitalize on search-driven channels faster |
| Industry relationships | Potential for partnerships, cross-promotion, press |
| None identified | Must rely on product-led or paid growth — harder path |

### Step 6 — Distribution Verdict

Compute the overall verdict by evaluating all dimensions together, then **adjust for founder tier**.

#### Raw verdict logic

| Condition | Raw verdict |
|---|---|
| B2C: k-factor ≥ 0.5 OR (ASO = high AND creator_fit = high) OR founder has existing audience | **strong** |
| B2B: discovery score = high AND at least one more channel with a real ceiling behind the warm network (content, communities, partnerships, or paid at ≥ 3:1), OR founder has an inner-circle buyer plus one scalable channel | **strong** |
| k-factor ≥ 0.2 AND at least one other dimension scores medium+ (both lanes); B2B: exactly one channel with a real ceiling | **moderate** |
| All dimensions low/marginal, no organic path, paid not viable at budget; B2B: only the warm network works and it exhausts under 30 customers | **weak** |

#### Tier adjustment

The same distribution profile means different things to different founders. Apply this adjustment:

| Founder tier | Adjustment |
|---|---|
| **beginner** | Downgrade verdict by one level if the only viable channels require technical skill (SEO, paid optimization, ASO keyword research). Beginners need channels with fast feedback loops: TikTok organic, community posting, referral-based growth. Flag complex channels as "aspirational — learn first." |
| **builder** | No adjustment. Builders can execute most channels with some learning curve. Flag paid channels > $500/mo as risky given typical builder budgets. |
| **growth** | Upgrade verdict by one level if paid channels are viable and the founder has optimization experience. Growth-tier founders can unlock channels that are traps for beginners. |

If `user_profile.md` is unavailable, skip tier adjustment and note it as a gap.

## Output

Write to `memory/ideas/<slug>/distribution.json`:

```json
{
  "idea_slug": "",
  "analyzed_at": "YYYY-MM-DD",
  "lane": "b2c | b2b",
  "organic_reach_potential": "high | medium | low",
  "viral_loop_exists": false,
  "viral_loop_type": "inherent | collaborative | word-of-mouth | incentivized | content-as-distribution | none",
  "viral_loop_description": "",
  "k_factor_estimate": 0.0,
  "k_factor_classification": "viral-growth-engine | viral-assist | marginal | non-viral",
  "paid_feasibility": "viable | marginal | not-viable",
  "minimum_paid_budget_monthly": null,
  "paid_feasibility_rationale": "",
  "platform_advantage": {
    "aso_opportunity": "high | medium | low",
    "aso_score_breakdown": {
      "category_competition": 0,
      "keyword_opportunity": 0,
      "search_intent_match": 0,
      "review_velocity_potential": 0,
      "visual_differentiation": 0,
      "total": 0
    },
    "featured_potential": false,
    "featured_criteria_met": []
  },
  "creator_economy_fit": "high | medium | low",
  "creator_fit_rationale": "",
  "creator_fit_breakdown": {
    "content_generation": "high | medium | low",
    "audience_alignment": "high | medium | low",
    "demo_ability": "high | medium | low",
    "authenticity": "high | medium | low",
    "affiliate_fit": "high | medium | low"
  },
  "discovery_channel_score": {
    "category_competition": 0,
    "keyword_opportunity": 0,
    "search_intent_match": 0,
    "advocacy_prompt_potential": 0,
    "differentiation_visibility": 0,
    "total": 0,
    "opportunity": "high | medium | low",
    "factor_rationale": {}
  },
  "advocacy_fit": "high | medium | low",
  "advocacy_fit_rationale": "",
  "founder_distribution_edge": {
    "exists": false,
    "strength": "high | medium | low | none",
    "advantage_type": "audience | community | content-skills | seo-aso | relationships | inner-circle-buyer | none",
    "components": [],
    "limitations": []
  },
  "recommended_first_channel": "",
  "recommended_first_channel_rationale": "",
  "channels_ranked": [
    { "channel": "", "viability": "high | medium | low", "time_to_first_100_users": "", "estimated_cac": "", "ceiling": "" }
  ],
  "distribution_verdict": "strong | moderate | weak",
  "tier_adjustment_applied": "",
  "distribution_verdict_rationale": "",
  "market_insights_sources_used": [],
  "sources": [
    { "url": "https://", "title": "", "accessed": "YYYY-MM-DD", "used_for": "" }
  ]
}
```

Fill `platform_advantage` + `creator_economy_fit` (+ breakdown) in the B2C lane, or `discovery_channel_score` + `advocacy_fit` in the B2B lane; the other lane's blocks may be omitted. `channels_ranked[].ceiling` states how far the channel can carry the business (a customer count or an MRR figure) so cac-modeler and the memo can see where growth stalls. `sources` lists keyword, community, and partner-directory pages consulted.

## Notes

- The `recommended_first_channel` should always be the highest-viability channel the founder can realistically execute given their tier. Don't recommend "TikTok organic" to someone who has never made a video; don't recommend "ASO" to someone who doesn't know what keywords are.
- If `competitors.json` is available, check competitor distribution strategies — an app succeeding via a channel the founder can replicate is a strong positive signal.
- k-factor estimates are inherently speculative pre-launch. Treat them as directional, not precise. Flag any estimate above 0.5 as "optimistic until validated."
- In the B2B lane the recurring failure is channel depth: the warm network works and then exhausts at 20–30 customers. Always name the channel that must be ramping before that happens and how long it takes to ramp.
