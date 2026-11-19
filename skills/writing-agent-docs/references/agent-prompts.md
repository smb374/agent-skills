# Agent prompts

Use this file when you write an agent definition, a system prompt, or a brief for a subagent. This file covers the portable craft. A harness or a workflow can add its own templates.

## Contents

- [Three parts, three loads](#three-parts-three-loads)
- [The description](#the-description)
- [The body](#the-body)
- [The brief](#the-brief)
- [Model-specific rules](#model-specific-rules)
- [Checklist](#checklist)

## Three parts, three loads

| Part | Load | Holds |
| --- | --- | --- |
| description | always, in the context of the orchestrator | the trigger words only |
| body (the system prompt of the agent) | each run of the agent | the role, the method, the constraints, the report shape |
| brief (the first message to the agent) | one dispatch | the task: the goal, the facts, the scope, the done condition |

Put each piece in the part with the lowest load that still reaches the agent in time.

## The description

The description is a context pointer. The orchestrator reads it to choose an agent. Use the pointer rules in `levers.md`.

Bad: `This agent is a very capable reviewer with deep expertise in many languages, and it can check style, security, and tests.`
Good: `Code reviewer. Use after a code change.`

Check the field names in the harness docs. Claude Code ignores an unknown frontmatter field with no error.

## The body

The body is the system prompt of the agent. The agent loads it on each run, so it can hold detail.

- State the role in one line, then the method, then the constraints.
- Name the safe actions and the unsafe actions. Name when the agent hands back to the caller.
- For an orchestrator, say when to work directly and when to delegate. Some models delegate a task that a direct edit solves.
- Define the report shape: the sections, in order.

## The brief

A subagent starts cold. It gets its own system prompt, basic environment details, and the brief. It does not get the system prompt of the parent or the conversation so far. Some harnesses can also drop the instructions files. The brief must hold each fact that the subagent needs.

A brief holds these parts:

| Part | Content |
| --- | --- |
| goal | the outcome, and why the caller needs it |
| facts | what the caller already found: paths, symbols, decisions. The subagent must not find them again |
| scope | the files or areas in scope and out of scope. Say whether the subagent edits or only reports |
| done | a checkable, exhaustive completion criterion |
| stop | the stop conditions, and when to hand back instead of going on |
| missing facts | one policy: "assume, go on, and record the assumption", or "stop and report the open question" |
| report | the shape of the return: a summary, not a transcript |

Use imperative verbs. "Can you suggest changes" gets suggestions. "Change the function" gets an edit.

Ask for more than the minimum in words when you want it. The model does not infer extra scope from a vague brief.

Bad:

```
Look into the flaky login test and see what you can find.
```

Good:

```
Goal: find why tests/login.spec.ts fails about 1 run in 5 on CI, so that we can fix it.
Facts: it passes locally 50 of 50 runs. CI uses 2 CPUs. The test waits on a 500 ms timer.
Scope: tests/login.spec.ts and src/auth/. Read only: report, and leave the files unchanged.
Done: one root cause with evidence from a CI log or a local repro, or a list of the causes that you ruled out.
Stop: hand back when a repro needs CI secrets.
Missing facts: stop and report the open question.
Report: root cause, evidence, proposed fix, in under 200 words.
```

## Model-specific rules

Some rules help one model and hurt another. Examples: a request for status updates between tool calls, a request for an upfront plan, and strong words about thoroughness. Keep these out of a portable prompt. Check the prompting guide of the target model, and add the rule only in a prompt for that model.

## Checklist

- [ ] The description holds trigger words only.
- [ ] The body names the safe actions, the unsafe actions, and the hand-back condition.
- [ ] The brief has each part: goal, facts, scope, done, stop, missing facts, report.
- [ ] Each verb in the brief is imperative, and the brief says whether to edit.
- [ ] No rule depends on one model, or the prompt names that model.
