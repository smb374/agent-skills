# handoff provenance

## Upstream

- repository: mattpocock/skills, https://github.com/mattpocock/skills
- path: `skills/productivity/handoff/SKILL.md`
- commit: 0f5e033ebc47b142f5ffa56a582ede6d9d9bada3 (0f5e033)
- license: MIT, see `LICENSE`
- status: derived

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| mattpocock/skills `handoff` @ 0f5e033 | code | primary | 2026-11-20 | save to `$TMPDIR`, refer to artifacts by path or URL, the suggested-skills section, redact secrets, user arguments set the focus | MIT |
| Pi config `agent-handoff` skill | note | secondary | 2026-11-20 | the receiver rules (authority, gaps, evidence, report shape) and the parent check of a report | none recorded |
| smb374/agent-skills #2, section "handoff skill" | specification | primary | 2026-11-20 | the two-axis table, the sender and receiver rules, the session template fields, the `fill` steps | none |
| hyperturtle/Stache | code | secondary | 2026-11-19 | design inspired by hyperturtle/Stache (MIT) for `fill`: a tokenizer and a renderer. No code is copied | MIT |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| a listed knowledge skill, but a handoff starts only from user input or from a step of a flow that the user started | #2 | adopted |
| two axes (inherits context, a parent waits) decide the rules for the brief | #2 | adopted |
| ship one template, `assets/session.md`. A subagent template comes from the user or the flow, else ask the user | #2. The Pi templates serve Pi flows only | adopted |
| `fill` fills the template, so a missing, empty, or mistyped value fails before the brief exists | #2 | adopted |
| the template is in `assets/`, not `templates/` | skill-writer `references/writing-rules.md`: templates go in `assets/` | adopted |
| a Superseded field, for the delta of a fork session | #6 amendment | adopted |
| the template ends with a line that points the receiver to this skill | #6 amendment. A new session has not loaded the skill | adopted |
| Done when must have at least one item. The other lists render `None` when empty | #6 amendment | adopted |
| IDs, severity, and certainty of review findings | Pi review-flow rules. They stay in the Pi templates | rejected |
| `disable-model-invocation: true`, as upstream has | the skill also holds the receiver rules, which a receiver loads on its own | rejected |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing | run `just eval handoff` |
| trigger check with near-miss queries | missing | run the trigger loop of skill-writer when a trigger failure shows |

## Local changes

- Rewrite the upstream prose as rules for a fork session, a new session, and a subagent.
- Add the receiver rules.
- Add the session template and the `fill` steps.
- Remove `argument-hint` and `disable-model-invocation`.
