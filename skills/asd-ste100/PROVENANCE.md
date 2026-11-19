# asd-ste100 provenance

## Upstream

- repository: danyuchn/asd-ste100-skill, https://github.com/danyuchn/asd-ste100-skill
- path: repository root
- commit: 707362731928d0d92526c066df15dbbe6a378c07 (7073627)
- license: MIT, see `LICENSE`
- status: modified

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| danyuchn/asd-ste100-skill @ 7073627 | code | primary | 2026-11-19 | the full skill | MIT |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| fork `danyuchn/asd-ste100-skill`, not `0xpili/simplified-technical-english` or a new skill | it is the skill that the user used before, and it has a lint script | adopted |
| the description: rewrite given text. Send whole agent documents to `writing-agent-docs` | both descriptions named system prompts and tool descriptions. This was an open decision in `docs/catalog.md` | adopted |
| `README.md` and `.claude-plugin/` | repository files, not part of the skill | rejected |
| reformat `scripts/ste-lint.py` with `ruff format` | `just check` runs `ruff format --check` on every Python file. The user chose a reformat over an exclude | adopted |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing | add an eval case in `evals/` of this repo when an STE rewrite failure shows |
| trigger split with `writing-agent-docs` | not tested | run both descriptions on the same prompts when the evals cover triggers |

## Local changes

- Change the description: rewrite given text, and send whole agent documents to `writing-agent-docs`.
- Add `license: MIT` to the frontmatter.
- Reformat `scripts/ste-lint.py` with `ruff format`. The code does not change.
