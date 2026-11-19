# grilling provenance

## Upstream

- repository: mattpocock/skills, https://github.com/mattpocock/skills
- path: `skills/productivity/grilling`
- commit: 5863806dd4e15c63174bee4e7515a4256792ecfa (5863806)
- license: MIT, see `LICENSE`
- status: modified

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| mattpocock/skills `grilling` @ 5863806 | code | primary | 2026-11-19 | the full skill: design tree, frontier, rounds, text format | MIT |
| Pi config fork of `grilling` | note | secondary | 2026-11-19 | the question-tool rules and the final confirm round | none recorded |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| use a multiple-choice question tool when the harness has one, and keep the upstream text format as the fallback | Pi config fork. Not all harnesses have such a tool | adopted |
| name no tool. Describe its function | this repo holds portable skills only | adopted |
| `agents/openai.yaml` | Codex UI metadata only. The skill does not need it | rejected |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing | add an eval when a grilling failure shows |

## Local changes

- Remove `agents/openai.yaml`.
- Add "Ask with a question tool": the round goes through a multiple-choice tool when the harness has one. The upstream text format becomes the fallback.
- Add a fallback for a harness with no sub-agent tool: find the fact yourself.
- Add a last round that asks the user to confirm or to reopen a branch.
