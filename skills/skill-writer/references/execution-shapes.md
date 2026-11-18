<!-- Derived from getsentry/skills skills/skill-writer @ a582c51 (Apache-2.0); modified. -->

# Execution shapes

Use this file to choose the runtime shape of a skill before you decide its files. The default is the simplest shape that works. Add complexity only when it clearly improves the result.

## Contents

- [Start from the simplest shape](#start-from-the-simplest-shape)
- [Complexity budget](#complexity-budget)
- [Shape table](#shape-table)
- [Inline guidance](#inline-guidance)
- [Reference-backed expert](#reference-backed-expert)
- [Script-backed workflow](#script-backed-workflow)
- [Argument-driven](#argument-driven)
- [Asset or template](#asset-or-template)
- [Secondary workflow mechanics](#secondary-workflow-mechanics)
- [Parallel work](#parallel-work)
- [Orchestrator and workers](#orchestrator-and-workers)
- [Validation loops](#validation-loops)
- [Plan, validate, execute](#plan-validate-execute)
- [Hybrid shapes](#hybrid-shapes)
- [Hard stops](#hard-stops)

## Start from the simplest shape

Ask these questions in order. Take the first shape that fits.

1. Can one set of instructions answer most requests? Use inline guidance.
2. Is the main complexity optional knowledge, and not control flow? Use a reference-backed expert.
3. Is the hard part data extraction, validation, or repeatable automation? Use a script-backed workflow.
4. Does the user usually start the skill with explicit parameters? Add an argument-driven shape.
5. Only then consider routing, parallel work, worker delegation, or templates.

Do not take an advanced shape because it sounds powerful. Name the simpler shapes that you rejected, and say why.

## Complexity budget

Complexity must remove ambiguity. It must not add ceremony.

| Addition | Require |
| --- | --- |
| a new reference | a lookup need that the existing files cannot answer |
| a new script | a repeated operation that plain instructions do badly |
| a new route | inputs that need different tools, references, or output |
| a harness-specific mechanic | a capability that portable guidance cannot provide |

When the only benefit is "more thorough", keep the simple shape and tighten the existing instructions.

## Shape table

| Shape | Use when | File layout |
| --- | --- | --- |
| inline guidance | one policy, checklist, or procedure is enough | `SKILL.md` only |
| reference-backed expert | optional deep knowledge is the main complexity | `references/` |
| script-backed workflow | parsing, validation, or transformations are fragile in prose | `scripts/` |
| argument-driven | the user supplies issue numbers, paths, targets, or modes | `SKILL.md` plus the fields it needs |
| router | distinct categories need different prompts, tools, or references | `references/` plus a route table |
| parallel work | independent subtasks, or several votes, improve the result | work units and a merge rule |
| orchestrator and workers | the agent finds the subtasks at runtime | a worker contract and a stop rule |
| asset or template | templates, schemas, or static files carry the value | `assets/` |

If the chosen shape also needs explicit arguments or shell preprocessing, give a fallback for each harness that has neither.

## Inline guidance

Use it when the skill has one dominant path, each run needs the same instructions, and deep optional knowledge is not the problem.

```text
my-skill/
└── SKILL.md
```

Required:

1. Keep the body small enough to scan in one read.
2. Put all universal steps in `SKILL.md`.
3. Add a reference only when a real branch or lookup need appears.

Do not use it when most runs need a subset of a large knowledge base, when a script carries runtime behaviour, or when routing is central.

## Reference-backed expert

Use it when the skill needs deep knowledge, but most runs need one part of it.

```text
my-skill/
├── SKILL.md
└── references/
    ├── focused-topic-a.md
    ├── focused-topic-b.md
    └── troubleshooting.md
```

Required:

1. `SKILL.md` says when to open each reference.
2. The file name predicts the contents.
3. No reference mixes routing, troubleshooting, examples, and source notes.
4. A large reference has a contents list, or is split.
5. The files stay flat under `references/`, unless the content is evidence or an asset.

Do not use it when the skill is small enough to stay inline, or when the references would be vague topic buckets.

## Script-backed workflow

Use it when parsing, validation, or a repeated transformation is fragile in prose.

```text
my-skill/
├── SKILL.md
└── scripts/
    ├── fetch.py
    └── validate.py
```

Required:

1. `SKILL.md` names each script, with its arguments, its output, and its fallback.
2. The script does not ask questions.
3. The output is structured when practical.
4. The skill says what to do when a script fails or is missing.

Do not use it when one shell command is enough.

## Argument-driven

Use it when the user starts the skill with a number, a path, a mode, or a target.

Required:

1. Document the expected arguments, and the behaviour with no argument.
2. Make the skill user-only when the side effects are large.
3. Add a portability note when the argument syntax is harness-specific.

## Asset or template

Use it when the skill fills in a template or a schema, and the procedure is small compared to the asset.

```text
my-skill/
├── SKILL.md
└── assets/
    ├── template.md
    └── schema.json
```

Required:

1. `SKILL.md` says when to load each asset.
2. The skill explains how to fill each placeholder.
3. A filled-in output can drift silently: add a validation checklist.

Do not use it when the template is small enough to stay inline.

## Secondary workflow mechanics

These are not usually the primary shape. They often refine one.

### Prompt chaining

Use it when the decomposition is known in advance and the step order matters.

Required: the step order, the input and output of each step, and the gate between steps.

```markdown
1. Summarize the current state
2. Propose the target state
3. Validate the proposal against the constraints
4. Write the final document
```

### Routing

Use it when the request must go to different prompts, references, scripts, or tools.

Required: the route criteria, a default route or a clarification step, a recovery path for a wrong route, and the output contract of each route.

```markdown
1. Classify the request:

   **Billing question?** -> Load `references/billing.md`
   **Refund request?** -> Run `scripts/refund_intake.py`
   **Technical bug?** -> Load `references/triage.md`

2. If the classification is uncertain, ask one question before you continue.
```

### Parallel work

Use it when the work units are independent, or when several judgments improve the confidence.

Required: the unit of work, the merge or vote rule, the conflict rule, and the cost or latency cap.

The two common forms are sectioning (split the task) and voting (aggregate several judgments). Dispatch a subagent for each unit when the harness has one. If no subagent tool is available, do the steps in sequence.

### Orchestrator and workers

Use it when the agent must find the work units at runtime.

Required: the worker task schema, the worker output schema, an expansion limit, and the final synthesis rule.

```markdown
1. Inspect the request, and identify the work units
2. Dispatch a subagent for each work unit
3. Collect the worker summaries in a fixed schema
4. Synthesize the result
```

If no subagent tool is available, do the steps in sequence.

### Validation loops

Use it when a validator catches errors before the skill claims completion.

Required: the check, when it runs, what to fix before the retry, and the passing state.

```markdown
1. Make the change
2. Validate immediately
3. If the validation fails, fix the issue
4. Validate again
5. Continue only when the validation passes
```

Give every loop a cap. "Repeat until it is good" has no stop condition.

### Plan, validate, execute

Use it when a destructive or high-stakes action needs a machine-checkable plan.

Required: the plan artifact and its schema, the validation step and its source of truth, the rework rule, and the final verification.

```markdown
1. Analyze the input, and generate `changes.json`
2. Validate the plan against the source of truth
3. Revise until the validation passes
4. Execute the plan
5. Verify the result
```

## Hybrid shapes

Use a hybrid only when one primary shape is not sufficient.

1. Declare one primary shape.
2. Add the minimum number of secondary shapes.
3. Keep each secondary shape on one concrete need.
4. Remove the older guidance that the secondary shape replaces.

## Hard stops

Do not finish a skill when one of these is true:

1. The shape is implied but not named.
2. A simpler shape was not considered.
3. A router has no fallback or default path.
4. A loop has no stop condition.
5. A harness-specific mechanic has no fallback and no portability note.
6. Workers are dispatched with no output schema.
