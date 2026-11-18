<!-- Derived from getsentry/skills skills/skill-writer @ a582c51 (Apache-2.0); modified. -->

# Descriptions

Use this file in step 5, when you write or repair the description and the name of a skill. The description is the text that the harness shows to the model before the skill runs. A weak description gives a skill that never triggers, or one that competes with its neighbours.

## The description rules

1. Write the third person. "Creates a report." Do not write "I can..." or "You can...".
2. Say what the skill does, and when to use it.
3. Put the words that users type at the front: "create a skill", "fix a skill that does not trigger".
4. Keep the internal details out, unless they improve the trigger.
5. Keep it at most 1,024 characters. This is the portable limit across the harnesses.
6. Avoid provider-specific phrasing, unless the skill is provider-specific by design.

## The name rules

| Rule | Value |
| --- | --- |
| length | 1 to 64 characters |
| pattern | `^[a-z0-9]+(-[a-z0-9]+)*$` |
| directory | equal to the directory name |
| form | a gerund, such as `processing-pdfs`, or a clear noun phrase |
| banned words | `helper`, `utils`, `tools`, `anthropic`, `claude` |

Two harnesses break the rule in different ways. One uses `name` as the skill ID, and another uses the directory name. A mismatch gives the skill two IDs.

## Near-miss routing

Name the sibling skill for the near-miss case: "For a closed ticket, use `ticket-postmortem`." This stops two sibling skills from competing for one prompt.

The near-miss sentence is the only place where a skill names another skill.

## Say when, not how

Do not summarize the steps of a multi-step body in the description. An agent follows the summary and skips the body.

## Trigger strength depends on the model

One model under-triggers, so its authoring guide adds "even if the user does not ask for it". Another model over-triggers on the same words. Measure the trigger rate for each model that you support. Do not copy the advice of one model into another.

## The trigger loop

1. Write a description with the words that users really type.
2. Write two query sets: the should-trigger queries, and the should-not-trigger queries. Use 8 to 10 queries in each set.
3. Check the current description against both sets.
4. Edit the words to raise the recall and lower the false matches.
5. Repeat until the false positives and the false negatives are acceptable.

A should-not-trigger query is a near miss: it shares the domain, and it needs another skill.

## Output

- the final description
- the should-trigger query set
- the should-not-trigger query set
- a summary of the edits that you made to the trigger behaviour
