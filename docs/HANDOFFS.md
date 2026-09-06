# Handoffs

Learnings from completed tasks, for whoever picks up the next one. Add a section per task; keep entries specific.

## Task 1 — Skill Quality Hardening (2026-09-06)

### Harness
- `python tests/validate_memory.py --check-specs` is the fastest signal that a skill or workflow edit broke a contract: it parses every json block, cross-checks workflow reads against skill outputs, and asserts adapter parity. Run it after every spec edit.
- `--baseline` is for the legacy corpus (pre-contract ideas report ~313 errors and that is expected). Use the default strict mode only on fresh runs or fixtures.
- `python tests/make_fixtures.py --out <dir>` then `--memory <dir>/memory --idea fixture-b2b` reproduces the pass path; `--idea fixture-broken` reproduces 23 expected errors. When changing the harness, run both before trusting a green result.
- Report paths for files outside the repo print as absolute paths; that is by design (fixtures live in a temp dir).

### Editing skills
- Skill files are read by a model, not compiled: keep B2B rows inside the same rubric tables as B2C rows, and put a "Lane selection" paragraph right under `## Input` so the lane choice is made before any rubric is read.
- Every json block in a SKILL.md must parse. Enum choices are written as string values ("a | b"); never use bare `0 | 1` or `//` comments. The harness enforces this.
- Bump the `<!-- version: -->` comment on every skill you touch; several skills were at 0.1.0 with TODO placeholders for a long time and nobody noticed because nothing checked.
- Shell heredocs with apostrophes fail in this environment (Git Bash on Windows with the RTK hook). Use Python patch scripts with exact-anchor replacement and `assert text.count(old) == 1`.
- Working directory persists between shell calls. A `cd` in one call leaks into the next; always use repo-relative or absolute paths.

### Scoring semantics
- Candidate quick-scores in idea-generation carry `rank_label`, never a verdict; competition is capped at 60 until competitor-mapper runs. Evidence: four consecutive validations dropped competition 20-40 points under research.
- `final_score` uses round-half-to-even. If a future edit changes the algorithm, change the harness and the skill in the same commit.
- The B2B retention bridge is `d30_equivalent = clamp(1 - 12 × monthly_churn, 0, 1) × 100`. It is a heuristic so idea-scoring's single retention rubric applies to both lanes; do not treat it as a measurement.

### Open items (not done in task 1)
- Two live validations (one B2B, one B2C) with web research have not been run against the new specs. Run them in a session and check with `--idea <slug>`; that is the acceptance test that matters.
- The 20 legacy ideas under `memory/ideas/` do not carry `business_model` or `sources`. Migrate them only if they are still in play; `--baseline` tolerates them.
- Task 2 (DONE 2026-09-06) resolved the fast-path, micro-pivot, and slug-rule TODOs. The remaining open item is task 3: the live validation runs.

## Task 2 — Workflow Paths (2026-09-06)

### Shortcuts and their guard rails
- Three shortcuts now exist: the fast path in idea-validation, the micro-pivot in pivot-optimization, and the quick scan in market-deep-dive. Each is a second fenced chain under the full one, and the harness asserts the section heading exists so a future edit cannot quietly delete a path.
- The fast path scores four dimensions and writes no memo. It can rule an idea out but never rule one in: the 4-of-6 missing-input discount caps the ceiling, so `pursue` would need a base score above 112. Never present a fast score beside a full score without naming both stages.
- A micro pivot is defined by the user naming the variable, so weakness-detection is skipped. `pivot_scope: micro` forces exactly one option with `variables_changed: 1`, enforced by the harness.

### The slug rule
- One variable changed updates in place; two variables, a `business_model` change, or a problem change creates `<slug>-<pivot-word>/` with `pivot_of`, and pauses the original with `superseded_by`.
- Dimension files are deliberately not copied into the new directory. A pivot that large changes the competitive set and the channels, so they are researched again; `idea.md` is the only inheritance.

### Testing spec assertions
- String-presence assertions in `--check-specs` are easy to write and easy to write wrong. After adding one, mutation-test it: remove the needle, confirm exit 1, restore. A scripted loop over the new needles took seconds and proved none was inert. Do this every time `check_specs` grows.
- Fixture error counts are the regression signal for harness refactors. When the confidence check was simplified, `fixture-broken` staying at exactly 23 errors was the proof that behaviour had not changed.

## Task 3 — Live validation runs (2026-09-06)

