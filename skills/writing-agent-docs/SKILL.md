---
name: writing-agent-docs
description: Writes, edits, and prunes the documents that agents read, other than skills. These are AGENTS.md, CLAUDE.md, docs that an instructions file points to, agent briefs, agent definitions, system prompts, tool descriptions, and error or hook messages. Use when asked to create, edit, shorten, or fix one of these, or when an agent ignores or misreads one. For skills, use skill-writer.
license: MIT
---

# Writing agent docs

Use this skill to write or change one document that an agent reads. Success has two parts: the document changes what the agent does, and it costs the least context that can do that.

## Critical rules

- Each line must change what the agent does. Cut each line that does not.
- Put a rule that must hold every time in a hook, a lint rule, or a permission rule. Prose is context, not enforcement.
- State the target behaviour. When a ban is necessary, pair it with the safe path.
- Keep each meaning in one place. Two places drift, and a contradiction costs the agent reasoning on each run.
- Write prose in Simplified Technical English: short common words, active voice, simple tenses, one instruction per sentence.

## Router

| Open when you need to... | Read |
| --- | --- |
| apply the shared craft: pointers, loads, hierarchy, completion criteria, leading words, emphasis, pruning | `references/levers.md` |
| write an AGENTS.md, a CLAUDE.md, or a doc that one of them points to | `references/instructions-files.md` |
| write an agent definition, a system prompt, or a brief for a subagent | `references/agent-prompts.md` |
| write a tool description, an error message, or a hook message | `references/tool-descriptions.md` |

## Step 1: Classify the document

Find the type, the load, and the reader. The load tells you how hard to prune.

| Type | Load | Reader | Reference |
| --- | --- | --- | --- |
| AGENTS.md, CLAUDE.md | each session, always | the main agent | `instructions-files.md` |
| disclosed doc | only when its pointer fires | the main agent | `instructions-files.md` |
| agent definition: description | each turn, always | the orchestrator that picks an agent | `agent-prompts.md` |
| agent definition: body, system prompt | each run of that agent | the agent itself | `agent-prompts.md` |
| brief | one dispatch | a subagent with no parent context | `agent-prompts.md` |
| tool description | each turn while the tool is active | the agent that picks and calls tools | `tool-descriptions.md` |
| error or hook message | each time it fires | the agent that must act next | `tool-descriptions.md` |

Done when you can name the type, the load, and the reader of the document.

## Step 2: Place each piece

| The piece is | Put it in |
| --- | --- |
| a convention for each task in the repo | the instructions file |
| a convention for one part of the repo | a nested instructions file, or a disclosed doc behind a pointer |
| a procedure that the agent needs sometimes | a skill. Use `skill-writer` |
| a constraint that a regex, a path, or a command can check | a hook, a lint rule, or a permission rule |
| a fact that config, a script, or `--help` already shows | nothing. The environment is the source |
| a one-off fix | nothing |

Done when each piece has one place, and no piece restates the environment.

## Step 3: Write

1. Open the reference for the type from Step 1.
2. Open `references/levers.md` for the craft that each type uses.
3. Write the target behaviour first. Add a ban only as a guardrail with its safe path.

Done when each section of the document has a completion criterion or a lookup purpose.

## Step 4: Prune

Run each test of the pruning pass in `references/levers.md` on each changed line.

Record each change as replaced, narrowed, moved, deleted, or added with a reason. A document that only gains lines grows without limit.

## Step 5: Test

| Change | Minimum test |
| --- | --- |
| a new document or a new section | Run 2 or 3 realistic prompts with the document and without it. Read the transcripts. |
| a small edit | Apply the no-op test to each changed line. Run 1 prompt with the change. |
| a tool description or a message | Run 1 prompt that must use the tool and 1 near-miss prompt. Check the call arguments and the next action. |

Run each prompt in a fresh context: a subagent, or a new session when no subagent is available. A cold reader shows what the document leaves out.

When the agent ignores a rule, sharpen its wording first. Move the rule to a hook when sharper wording also fails.

## Output contract

Return these four sections, in this order:

1. `Summary`
2. `Changes Made`: each change, recorded as replaced, narrowed, moved, deleted, or added
3. `Validation Results`: the prompts that you ran, and what the agent did
4. `Open Gaps`
