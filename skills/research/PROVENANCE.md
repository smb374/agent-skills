# research provenance

## Upstream

- repository: mattpocock/skills, https://github.com/mattpocock/skills
- path: `skills/engineering/research`
- commit: 5863806dd4e15c63174bee4e7515a4256792ecfa (5863806)
- license: MIT, see `LICENSE`
- status: modified

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| mattpocock/skills `research` @ 5863806 | code | primary | 2026-11-19 | the full skill | MIT |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| fallback: research in this session when the harness cannot start a background agent | `docs/catalog.md` | adopted |
| `agents/openai.yaml` | Codex UI metadata only. The skill does not need it | rejected |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing | add an eval when a research failure shows |

## Local changes

- Remove `agents/openai.yaml`.
- Add the fallback for a harness with no background agent.
- Change "Its job" to "The job", because the fallback gives the job to the main agent.
