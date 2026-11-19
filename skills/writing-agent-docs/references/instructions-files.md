# Instructions files

Use this file when you write an AGENTS.md, a CLAUDE.md, or a doc that one of them points to. The harness loads an instructions file in each session, so each line pays context load on each turn.

## Contents

- [What goes in](#what-goes-in)
- [Size](#size)
- [Disclosed docs](#disclosed-docs)
- [Nested files](#nested-files)
- [Harness table](#harness-table)
- [Checklist](#checklist)

## What goes in

Write what the agent cannot find by looking:

- an unwritten convention of the repo
- the reason for a choice that looks wrong
- a trap that no config file shows
- a command only when no script, config file, or `--help` shows it

Add a rule when the agent makes the same mistake a second time, or when a review catches something that the agent should know.

Write each rule so that a reviewer can check it. Name the behaviour to flag and its safe path. Leave format and lint rules to the tools.

Bad: `Format code properly.`
Good: the formatter config holds the format rule, and the file has no line about it.

Claude Code and Codex give the file to the model as a user message, not as the system prompt. Call the file "project instructions" in its own text.

## Size

There is no measured limit. Use the vendor limits as the ceiling:

- Claude Code advises under 200 lines in each file. Longer files cost more context and reduce adherence.
- Codex stops adding files when all the files together reach 32 KiB (`project_doc_max_bytes`).

A shorter file is easier to keep relevant. When a file passes the ceiling, disclose before you cut: move a branch to a disclosed doc or to a nested file.

## Disclosed docs

A disclosed doc is a file that the instructions file names in a pointer. The agent reads it only when the pointer fires.

- Write the pointer as plain text, with the condition first: `Before you change the schema, read docs/schema.md.`
- A Claude Code `@path` import is not a pointer. It loads the file with the importing file, up to 4 hops deep, so it saves no context. Use it only to split a long file for the human reader.
- Codex and Pi document no import. A portable file uses plain-text pointers.
- Claude Code removes an HTML comment before the model reads it. Other harnesses may not. Keep hidden text out of a portable file.

## Nested files

A nested file is an instructions file in a subdirectory. The harnesses merge them in different ways: Claude Code joins all of them, Codex lets the later file win by order, and the agents.md spec says the closest file wins.

- Write a child file to add to its parent, never to contradict it. Claude Code can pick either side of a contradiction.
- Put a rule for one part of the repo in the file of that part.

Bad: root AGENTS.md says `Use Jest.` and `web/AGENTS.md` says `Use Vitest, not Jest.`
Good: root AGENTS.md says `Each package names its test runner in its own AGENTS.md.` `web/AGENTS.md` says `Use Vitest.`

## Harness table

Check the harness docs before you rely on a row. The docs change often.

| Harness | File names | Discovery | Merge | Limit | Import |
| --- | --- | --- | --- | --- | --- |
| Claude Code | `CLAUDE.md`, `CLAUDE.local.md`. `AGENTS.md` only when no `CLAUDE.md` exists in the cwd or above | parent directories at launch. A subdirectory file when the agent touches a file in that subdirectory | joins all files | advice: under 200 lines per file | `@path`, eager |
| Codex | `AGENTS.override.md`, else `AGENTS.md`. One file per directory | from the repo root down to the cwd | joins all files. A later, closer file wins by order | 32 KiB for all files | none documented |
| Pi | `AGENTS.override.md`, `AGENTS.md`, `AGENTS.MD`, `CLAUDE.md`, or `CLAUDE.MD` | the agent directory, the cwd, and each parent directory | `AGENTS.override.md` replaces the others in its directory only | none documented | none documented |
| agents.md spec | `AGENTS.md` | nested files allowed | the closest file wins | none | none |

For a repo that Claude Code and other harnesses both use, keep the text in `AGENTS.md`. Add a `CLAUDE.md` that holds only the line `@AGENTS.md`. A symlink can fail on Windows.

## Checklist

- [ ] Each line passes the pruning pass in `levers.md`.
- [ ] No line restates a script, a config file, or `--help`.
- [ ] Each must-hold rule is a hook, a lint rule, or a permission rule.
- [ ] Each pointer starts with its condition.
- [ ] No nested file contradicts its parent.
- [ ] The file is within the vendor limits: 200 lines per file, 32 KiB for all files.
