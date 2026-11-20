## Builder contract

Build one stage of this plan in one run, then stop. The user or the flow names the stage.

1. Build only the named stage. Do not start the next stage.
2. Change only the files in the Scope of the stage. When the work needs another file, stop and ask.
3. Add only the tests in Tests to add of the stage.
4. Change only the existing tests in Existing tests permitted to change of the stage. When the work needs another one, stop and ask.
5. Leave the tree green at the end of the stage. Never report the stage as done with a failing gate. Never defer a failure.

Report `status: failed`, and name each cause under Deviations, when any of these occur:

- The verification gate fails twice for the same root cause.
- The work would exceed the Budget of the stage.
- A gate command is missing or labeled `(unconfirmed)`.
- A blocking ticket in Current state, or a stage in Depends on, has not landed.

## Report

Reply in this shape:

```markdown
status: done|failed, stage: <N>

### Changes

Each changed file. Give each changed existing test expectation its own line, with a one-line justification.

### Deviations

Each cause of a failed status, and each departure from the plan, or None.
```
