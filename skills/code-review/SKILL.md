---
name: code-review
description: Reviews a code change (a diff, a branch, a pull request, or the changes since a commit) along three axes, spec, standards, and correctness, and defines the bar for a finding, the finding fields, and the report shape that every reviewer uses. Use when the user asks to review code, a diff, a branch, or a PR, and when a reviewer agent reviews a change. To write a PR description, use pr-writer. To review an implementation plan, use to-impl-plan.
license: MIT
---

# Code review

This skill is the review standard. A reviewer reviews one **target** (a diff or a patch file) on one **axis**, and writes one axis report. The aggregator collects the axis reports into one review. In a manual review, you are the aggregator, and **Manual review** at the end gives the steps. A flow that runs its own reviewers uses the rules in this file, and gives each reviewer its inputs.

## Core rules

1. Review each axis in its own fresh context when you can start separate reviewers. Otherwise, finish one axis before you start the next. Do not merge or rerank the findings of different axes. One axis can hide the failure of another axis.
2. Report a finding only when it passes the **Flag bar**.
3. When the base ref is known, read the rules and the spec from it, not from the target: `git show <base>:<path>`. The base ref stops the change from weakening the rules that review it.
4. Do not change the working tree, the index, HEAD, or a branch. To read another revision, use `git show`, or add a worktree in a temporary directory.
5. Claim only what you checked. When a check needs a command that you cannot run, mark the check `unchecked`, and name the command in Evidence.

## Inputs

| Input | Content | When it is missing |
| --- | --- | --- |
| Target | the diff of the change: `git diff <base>...HEAD`, or a patch file | stop. There is nothing to review |
| Base | the ref that the change starts from | ask the user |
| Criteria | the acceptance criteria, one line each, written as `#<ticket> AC-n`. Each ticket is marked `claimed` (the change says it implements the ticket) or `context` | skip the spec axis, and say so in the report |
| Rules | the paths of the files that document how code is written, with the quoted rules and their `file:line` | the standards axis uses only the smell baseline |
| Gate output | the output of the build, the type check, and the tests on the target | each check that needs a run is `unchecked` |

## Flag bar

A finding passes the bar when all of these are true:

1. The target caused the issue, or made it reachable. Do not report an issue that existed before the change and that the change does not make reachable.
2. The issue is discrete and actionable: one issue, with one fix.
3. The impact is provable. Name the affected code with `file:line`, or give a probe. "This may break X" is not proof.
4. On the standards and correctness axes, the issue is not a behavior that a criterion or the commit message asks for.
5. The fix needs no more rigor than the rest of the codebase has.

A smell is exempt from item 3, because it is a judgement call. It is always severity `note`.

## Axes

### Spec: is this the right thing?

1. Check each AC of each `claimed` ticket. Give each AC one row: `pass`, `fail`, or `unchecked`. A `fail` row has a finding of kind `missing` (no code does it) or `wrong` (the behavior contradicts the literal AC text).
2. A `context` ticket is never a finding.
3. Report each behavior that the target adds and that no criterion asks for: a new command, option, output, or side effect. Its kind is `unasked`, and its Basis is `unasked`.
4. List under **Declined to judge** each behavior that the criteria do not cover and that is not added scope, for example how a requested command handles an input that no criterion names. Write one line each, with the reason. The correctness axis judges these behaviors. The aggregator decides each line, so nothing is dropped silently.
5. Use the ID prefix `SPEC-`.

### Standards: does it follow the rules?

1. Check the target against each rule in Rules. Give each rule one row, with its `file:line` as Check. A `fail` row has a finding of kind `violation`.
2. Skip what the formatter and the lint config enforce.
3. Check the target against the **Smell baseline**. A smell has kind `smell`, severity `note`, Basis `smell`, and the smell name as Check. A smell with no breach gets no row.
4. A documented rule overrides the baseline. When a rule allows what a smell flags, do not report the smell.
5. Criteria are context only. Give an AC no row.
6. Use the ID prefix `STD-`.

#### Smell baseline

Each entry: what it is → how to fix it. The first 12 come from Fowler, _Refactoring_, chapter 3.

