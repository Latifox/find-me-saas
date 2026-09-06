---
prompt_for: b2b-communities
placeholder: "[NICHE]"
usage: Replace [NICHE] with the target buyer niche (e.g., "AI automation agencies", "MSP tooling", "freelance designers") before invoking. Use for b2b-smb, b2b2c, and prosumer ideas.
---

**Objective:**
Identify and analyze **what business buyers in the [NICHE] niche are complaining about, asking for, paying for, and switching between**, using **credible, recent sources (published within the last 6 months)** from the places where operators talk to each other rather than to vendors.

---

**Instructions:**

1. **Source Criteria**

   * Use only **credible and recent sources (≤ 6 months old)**
   * At the beginning of the response, clearly state:
     **"Data observed as of [month/year]"**
   * Prioritize sources in this order:

     **Tier 1 — Buyer review platforms (revealed preference, priced)**
     * G2 — category pages for the closest categories; read 1–2 star and 3 star reviews of the top 5 products; note review counts (a proxy for installed base) and "what do you dislike" answers
     * Capterra / GetApp / Software Advice — same method; useful for SMB pricing tiers and "alternatives to X" pages
     * Product Hunt — launches in the past 18 months in the category; comment threads reveal what buyers asked for that the launch did not have

     **Tier 2 — Operator communities (pain language, workarounds, budgets)**
     * Hacker News — "Ask HN" and "Show HN" threads about the problem; comments from people who run the process by hand
     * Indie Hackers — revenue posts and "how I got my first customers" posts for comparable products; these give real ACV, churn, and channel data
     * Reddit operator subreddits (r/msp, r/agency, r/smallbusiness, r/SaaS, r/freelance, niche-specific) — recurring complaints, tool stacks, "what do you use for X" threads
     * Niche Slack / Discord / Circle communities and their public digests; trade-association forums

     **Tier 3 — LinkedIn (buyer identity and demand signals)**
     * Posts by operators in the niche describing a problem or a tool switch; comment volume and who comments (titles) show who the buyer actually is
     * Sales Navigator or LinkedIn search headcount for the ICP definition (company type × size × role) as an ICP count proxy for market sizing

     **Tier 4 — Vendor and ecosystem pages (pricing anchors, partner motions)**
     * Pricing pages of the top 5 products (tiers, per-seat vs per-client vs flat, published vs "contact us")
     * Partner and integration directories (n8n, Zapier, HubSpot, Shopify, MSP tool marketplaces) — which products are listed, which are missing
     * GitHub issues and discussions of open-source alternatives — feature requests are unpaid product research

     **Tier 5 — Trade press and analyst notes (channel and budget context)**
     * Niche trade publications and MSP/agency industry surveys (budget priorities, top client needs, monetisation gaps)
     * Funding announcements in the category (who is funded, at what stage)

---

2. **Trend Identification**
   Identify both:

   * **Established pains** (recurring across communities and years; incumbents exist and are reviewed)
   * **Emerging pains** (new in the last 6–12 months; caused by a regulation, a platform change, a new technology, or a new buyer type; few or no products yet)

   For each, note whether it is **single-community** (one subreddit or forum) or **cross-community** (appears in reviews, HN, and LinkedIn) — cross-community pains are the stronger product signal.

---

3. **For EACH pain or demand theme, provide:**

**A. Basic Information**

* Theme name
* Who has it (role, company type, company size)
* Category (recurring complaint, tool-switch discussion, feature request, workaround description, budget or pricing debate, compliance trigger)

**B. Description**

