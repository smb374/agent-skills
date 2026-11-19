# to-tickets provenance

## Upstream

- repository: mattpocock/skills, https://github.com/mattpocock/skills
- path: `skills/engineering/to-tickets`
- commit: 5863806dd4e15c63174bee4e7515a4256792ecfa (5863806)
- license: MIT, see `LICENSE`
- status: modified

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| mattpocock/skills `to-tickets` @ 5863806 | code | primary | 2026-11-19 | the full skill | MIT |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| replace `/setup-matt-pocock-skills` with `/setup-project` (2 places) | this repo replaces that skill with `setup-project` (issue #1) | adopted |
| `agents/openai.yaml` | Codex UI metadata only. The skill does not need it | rejected |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing | the changes only rename a skill and a tool phrase. Add an eval when a failure shows |

## Local changes

- Replace `/setup-matt-pocock-skills` with `/setup-project` in 2 places.
- Remove `agents/openai.yaml`.
