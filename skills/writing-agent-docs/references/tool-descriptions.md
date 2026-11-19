# Tool descriptions and messages

Use this file when you write a tool description, a parameter description, an error message, or a hook message. The agent reads each of these at the moment it chooses or repairs an action.

## Contents

- [Tool descriptions](#tool-descriptions)
- [Names](#names)
- [Tool output](#tool-output)
- [Error and hook messages](#error-and-hook-messages)
- [Checklist](#checklist)

## Tool descriptions

A tool description is a guide, not a pointer. It is the only guide that the agent has to the tool, so it can hold detail: aim for 3 or 4 sentences or more. Write it as a briefing to a new team member. State the context that you know and the agent does not: query formats, terms of the domain, links between resources.

Cover these parts:

1. What the tool does.
2. When to use it, and when to use another tool. Name the near-miss tool.
3. What each parameter means, and its format.
4. The limits: size caps, side effects, slow paths.

Add an input example only for a complex input, such as a nested object or a strict format.

Ask a parameter for an explanation, not for the reasoning of the model. A request for step-by-step reasoning can cause a refusal.

When the agent calls a tool wrongly more than once, fix the description first. Then test it with a prompt that must use the tool and a near-miss prompt.

Bad: `Searches the codebase.`
Good: `Searches file contents with a regex or a literal string. Use it to find where text occurs. To find a file by name, use find_files. pattern is a Rust regex. path limits the search to a directory or a glob. Returns at most 20 matches. Use cursor to get the next page.`

## Names

- Name each parameter so that it has one meaning: `user_id`, not `user`.
- Name each tool for its exact action: `semantic_search`, not `search`.
- Fewer tools with clear limits work better than many tools that overlap. When two tools overlap, merge them or state the limit in each description.

## Tool output

- Return names and short IDs, not opaque UUIDs.
- When the tool truncates its output, add one line that says how to get the rest. Example: `Output truncated at 20 matches. Narrow the path, or pass cursor.`

## Error and hook messages

First, find the channel that reaches the model. A message on a channel that the model never sees changes nothing. The channels differ by harness and by event. Check the harness docs.

Example, Claude Code hooks:

- Exit code 2: on most events, the model sees stderr. The `Notification` event ignores it.
- Exit code 0: the model never sees stderr.
- Plain stdout reaches the model as context on some events only, such as `UserPromptSubmit` and `SessionStart`.
- A `Stop` hook with exit code 2 keeps the agent going. Its stderr is the next instruction.

Then write the message as an instruction. State what went wrong, and what the agent does next. Give the safe path for a block.

Bad: `Blocked: rm commands are not allowed.`
Good: `rm is blocked in this repo. Use trash <path>, or ask the user to delete the file.`

Bad: `Error: 429`
Good: `Rate limit exceeded. Retry after 60 seconds.`

## Checklist

- [ ] The description states what, when, when not, each parameter, and the limits.
- [ ] The description names the near-miss tool.
- [ ] Each name has one meaning.
- [ ] Each truncation line says how to get the rest.
- [ ] Each message travels on a channel that the model sees.
- [ ] Each message states what went wrong and the next action.