### The specs work; here is what to watch
- Two full chains ran with real research and both passed the harness with zero errors. The B2B lane produced every promised field with no improvisation. The task-1 failure mode, a run apologising in a `methodology_note` that the rubric did not fit, did not recur.
- The lanes stay separate on their own. The B2B run carries no ASO breakdown and no `cac_by_channel` object; the B2C run carries no `discovery_channel_score` and no `cac_by_channel_b2b`. `business_model` selected correctly in every skill without prompting.
- Both runs tripped the multiplicative floor penalty, the first two times in this project. In each case one structural failure at 22 correctly pulled down an otherwise ordinary score.

### Research practice that paid off
- **Mine competitor complaints before trusting the problem statement.** The B2C idea died on this: across three apps, every documented complaint was technical (force gauges, periodization, session length) and none was about habit consistency, which was the idea's entire premise. Two searches found it. Do this early, not after pricing.
- **Look for the bundled substitute.** The single most damaging B2B finding was Microsoft bundling Purview into M365 Business Premium. A capability arriving inside a licence the buyer already owns caps willingness to pay harder than any competitor's list price. Ask "is a platform vendor giving this away?" during competitor mapping, not later.
- **Check the channel's qualification gate, not just its size.** MSP vendor selection requires SOC 2 Type II, ISO 27001 and pen-test reports. That is not a slow channel, it is a closed one, and no amount of founder effort opens it at a bootstrap budget.

### Scoring calibration
- Competition fell 33 points under research (55 to 22), the fifth consecutive validation dropping 20-40. The task-1 cap of 60 is directionally right but still generous; 45 would track the observed pattern better. Revisit if a sixth run repeats it.
- The freemium ARPU formula (price x conversion) produces install values in cents and will fail almost any consumer idea facing a credible free competitor. That is correct arithmetic, not a bug, but expect B2C ideas to die on monetization rather than demand.

### Open items
- Four defects logged in `.ay/plans/task-3/references/defects.md`, all proposed as task 4: memo word budget unachievable, CAC viability ignores channel ceiling, no penalty for a niche market size, no guidance when a research platform returns nothing usable.
- The 19 remaining legacy idea directories still lack `business_model` and `sources`. `--baseline` tolerates them; migrate only if one comes back into play.

## Task 4 — Spec fixes from the live runs (2026-09-06)

### What changed
- Memo budget is 700-1000 words of **prose**. The harness splits the body at `## Sources` and counts only what comes before it; the 1200 hard error still applies to the full body. Both task-3 memos passed unchanged, which is how the band was chosen rather than guessed.
- `cac.json` in the B2B lane must carry `blended_ceiling_customers`. It joins the B2B `one_of` group, so the B2C lane is unaffected. Derive it by summing the ceilings of channels rated viable or marginal, excluding one-time launch cohorts and contributing zero for blocked channels.
- Monetization now penalises a small market in both lanes: -5 niche, -10 micro-niche, against the existing +5 large.
- Candidate competition cap is 45, down from 60, and now lives in `CANDIDATE_COMPETITION_CAP` in the harness so it cannot drift from the skill.
- trend-analysis has a rule for a platform that yields nothing: write no file, record the attempted queries in the consumer's `inputs_missing`, lower confidence, never substitute another platform's data.

### Lessons worth keeping
- **Verify a new required field bites before satisfying it.** Adding `blended_ceiling_customers` to the schema and running the live B2B idea produced exactly one error naming the unsatisfied `one_of` group. That two-minute check proves the contract is live; adding field and data in the same commit proves nothing.
- **A tightened threshold will break a fixture, and that is the fixture earning its keep.** Dropping the cap to 45 immediately failed `fixture-b2c-candidate`, which carried 60. When adjusting the fixture, keep it exercising the same band it was written for: demand was raised so `base_score` stayed at 50.5 and the fixture still covers the middle `candidate` label rather than sliding into `weak-candidate`.
- **Put a threshold used in two places into one named constant.** The cap was hardcoded twice in `check_scores` and once in prose in the skill. It is now a constant with its evidence in a comment.
- **Expect the legacy baseline to move when a threshold tightens.** Errors went 306 to 309 because fourteen legacy candidates now exceed 45 where eleven exceeded 60. No legacy file was touched and `--baseline` still exits 0. Record the movement rather than chasing it.

### State after task 4
All four tasks are DONE and the board is empty. `--check-specs` is at 0 errors, both live runs are at 0 errors and 0 warnings, the fixture suite is at its documented 29, and `--baseline` exits 0.

## Task 5 — Public launch: FindMeSaaS (2026-09-06)

