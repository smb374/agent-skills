---
name: to-impl-plan
description: Turns one ticket into an implementation plan for builder runs, with cited behavior, named tests, a file scope, and a budget in each stage. A plan has one or more stages, and each stage fits one builder run. It also holds the checks to review a plan that it wrote. Use when the user asks for an implementation plan or a plan review, when a ticket is too big for one builder session, or when a builder went wrong on a ticket. To split a spec into tickets, use to-tickets. To hand off a session, use handoff.
compatibility: scripts/fill.py needs Python 3.10 or later. The install script of smb374/agent-skills adds it.
---

# To implementation plan

Turn **one ticket** into an **implementation plan** with one or more **stages**. A builder agent builds one stage in one run, in a fresh context. The builder can be a weaker model than you, and it cannot derive missing behavior. Write everything that it needs into the plan.

Start this skill only when the user asks for it, or when a step of a flow that the user started asks for it. Do not start it on your own, because the user decides how the work is built.

In this file, `<skill>` is the directory that contains this SKILL.md.

## Core principles

1. **Stop and report.** Stopping and reporting is always a correct outcome. Inventing behavior, sequences, or expected values is not.
2. **Literal verification.** Every gate is checkable by comparison with a concrete artifact in the plan. Never write "behavior remains correct", "semantics are preserved", or "traces remain exact".
3. **One ticket, one plan, one or more stages.** Each stage fits the budget of one builder run. Use one stage when the ticket fits one run, for example after a builder that took the ticket directly went wrong. Use more stages when the ticket is too big for one run. When the ticket holds more than one feature that a user can use alone, stop, and tell the user to split it with `/to-tickets`. A stage that only adds a module for a later stage is not such a feature.
4. **Green tree after each stage.** Never defer a failure to a later stage.

## Process

### 1. Gather

1. Fetch the ticket. The user or the flow gives a path or an issue number. For an issue number, use `docs/agents/issue-tracker.md`. When that file is missing, tell the user to run `/setup-project`. Read the body of the ticket, its comments, and its parent spec.
2. Read the `AGENTS.md` of the project and every standards file that it names. Take the ticket-sizing budget and the forms of the verification artifacts from them.
3. Read `GLOSSARY.md` and the ADRs in the area that the ticket touches, when they exist. Use the glossary terms.
4. When a builder already went wrong on the ticket, read its report or its diff. Record what went wrong in Current state.

### 2. Intake

Establish each item below, or record the gap under **Open questions**. Write only what you can complete without guessing.

1. **The code that exists.** Read the files that the ticket touches. Name only paths that you confirmed exist. Mark a path for a file that does not exist yet as `(new)`.
2. **The real verification commands.**
   - Read them from the build config, the CI definition, or the documented instructions of the project. Record the literal command lines.
   - A command that you derived from the toolchain, and did not read from the project, is _unconfirmed_. Label it `(unconfirmed)`, and list it under **Open questions**.
   - Two kinds of derived command are confirmed: a documented command narrowed to a subset of tests, such as one test module, and a read-only `git` command, such as `git status --short`.
   - A gate command must not change the working tree. Use a check mode (`--check`, `--dry-run`, `-l`). A formatter in write mode cannot fail, so it verifies nothing.
3. **The test conventions.** Find where tests live, how they are named, and which harness and assertion style the project uses.
4. **The acceptance criteria.** Take them from the ticket. Rewrite each vague criterion as a literal, or list it under **Open questions**.
5. **The authoritative references.** Find the specs, reference code, or documents that constrain the behavior. Cite each one with a file and a line range or a section.

A plan with open questions is a valid outcome. A plan with guessed paths or unlabeled unconfirmed commands is not.

Completion criterion: each of the five items is established or listed under **Open questions**.

### 3. Agree the stages, seams, and tests

Propose the stages, the seams under test, and the named tests in each stage, with a one-line summary of the artifact of each test. Ask the user, or the flow that started this skill, to confirm them. When you have no tool to ask, end your turn with the proposal.

Naming tests up front is not horizontal slicing. The builder still writes them one red → green slice at a time, in the order of the Action items. The expected values come from cited references, not from imagined behavior.

Completion criterion: the user or the flow confirmed the stages, the seams, and the tests.

### 4. Write the plan

