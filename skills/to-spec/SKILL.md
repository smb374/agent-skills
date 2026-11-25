---
name: to-spec
description: "Turns the current conversation into a spec and publishes it to the project issue tracker as a Feature or a Task. Use when the user wants a spec, a PRD, or a written plan from what they already discussed. To cut a spec into tickets, use to-tickets. To map a large unclear goal, use wayfinder."
disable-model-invocation: true
---

This skill takes the current conversation and your knowledge of the codebase, and writes a spec. Do not interview the user. Ask one question only: confirm the test seams.

The issue tracker and triage label vocabulary must be in your context. If not, tell the user to run `/setup-project`.

## Process

1. Explore the repo to learn the current state of the code, if you have not done so. Use the domain glossary words in the spec. Follow the ADRs of the area that you change.

2. Sketch the seams where you will test the work. Prefer an existing seam to a new one. Use the highest seam that you can. If you need a new seam, put it as high as you can. Fewer seams are better. The ideal number is one.

   Ask the user to confirm that these seams match what they expect.

3. Choose the issue type from `docs/agents/issue-types.md`. Use `[Feature]` for new behavior. Use `[Task]` for a change to existing behavior. The template is the same for both.

4. Write the spec with the template below. Publish it to the issue tracker with the type label and the title prefix. Apply the `ready-for-agent` triage label. The spec needs no more triage.

5. If the spec has an Epic or a Bug as its source, make the spec a sub-issue of that parent.

6. Report: the issue number, the type, and the parent (or "none").

<spec-template>

## Problem Statement

The problem that the user has, from the point of view of the user.

## Solution

The solution to the problem, from the point of view of the user.

## User Stories

A numbered list. Write one story for each distinct behavior. Do not pad the list. Use this format:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see the balance of my accounts, so that I can make better decisions about my spending
</user-story-example>

For a Task that changes no behavior that a user can see, write "None".

## Implementation Decisions

A list of the implementation decisions that were made. It can include:

- The modules that you build or change
- The interfaces of those modules that change
- Technical clarifications from the developer
- Architecture decisions
- Schema changes
- API contracts
- Specific interactions

Do not include file paths or code snippets. They go stale fast.

Exception: a prototype can produce a snippet that states a decision more precisely than prose (a state machine, a reducer, a schema, a type shape). Put it inside the related decision, and say that it came from a prototype. Keep only the parts that carry the decision.

## Testing Decisions

A list of the testing decisions that were made. Include:

- What makes a good test. Write this line only if you discussed it with the user. Otherwise omit it.
- Which modules are tested
- Prior art for the tests (similar tests in the codebase)

## Out of Scope

The things that are out of scope for this spec.

</spec-template>
