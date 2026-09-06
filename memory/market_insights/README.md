---
description: Index and conventions for the market_insights directory
---

# Market Insights Directory

Each file in this directory is one completed market analysis. Files are written by the `trend-analysis` skill (one file per niche + platform + month).

## Naming Convention

```
<niche>-<platform>-<YYYY>-<MM>.md
```

Examples:
- `nutrition-tiktok-2026-04.md` — TikTok nutrition trends, April 2026
- `fitness-reddit-2026-05.md` — Reddit fitness community analysis, May 2026
- `personal-finance-apps-2026-03.md` — App Store personal finance trends, March 2026
- `productivity-web-search-2026-06.md` — Web search trends for productivity, June 2026
- `agency-tooling-b2b-communities-2026-09.md` — LinkedIn / G2 / HN / Indie Hackers signals for agency tooling, September 2026

For multi-platform analyses (no single platform focus):
```
<niche>-multi-<YYYY>-<MM>.md
```

## Frontmatter Schema

Each file must include:

```yaml
---
niche: <topic>
platform: tiktok | reddit | apps | web-search | x-twitter | b2b-communities | multi
analyzed_at: YYYY-MM-DD
status: fresh | stale
stale_after: YYYY-MM-DD   # 6 months after analyzed_at
---
```

## Freshness Rule

Analyses older than 6 months should be flagged `status: stale`. Re-run `trend-analysis` to produce a new file — do not overwrite the old one.

## Sources Rule

Every file ends with a `## Sources` section listing the URLs consulted as markdown links. Downstream skills copy URLs from here into their own `sources` arrays. A file with no URLs fails `python tests/validate_memory.py`.

## Files

This index is maintained by `trend-analysis`: append one row after every run. Analysis files are gitignored, so a fresh clone starts with an empty table.

| File | Niche | Platform | Period | Status |
|---|---|---|---|---|
| [agentic-vertical-scan-web-search-2026-08.md](agentic-vertical-scan-web-search-2026-08.md) | agentic-vertical-scan | web-search | August 2026 | fresh |
| [ai-agent-ops-security-web-search-2026-08.md](ai-agent-ops-security-web-search-2026-08.md) | ai-agent-ops-security | web-search | August 2026 | fresh |
| [ai-seo-geo-web-search-2026-08.md](ai-seo-geo-web-search-2026-08.md) | ai-seo-geo | web-search | August 2026 | fresh |
| [b2b-saas-web-search-2026-08.md](b2b-saas-web-search-2026-08.md) | b2b-saas | web-search | August 2026 | fresh |
| [claude-code-agency-ops-web-search-2026-08.md](claude-code-agency-ops-web-search-2026-08.md) | claude-code-agency-ops | web-search | August 2026 | fresh |
| [shadow-ai-msp-b2b-communities-2026-09.md](shadow-ai-msp-b2b-communities-2026-09.md) | shadow-ai-msp | b2b-communities | September 2026 | fresh |
| [habit-tracking-climbing-apps-2026-09.md](habit-tracking-climbing-apps-2026-09.md) | habit-tracking-climbing | apps | September 2026 | fresh |