1. Name the plan `plan-<ticket-id>`. `<ticket-id>` is the ID of the tracker: the local `NN` or the issue number. Write all files to the temporary directory of the OS, not to the workspace. Get its path `<tmp>` with `python3 -c "import tempfile; print(tempfile.gettempdir())"`. This command reads `TMPDIR`, `TEMP`, and `TMP`, so do not pick a directory yourself.
2. Run `<skill>/scripts/fill.py --fields <skill>/assets/plan.md <tmp>/<name>.values.json`. It writes a values file with each key set to `null`. It prints each key with its type and a hint.
3. Replace each `null` in the values file. Use a non-empty string for a `string`, and an array of non-empty strings for a `list`. Use `[]` only when the template prints `None` for an empty list.
4. Write each item of `stages` in the shape of **Stage shape** below.
5. Run `<skill>/scripts/fill.py <skill>/assets/plan.md <tmp>/<name>.values.json <tmp>/<name>.md`.
6. When `fill` exits 1, it writes nothing and lists each problem. Fix each problem in the values file, then do step 5 again. When the plan exists from an earlier run, delete it, then do step 5 again.

When `<skill>/scripts/fill.py` does not exist, the skill was not installed with its install script. Tell the user, and stop.

Completion criterion: `fill` exited 0, every stage has all subsections of **Stage shape**, and every test name under **Tests to add** has a matching artifact under **Behavior specification**.

### 5. Give the path

Give the path of the plan to the user or to the flow. Tell the user to start each builder run in a fresh context with the plan path and one stage number, in stage order.

## Review a plan

To review a plan that this skill wrote, read `references/plan-review.md`.

## Stage shape

Write each stage as one Markdown string with these headings, in this order:

```markdown
### Stage <N>: <name>

#### Depends on

The stages that must land first, or `None`.

#### Scope

The exact list of files to create or change, each marked `(new)` or `(modified)`. No other file may change.

#### Tests to add

The named tests, in build order. Each name has a matching artifact under Behavior specification. A name without a fixture behind it asks the builder to invent one: write the expected values, or drop the test.

#### Existing tests permitted to change

An explicit list, or `None`. Never write "update affected tests". For each test, write the artifact that it asserts after this stage, with its citation and a one-line justification.

#### Budget

- Maximum files touched
- Number of new tests
- Maximum modified existing tests

#### Action items

Ordered, concrete steps that the builder can follow without invention. Order them as red → green slices: one test, then the minimum code that makes it pass.

#### Verification gate

- "All common verification commands exit 0." Do not restate the command lines. Write any additional command here in full. An additional command is a common verification command narrowed to a subset of tests, or a read-only `git` command. Write any other check as a test under Tests to add.
- The pass conditions, each as a literal that a reviewer can compare: an exit status, an expected count, or an exact output line.
```

Take the Budget limits from the ticket-sizing rules of the project.

## Verification artifacts

Use the artifact forms of the project when its standards name them. Otherwise, pick the form that fits the work. Write the artifact in full, so a reviewer checks by comparison, not by deriving correctness again.

| Kind of work                 | Artifact                                                                                            |
| ---------------------------- | --------------------------------------------------------------------------------------------------- |
| State machines and protocols | A step-by-step sequence, or a table of states and transitions                                       |
| APIs and functions           | Exact inputs → exact expected outputs and side effects                                              |
| UI and UX                    | Concrete before and after observations, or acceptance checks                                        |
| Data and persistence         | The schema plus example rows, or the migration outcome                                              |
| Timing and ordering          | An ordered timeline, or a table keyed by step or event                                              |
| Refactors                    | The exact test names and their current expected artifacts, written in full, plus each new invariant |
| Everything else              | Named exact inputs and exact expected outputs                                                       |

## Output style

Write for a weaker model that implements exactly what is written, and no more.

- Write one instruction per sentence.
- Use one term per concept. Take the term from `GLOSSARY.md` or the code, and reuse it every time. A synonym reads as a second concept.
- Use the imperative and the active voice: "Return an error when a successor exists."
- Replace each vague quantifier (`several`, `various`, `as appropriate`, `if needed`, `etc.`) with the list or the number.
- Make every pronoun refer to the nearest noun before it. If it cannot, repeat the noun.
- Use literal identifiers: real type names, function names, file paths, and command lines.