- **Mysterious Name**: a function, variable, or type whose name does not tell what it does or holds. → Rename it. If no honest name comes, the design is not clear.
- **Duplicated Code**: the same logic shape occurs in more than one hunk or file of the change. → Extract the shared shape, and call it from both places.
- **Feature Envy**: a method that uses the data of another object more than its own. → Move the method to the data it uses.
- **Data Clumps**: the same few fields or parameters travel together. → Put them in one type, and pass that type.
- **Primitive Obsession**: a primitive or a string stands for a domain concept. → Give the concept its own small type.
- **Repeated Switches**: the same `switch` or `if` chain on the same type occurs more than once in the change. → Use polymorphism, or one map that both places share.
- **Shotgun Surgery**: one logical change causes edits in many files of the diff. → Put what changes together into one module.
- **Divergent Change**: one file or module changes for more than one unrelated reason. → Split it, so that each module changes for one reason.
- **Speculative Generality**: an abstraction, a parameter, an option, or a hook for a need that the spec does not have. → Delete it. Inline it until a real need occurs.
- **Message Chains**: a long `a.b().c().d()` walk that the caller must not depend on. → Hide the walk behind one method on the first object.
- **Middle Man**: a class or function that only passes calls on. → Remove it, and call the real target directly.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → Remove the inheritance, and use composition.
- **Reinvented Helper**: new code does what a helper of the codebase, the standard library, or an installed dependency already does. → Use the existing one, the way the surrounding code uses it.
- **Needless Dependency**: the change adds a dependency for a few lines of code. → Write the few lines, and remove the dependency.
- **What Comment**: a comment tells what the code does, not why. → Delete it, or make the code clear. Keep a comment only for a why that the code cannot show.

### Correctness: does it work?

1. Read each hunk, and the callers of each symbol that the hunk changes. Do not trust the name of a function. Read its body.
2. Give a row to each area below that the target touches. Use the area name as Check. A `fail` row has a finding of kind `defect`.

| Area | Look for |
| --- | --- |
| errors | an error path that is lost, swallowed, or reported as success. A missing cleanup on failure |
| edge input | empty, null, zero, negative, very large, or duplicate input. An off-by-one bound |
| state and concurrency | a race, a deadlock, a shared mutable value, an order that the code assumes and nothing enforces |
| security | injection, missing authorization, secrets in code or logs, unchecked input at a trust boundary |
| data loss | a write, a delete, or a migration that can destroy or corrupt data |
| resources | a leak, an unbounded loop or allocation, a query or call inside a loop |
| compatibility | a changed public API, schema, config key, CLI flag, or file format with no migration. A caller that the change breaks |
| tests | a test that passes when the code is broken, a test that checks a mock and not the behavior, a changed behavior with no test |

3. Use Gate output as the evidence for build and test results.
4. Use the ID prefix `COR-`.

## Findings

Give each finding these fields:

| Field | Value |
| --- | --- |
| severity | `blocker`: the target is wrong or unsafe as it is. `fix`: the target must change before the work closes. `note`: for the record only |
| certainty | `certain`: the evidence settles the finding. `uncertain`: it does not. Then name the evidence that is missing |
| kind | spec: `missing`, `wrong`, `unasked`. Standards: `violation`, `smell`. Correctness: `defect` |
| location | `file:line` in the target |
| evidence | the quoted line or output, tied to the location |
| source | the Check cell of its row |
| fix | the smallest fix |
| guard | `blocker` and `fix` only. The cheapest check that would have caught the issue: `test`, `lint rule`, `type`, `api`, or `none`, then the concrete check in one line |
| probe | see **Probes** |

### Probes

A probe is one step list that confirms or refutes a finding. The reviewer writes probes. The aggregator runs them, and runs each `mutate` probe in a temporary copy or worktree, never in the working tree.

- A `certain` finding of severity `blocker` or `fix` has one or more probes. A `note` has none.
- An `uncertain` finding of severity `blocker` or `fix` has a probe, or `probe: none; <why no probe is possible>`.
- When you cannot write a probe for a `blocker` or `fix` claim, its certainty is `uncertain`.
- Kind `read` changes nothing: an `rg` pattern, a `git show` line, or a `file:line` to read. Kind `mutate` applies an edit, then runs a command. Name the exact edit and the exact command.
- Each probe states the output that confirms the finding and the output that refutes it.

