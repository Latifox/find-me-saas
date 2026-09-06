# Validation harness

`tests/validate_memory.py` checks that the skill system's outputs and specs match their contracts. Standard library only (Python 3.10+). No network.

## Run

```bash
python tests/validate_memory.py                 # strict: corpus under memory/, exit 1 on errors
python tests/validate_memory.py --baseline      # same report, always exit 0 (legacy corpora)
python tests/validate_memory.py --idea <slug>   # one idea directory
python tests/validate_memory.py --check-specs   # skills/ and workflows/ instead of the corpus
python tests/validate_memory.py --memory path   # point at another memory root (fixtures)
```

## Fixtures (the pass and fail paths)

```bash
python tests/make_fixtures.py --out /tmp/fx
python tests/validate_memory.py --memory /tmp/fx/memory                    # expect exit 1, 29 errors
```

| Fixture | Exercises | Expected |
|---|---|---|
| `fixture-b2b` | complete full-validation run, B2B lane | exit 0 |
| `fixture-b2c-candidate` | candidate quick-score, rank label, capped competition | exit 0 |
| `fixture-fast` | fast-validation: four dimensions, verdict, RAT, medium confidence | exit 0 |
| `fixture-micro` | micro pivot: one option, in-place slug decision, pivot re-score | exit 0 |
| `fixture-superseded` + `fixture-superseded-v2` | pivot lineage: paused original, successor pointing back | exit 0 |
| `fixture-broken` | wrong final score, verdict on a quick-score, uncapped competition, malformed memo, stale status | 23 errors |
| `fixture-fast-broken` | fast-validation with five dimensions, high confidence, no RAT | 3 errors |
| `fixture-micro-broken` | micro pivot carrying two options | 1 error |
| `fixture-superseded-broken` | `superseded_by` with the wrong status and a missing target | 2 errors |

Run these after any change to the harness or to `schemas.json`. The legacy corpus under `memory/ideas/` predates the contract and is expected to fail in strict mode; use `--baseline` there.

Report lines are `ERROR`, `WARN`, or `INFO`, followed by `SUMMARY checked=N errors=N warnings=N`. Report output uses `print` deliberately: it is the tool's product. Diagnostics use `logging` (`-v`).

## Corpus checks (default mode)

| Check | Error when | Warning when |
|---|---|---|
| JSON validity | any `memory/ideas/*/*.json` fails to parse | |
| Contract (`schemas.json`) | required key missing, enum value wrong, null where not nullable, nested required key missing, no `one_of` group present | unknown directive in the schema file, JSON file with no schema |
| B2B CAC ceiling | a B2B `cac.json` omits `blended_ceiling_customers`, which joins `cac_by_channel_b2b`, `ltv_cases` and `gross_margin` in the B2B `one_of` group | |
| `idea.md` frontmatter | `idea_slug` differs from directory; `status` or `business_model` not in enum; `business_model` missing | |
| Scores arithmetic | `base_score`, `floor_penalty`, `missing_discount`, `final_score` differ from recomputation; verdict does not match the 75/55/35 table; quick-score has a verdict or a wrong `rank_label`; competition above 60 without `competitors.json`; confidence higher than the dimension count allows | |
| Memo shape | frontmatter keys missing, a required heading missing, more than 1200 words in the full body, fewer than 3 URLs | fewer than 700 or more than 1000 words of prose |
| Lifecycle | `decision_memo.md` exists but status is still `candidate` or `in-validation` | |
| Fast validation | `scoring_stage: fast-validation` scores more than four dimensions, or claims a confidence the dimension count does not support, or omits `verdict` / `riskiest_assumption_test` | |
| Micro pivot | `pivot_scope: micro` with anything other than exactly one option, or an option whose `variables_changed` is not 1, or `slug_decision: new-slug` with an empty `new_slug` | |
| Pivot lineage | `superseded_by` set while status is not `paused` or `dropped`, or either `superseded_by` / `pivot_of` naming a directory that does not exist | |
| Provenance | a `sources[].url` is not http(s) | |
| Improvisation | | file contains "assumes B2C" or "replaced with an equivalent" |
| Market insights | frontmatter key missing, `platform` not in enum, `stale_after` is not `analyzed_at` + 6 months, no URLs | file is past `stale_after` but not marked stale |

