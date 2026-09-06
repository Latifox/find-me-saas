"""Build synthetic memory fixtures that exercise the harness pass and fail paths.

Usage: python tests/make_fixtures.py --out <dir>

Writes <dir>/memory with three ideas: ``fixture-b2b`` (a complete, valid
full-validation run in the B2B lane), ``fixture-b2c-candidate`` (a valid
quick-score) and ``fixture-broken`` (wrong final score, a verdict on a
quick-score, uncapped competition, a malformed memo, and a stale status), plus
one market insight file. Then run ``python tests/validate_memory.py --memory
<dir>/memory --idea fixture-b2b`` (expect exit 0) and ``--idea fixture-broken``
(expect exit 1). See tests/README.md.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

FIX = Path("fixtures")
SRC = {"url": "https://example.com/pricing", "title": "Example pricing", "accessed": "2026-09-06", "used_for": "anchor"}
W = {"demand": 0.20, "competition": 0.10, "monetization": 0.20, "distribution": 0.20, "retention": 0.15, "founder_market_fit": 0.15}


def scores(slug, dims, stage, **extra):
    """Return a scores.json document whose arithmetic matches the harness."""
    avail = {k: v for k, v in dims.items() if v is not None}
    base = sum(avail[k] * W[k] for k in avail)
    floor = 1.0
    for v in avail.values():
        if v < 25:
            floor *= v / 25
    disc = len(avail) / 6
    doc = {
        "idea_slug": slug, "scored_at": "2026-09-06", "scoring_stage": stage, "lane": "b2b",
        "dimension_scores": dims, "weights_applied": W, "floor_penalty": floor,
        "base_score": round(base, 2), "missing_discount": round(disc, 4),
        "final_score": round(base * floor * disc), "score_confidence": "high" if len(avail) == 6 else "medium",
        "missing_inputs": [], "killer_dimensions": [],
        "top_strengths": [{"dimension": "demand", "score": dims["demand"], "reason": "r"}],
        "top_weaknesses": [{"dimension": "competition", "score": dims["competition"], "reason": "r"}],
    }
    doc.update(extra)
    return doc


def rat():
    """Return a minimal riskiest_assumption_test block."""
    return {"assumption": "a", "category": "demand", "criticality": 5, "uncertainty": 4, "rat_score": 20,
            "experiment": {"type": "t", "description": "d", "duration": "14 days", "estimated_cost": "$0", "pass_threshold": "p", "fail_action": "drop"},
            "all_assumptions_ranked": [{"assumption": "a", "criticality": 5, "uncertainty": 4, "rat_score": 20}]}


def memo(slug, verdict, score):
    """Return a decision memo with every required heading and three URLs."""
    filler = " ".join(["evidence"] * 40)
    body = f"""---
idea_slug: "{slug}"
verdict: "{verdict}"
final_score: {score}
score_confidence: "high"
created_at: "2026-09-06"
---

# Decision Memo: Fixture

## Verdict: {verdict.upper()}

**Score: {score}/100** | Confidence: high

## Why This Score

{filler}

## Top 3 Strengths

1. **Demand** (80/100): {filler}

## Top 3 Risks

1. **Competition** (50/100): {filler}

## Riskiest Assumption

> "a"

{filler}

## Pre-mortem: If This Fails in 12 Months

1. {filler}
2. {filler}
3. {filler}

## Devil's Advocate

1. {filler}
2. {filler}
3. {filler}

## What To Do Now

{filler}

**Kill criteria:** {filler}

## If That Doesn't Work

{filler}

## Sources

