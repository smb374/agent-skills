# Issue tracker: Local files

Issues and specs for this repo live as Markdown files under `.scratch/`. The directory is in `.gitignore`.

## Conventions

- One feature has one directory: `.scratch/<feature-slug>/`.
- The spec is `.scratch/<feature-slug>/spec.md`.
- Each ticket is one file: `.scratch/<feature-slug>/issues/<NN>-<slug>.md`. Number the tickets from `01` in dependency order, blockers first.
- Each ticket file has a `**Blocked by:**` line and a `**Status:**` line. A ticket is unblocked when each blocker has `**Status:** done`.
- Triage state is the `**Status:**` line of the file. Use the role strings of `triage-labels.md`.
- Add a comment as a `## Comments` section at the end of the file.
- Close a ticket: set `**Status:** done`.

## When a skill says "publish to the issue tracker"

Create the file in `.scratch/<feature-slug>/`.

## When a skill says "fetch the relevant ticket"

Read the file at the path that the user gave.
