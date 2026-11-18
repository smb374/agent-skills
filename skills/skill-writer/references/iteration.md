<!-- Derived from getsentry/skills skills/skill-writer @ a582c51 (Apache-2.0); modified. -->

# Iteration

Use this file when the request holds examples, review feedback, validation results, or observed failures. Iteration turns each example into one change of behaviour.

## Contents

- [When to iterate](#when-to-iterate)
- [Step 1: Capture the examples](#step-1-capture-the-examples)
- [Step 2: Replay and review](#step-2-replay-and-review)
- [Step 3: Improve the skill](#step-3-improve-the-skill)
- [Store durable evidence](#store-durable-evidence)
- [Promote the evidence](#promote-the-evidence)
- [Output](#output)

## When to iterate

Iterate when the user supplies positive examples, negative examples, review feedback, or the output of a test run. Skip iteration when the request holds no example.

A positive example protects a behaviour that must not regress. A negative example shows the smallest failing decision: a wrong trigger, a missing source type, a skipped reference, an overloaded instruction, a weak output contract, a missing validation step, or an unsafe path assumption.

## Step 1: Capture the examples

Use one record for each example. Redact secrets, customer data, private URLs, and user content that the reproduction does not need.

```markdown
## EX-001: Short label

- Label: positive | negative
- Kind: true-positive | false-positive | false-negative | fix | regression | edge-case
- Origin: human-verified | mixed | synthetic
- Source: the issue, pull request, commit, log, note, or validation result
- Status: working | holdout | resolved | deferred
- Expected behaviour: one sentence
- Observed behaviour: one sentence
- Skill delta: the instruction, reference, description, or validation change
- Anonymization: what you removed or generalized
```

Then add the example content, summarized or redacted.

## Step 2: Replay and review

1. Review the behaviour against the working set.
2. Review the behaviour against the holdout set.
3. Record each outcome as improved, unchanged, or regressed.
4. Confirm that the positive behaviour and the negative behaviour moved in the direction that you expected.

Do not tune the skill against the holdout set. The holdout set stays unseen until the end, unless the user moves an example into the working set.

## Step 3: Improve the skill

1. Fix the repeated negative pattern first.
2. Keep the behaviour that succeeds on the positive examples.
3. Update the transformed examples when you change the guidance.
4. Record each delta in the local changes section of `PROVENANCE.md`.
5. Collect more examples when a failure shows a coverage gap.
6. Keep the holdout examples apart from the working examples until the validation is complete.
7. Update `PROVENANCE.md` when the iteration changes the scope, the evidence model, the validation, or the known limits.

## Store durable evidence

Keep an example in `references/evidence/` of the target skill only when it must outlive the current task. For a one-off fix, summarize the example in `PROVENANCE.md` instead.

```text
references/evidence/
├── findings-log.md
├── working-set.md
└── holdout-set.md
```

- `findings-log.md` holds the interpreted findings: the repeated failures, the successes to protect, the suspected causes, the changes that answer them, and the unresolved risks.
- `working-set.md` holds the examples that you use while you edit the skill.
- `holdout-set.md` holds the examples that wait for the validation after the edit.

## Promote the evidence

Move an example into the skill files only when it changes future behaviour.

- A universal rule goes in `SKILL.md`.
- A domain example goes in one focused reference.
- A raw or semi-raw example stays in `references/evidence/`.

Do not turn `references/evidence/` into a changelog. The changes go in `PROVENANCE.md`.

## Output

- the example intake summary
- the deltas of behaviour
- the updated files
- the replay summary
