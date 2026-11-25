---
name: to-tickets
description: "Breaks a plan, a spec, or the current conversation into tickets that each name the tickets that block them, and publishes them to the configured tracker. Use when the user wants a spec or a plan cut into tickets for implementation agents. To plan the build of one ticket, use to-impl-plan."
disable-model-invocation: true
---

# To Tickets

Break a plan, a spec, or a conversation into **tickets**. A ticket is a tracer bullet: a thin vertical slice that cuts through every layer. Each ticket names the tickets that **block** it.

The issue tracker and triage label vocabulary must be in your context. If not, tell the user to run `/setup-project`.

## Process

### 1. Gather context

Use what is already in the conversation. If the user gives a reference (a spec path, an issue number, or a URL), fetch it. Read its full body and its comments.

### 2. Explore the codebase (optional)

If you have not explored the codebase, do so now. Use the domain glossary words in ticket titles and descriptions. Follow the ADRs of the area that you change.

Look for prefactoring that makes the work easier. "Make the change easy, then make the easy change."

### 3. Draft the tickets

<ticket-rules>

- Each ticket cuts a narrow but complete path through every layer (schema, API, UI, tests). Do not cut a horizontal slice of one layer.
- A finished ticket is verifiable on its own.
- A ticket is one review stop.
- Do prefactoring first.

</ticket-rules>

Give each ticket its **blocking edges**: the tickets that must finish before it can start. A ticket with no blockers can start at once.

**A wide refactor is the exception to vertical slicing.** A wide refactor is one mechanical change (rename a column, retype a shared symbol) that reaches the whole codebase. One edit breaks thousands of call sites, so no vertical slice can land green. Write it as these numbered steps:

1. Expand: add the new form beside the old form, so nothing breaks.
2. Migrate: move the call sites in batches, sized by the blast radius (for example per package or per directory). Each batch is one ticket, blocked by the expand ticket.
3. Contract: delete the old form when no caller remains. This ticket is blocked by every migrate ticket.

If the batches cannot stay green alone, keep the same steps. Let the batches share one integration branch. All of them block a final integrate-and-verify ticket. Green is promised only there.

### 4. Quiz the user

Show the draft as a numbered list. For each ticket, show:

- **Title**: a short name
- **Blocked by**: the tickets that must finish first, if any
- **What it delivers**: the end-to-end behavior that the ticket makes work

Ask the user:

- Is the size right? (too big, or too small)
- Are the blocking edges correct? Does each ticket depend only on tickets that really gate it?
- Must any tickets be merged or split?

The user decides the size. Repeat the quiz up to 3 rounds. If the user has not approved after round 3, ask whether the spec needs rework (use to-spec or wayfinder).

### 5. Publish the tickets

Publish the approved tickets. The tickets are the same for each tracker. Only the shape of the blocking edges changes.

- **Local files**: write one file for each ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`. Number them from `01` in dependency order, blockers first. In each file, "Blocked by" lists the numbers and titles of its blockers. Use the local template below. Never write one combined file.
- **A real issue tracker (GitHub, Linear, and others)**: publish one issue for each ticket, in dependency order, blockers first. Then each ticket can name real identifiers as its blockers. Use the title prefix `[Ticket]`, and apply the labels `type:ticket` and `ready-for-agent`. Use the native blocking link of the tracker when it has one. Otherwise set "Blocked by" in each ticket to its blocking issues. If the source was an existing issue, make each ticket a sub-issue of it (see the tracker doc). Omit `## Parent` when the native sub-issue link exists. Keep it only as the fallback.

Do not close or change a parent issue.

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** the end-to-end behavior that this ticket makes work, from the point of view of the user. Do not list the work layer by layer.

**Blocked by:** the numbers and titles of the tickets that gate this one, or "None (can start immediately)".

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker. Use this section only as the fallback, when the native sub-issue link does not exist. Omit it when the source was not an issue.

## What to build

The end-to-end behavior that this ticket makes work, from the point of view of the user. Do not list the work layer by layer.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)". Omit this section when you set the blockers as native edges.

</issue-template>

In both forms, do not include file paths or code snippets. They go stale fast. Exception: a prototype can produce a snippet that states a decision more precisely than prose (a state machine, a reducer, a schema, a type shape). Put it in the ticket, and say that it came from a prototype. Keep only the parts that carry the decision.

### 6. Report

List one line for each ticket, in dependency order: the number, the title, and the blocked-by. In local mode, list the file paths.
