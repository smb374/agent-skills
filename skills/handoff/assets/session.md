{{! fill: no-escape }}
# Handoff

## Goal

{{! One sentence: what the next session must achieve. Put the focus of the user here. }}
{{goal}}

## State

{{! What is done and what is in progress. Name each branch, commit, and changed file. }}
{{state}}

## Decisions

{{! Each decision with its reason: "<decision>. Why: <reason>". }}
{{#decisions}}
- {{.}}
{{/decisions}}
{{^decisions}}
None
{{/decisions}}

## Superseded

{{! Fork session only: each point in the history that no longer holds. Use [] for a new session. }}
{{#superseded}}
- {{.}}
{{/superseded}}
{{^superseded}}
None
{{/superseded}}

## Open questions

{{! Each question that the user must still answer. }}
{{#open_questions}}
- {{.}}
{{/open_questions}}
{{^open_questions}}
None
{{/open_questions}}

## Artifacts

{{! Each path or URL, with what it holds: specs, plans, ADRs, issues, diffs, commits. }}
{{#artifacts}}
- {{.}}
{{/artifacts}}
{{^artifacts}}
None
{{/artifacts}}

## Next action

{{! The first step of the next session. }}
{{next_action}}

## Done when

{{! Each check that proves the work is done, and where the result goes. At least one item. }}
{{#done_when}}
- {{.}}
{{/done_when}}

## Suggested skills

{{! Each skill that the next session loads, with the reason. }}
{{#suggested_skills}}
- {{.}}
{{/suggested_skills}}
{{^suggested_skills}}
None
{{/suggested_skills}}

---

Before you start, load the `handoff` skill, and follow its rules to receive a handoff.