Memo word count: the 700-1000 band applies to prose only, measured from the end of the frontmatter to the `## Sources` heading, so citations do not compete with analysis for space. The 1200 hard error still applies to the full body. Raised from 600-900 in task 4 after seven memos exceeded the old budget on first draft.

Candidate competition cap: quick-scores without `competitors.json` may not score competition above `CANDIDATE_COMPETITION_CAP` (45, tightened from 60 in task 4). Five full validations landed at 38, 45, 65, 32 and 22.

Rounding: `final_score = round(base * floor_penalty * missing_discount)` uses Python's `round` (half to even). The idea-scoring skill states the same rule.

## Spec checks (`--check-specs`)

- Every fenced ```json block in `skills/*/SKILL.md` parses (blocks inside HTML comments are ignored).
- Every `memory/ideas/<slug>/<file>` a workflow `reads` is produced by some skill (`outputs:` comment or a "Write to" line), unless the read is marked `(optional)`, `(opt)`, `(if present)`, or `(if available)`.
- Every `skills/<name>` has a stub in `.claude/skills/`, `.codex/skills/`, and `.cursor/rules/`.
- The four former stub skills contain no `<!-- TODO`.
- The eight lane skills mention `business_model` and have a B2B row or heading; `retention-predictor` defines `d30_equivalent`.
- `workflows/idea-validation.md` includes the tam-sam-som step, the profile-gap gate, the concurrency note, `business_model` at entry, and the `status: scored` update.
- No `pivot_options.md` or `-deep-dive-` references; `memory/README.md` lists no phantom files or `signal-aggregator`.
- `.claude/settings.json` allows WebSearch, WebFetch, Read(memory/**), Write(memory/**).
- `skills/trend-analysis/prompts/b2b-communities.md` exists with 8 numbered sections.
- `skills/idea-scoring/SKILL.md` defines the `fast-validation` stage; `skills/pivot-engine/SKILL.md` has a Micro-pivot Mode section, a Slug Rule section, and the `pivot_scope` field; `skills/decision-memo/SKILL.md` carries the superseded-memo rule.
- `workflows/idea-validation.md` has a `### Fast path` chain, `workflows/market-deep-dive.md` a `### Quick scan`, and `workflows/pivot-optimization.md` a `### Micro-pivot` chain plus the Slug Rule.
- `CLAUDE.md` and `AGENTS.md` route the fast path (they mention "gut check").
- No `(task-2)` TODO remains anywhere in `skills/` or `workflows/`.
- `skills/user-background-interviewer/SKILL.md` has a First-Run Onboarding section and captures `risk_tolerance` and `preferred_business_model`.
- `CLAUDE.md` and `AGENTS.md` route first-run onboarding.
- All nine slash commands exist under `.claude/skills/` with a `description` and a `name` matching their directory.
- `.claude/settings.json` registers the `SessionStart` and `PostToolUse` hooks, and both hook scripts exist on disk.

## Adding or changing a contract

Edit `tests/schemas.json`. Each entry is keyed by output filename and may use exactly these directives:

| Directive | Meaning |
|---|---|
| `required` | top-level keys that must exist (null allowed only if listed in `nullable`) |
| `enums` | `{field: [allowed string values]}` |
| `nullable` | keys that may be `null` |
| `conditional` | `[{when: {field: value}, required: [...], absent: [...]}]` |
| `nested_required` | `{"a.b[].c": [keys]}` paths; `[]` iterates a list |
| `one_of` | list of key groups; at least one group must be fully present |

Any other directive is reported as a warning and ignored, so the file cannot drift silently. Keep the JSON example in the skill's `## Output` section in sync with the contract; the skill is what the model reads, the schema is what the harness enforces.
