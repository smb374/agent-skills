{{! fill: no-escape }}
{{! The ticket title. }}
# {{title}}: implementation plan

## Ticket

{{! The ticket ID or URL, its parent spec, and each acceptance criterion as a literal. }}
{{ticket}}

## Current state

{{! What exists now, with confirmed file paths. Each blocking ticket, and whether it landed. What a builder that already ran on this ticket got wrong. }}
{{current_state}}

## Out of scope

{{! Each thing that this plan deliberately does not change. }}
{{#out_of_scope}}
- {{.}}
{{/out_of_scope}}
{{^out_of_scope}}
None
{{/out_of_scope}}

## Common verification commands

{{! Each literal command line that every gate runs. Label a command that you did not read from the project "(unconfirmed)". At least one item. }}
{{#commands}}
- `{{.}}`
{{/commands}}

## Behavior specification

{{! A literal expected artifact for each behavior that the plan adds or changes, in the form of the Verification artifacts table. Name the test that checks each artifact. }}
{{behavior}}

## Rules / constraints

{{! Each behavioral constraint, with its source: a file and a line range or a section. }}
{{#rules}}
- {{.}}
{{/rules}}
{{^rules}}
None
{{/rules}}

## Stages

{{! Each stage as one Markdown string in the Stage shape of the skill, in build order. At least one item. }}
{{#stages}}
{{.}}

{{/stages}}
## Open questions

{{! Each gap that intake could not establish, and each unconfirmed command. }}
{{#open_questions}}
- {{.}}
{{/open_questions}}
{{^open_questions}}
None
{{/open_questions}}

{{> builder-contract.md}}

---

Before you start, load the `handoff` skill, and follow its rules to receive a handoff.
