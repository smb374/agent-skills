<!-- Derived from getsentry/skills skills/skill-writer @ a582c51 (Apache-2.0); modified. -->

# Synthesis

Use this file for a new skill, for a material change to one, or for research-first planning. Synthesis answers one question before authoring: which sources must shape this skill, and which gaps stay open.

## Contents

- [When to synthesize](#when-to-synthesize)
- [Step 1: Classify the skill](#step-1-classify-the-skill)
- [Step 2: Collect the sources](#step-2-collect-the-sources)
- [Step 3: Adapt the upstream material](#step-3-adapt-the-upstream-material)
- [Step 4: Record the decisions](#step-4-record-the-decisions)
- [Step 5: Check the coverage](#step-5-check-the-coverage)
- [Output](#output)

## When to synthesize

Synthesize for a new skill, for a material change to one, or for research-first planning. For a wording-only fix, skip it and record the change in `PROVENANCE.md`.

Keep the notes short. Use tables, status lists, and gap lists. Do not write a narrative summary.

## Step 1: Classify the skill

Record the parts that change behaviour or maintenance: the skill class, the primary execution shape, each secondary shape, and why the simpler shapes were not enough.

| Skill class | Typical request | Required dimensions |
| --- | --- | --- |
| workflow-process | repeatable operations, CI or task orchestration | preconditions, ordered flow, failure handling, safety boundaries |
| integration-documentation | library or framework integration, SDK usage, API correctness | API surface, options, common use cases, known issues with workarounds, version variance |
| skill-authoring | creating or updating other skills | source provenance, precision pass, transformed examples, registration and validation |
| generic | no match | the dimensions that you name, with a reason |

When the class is ambiguous, ask one question before synthesis.

## Step 2: Collect the sources

Prefer the sources in this order:

1. Local authority: the instructions file, `README.md`, the manifests, the validators, the scripts, the tests, and the neighbouring skills.
2. Primary upstream material: specifications, product documentation, API references, release notes, and source code.
3. Operational evidence: issue threads, pull request discussions, CI failures, incident notes, and migration notes.
4. Historical evidence: commit logs, blame, reverted changes, and changelog diffs.
5. Secondary summaries: blog posts, tutorials, and community examples.

Treat a secondary source, and any generated text, as a lead. Do not treat it as authority.

### Retrieval passes

Run the passes that match the risk of the skill.

| Pass | Retrieve |
| --- | --- |
| core behaviour | the happy path and the main workflow |
| edge behaviour | failures, retries, permissions, validation, and cleanup |
| negative behaviour | bug fixes, reverted commits, issue reports, review comments, skipped tests |
| usage behaviour | callers, downstream examples, configuration samples, migration guides |
| maintenance behaviour | changelogs, deprecations, and the files that change most often |
| shape mechanics | routes, delegation, loop stops, and the harness constraints |

### Commit logs

Use the commit history when the behaviour that matters is the behaviour that happened, and not the behaviour that the design intended.

```bash
git log --oneline -- <path>
git log --stat -- <path>
git log -G '<behaviour|symbol|error>' -- <path>
git blame <path>
```

Keep the commit SHA, the date, the path, the observed behaviour, and the decision for each finding. Do not copy a long commit message or a diff into `SKILL.md`.

### Stop conditions

Stop collecting a source when all of these are true:

- Each required dimension is complete, or it has an explicit next retrieval action.
- A new source repeats the facts that you have.
- The open questions are low impact, or they need access that you do not have.
- A high-risk workflow has both the intended behaviour and the observed behaviour.

Record the reason why you stopped.

## Step 3: Adapt the upstream material

Use this step when an upstream prompt, workflow, rubric, benchmark, guide, or documentation set is a primary input.

| Decision | Record |
| --- | --- |
| source intent | the behaviour that the source tries to cause |
| local target | the behaviour that the new skill must cause here |
| fidelity boundary | what must stay equivalent to the source |
| local replacement | what you rewrite to match the local conventions |
| omitted material | what you did not carry over, and why |
| provenance | the URL or path, the version or commit, the trust tier, and the confidence |
| rights | the license, the notice, the attribution, or the excerpt limit |

Rewrite rules:

1. Do not copy the section structure of the source unless it improves the runtime behaviour.
2. Turn narrative instructions into decisions, checklists, examples, or output contracts.
3. Replace the tool names, the paths, the severity labels, and the provider assumptions of the source with the local equivalents.
4. Keep the provenance, the rights, the versions, and the fidelity trade-offs in `PROVENANCE.md`.
5. Keep only the instructions that help the agent decide, act, or verify at runtime.
6. When you preserve benchmark behaviour, state the invariant and do not tune the skill to the expected answers.

Answer these questions before you author. When an answer is weak, tighten an existing file instead of adding guidance.

1. Which existing rule must a source rule replace?
2. Which source rule is too broad, stale, provider-specific, or not about runtime?
3. Which added instruction prevents a concrete mistake that the current guidance does not cover?
4. Which source detail belongs in `PROVENANCE.md`, or in one focused reference, and not in `SKILL.md`?

## Step 4: Record the decisions

Map each large decision to its evidence: the class, the shape, each harness-specific mechanic, and each deferred gap.

Use one status for each decision:

- `adopted`: the source shapes the skill.
- `rejected`: the source does not fit, and the reason is recorded.
- `deferred`: the decision waits for evidence that is missing.

## Step 5: Check the coverage

Address each item before authoring, or report it as an explicit gap.

1. No high-impact dimension is missing.
2. A partial dimension has a next retrieval action.
3. A skill-authoring skill has transformed examples.
4. The requirements of the selected shape are satisfied.
5. The coverage passes appear in the coverage table.
6. The reason to stop collecting is explicit.
7. Each reference is focused, and `SKILL.md` lists it.
8. `PROVENANCE.md` exists, or this change updates it.
9. An advanced mechanic has its contract and its justification.
10. A harness-specific mechanic has a portability note.

## Output

Write the result into `PROVENANCE.md` of the target skill.

- the source inventory, with a trust tier for each source
- the class and the execution shape
- the decisions, with the status of each one
- the coverage table
- the gaps and the next retrieval action for each one
- the adaptation notes, when an upstream source shapes the skill
- the reason why you stopped collecting
