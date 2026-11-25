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
| apply `[Ticket]`, `type:ticket`, and `ready-for-agent` | #13 decision 1 | adopted |
| delete "sized to fit in a single fresh context window". Keep "verifiable on its own" and "one review stop" | #13 decision 2. The user quiz decides the size | adopted |
| quiz maximum of 3 rounds, then ask whether the spec needs rework | #13 decision 3 | adopted |
| wide refactor as numbered steps: expand, migrate, contract, integration-branch fallback | #13 decision 4 | adopted |
| delete the "Work the frontier" sentence | #13 decision 5 | adopted |
| omit `## Parent` when the native sub-issue link exists | #13 decision 6 | adopted |
| keep the local-files branch | #13 decision 7 | adopted |
| end with a Report step: one line for each ticket, file paths in local mode | #13 decision 8 | adopted |
| third-person description with "Use when" and the near-miss sibling `to-impl-plan`. Full STE pass. One term, "ticket". Templates stay inline, no `fill.py` | #13 "Both skills" | adopted |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing | the changes only rename a skill and a tool phrase. Add an eval when a failure shows |

## Local changes

- Replace `/setup-matt-pocock-skills` with `/setup-project` in 2 places.
- Remove `agents/openai.yaml`.
- Apply the #13 decisions: ticket labels and prefix, no context-window sizing, 3-round quiz, numbered wide refactor steps, no frontier sentence, native parent link, Report step, new description, STE pass.