- [A](https://example.com/a) — x
- [B](https://example.com/b) — y
- [C](https://example.com/c) — z
"""
    return body


def write(slug, files):
    """Write one fixture idea directory under FIX/memory/ideas."""
    d = FIX / "memory" / "ideas" / slug
    d.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        p = d / name
        if isinstance(content, str):
            p.write_text(content, encoding="utf-8")
        else:
            p.write_text(json.dumps(content, indent=2), encoding="utf-8")


def idea_md(slug, status, bm, extra=""):
    """Return idea.md frontmatter for a fixture; `extra` adds raw frontmatter lines."""
    return (f"---\nidea_slug: {slug}\nstatus: {status}\ncreated_at: 2026-09-06\n"
            f"business_model: {bm}\nbuyer: \"x\"\n{extra}---\n\n# Fixture\n")


def verdict_for(final):
    """Return the verdict the 75/55/35 table assigns to a final score."""
    return "pursue" if final >= 75 else "test" if final >= 55 else "pivot" if final >= 35 else "drop"


def pivot_option(pivot_id="pivot-1", variables_changed=1):
    """Return one fully-formed pivot option."""
    return {
        "pivot_id": pivot_id, "pivot_type": "Pricing pivot", "description": "d",
        "specific_change": "Charge per client instead of per seat", "evidence": "e",
        "evidence_source": "competitors.json", "meets_minimum_viable_pivot": True,
        "scoring_simulation": {
            "dimensions_improved": [{"dimension": "monetization", "current": 55, "projected_low": 65, "projected_high": 75}],
            "dimensions_worsened": [], "dimensions_unchanged": ["demand"],
            "projected_score_range": {"low": 60, "high": 68}, "projected_verdict_range": "test",
        },
        "effort": {"level": "low", "tier_adjusted_level": "low", "timeline": "1-3 days", "what_changes": "pricing page", "what_stays": "product"},
        "indie_buildability": {"passes": True, "constraints_checked": ["solo_buildable", "budget_feasible", "time_feasible", "skill_feasible", "sales_cycle_guard"], "failed_constraints": []},
        "trade_offs": ["t"], "variables_changed": variables_changed,
    }


def pivot_options_doc(slug, scope, options):
    """Return a pivot_options.json document with the given scope and options."""
    return {
        "idea_slug": slug, "generated_at": "2026-09-06", "lane": "b2b",
        "pivot_scope": scope, "slug_decision": "in-place", "new_slug": None,
        "original_score": 52, "original_verdict": "pivot",
        "triggered_by_weaknesses": [], "structural_weaknesses_unpivotable": [],
        "pivot_options": options, "recommended_pivot": options[0]["pivot_id"],
        "recommended_pivot_rationale": "r", "drop_recommendation": False,
        "market_insights_sources_used": [],
    }


def main() -> None:
    """Parse --out and write the fixtures."""
    global FIX
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", required=True, help="directory to create the fixture memory tree in")
    FIX = Path(parser.parse_args().out)
    build()


def build() -> None:
    """Write all fixture files under FIX."""
    b2b_dims = {"demand": 80,     "competition": 50, "monetization": 70, "distribution": 65, "retention": 60, "founder_market_fit": 85}
    write("fixture-b2b", {
        "idea.md": idea_md("fixture-b2b", "scored", "b2b-smb"),
        "scores.json": scores("fixture-b2b", b2b_dims, "full-validation", verdict="test", riskiest_assumption_test=rat(),
                              dimension_rationale={k: "r" for k in W}),
        "competitors.json": {"idea_slug": "fixture-b2b", "mapped_at": "2026-09-06", "lane": "b2b", "direct_competitors": [{"name": "X", "pricing": "$99", "pricing_model": "flat", "top_features": [], "top_complaints": []}],
                             "indirect_competitors": [], "substitutes": [], "emerging_threats": [],
                             "review_mining_summary": {"most_common_complaint_across_competitors": "", "strongest_gap_signal": "", "competitors_mined": 1},
                             "positioning_gaps": [{"gap_type": "trust", "description": "", "defensibility": "high", "evidence": ""}],
                             "saturation_score": {"direct_competitor_count": 1, "incumbent_dominance": 1, "funding_in_space": 1, "keyword_saturation": 1, "content_saturation": 1, "total": 5},
                             "saturation_rationale": "", "market_saturation": "low", "differentiation_opportunities": [], "market_insights_sources_used": [], "sources": [SRC]},
        "pricing.json": {"idea_slug": "fixture-b2b", "modeled_at": "2026-09-06", "lane": "b2b", "van_westendorp": {"too_cheap": 49, "cheap_but_acceptable": 99, "getting_expensive": 199, "too_expensive": 449},
                         "recommended_pricing_model": "tiers", "pricing_model_rationale": "", "competitive_pricing_range": {"min": 59, "max": 349, "modal": None},
                         "freemium_conversion_estimate": None, "monetization_risk": "medium", "market_insights_pricing_signals": [], "sources": [SRC],
                         "target_wtp_range": {"low": 99, "target": 199, "high": 399, "unit": "USD per month per company"},
                         "recommended_tiers": [{"name": "Agency", "price": 199, "billing": "per month", "scope": "s", "target": "t"}]},
        "distribution.json": {"idea_slug": "fixture-b2b", "analyzed_at": "2026-09-06", "lane": "b2b", "viral_loop_exists": False, "viral_loop_type": "word-of-mouth", "k_factor_estimate": 0.1, "k_factor_classification": "marginal",
                              "paid_feasibility": "marginal", "paid_feasibility_rationale": "", "founder_distribution_edge": {"exists": True, "strength": "high", "components": [], "limitations": []},
                              "recommended_first_channel": "warm", "recommended_first_channel_rationale": "", "channels_ranked": [{"channel": "warm", "viability": "high", "time_to_first_100_users": "6 months"}],
                              "distribution_verdict": "strong", "tier_adjustment_applied": "none", "distribution_verdict_rationale": "", "market_insights_sources_used": [], "sources": [SRC],
                              "discovery_channel_score": {"category_competition": 2, "keyword_opportunity": 3, "search_intent_match": 2, "advocacy_prompt_potential": 3, "differentiation_visibility": 3, "total": 13, "opportunity": "high"}},
        "retention.json": {"idea_slug": "fixture-b2b", "predicted_at": "2026-09-06", "lane": "b2b", "natural_usage_frequency": "monthly", "external_trigger": "report cycle", "habit_formation_score": 3,
                           "churn_risk_factors": [], "predicted_retention": {"monthly_churn_estimate": 0.05}, "d30_equivalent": 40, "top_churn_risk_factor": "mortality",
                           "retention_levers": [{"lever": "rebilling", "impact": "high", "detail": ""}], "churn_risk": "medium", "retention_verdict": "moderate"},
        "cac.json": {"idea_slug": "fixture-b2b", "modeled_at": "2026-09-06", "lane": "b2b", "ltv": {"estimated_ltv": 3500, "arpu_monthly": 199, "average_lifespan_months": 20, "ltv_confidence": "medium", "ltv_assumptions": []},
                     "gross_margin": 0.88, "ltv_cases": {"base": {}, "optimistic": {}, "pessimistic": {}},
                     "cac_by_channel_b2b": [{"channel": "warm", "estimated_cac": 200, "ltv_cac_base": 17.5, "payback_months": 1.1, "viability": "viable", "scale_ceiling": "30 customers"}],
                 "blended_ceiling_customers": 30, "blended_ceiling_basis": "single viable channel, midpoint of its stated ceiling",
                     "founder_budget_tier": "unknown", "recommended_first_channel": "warm", "recommended_first_channel_rationale": "", "payback_period_months": 1.1,
                     "viability_verdict": "viable", "viability_verdict_rationale": "", "market_insights_adjustments": [], "sources": [SRC]},
        "desire_scores.json": {"idea_slug": "fixture-b2b", "evaluated_at": "2026-09-06", "scores": {"survival": 4, "status": 5, "belonging": 2, "control": 4, "curiosity": 1},
                               "score_rationale": {k: "" for k in ("survival", "status", "belonging", "control", "curiosity")}, "primary_driver": "status", "secondary_driver": "survival",
                               "desire_strength": 4.0, "desire_strength_label": "strong", "virality_potential": "medium", "notes": ""},
        "market_size.json": {"idea_slug": "fixture-b2b", "estimated_at": "2026-09-06", "lane": "b2b", "methodology": "icp-count",
                             "estimation_approaches": [{"approach": "icp-count", "tam_estimate": 1000000, "key_assumptions": []}], "triangulation_confidence": "medium",
                             "tam": {"value": 1000000, "currency": "USD", "period": "annual", "assumptions": []}, "sam": {"value": 300000, "filter_criteria": [], "sam_to_tam_ratio": 0.3},
                             "som": {"year_1": 30000, "year_3": 90000, "capture_rate_year_1_pct": 1, "capture_rate_year_3_pct": 3, "growth_multiplier": 1.5, "growth_multiplier_source": "rising-fast"},
                             "market_insights_used": [], "trend_velocity_observed": "rising-fast", "monetization_evidence_found": True, "reality_checks_triggered": [], "market_size_verdict": "niche", "sources": [SRC]},
        "decision_memo.md": memo("fixture-b2b", "test", 71),
    })

    # B2C candidate quick-score: rank label, no verdict, capped competition
    c_dims = {"demand": 80, "competition": 45, "monetization": 55, "distribution": 50, "retention": None, "founder_market_fit": 60}
    write("fixture-b2c-candidate", {
        "idea.md": idea_md("fixture-b2c-candidate", "candidate", "b2c"),
        "scores.json": scores("fixture-b2c-candidate", c_dims, "candidate-quick-score", rank_label="candidate", competition_prior_capped=True),
    })

    # Broken: wrong final score, verdict on a quick-score, uncapped competition, status not advanced
    b_dims = {"demand": 70, "competition": 75, "monetization": 55, "distribution": 50, "retention": None, "founder_market_fit": 60}
    bad = scores("fixture-broken", b_dims, "candidate-quick-score", verdict="pivot")
    bad["final_score"] += 3
    write("fixture-broken", {
        "idea.md": idea_md("fixture-broken", "candidate", "b2c"),
        "scores.json": bad,
        "decision_memo.md": "---\nidea_slug: fixture-broken\n---\n# short\n",
    })

    # Market insights fixture
    mi = FIX / "memory" / "market_insights"
    mi.mkdir(parents=True, exist_ok=True)
    (mi / "fixture-b2b-communities-2026-09.md").write_text("""---
niche: fixture
platform: b2b-communities
analyzed_at: 2026-09-06
status: fresh
stale_after: 2027-03-06
trend_velocity: rising
overall_verdict: warm
key_insight: "x"
top_signals:
  - "a"
monetization_evidence:
  - "b"
---

# Body

## Sources
- [A](https://example.com/a)
""", encoding="utf-8")
    # --- fast-validation: four dimensions, verdict, RAT, medium confidence
    fast_dims = {"demand": 90, "competition": 75, "monetization": None, "distribution": 80, "retention": None, "founder_market_fit": 90}
    fast = scores("fixture-fast", fast_dims, "fast-validation", riskiest_assumption_test=rat())
    fast["verdict"] = verdict_for(fast["final_score"])
    write("fixture-fast", {"idea.md": idea_md("fixture-fast", "in-validation", "b2b-smb"), "scores.json": fast})

    # --- fast-validation, broken: five dimensions, high confidence, no RAT
    broken_dims = dict(fast_dims, monetization=60)
    fast_broken = scores("fixture-fast-broken", broken_dims, "fast-validation")
    fast_broken["verdict"] = verdict_for(fast_broken["final_score"])
    fast_broken["score_confidence"] = "high"
    write("fixture-fast-broken", {"idea.md": idea_md("fixture-fast-broken", "in-validation", "b2b-smb"), "scores.json": fast_broken})

    # --- micro pivot: exactly one option, re-scored in place
    micro_scores = scores("fixture-micro", b2b_dims, "pivot-rescore", verdict="test", pivot_id="pivot-1")
    micro_scores["verdict"] = verdict_for(micro_scores["final_score"])
    write("fixture-micro", {
        "idea.md": idea_md("fixture-micro", "scored", "b2b-smb"),
        "pivot_options.json": pivot_options_doc("fixture-micro", "micro", [pivot_option()]),
        "pivot_scores.json": micro_scores,
    })

    # --- micro pivot, broken: two options under a micro scope
    write("fixture-micro-broken", {
        "idea.md": idea_md("fixture-micro-broken", "scored", "b2b-smb"),
        "pivot_options.json": pivot_options_doc("fixture-micro-broken", "micro", [pivot_option(), pivot_option("pivot-2")]),
    })

    # --- pivot lineage: original paused and superseded, successor points back
    write("fixture-superseded", {"idea.md": idea_md("fixture-superseded", "paused", "b2c", "superseded_by: fixture-superseded-v2\n")})
    write("fixture-superseded-v2", {"idea.md": idea_md("fixture-superseded-v2", "in-validation", "b2b-smb", "pivot_of: fixture-superseded\n")})

    # --- pivot lineage, broken: wrong status and a target that does not exist
    write("fixture-superseded-broken", {"idea.md": idea_md("fixture-superseded-broken", "scored", "b2c", "superseded_by: fixture-does-not-exist\n")})

    print("fixtures written to", FIX)


if __name__ == "__main__":
    main()
