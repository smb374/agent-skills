---
name: setup-project
description: "Set up a repo for the engineering skills and for issue-linked commits: the issue tracker, the issue types, the triage and wayfinder labels, the domain doc layout, AGENTS.md, CONTRIBUTING.md, and pre-commit hooks that scan for secrets and check the commit header and the issue footer. Run once per repo, before the first use of the other engineering skills."
license: MIT
disable-model-invocation: true
---

# Setup Project

Scaffold the per-repo configuration that the engineering skills assume, and the commit rules that link the work to its issues:

- **Issue tracker**: where issues live (GitHub by default, or a workflow that the user describes)
- **Issue types**: the `type:*` label and the title prefix of each issue, and the Epic, Feature, Task, and Ticket hierarchy
- **Triage labels**: the strings used for the five canonical triage roles, and the labels in the tracker
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them
- **AGENTS.md**: the project commands and the `## Agent skills` block
- **CONTRIBUTING.md and git hooks**: Conventional Commits, the issue footer, the branch name, and a pre-commit config that checks them and scans for secrets

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` section in either?
- `GLOSSARY.md` and `GLOSSARY-MAP.md` at the repo root, and the legacy `CONTEXT.md` / `CONTEXT-MAP.md`. If a legacy file exists, offer to `git mv` it to its `GLOSSARY` name and rewrite those names in `docs/agents/domain.md`.
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/`: does this skill's prior output already exist?
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.
- The project commands: `justfile`, `Makefile`, the `scripts` of `package.json`, and the tasks of `pyproject.toml`, `Cargo.toml`, or `flake.nix`. Find the commands to format, lint, test, and check.
- `CONTRIBUTING.md`: does it exist? Does it already state a commit or branch convention?
- Git hooks: `.pre-commit-config.yaml`, `.husky/`, `lefthook.yml`, `.lefthook.yml`, a commitlint config (`commitlint.config.*`, `.commitlintrc*`), and `git config core.hooksPath`.
- `command -v pre-commit`: is pre-commit on the `PATH`?

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when there's no monorepo).

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, and `to-spec` read from and write to it. They need to know whether to call `gh issue create` or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. Otherwise (or if the user prefers), offer:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **Local files**: issues live as Markdown files under `.scratch/`, which is not tracked by git (no remote needed)
- **Other** (GitLab, Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub template carries a "PRs as a request surface" flag, defaulted **off**. Leave it off and don't raise it: a user who wants external PRs in the triage queue can flip the flag in the file later.

A GitHub tracker needs a reachable repo. When the user picks it and no `git remote` points at GitHub, get the repo URL from them and wire it up (`git init` if needed, `git remote add origin <url>`) before going further. Done when `gh repo view` prints the project from inside this directory; if it can't, stop and tell the user what's missing.

**Section B: Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you), since an uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no, usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`), collect the overrides so `triage` applies existing labels instead of creating duplicates.

**Section C: Domain docs.** Default to **single-context** (one `GLOSSARY.md` + `docs/adr/` at the repo root). This fits almost every repo; write it without asking.

Offer **multi-context** (a root `GLOSSARY-MAP.md` pointing to per-context `GLOSSARY.md` files) only when exploration found monorepo signals. Then confirm which layout they want.

**Section D: Commit rules and git hooks.** Do not ask about the rules. They come from [contributing.md](./contributing.md) and [pre-commit-config.yaml](./pre-commit-config.yaml). Check the preconditions:

- In local mode, the issue-footer hook and the footer rule do not apply. A local ticket has no `#N`, and the hook requires `Refs|Fixes|Closes #N`. Skip them in step 4.
- When exploration found husky, lefthook, a commitlint config, or a `core.hooksPath` value, stop this section. Tell the user what you found, and ask how to continue. `pre-commit install` refuses to run when `core.hooksPath` is set.
- When `pre-commit` is not on the `PATH`, ask the user to install it with their tool of choice (for example nix, mise, pipx, or the system package manager). Continue when `pre-commit --version` succeeds.
- When `CONTRIBUTING.md` already states a different commit or branch convention, show the conflict and ask which one to keep.

