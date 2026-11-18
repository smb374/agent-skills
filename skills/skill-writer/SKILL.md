---
name: skill-writer
description: Creates, updates, and improves agent skills that follow the Agent Skills specification. Use when asked to create a skill, write a skill, update a skill, improve a skill, synthesize sources into a skill, or fix a skill that does not trigger or that gives weak results. For AGENTS.md, CLAUDE.md, agent briefs, system prompts, and tool descriptions, use writing-agent-docs.
license: Apache-2.0
compatibility: scripts/quick_validate.py needs Python 3.12 or later with the PyYAML package.
---

<!-- Derived from getsentry/skills skills/skill-writer @ a582c51 (Apache-2.0); modified. -->

# Skill writer

Use this skill to create one agent skill, or to change one that exists. Success has two parts: the skill changes what an agent does, and it costs less context than the behaviour that it replaces.

Follow the seven steps in order. Open a reference only for the step that you are on.

## Router

| Open when you need to... | Read |
| --- | --- |
| choose the simplest execution shape, or the file layout for it | `references/execution-shapes.md` |
| collect sources, adapt upstream material, and record the decisions | `references/synthesis.md` |
| improve the skill from positive or negative examples | `references/iteration.md` |
| write the body, place the files, and shape the output | `references/writing-rules.md` |
| write or repair the description and the skill name | `references/descriptions.md` |
| make the skill work in more than one harness | `references/portability.md` |
| test the skill, and keep it correct after release | `references/testing.md` |
| fill `PROVENANCE.md` for the target skill | `references/provenance-template.md` |
| check the structure of the target skill | run `scripts/quick_validate.py` |

## Step 1: Resolve the operation, the directory, and the shape

1. Prove the gap. Run 2 or 3 real prompts without the new skill. Write down what goes wrong. If the agent does the job, write no skill.
2. Decide what the request needs:

| The need is | Put it in |
| --- | --- |
| a reusable procedure or domain knowledge, needed sometimes | a skill |
| a project convention for every task in the repo | the instructions file of the harness, such as `AGENTS.md` or `CLAUDE.md` |
| a constraint that a regex, a path, or a command can check | a hook, a permission rule, or an extension |
| a rule that must hold on every turn | a hook or a permission rule |
| a one-off fix | nothing. A skill is not the record of one repair |

3. Name the operation: create, update, synthesize, or iterate.
4. Choose the target directory. Inspect the prior art of the workspace first: the neighbouring skills, the instructions file, and the repo scripts. Use the location that the workspace already uses. When the workspace has no prior art, use `.agents/skills/<name>/`. When more than one location fits, ask the user one question before you write a file.
5. Choose the execution shape with `references/execution-shapes.md`.
6. Decide what this change replaces, narrows, or deletes. A skill that only gains text grows without limit.
7. When the skill must work outside one harness, read `references/portability.md` before you write the body.

## Step 2: Synthesize the sources

Read `references/synthesis.md` for a new skill, for a material change, or for research-first planning.

1. Classify the skill, and choose its execution shape.
2. Collect the sources, with a trust tier for each one.
3. Adapt the upstream material that shapes the skill.
4. Record each decision as adopted, rejected, or deferred.
5. Report the gaps. Do not start authoring until each gap is explicit.

## Step 3: Iterate from examples

Read `references/iteration.md` when the request holds examples, review feedback, or observed failures. Skip this step when the request holds no examples.

1. Capture each example with its label, kind, and origin.
2. Compare the behaviour against the working set and the holdout set.
3. Record each delta as improved, unchanged, or regressed.
4. Keep a durable example in `references/evidence/` of the target skill.

## Step 4: Author the files

Read `references/writing-rules.md`.

1. Run the precision pass before you add a section, a file, or a rule.
2. Keep `SKILL.md` as the router. Move optional depth into `references/`.
3. Write the body in Simplified Technical English: short common words, active voice, simple tenses, one instruction per sentence.
4. Add a bundled file only when it has a direct "open when" reason, and then list it in `SKILL.md`.
5. Create `PROVENANCE.md` from `references/provenance-template.md`.
6. Run the post-change pass, and record its result as replaced, narrowed, moved, deleted, or added with a reason.

## Step 5: Write the description

Read `references/descriptions.md`.

1. Write the description in the third person: what the skill does, and when to use it.
2. Keep the trigger phrases in the words that users type.
3. Name the sibling skill for the near-miss case.
4. Check the name against the specification pattern, and keep it equal to the directory name.

## Step 6: Test the skill

Read `references/testing.md`.

1. Run the baseline prompts again with the skill.
2. Run the trigger check, with should-trigger and near-miss queries.
3. Test each harness and model that you support.
4. Read the transcripts. Fix the wasted steps and the sections that the agent never opens.

## Step 7: Validate and register

1. Run `python3 scripts/quick_validate.py <skill-directory>` from the skill-writer directory.
2. Fix each error. Read each warning, and decide it with judgment.
3. Confirm that `SKILL.md` lists each bundled file.
4. Apply the registration steps that the workspace requires: a catalog table, a settings file, or an allowlist.
5. Report the open gaps.

## Pre-commit checklist

Portability
- [ ] `name` equals the directory name and matches `^[a-z0-9]+(-[a-z0-9]+)*$`. The description is at most 1,024 characters.
- [ ] Only `name`, `description`, `license`, `compatibility`, and `metadata` are needed for the skill to work. Each other field degrades safely.
- [ ] The body names actions, not tools. A fallback exists for a subagent and for a todo list.
- [ ] The paths are relative to the skill directory. The body has no harness-specific path variable, argument substitution, or shell preprocessing.
- [ ] `compatibility` states the runtime needs.

Trigger
- [ ] A baseline run without the skill showed a real gap.
- [ ] The description is in the third person, and it says what the skill does and when to use it.
- [ ] The description names the near-miss sibling skill.
- [ ] A skill with side effects is user-only.

Body
- [ ] `SKILL.md` is under 500 lines. The references are one level deep. Each reference over 100 lines starts with a contents list.
- [ ] The critical rules are at the top.
- [ ] The form of each rule matches the failure that you saw. There is no nuance clause and no exemption clause.
- [ ] Each rule gives one short sentence of why. `MUST` appears only in a discipline rule.

Testing
- [ ] You ran 3 or more realistic prompts, with and without the skill, on each target harness and model.
- [ ] The trigger check includes near-miss negatives.
- [ ] The validator passed on the frontmatter.

## Output contract

Return these four sections, in this order:

1. `Summary`
2. `Changes Made`
3. `Validation Results`
4. `Open Gaps`