* What the discussions look like (quote 1–2 short passages in the buyer's own words)
* What the buyer currently does instead (spreadsheet, agency, intern, nothing)
* What triggers the search for a solution (client request, audit, renewal, hire, incident)

**C. Quantitative Metrics**

* Review counts and average ratings of the incumbents on G2/Capterra
* Thread or post volume and engagement (upvotes, comments) where available
* Published prices of incumbents (tier, unit, monthly or annual)
* ICP count proxy (LinkedIn headcount, directory size, association membership) if obtainable

**D. Growth Analysis**

* For **emerging pains only**: what changed, when, and how fast the discussion volume is growing (compare 6 months ago vs now)
* Velocity classification (slow / moderate / explosive)

---

4. **Structure the Output**
   Organize findings into clearly separated sections:

* **1. Executive Summary (Key Insights)**
* **2. Established Pains**
* **3. Emerging Pains**
* **4. Buyer Vocabulary and Triggers (the exact phrases buyers use; the events that make them look)**
* **5. Strategic Insights (positioning, channel, and packaging takeaways)**

---

5. **Additional Analysis (Value Add)**
   Include:

* Incumbent weaknesses that appear in 2+ products' negative reviews (the shared complaint is the gap)
* Pricing-model patterns (per-seat vs per-client vs flat; which one buyers resent)
* Channel evidence: how comparable products got their first 100 customers according to Indie Hackers or founder posts (warm network, content, community, partnerships, outbound, paid)
* Buyer sophistication: do they build it themselves (Zapier, spreadsheets), and what makes them stop building and start buying

---

**Goal:**
Deliver a **data-backed, structured analysis** of what this buyer segment pays for, what it hates, and how comparable products reached it, so that downstream skills can map pains to products, price against real anchors, and pick channels with evidence.

---

6. **Financial Opportunities**
   Identify the **most monetarily interesting, not yet saturated pains** where buyers are **already paying** (to a vendor, a consultant, or in staff time). Base conclusions on realistic data — published prices, review counts, revenue posts, consulting rates — avoid speculative sizing.

   For each opportunity, provide:

   * **Pain and buyer**: who, and what they are trying to get done
   * **Evidence of commercial value**: incumbent prices, consulting or agency rates for the manual version, revenue posts for comparables, budget lines named in surveys
   * **Saturation assessment**: how many reviewed products serve it; is any one dominant (review count > 500); is anyone funded; is pricing transparent
   * **Realistic market size estimate**: bottom-up (ICP count × plausible ACV × plausible penetration), citing the ICP count source
   * **Why now**: regulation, platform change, new buyer type, incumbent price hike, or channel opening

   Prioritize opportunities that are:
   * Anchored in **revealed spending** (someone already charges or someone already pays a human)
   * **Reachable** by a solo founder (self-serve or light sales, ACV under ~$10k, no procurement)
   * **Emerging or underserved** — avoid categories with a dominant reviewed incumbent unless a philosophy or trust gap is documented in its reviews

---

7. **Niche Risks**
   Identify the **most significant risks** for a product targeting this buyer, based on signals from the communities and reviews. Base conclusions on data — not assumptions.

   For each risk, provide:

   * **Risk**: short label
   * **Signal**: specific evidence (a thread, a review pattern, a pricing page, a funding round)
   * **Severity**: Low / Medium / High
   * **Mitigation angle**: positioning, packaging, or channel that reduces exposure

   Risk types to consider:
   * **Build-it-ourselves** — buyers who automate for a living may never buy; look for evidence of who actually pays despite being able to build
   * **Incumbent one-module-away** — a funded product already owns the buyer relationship and could add the feature
   * **Latent demand** — the pain is discussed but nobody has a budget line yet; check for forcing functions (audit, insurance, regulation, client request)
   * **Buyer mortality** — the buyer segment itself churns (new agencies, first-year freelancers)
   * **Sales-cycle creep** — the real buyer turns out to be mid-market with procurement and security reviews
   * **Platform dependency** — the pain exists only because of one platform's current behaviour (a pricing change or a feature release removes it)

---

8. **Sources**
   At the end of the document, include a **"Sources" section** listing all URLs referenced during research as markdown hyperlinks:

   ```
   ## Sources
   - [Publication / Page Title](https://url.com)
   - [Publication / Page Title](https://url.com)
   ```

   * Include every source consulted, even if not directly quoted
   * Use the actual page title or publication name as the link label
   * Do not omit sources — completeness is required; downstream skills copy these URLs into their own `sources` arrays
