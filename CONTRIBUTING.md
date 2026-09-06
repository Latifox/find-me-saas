# Contributing to FindMeSaaS

Thanks for looking. This project is a set of Markdown specifications executed by an AI agent, plus a small Python harness that keeps those specifications honest. There is no build step and no runtime dependency beyond Python 3.10 for the tests.

## The one rule that matters

**Edit the canonical skill, then leave the adapters alone.**

```
skills/<name>/SKILL.md          <- canonical. Edit this.
.claude/skills/<name>/SKILL.md  <- 6-line stub pointing at the canonical
.codex/skills/<name>/SKILL.md   <- same
.cursor/rules/<name>.mdc        <- same
```

The three adapters exist so Claude Code, Codex and Cursor can each discover the skill. They are stubs that link back to the canonical file. Only touch them if you add a new skill or change a skill's one-line description.

Directory names and skill identifiers are stable identifiers. FindMeSaaS is the product name; it does not appear in any path, and renaming directories would break the harness and all three adapters.

## Before you open a pull request

```bash
python tests/validate_memory.py --check-specs    # specs and workflows must be clean
python tests/make_fixtures.py --out /tmp/fx
python tests/validate_memory.py --memory /tmp/fx/memory   # fixture suite
```

`--check-specs` must exit 0. The fixture suite has six passing fixtures that must exit 0, and four deliberately broken ones that must report exactly 23, 3, 1 and 2 errors. If your change moves a fixture count on purpose, update the table in `tests/README.md` in the same commit.

If you have run the agent and produced idea directories, `python tests/validate_memory.py --idea <slug>` checks one of them. Use `--baseline` on older corpora; it reports without failing.

## Two kinds of thing live in `.claude/skills/`

This trips people up, so it is worth stating plainly.

| Kind | Example | What it is |
|---|---|---|
| **Adapter** | `.claude/skills/idea-scoring/` | A six-line stub pointing at `skills/idea-scoring/SKILL.md`. One per canonical skill, mirrored in `.codex/` and `.cursor/` |
| **Command** | `.claude/skills/validate-idea/` | A slash command the user types. Dispatches to a workflow; has no canonical counterpart |

Adapters are named after the analysis they wrap (nouns). Commands are named after
what the user wants to do (verbs). The harness checks that every canonical skill has
its three adapters, and separately that all nine commands exist.

## Adding a command

1. Create `.claude/skills/<verb-name>/SKILL.md`. **The directory name becomes the
   command**, so `/validate-idea` comes from `.claude/skills/validate-idea/`.
2. Frontmatter needs `name` (must match the directory), `description` (Claude uses
   this to decide when to auto-invoke), and `argument-hint` if it takes arguments.
3. In the body, dispatch to a workflow rather than restating its logic. A command
   that duplicates a workflow will drift from it.
4. Add the name to `COMMANDS` in `tests/validate_memory.py` and to the table in the
   README.
5. Run the harness.

Command names are flat. Namespacing by subdirectory only works for monorepo project
directories, so there is no way to get `/fms:validate`; pick a name unlikely to
collide with the user's own commands.

## Adding a skill

1. Write `skills/<name>/SKILL.md` following the shape of an existing one: frontmatter, a version comment, Purpose, Input, rubric tables, a numbered Process, an Output section with a single parseable JSON block, and Notes.
2. Create the three adapter stubs.
3. Add the output contract to `tests/schemas.json` if the skill writes JSON.
4. Add the skill to the relevant workflow in `workflows/`.
5. Add a row to the table in `skills/README.md`.
6. Run the harness.

Every fenced ```json block in a skill must parse. Enum choices are written as string values such as `"pursue | test | pivot | drop"`, never as bare tokens or with comments.

## Editing a rubric

- Keep the score bands identical across lanes (80-100 / 60-79 / 40-59 / 15-39 / 0-14) so the aggregator stays mechanical.
- Add B2B rows inside the existing table rather than forking the skill. The `business_model` field on each idea selects the lane.
- Every benchmark number needs a `source:` note or an explicit `heuristic` marker.
- Bump the `version:` comment on any skill you change.

## The memory contract

Everything the agent produces lands in `memory/`, one directory per idea. Skills never call each other; the orchestrator reads each output and passes context to the next. Idea directories are never deleted, only marked `dropped` or `paused`. `tests/schemas.json` is the contract for every JSON file written there.

## Style

Specifications are read by a language model, so write for one: short declarative sentences, tables for rubrics, explicit thresholds, and a stated reason for every number. Vague guidance produces vague analysis.

## Reporting a bad verdict

If the agent produced an analysis you think is wrong, that is the most useful issue you can file. Include the idea slug, the score, and which dimension you disagree with. Rubrics have been recalibrated five times from exactly this kind of evidence; see `docs/HANDOFFS.md` for the record.

## Licence

Contributions are accepted under the MIT licence in `LICENSE`, which carries the original copyright from the upstream project alongside the copyright on later extensions.