### 3. Confirm and edit

Show the user a draft of:

- The `AGENTS.md` changes (see step 4)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/issue-types.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` (the last only when `triage` is installed)
- The `CONTRIBUTING.md` sections and the `.pre-commit-config.yaml` hooks

Let them edit before writing.

### 4. Write

**AGENTS.md:**

- Always write the instructions to `AGENTS.md`.
- If only `CLAUDE.md` exists, ask the user to move its content into `AGENTS.md` and to make `CLAUDE.md` the single line `@AGENTS.md`. Do the move only when the user agrees. If the user says no, write to `CLAUDE.md`.
- If neither file exists, create `AGENTS.md` with a `## Commands` section and the `## Agent skills` block. `## Commands` lists only the commands that exploration found, one line each (for example `- Test: just test`). Add nothing that an agent can read from the code.

If an `## Agent skills` block already exists, update its contents in place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Issue types

Each issue has one `type:*` label and a matching title prefix: `[Epic]`, `[Bug]`, `[Feature]`, `[Task]`, `[Ticket]`. Wayfinder child issues have no `type:*` label and use `[WF]`. See `docs/agents/issue-types.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### Commits

Conventional Commits with an issue footer (`Refs: #N`, `Fixes #N`). See `CONTRIBUTING.md`.

In local mode, write: "Conventional Commits. See `CONTRIBUTING.md`."
```

Include the `### Triage labels` sub-block, and write `docs/agents/triage-labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted.

**Docs files:** write them from the seed templates in this skill folder:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local files tracker
- [issue-types.md](./issue-types.md): issue types, title prefixes, and hierarchy
- [triage-labels.md](./triage-labels.md): label mapping (only if `triage` is installed)
- [domain.md](./domain.md): domain doc consumer rules + layout

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

**GitHub labels:** on a GitHub tracker, create each label of this table that `gh label list` does not show. Skip the triage rows when Section B did not run. When Section B changed a triage label name, use the new name with the same color and description. Do not change a label that exists. `gh issue create --label` fails on a label that does not exist.

| Label | Color | Description |
| --- | --- | --- |
| `type:epic` | `5319e7` | Large work and discussion |
| `type:bug` | `d73a4a` | Failure that the automated tests do not catch |
| `type:feature` | `a2eeef` | Spec: new behavior |
| `type:task` | `fbca04` | Spec: change to existing behavior |
| `type:ticket` | `0e8a16` | Unit of work for an implementation agent |
| `needs-triage` | `ededed` | Maintainer needs to evaluate this issue |
| `needs-info` | `d876e3` | Waiting on reporter for more information |
| `ready-for-agent` | `0e8a16` | Fully specified, ready for an AFK agent |
| `ready-for-human` | `1d76db` | Requires human implementation |
| `wontfix` | `ffffff` | This will not be worked on |
| `wayfinder:map` | `5319e7` | Wayfinder map |
| `wayfinder:research` | `c5def5` | Wayfinder research ticket |
| `wayfinder:prototype` | `c5def5` | Wayfinder prototype ticket |
| `wayfinder:grilling` | `c5def5` | Wayfinder grilling ticket |
| `wayfinder:task` | `c5def5` | Wayfinder task ticket |

```bash
gh label create <label> --color <color> --description "<description>"
```

**CONTRIBUTING.md:** add the sections of [contributing.md](./contributing.md). When `CONTRIBUTING.md` exists, update its matching sections in place, and keep the other sections. In local mode, leave out the issue footer paragraph, the list of footers, and the sentence about commits with no footer.

**.gitignore (local mode only):** add `.scratch/` to `.gitignore`. Create the file if it does not exist.

**pre-commit:** copy the hooks of [pre-commit-config.yaml](./pre-commit-config.yaml) into `.pre-commit-config.yaml`. In local mode, leave out the `issue-footer` hook. When the file exists, add the hooks and the `commit-msg` hook type, and keep the other hooks. Then run:

```bash
pre-commit install
```

Done when the output names `.git/hooks/commit-msg`.

### 5. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md`, `CONTRIBUTING.md`, and `.pre-commit-config.yaml` directly later; re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.
