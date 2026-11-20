# to-impl-plan provenance

## Upstream

- repository: none
- path: none
- commit: none
- license: none
- status: own

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| Pi config `plan-ticket-impl` skill | note | primary | 2026-11-20 | the core principles, gather, intake, agree the seams and tests, the plan sections, the Builder contract rules, the verification artifacts table, the output style | none |
| smb374/agent-skills #2, section "to-impl-plan skill" | specification | primary | 2026-11-20 | the parts to keep and to remove | none |
| smb374/agent-skills #8, Amendments | specification | primary | 2026-11-20 | stages, the start condition, the brief output with `fill`, the contract partial, the Report section | none |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| one plan with one or more stages, one builder run for each stage | #8 amendment. A ticket too big for one builder session stays one ticket | adopted |
| one stage when the ticket fits one run but a builder went wrong on it | #8 amendment. The implement flows give the ticket to the worker directly | adopted |
| a listed knowledge skill with the start rule of `handoff`, not a flow | #8 amendment | adopted |
| the plan is a brief filled with `fill` in the temporary directory, not a file in a plan directory | #8 amendment | adopted |
| the plan rules of the contract in the static partial `assets/builder-contract.md`, with the Report section | #8 amendment. A harness wrapper swaps one file for its own contract | adopted |
| each stage is one Markdown string, and SKILL.md names its subsections | `fill` accepts strings, lists of strings, and bools only | adopted |
| the general receiver rules (authority, gaps, evidence) in the contract | `handoff` has them. The plan ends with a line that loads `handoff` | rejected |
| the plan review by a reviewer subagent, `ask_parent`, and the Pi worker Report shape | #2. They stay in the Pi wrapper `plan-ticket-impl` | rejected |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | done: `just eval to-impl-plan --runs 2` on 2026-11-20 with `claude-haiku-5-5`. Skill 18/18, baseline 0/18. Earlier runs found two faults: a plan written to `/tmp` and not `$TMPDIR`, and an ad-hoc `python3 -c` gate command. Step 4 and the Verification gate text fix them | run again after a change to the body or the templates |
| trigger check with near-miss queries | missing | run the trigger loop of skill-writer when a trigger failure shows |

## Local changes

- Replace the plan directory with a brief in the temporary directory, filled with `fill`.
- Split the per-run sections (Scope, Tests to add, Existing tests permitted to change, Budget, Action items, Verification gate) into stages, with a Depends on section.
- Move the Builder contract into `assets/builder-contract.md`. Remove `ask_parent` and the authority order. Add the stage rules and the Report shape.
- Remove step 5 (the plan review) and the reference to `implement-flow`.
- Replace `/skill:setup-project` and `/skill:to-tickets` with `/setup-project` and `/to-tickets`.
- Remove `disable-model-invocation`. Add the start rule of `handoff`.
