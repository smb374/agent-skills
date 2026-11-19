<!-- Derived from mattpocock/skills skills/productivity/writing-for-agents @ 3216582 (MIT); rewritten. -->

# Levers

Use this file in Step 3 and Step 4. Each lever is one way to make an agent take the same path on each run. Each lever has one example: a bad version, then a good version.

## Contents

- [Context pointers](#context-pointers)
- [The two loads](#the-two-loads)
- [The information hierarchy](#the-information-hierarchy)
- [Completion criteria](#completion-criteria)
- [Leading words](#leading-words)
- [The positive target](#the-positive-target)
- [Emphasis is model-relative](#emphasis-is-model-relative)
- [Prose or enforcement](#prose-or-enforcement)
- [Single source of truth](#single-source-of-truth)
- [The environment is a cache source](#the-environment-is-a-cache-source)
- [The reason behind a rule](#the-reason-behind-a-rule)
- [The pruning pass](#the-pruning-pass)

## Context pointers

A context pointer is a line in context that names material outside context, and the condition to reach it. A skill description, an agent description, and a line in AGENTS.md that names a doc are all pointers. The wording of the pointer decides when the agent reaches the material, and how reliably.

- Put the condition first. The condition is the part that triggers.
- Write one trigger for each branch. Two synonyms for one branch are one trigger written twice.
- Cut the identity that the target already carries.
- When a must-have target is missed, sharpen the pointer first. Inline the material only when sharper wording fails.

Bad: `See docs/database.md for more information about the database.`
Good: `Before you write a migration, read docs/database.md.`

## The two loads

- **Context load** is the cost of always-loaded text on the window of the agent. It costs tokens and attention on each turn, even when the text does not apply.
- **Cognitive load** is the cost on the human, who must know which documents exist and when to use each. Spend it where human judgment matters.

Put the detail where the load is paid only on use. A pointer that is always loaded holds trigger words only. The target, which loads on use, holds the detail.

Bad (agent description, always loaded): `Reviews code. It checks style, naming, tests, security, performance, and docs, and it writes a report with a severity for each finding, grouped by file.`
Good (agent description): `Code reviewer. Use after a code change.` The checks and the report shape go in the body.

## The information hierarchy

A document holds **steps** (ordered actions) and **reference** (rules and facts to look up). Place each piece on a ladder, by how soon the agent needs it:

1. In-file step: what the agent does, in order.
2. In-file reference: looked up on demand. A flat list of peer rules is fine.
3. Disclosed reference: a separate file behind a pointer, loaded only when the pointer fires.

**Progressive disclosure** moves a piece down the ladder. The test is the branch: keep in the file what each branch needs. Move behind a pointer what only some branches need.

**Co-location**: keep the definition, the rules, and the caveats of one concept under one heading.

**Sprawl** is a document that is too long, even when each line is useful. Attention thins across the excess. Disclose reference, or split by branch.

Bad: an AGENTS.md with 60 lines of release procedure between the test command and the commit rules.
Good: `Before you cut a release, read docs/release.md.` The procedure moves to that file.

## Completion criteria

Each step ends on a completion criterion: the condition that tells the agent that the step is done.

- **Clarity**: the agent can tell done from not done. A vague criterion invites the agent to stop early. Sharpen the criterion first. Hide the later steps only across a real context boundary, such as a subagent dispatch.
- **Demand**: how much the criterion asks. "Each changed model has a migration" drives more work than "list the changes".

The strongest criteria are checkable and exhaustive.

Bad: `Investigate the failing tests.`
Good: `Done when each failing test has a root cause, or a note that says which fact is missing.`

## Leading words

A leading word is a short concept from pretraining that the agent thinks with, such as _tight_, _red_, or _tracer bullet_. Repeat the word, not its definition. It anchors behaviour in the body, and it helps the agent link a pointer to your prompts and your code. Use an existing word before you coin one. A coined word costs definition tokens.

Look for a phrase that the document spells out at several sites. Collapse it into one word.

Bad: `Write a test that fails because of the bug, that runs fast, and that you trust.`
Good: `Make the loop go red on the bug. Keep it tight.`

## The positive target

A prohibition puts the banned behaviour in context, and the agent can half-read it as an instruction. State the target behaviour instead. Keep a ban only as a hard guardrail, and pair it with the safe path.

Bad: `Do not use markdown in your reply.`
Good: `Write the reply as plain prose paragraphs.`

## Emphasis is model-relative

The effect of a strong word depends on the model. A newer model can over-act on "CRITICAL" or "MUST". Choose the strength from a run, not from a guess:

- The agent under-acts in a run: use a stronger word.
- The agent over-acts in a run: soften the word.
- Write the model name next to the change in the provenance or the commit, because the next model can need the opposite.

Bad: `CRITICAL: You MUST ALWAYS use the search tool before you answer.`
Good: `Use the search tool when the answer depends on code that you have not read.`

## Prose or enforcement

An instructions file is context, not configuration. The agent can skip a prose rule. Some rules must run at a fixed point, such as before each commit or after each edit. Use a hook, a lint rule, or a permission rule for them. Keep prose for judgment.

Bad: `Always run the formatter after you edit a file.`
Good: a post-edit hook runs the formatter. The prose line goes away.

## Single source of truth

Keep each meaning in one place. Duplication costs maintenance and tokens, and it makes the meaning look more important than it is. Two copies drift into a contradiction. A contradiction costs the agent reasoning on each run, and the agent can follow either side.

Bad: AGENTS.md says `Use pnpm.` and docs/setup.md says `Run npm install.`
Good: AGENTS.md says `Use pnpm.` docs/setup.md says `pnpm install`.

## The environment is a cache source

Scripts, config files, the directory layout, and `--help` output are sources of truth. A document that restates them is a cache. A cache goes stale. Write what the agent cannot find by looking: an unwritten convention, the reason for a choice, a trap that no config shows.

Bad: `Run tests with npm test. Lint with npm run lint.` when `package.json` shows both.
Good: `The integration tests need Docker. Start it before you run npm test.`

## The reason behind a rule

Give one short sentence of reason when the agent can apply the rule wrongly without it. A reason lets the agent handle a case that the rule does not name.

Bad: `Never use ellipses.`
Good: `A text-to-speech engine reads the reply, so never use ellipses. It cannot speak them.`

## The pruning pass

Run each test on each changed line. When a sentence fails, delete the whole sentence.

| Test | Question | Action on fail |
| --- | --- | --- |
| no-op | Does the line change what the model does by default? | delete |
| cache | Can the agent find this in one file or one command? | delete, or point to the source |
| contradiction | Does another line, file, or nested file say the opposite? | keep one, delete the other |
| duplicate | Does another place say the same meaning? | keep one place |
| relevance | Does the line still bear on the task and the current code? | delete or update |
| model audit | Was the line written for an older model, and does it now cause over-action? | delete, do not rewrite |

The no-op test is model-relative. Settle a disagreement by a run, not by debate. A leading word too weak to change the default is a no-op too. Use a stronger word only after a run shows under-action, as in [Emphasis is model-relative](#emphasis-is-model-relative).

Without this pass, a document collects **sediment**: stale layers that stay because an addition feels safe and a removal feels risky.

Bad: `Be careful and thorough. Write clean code.`
Good: the line goes away. It changes nothing.
