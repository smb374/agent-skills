<!-- Derived from getsentry/skills skills/skill-writer @ a582c51 (Apache-2.0); modified. -->

# Writing rules

Use this file in step 4, when you write the body, place the files, and shape the output of a skill.

## Contents

- [Core rules](#core-rules)
- [The precision pass](#the-precision-pass)
- [Keep or cut](#keep-or-cut)
- [Match the structure to the fragility](#match-the-structure-to-the-fragility)
- [Instruction shapes](#instruction-shapes)
- [Runtime writing rules](#runtime-writing-rules)
- [Simplified Technical English](#simplified-technical-english)
- [The reference architecture](#the-reference-architecture)
- [Place the files](#place-the-files)
- [Match the form to the failure](#match-the-form-to-the-failure)
- [State the reason, and its strength](#state-the-reason-and-its-strength)
- [Structure rules](#structure-rules)
- [Scripts](#scripts)
- [Structure troubleshooting](#structure-troubleshooting)
- [Output](#output)

## Core rules

- Each line must help the agent decide, act, or verify something.
- Prefer tables, checklists, templates, and input and output examples to prose.
- Give the reason in one short sentence, and only when the agent would otherwise choose wrong.
- Use one term for one concept. Do not rotate synonyms.
- State one default path before you mention an alternative.

## The precision pass

Run the pass before you add a section, a file, or a rule.

| Action | Use it when |
| --- | --- |
| replace | an existing rule is vague, stale, or points at the wrong behaviour |
| narrow | the rule is mostly right, but it invites extra work |
| move | the content belongs in `PROVENANCE.md` or in a reference |
| delete | the content repeats a rule, or it changes no behaviour |
| add | no existing rule covers the behaviour without losing precision |

Do not add a section, a reference, or a checklist until you consider replace, narrow, move, and delete.

Answer these questions before an edit:

| Question | Required answer |
| --- | --- |
| Which behaviour must change? | one concrete delta |
| Which existing rule can you narrow or replace? | the file and the section, or `none` with a reason |
| What can leave the runtime files? | the obsolete, the duplicate, the provenance, the maintenance text |
| Why must the new file exist? | a branch, a lookup, an automation, a template, or a validation need |

Run the pass again after the edit:

1. Read the changed files as a user of the skill.
2. Remove or narrow each rule that the change made redundant.
3. Move the provenance, the reasons, and the maintenance notes out of the runtime files.
4. Confirm that each added line changes a decision, an action, or a check.
5. Record the result as replaced, narrowed, moved, deleted, or added with a reason.

This is a judgment pass. Do not add a validator only to make it machine-checkable.

## Keep or cut

| Keep | Cut |
| --- | --- |
| the conventions of the project | the background that the agent already knows |
| a non-obvious trap | motivational filler |
| the exact command, schema, or template | a repeat of the same rule |
| branch logic and defaults | a long essay that a table replaces |
| one strong example | three weak examples of one point |
| a constraint that changes behaviour | a source note that belongs in `PROVENANCE.md` |

## Match the structure to the fragility

| Fragility | Preferred structure | Avoid |
| --- | --- | --- |
| high | exact steps, a strict template, a validation gate | open-ended guidance |
| medium | a short checklist and examples | a long reasoned prose |
| low | short goals and constraints | an overspecified playbook |

## Instruction shapes

| Need | Shape |
| --- | --- |
| choose a path | decision table |
| repeat a task | numbered checklist |
| enforce an output | template or schema |
| show a style | input and output example |
| diagnose a failure | symptom, cause, and fix matrix |
| state an exact fact | compact reference table |

## Runtime writing rules

1. The frontmatter starts on the first line.
2. `name` equals the directory name.
3. `description` holds the words that users type.
4. Keep the guidance imperative and compact.
5. Keep `SKILL.md` as the decision layer. Move the depth into references.
6. Keep the trigger language in `description`, and not in the body. The body runs after the trigger.
7. State the required output, and the order of its parts.

## Simplified Technical English

Write the skill body, the references, and the output in ASD-STE100 Simplified Technical English. A model parses this text with no human to resolve an ambiguity.

- Use short common words.
- Use the active voice. "The agent deletes the file."
- Use the simple tenses: the imperative, the simple present, the simple past, and the simple future.
- Write one instruction in one sentence.
- Keep the sentence under 20 words in a procedure, and under 25 words in a description.
- Do not use a semicolon. Write two sentences.
- Keep a noun cluster to 3 words or fewer.
- Keep the subject, the verb, and the article in the sentence.
- Use one name for one thing in the whole skill.
- Keep a hedge, such as "may" or "usually", or the text claims more than the source.
- Define a domain term once, when a reader outside the domain reads it.
- No marketing adjectives: "seamless", "robust", "powerful".

The rule covers prose only. It does not cover code, identifiers, or quoted source text.

## The reference architecture

`SKILL.md` is the router. Each reference is a leaf that answers one lookup question. `PROVENANCE.md` is the maintenance contract.

Test each reference with one sentence:

- "I need to decide X, so read <file>."
- "I need to do Y, so read <file>."
- "I need to diagnose Z, so read <file>."

When the sentence is "I need context" or "I need patterns", the file is too vague.

| Put it in | When it belongs there |
| --- | --- |
| `SKILL.md` | each run needs it |
| `references/` | only one branch needs it |
| `PROVENANCE.md` | it records the maintenance, the scope, or the evidence policy |

| Need | Reference shape |
| --- | --- |
| choose a path | decision guide |
| run a procedure | task guide |
| look up a fact | reference table |
| diagnose a failure | troubleshooting matrix |
| copy a quality | example set |
| judge the completeness | validation checklist |

Naming rules:

- Name the file for the question that it answers. Good: `execution-shapes.md`, `testing.md`. Bad: `notes.md`, `context.md`, `patterns.md`.
- Keep the references flat under `references/`. Use a subfolder only for evidence or an asset.

Split a reference when the content is needed only after a branch, when the section makes `SKILL.md` hard to scan, or when the file passes 100 lines and holds more than one lookup need.

Keep the content in `SKILL.md` when each run needs it, when it is short, or when a move would add a file read for no gain.

Final checks:

1. `SKILL.md` gives a direct "open when" reason for each reference.
2. The file name tells the agent why to open it.
3. No required instruction hides in an optional reference.
4. No reference became a second `SKILL.md`.

## Place the files

1. Treat the skill directory as the root of the bundled files.
2. Use `references/...`, `scripts/...`, and `assets/...` paths.
3. Reserve a repository path for a registration instruction only.
4. Follow the prior art of the workspace when it already sets a path form.
5. Do not use an absolute path of the host.

| File or directory | Use |
| --- | --- |
| `PROVENANCE.md` | the sources, the decisions, and the maintenance contract |
| `references/` | the optional depth, loaded by route |
| `references/evidence/` | the durable iteration examples |
| `scripts/` | the repeatable automation or the validation |
| `assets/` | the templates and the static files |
| `LICENSE` | the license text, when the license differs from the repository one |

Create a new reference only when it has a direct "open when" reason and a tightening of an existing reference cannot answer the need. Then add its router row in `SKILL.md`.

Do not create a catch-all file that mixes the workflow, the sources, the examples, and the validation results. Do not add a nested reference folder for runtime content.

### The class rules

| Skill class | Require |
| --- | --- |
| workflow-process | the preconditions, the ordered flow, the failure handling, and the safety boundaries |
| integration-documentation | the API surface, the options, 6 or more downstream use cases, 8 or more known issues with a workaround, and the version variance |
| skill-authoring | the provenance, the precision pass, a happy-path example, a secure variant, an anti-pattern with its correction, and the registration |

### The shape rules

| Shape | Require |
| --- | --- |
| router | the route criteria, a fallback, the output of each route, and a recovery path |
| script-backed workflow | the scripts, the arguments, the output, the failure behaviour, and a fallback |
| parallel or worker | the unit of work, the worker output schema, the merge rule, and the stop condition |
| asset or template | the routing of each asset, the placeholder guidance, and a validation checklist |
| argument-driven | the arguments, the behaviour with no argument, and the user-only use when the effect is large |

Do not accept abstract-only guidance when a concrete example is needed.

## Match the form to the failure

| Baseline failure | Right form | Wrong form |
| --- | --- | --- |
| knows the rule, skips it under pressure | a prohibition, a rationalisation table, and the red flags | a soft "prefer..." |
| complies, but the output has the wrong shape | a positive recipe: the parts of the output, in order | a list of "do not..." |
| leaves out a required element | a required slot in the template | a prose reminder near the template |
| behaves differently by condition | a conditional on something observable | one unconditional rule and an exemption clause |

No nuance clause. "Do not do X unless it matters" opens the negotiation again.

An exemption clause does not limit the scope. "This does not apply to a code block" still suppresses the code block.

## State the reason, and its strength

- Give one short sentence of reason. A rule with a reason is easier to apply to a new case.
- Do not use all-caps ALWAYS or NEVER. It reads as noise, and it ages badly.
- Keep `MUST` for a discipline rule only: a rule that holds against the pressure of a shortcut.
- Write each standing instruction for the whole task. A harness may compact the context and keep only the first part of the skill. Put the critical rules at the top.

## Structure rules

- Link each reference directly from `SKILL.md`, one level deep. An agent can read the first 100 lines of a file that it reaches through another reference, and miss the rest.
- Say whether to run a script or to read it: "Run `scripts/x.py`" and "See `scripts/x.py` for the algorithm".
- Use a relative path from the skill directory. A harness may give the model the path of the skill, so a relative path works. When a skill uses a directory variable of one harness, add the plain text "the directory that contains this SKILL.md" for the other harnesses.
- Do not use an `@file` link. One harness loads the file by force, and the others ignore the syntax.
- Use forward slashes in each path.

## Scripts

- Ship a script for deterministic work. A script behaves the same under each model.
- Handle the error in the script. Comment each timeout and each retry constant.
- Call the script through its interpreter: `python3 scripts/x.py`. A copy step can remove the executable bit.
- List the packages that a script needs in `compatibility`, and in the body.
- Document each environment variable, and fail with a clear message when it is missing.
- Bundle the helper that each test run writes again.

## Structure troubleshooting

| Symptom | Fix |
| --- | --- |
| `SKILL.md` passes 500 lines and reads as an encyclopedia | move the detail into focused references |
| each edit adds a rule, and no edit removes one | run the precision pass before and after the edit |
| the description is too vague to match | add the words that users type |
| the trigger guidance sits in the body | move it into `description` |
| the skill repeats the conventions of the repository | point at the instructions file, and keep the domain behaviour |
| the skill tells the agent to read each reference at the start | add a decision table, and load a reference on demand |
| a long reference is easy to misuse | add a contents list, or split the file by lookup need |
| the directory holds notes for the user | keep `SKILL.md`, `PROVENANCE.md`, `references/`, `scripts/`, `assets/`, and `LICENSE` only |
| `SKILL.md` names a script with no interface | document the arguments, the output, and the fallback |
| the skill embeds an absolute path | use a skill-root-relative path |
| the description says "I can..." or "You can..." | write the third person |
| the skill bakes in a date or a transition | label it as deprecated, or remove it |
| an advanced shape has no reason | name the shape, the rejected simpler shapes, and the portability note |
| a router has no default | add a safe default, or one clarifying question |
| a loop says "repeat until it is good" | add a rubric and a maximum count |
| a reference exists and `SKILL.md` never names it | add a router row, or remove the file |
| a file groups unrelated techniques under a vague name | split it by lookup need, and rename each leaf |

## Output

- the updated `SKILL.md`
- the updated `PROVENANCE.md` when the contract changed
- each added or changed supporting file
- the precision result: replaced, narrowed, moved, deleted, or added with a reason
- the large authoring decisions
- the handoff to the description step
