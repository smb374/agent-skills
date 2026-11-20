---
name: handoff
description: Rules and a template to hand work off to a forked session, a new session, or a subagent. Also rules for the agent that receives a handoff brief. Use when the user asks for a handoff or a brief for a subagent, or when a flow step hands work to a subagent. For AGENTS.md, system prompts, and agent definitions, use writing-agent-docs.
compatibility: scripts/fill.py needs Python 3.10 or later. The install script of smb374/agent-skills adds it.
---

# Handoff

A handoff gives work to another agent through a brief: a file that the receiver reads first. The sender writes the brief. The receiver acts on it.

Start a handoff only when the user asks for it, or when a step of a flow that the user started asks for it. Do not hand off work on your own, because the user decides where the work goes.

In this file, `<skill>` is the directory that contains this SKILL.md.

## Pick the target

| Target | Inherits context | A parent waits for a report |
| --- | --- | --- |
| Fork session | yes | no |
| New session | no | no |
| Subagent, fresh | no | yes |
| Subagent, forked | yes | yes |

Each axis sets a rule for the brief:

| Axis | Value | Rule for the brief |
| --- | --- | --- |
| Inherits context | no | Make the brief self-contained. Put each fact in the brief, or give the path or URL of a durable artifact. |
| Inherits context | yes | Write only the delta: the task, the scope, and what in the history no longer holds. The brief overrides the history. |
| A parent waits | yes | Give the brief a fixed Report section. The parent checks the report against it, and resumes the receiver once with the missing parts. |
| A parent waits | no | Name the done criteria, and where the result goes: a commit, an issue, or a file. |

## Send a handoff

1. Pick the template.
   - Fork session or new session: `<skill>/assets/session.md`.
   - Subagent: the template that the user or the flow names. When nobody names one, ask the user.
2. Pick a name for the brief, for example `handoff-<topic>`. Write both files to the temporary directory of the OS: `$TMPDIR`, else `/tmp`, or `%TEMP%` on Windows. Do not write them to the workspace.
3. Run `python3 <skill>/scripts/fill.py --fields <template> <tmp>/<name>.values.json`. It writes a values file with each key set to `null`. It prints each key with its type and a hint.
4. Replace each `null` in the values file:
   - `string`: a non-empty string. You can use Markdown.
   - `list`: an array of non-empty strings. Use `[]` only when the template prints `None` for an empty list. `fill` tells you when it does not.
   - `bool`: `true` or `false`.
5. Run `python3 <skill>/scripts/fill.py <template> <tmp>/<name>.values.json <tmp>/<name>.md`.
6. When `fill` exits 1, it writes nothing and lists each problem. Fix each problem in the values file, then do step 5 again.
7. Give the path of the brief to the receiver. For a session, give the path to the user.

When `<skill>/scripts/fill.py` does not exist, the skill was not installed with its install script. Tell the user, and stop.

## Sender rules

1. Copy the contract into the brief: the criteria, the findings to fix, and the scope. Refer to the rest by path or URL: specs, plans, ADRs, issues, diffs, and commits.
2. Redact secrets and personal data: API keys, passwords, tokens, and personal details.
3. Name each skill that the receiver must load.
4. When the user gives a focus for the next session, write the Goal and the Next action for that focus.

## Receive a handoff

1. Authority: the brief comes first, then the files that it cites, then nothing else.
2. When the brief has a gap, or it conflicts with a file or with the code, do not fill the gap yourself. Ask the parent when one exists, else ask the user. When you have no tool to ask, end your turn with the questions.
3. Support each claim with evidence: `file:line`, a quoted line, or a quoted command output.
4. When the brief has a Report section, reply in its shape. Put the status line first, then each heading in order. Write `None` under a heading with no content.
