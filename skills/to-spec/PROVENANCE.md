# to-spec provenance

## Upstream

- repository: mattpocock/skills, https://github.com/mattpocock/skills
- path: `skills/engineering/to-spec`
- commit: 5863806dd4e15c63174bee4e7515a4256792ecfa (5863806)
- license: MIT, see `LICENSE`
- status: modified

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| mattpocock/skills `to-spec` @ 5863806 | code | primary | 2026-11-19 | the full skill | MIT |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| replace `/setup-matt-pocock-skills` with `/setup-project` | this repo replaces that skill with `setup-project` (issue #1) | adopted |
| `agents/openai.yaml` | Codex UI metadata only. The skill does not need it | rejected |
| choose `[Feature]` or `[Task]` from `issue-types.md`, one template for both | #13 decision 1 | adopted |
| make the spec a sub-issue of its Epic or Bug | #13 decision 2 | adopted |
| one user story for each distinct behavior, "None" for a Task with no visible change | #13 decision 3. An agent asked for a long list hallucinates stories, about 20 or more on average | adopted |
| write "what makes a good test" only when discussed with the user | #13 decision 4 | adopted |
| delete the "Further Notes" section | #13 decision 5 | adopted |
| "Ask one question only: confirm the test seams" replaces "Do NOT interview the user" | #13 decision 6 | adopted |
| end with a Report step: issue number, type, parent | #13 decision 7 | adopted |
| third-person description with "Use when" and the near-miss siblings `to-tickets` and `wayfinder`. Full STE pass | #13 "Both skills" | adopted |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing | the changes only rename a skill and a tool phrase. Add an eval when a failure shows |

## Local changes

- Replace `/setup-matt-pocock-skills` with `/setup-project`.
- Remove `agents/openai.yaml`.
- Apply the #13 decisions: issue type choice, sub-issue link, user story rule, testing rule, no "Further Notes", one allowed question, Report step, new description, STE pass.
