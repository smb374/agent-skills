# triage provenance

## Upstream

- repository: mattpocock/skills, https://github.com/mattpocock/skills
- path: `skills/engineering/triage`
- commit: 5863806dd4e15c63174bee4e7515a4256792ecfa (5863806)
- license: MIT, see `LICENSE`
- status: modified

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| mattpocock/skills `triage` @ 5863806 | code | primary | 2026-11-19 | the full skill, `AGENT-BRIEF.md`, and `OUT-OF-SCOPE.md` | MIT |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| replace `/setup-matt-pocock-skills` with `/setup-project` | this repo replaces that skill with `setup-project` (issue #1) | adopted |
| write "load the `grilling` and `domain-modeling` skills" in place of "call the Skill tool" | the Skill tool exists in one harness only. `just check` bans the string | adopted |
| `agents/openai.yaml` | Codex UI metadata only. The skill does not need it | rejected |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing | the changes only rename a skill and a tool phrase. Add an eval when a failure shows |

## Local changes

- Replace `/setup-matt-pocock-skills` with `/setup-project`.
- Replace "call the Skill tool" with "load the `grilling` and `domain-modeling` skills".
- Remove `agents/openai.yaml`.