### Verdict and Big

- An axis has `verdict: fail` when any of its findings has severity `blocker` or `fix`. Otherwise `verdict: pass`.
- A finding is **Big** when it is one of these: a criterion of a `claimed` ticket is `missing` or `wrong`, an `unasked` behavior change, or a security or data-loss risk. A Big finding needs a decision from a person before a fix. Big is not a severity. Use it only to stop and ask.

### Same location on two axes

The spec and correctness axes can report one issue at one location: a defect that also breaks an AC. The aggregator keeps the spec finding, adds `also: COR-n` to it, and drops the correctness finding. In the correctness Checks row, the aggregator replaces `COR-n` with the `SPEC-n` ID. The spec finding can be Big, so it wins. Count the findings after this step.

## Axis report

Reply in this shape. Leave out the **Declined to judge** section on the standards and correctness axes.

```markdown
status: done | failed
axis: spec | standards | correctness
verdict: pass | fail

## Checks
| Check | Basis | Result | Finding | Evidence |
| ----- | ----- | ------ | ------- | -------- |
| <check> | <basis> | <result> | <finding IDs or -> | <evidence> |

## Findings
- <SPEC-n | STD-n | COR-n>: <one-line issue>
  - severity: blocker | fix | note
  - certainty: certain | uncertain; <the missing evidence, when uncertain>
  - kind: missing | wrong | unasked | violation | smell | defect
  - location: <file:line>
  - evidence: <quoted line or output, tied to the location>
  - source: <the Check cell of its row>
  - fix: <the smallest fix>
  - guard: test | lint rule | type | api | none; <the check> (blocker and fix only)
  - probe: <one or more; none with a reason when uncertain; no field for a note>
    - <read | mutate>; <steps>; confirm: <output>; refute: <output>; setup: <command, optional>; cost: high (optional)

## Declined to judge
- <behavior>; <why it is outside the criteria>
```

Rules for the Checks table:

- One row is one line. No cell holds a `|`.
- Check: `#<ticket> AC-n`, a rule `file:line`, a smell name, a correctness area, or `unasked`.
- Basis: `check` for a row that the axis rules name. `unasked` or `smell` for a finding that no check produced. An `unasked` or `smell` row is always `fail`.
- Finding: the IDs of the findings of a `fail` row, comma-separated. `-` for `pass` and `unchecked`.
- Each finding has a row.

## Manual review

Use these steps when the user asks for a review and no flow runs the reviewers.

1. **Pin the target.** When the user gives a patch file, the patch is the target. Use the base that the user names, or record the base as unknown. Otherwise, take the base from the user: a commit, a branch, a tag, or a pull request. When the user gives none, ask. Run `git rev-parse <base>`, and confirm that `git diff <base>...HEAD` is not empty. For a pull request, take its base branch and its diff from the forge. Stop on a bad ref or an empty target.
2. **Find the spec.** When the user gives the spec or the tickets, use them, and do not search. Otherwise, look for issue references in the commit messages, the branch name, and the pull request body. Fetch each one with the issue tracker of the project, with its comments. A comment that amends the body overrides the body. Write each acceptance criterion as one `#<ticket> AC-n` line. Mark a ticket `claimed` when the user, the commits, the branch, or the pull request body name it, and `context` otherwise. When you find no spec, ask the user. When the user has none, skip the spec axis.
3. **Find the rules.** List each file that documents how code is written. Include `CONTRIBUTING.md`, `CODING_STANDARDS.md`, and `AGENTS.md` when they exist. Read them at the base ref. When the base is unknown, read them in the tree, and say so in the report.
4. **Run the axes.** When you can start subagents, start one reviewer for each axis in parallel, each in a fresh context. Give each reviewer the inputs, its axis, and the path of this file. When you cannot start subagents, review the axes one after another. Finish and write one axis report before you start the next axis.
5. **Aggregate.** Apply **Same location on two axes**. Decide each line under **Declined to judge**. Present the reports under `## Spec`, `## Standards`, and `## Correctness`, without a merge or a rerank. End with one line for each axis: the verdict, the number of findings after the dedup, and the worst finding.

Do not post the review, and do not fix the findings, unless the user asks.