### Provenance, and why the licence looks like it does
This repository originates from `github.com/MaxKmet/idea-validation-agents`, MIT licensed, whose initial commit created the skill system, the workflow specifications and the memory protocol. MIT requires the copyright notice to survive in copies and substantial portions, so `LICENSE` carries two copyright blocks, each stating what it covers. Do not remove the upstream line in any future edit, and keep the one-line credit in the README. A fork that is open about its origin is also received better by this audience than one that is not.

### Branding without renaming
The product name lives in prose only: `README.md`, `CLAUDE.md`, `AGENTS.md`, `skills/README.md`. No directory, skill identifier, adapter path or harness needle encodes it. That made a rebrand a four-file change with zero regressions, and it is worth preserving. If a future rename is requested, change the same four files and nothing else.

### Writing a README that will not embarrass you later
- Every number was traced to a repository file before shipping. Four were wrong on the first pass: a line count that had moved during the same task, a citation year that disagreed with the skill citing it, a count of table rows, and a comparative claim about other projects that could not be verified. Do this pass every time the README changes.
- The strongest section is a real abridged verdict from `memory/ideas/`, not a feature list. It cannot be accused of being staged, and it demonstrates the product's actual character, which is that it disagrees with you.
- The five-run competition table is the second strongest, because it shows the system correcting itself with evidence rather than claiming accuracy.

### Onboarding
First-run onboarding now runs ahead of any workflow when no profile exists, not only before idea generation, and captures hours per week, monthly budget, risk tolerance and target buyer. The first three were flagged as missing by four separate decision memos; the fourth sets `preferred_business_model`, which selects the rubric lane in eight skills. The profile gate in idea-validation remains as a fallback for profiles created through the browse or skip paths.

### Testing gotcha worth remembering
A mutation test reported a false failure because the test removed a needle case-sensitively while the assertion lowercases the text before matching, leaving one capitalised occurrence alive. When mutation-testing a case-insensitive assertion, remove the needle case-insensitively too. The assertion was right and the test was wrong, which is the more dangerous of the two failure modes because it looks like a product bug.

### State after task 5
Five tasks DONE, board empty. `--check-specs` 0 errors, both live runs 0 errors and 0 warnings, fixture suite at 29, `--baseline` exits 0, 15 skills and 15 adapters intact. The README assumes a published slug of `Latifox/find-me-saas`; correct every link together if that changes.

## Task 6 — Distribution: installer, commands, autonomy, hooks (2026-09-06)

### Fetch the format, do not remember it
Both platform formats were fetched from the docs during planning, and both differed from what a reasonable guess would have produced. Slash-command namespacing by arbitrary subdirectory does not exist, so `/fms:validate` was impossible and command names had to be flat and collision-resistant. The documented hook example uses bash and `jq`, neither of which a Windows user reliably has, so the hooks were written in Python instead. Guessing either would have shipped something broken.

### Where the commands live, and why it is confusing
`.claude/skills/` now holds two kinds of entry: fifteen adapter stubs named after analyses (nouns, one per canonical skill) and nine commands named after jobs (verbs, dispatching to workflows). The harness checks both, in different ways. CONTRIBUTING explains the split; do not merge them.

Commands dispatch to workflows rather than restating them. A command that duplicates workflow logic will drift from it the first time the workflow changes.

### Hook design rules that earned their place
- **Fail open.** Both scripts wrap `main()` and exit 0 on any unexpected exception. A hook that breaks a session is worse than a hook that does nothing.
- **`PostToolUse` reports, it does not block.** On that event exit 2 does not undo the write; it surfaces stderr to the agent. That is the right shape: the file is already on disk and the agent still has the context to fix it.
- **Consume stdin even when returning early**, so the caller never blocks on a full pipe.
- Derive the project root from `Path(__file__).resolve().parents[2]` rather than trusting the working directory.

### The installer bugs, both found by running it
- The first dry run was packaging `.claude/scheduled_tasks.lock`, a local runtime artifact. An installer copies from the maintainer's working copy, so it needs an explicit exclusion list, not just a source manifest.
- The user-data guard initially classified `memory/ideas/.gitkeep` and `memory/market_insights/README.md` as user analyses, so a reinstall reported protecting its own scaffolding. Negative lookahead fixed it.
- A user with an existing `.claude/settings.json` would have silently received no hooks. The installer now detects that specific skip and prints the JSON block to merge.

Neither bug was visible by reading the code. Run the installer into a temp directory every time it changes.

### State after task 6
Six tasks DONE. `--check-specs` is at 28 checks and 0 errors, both live runs and the shipped examples are clean, the fixture suite is at 29, and `--baseline` exits 0. The npm name `find-me-saas` is unverified; run `npm view find-me-saas` before publishing and change `package.json` plus the README install command if it resolves.
