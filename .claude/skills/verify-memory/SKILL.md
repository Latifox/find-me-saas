---
name: verify-memory
description: Run the validation harness over your analyses and explain anything it flags
argument-hint: "[optional slug to check one idea]"
---

Run the project's own test suite and interpret the result.

Target: $ARGUMENTS

Commands, in order:

```bash
python tests/validate_memory.py --check-specs
python tests/validate_memory.py            # or --idea <slug> when one was named
```

`--check-specs` validates the skills and workflows themselves: every JSON example
parses, every file a workflow reads is produced by some skill, every skill has its
three platform adapters, and the commands and hooks are registered.

The second command validates your analyses: it recomputes every score from its
dimension values including the floor penalty and the missing-data discount, checks
each file against its contract, confirms verdicts match the threshold table, and
requires each memo to carry its sections, sit in its word budget and cite at least
three URLs.

Report the summary line, then for each ERROR explain in one sentence what the
contract expected and what it found, and offer to fix it. Warnings are advisory;
name them but do not treat them as failures.

If the corpus predates the current contracts, use `--baseline`, which reports
everything without failing the run.
