# setup-project provenance

## Upstream

- repository: mattpocock/skills, https://github.com/mattpocock/skills
- path: `skills/engineering/setup-matt-pocock-skills`
- commit: 5863806dd4e15c63174bee4e7515a4256792ecfa (5863806)
- license: MIT, see `LICENSE`
- status: modified

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| mattpocock/skills `setup-matt-pocock-skills` @ 5863806 | code | primary | 2026-11-19 | the process, the GitHub tracker template, the label and domain templates | MIT |
| mattpocock/skills `docs/engineering/setup-matt-pocock-skills.md` @ 5863806 | documentation | primary | 2026-11-19 | the known gaps: the `CLAUDE.md` choice, and no `wayfinder:*` labels | MIT |
| https://pre-commit.com/ (pre-commit 4.6.2 installed) | documentation | primary | 2026-11-19 | `pygrep` with `--multiline --negate`, `default_install_hook_types`, `commit-msg` stage, `core.hooksPath` refusal | none recorded |
| compilerla/conventional-pre-commit v4.5.0 | code | primary | 2026-11-19 | the commit header hook | none recorded |
| gitleaks/gitleaks v8.30.1 `.pre-commit-hooks.yaml`; the hook files of trufflesecurity/trufflehog v3.99.9, Yelp/detect-secrets v1.5.0, and thoughtworks/talisman v1.37.0 | code | primary | 2026-11-19 | the secret scan hook, and the compared options | none recorded |
| grilling session with the user | note | primary | 2026-11-19 | every decision below that cites the user | none recorded |
| smb374/otnes `docs/agents/issue-types.md`, `docs/agents/triage-labels.md`, `AGENTS.md`, and `gh label list` | code | primary | 2026-11-19 | the issue types, the title prefixes, the hierarchy, the category table, and the label colors and descriptions | the user's own repo |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| fork `setup-matt-pocock-skills` and name it `setup-project` | the vendored skills read its `docs/agents/` files. The user chose the fork and the name | adopted |
| trackers: GitHub, local files, and "other" | #13. "Other" covers GitLab by description. Local files was first rejected and is now added | adopted |
| `issue-tracker-gitlab.md`, `agents/openai.yaml` | not used, or Codex UI metadata only | rejected |
| local mode: add `.scratch/` to `.gitignore` | #13 | adopted |
| local mode: skip the issue-footer hook and the footer rule in `CONTRIBUTING.md` | #13. A local ticket has no `#N`, and the hook requires `Refs\|Fixes\|Closes #N` | adopted |
| create the triage and `wayfinder:*` labels with `gh label create` | upstream docs: `gh issue create --label <missing>` fails | adopted |
| always write `AGENTS.md`. Offer to move `CLAUDE.md` into it, with `@AGENTS.md` as the only line of `CLAUDE.md` | upstream docs: the block can land in a file that the harness does not read. The user's choice | adopted |
| a new `AGENTS.md` holds the found commands and the `## Agent skills` block only | the user's choice | adopted |
| `CONTRIBUTING.md`: Conventional Commits, issue footer, `<type>/<issue>-<slug>` branch name, `pre-commit install` | the user's choice. `pr-writer` reads the issue from the branch name and the footers | adopted |
| enforce the header and the footer with pre-commit `commit-msg` hooks | the user's choice over a convention only, commitlint, or a CI check | adopted |
| no footer needed for `docs`, `chore`, `ci`, `build`, `style`, `revert`, git `Merge`, and `fixup!`/`squash!`/`amend!` | the user's choice. `revert` replaces git's `Revert "..."`, which `conventional-pre-commit` rejects | adopted |
| stop and ask on husky, lefthook, commitlint, or `core.hooksPath` | the user's choice. `pre-commit install` refuses to run with `core.hooksPath` | adopted |
| ask the user to install pre-commit when it is not on the `PATH` | the user's choice | adopted |
| scan staged changes for secrets with the `gitleaks` hook | the user's choice. It scans only the staged diff, works offline, and needs no baseline file | adopted |
| TruffleHog, detect-secrets, and Talisman as the secret scan | TruffleHog calls provider APIs and fails only on verified secrets. detect-secrets needs a `.secrets.baseline` file. Talisman ignores files by checksum in `.talismanrc`, so each change to an ignored file needs a new entry | rejected |
| remove the `/improve-codebase-architecture` mention from `domain.md` | the catalog does not keep that skill | adopted |
| add the otnes issue types: `type:*` labels, title prefixes, hierarchy, and `[WF]` for Wayfinder children | the user's choice, from smb374/otnes | adopted |
| make the otnes-only text general: the `type:bug` meaning, the `type:ticket` description, and "Not a Bug" | otnes names test ROMs, `/implement`, and `just verify` | adopted |
| create each label with the otnes color and description, and do not change a label that exists | the user's choice | adopted |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| commit-msg hooks | tested: 14 sample messages give the expected pass or fail with `pre-commit run --hook-stage commit-msg` | add a case when a real message is classified wrong |
| a full run of the skill in a new repo | not tested | run it in a scratch GitHub repo |
| baseline runs with and without the skill | missing | add an eval when a setup failure shows |

## Local changes

- Rename to `setup-project`, add `license: MIT`, and rewrite the description.
- Keep the GitHub, local files, and "other" trackers. Remove the GitLab template and `agents/openai.yaml`.
- Add the `issue-tracker-local.md` template. In local mode, add `.scratch/` to `.gitignore`, and skip the issue-footer hook and the footer rule.
- Explore the project commands, `CONTRIBUTING.md`, the git hook managers, and `pre-commit`.
- Add Section D (commit rules and git hooks) with its preconditions.
- Always write `AGENTS.md`. Add a `### Commits` sub-block to `## Agent skills`.
- Create the triage and `wayfinder:*` labels on GitHub.
- Add the templates `contributing.md` and `pre-commit-config.yaml`.
- Remove the `/improve-codebase-architecture` mention from `domain.md`.
- Add the `issue-types.md` template and the `### Issue types` sub-block. Map the `bug` and `enhancement` categories to `type:bug` and `type:feature` in `triage-labels.md`. Set the title prefix and the `type:*` label in `issue-tracker-github.md`, and `[WF]` for Wayfinder children.
- Create the `type:*`, triage, and `wayfinder:*` labels with a color and a description.
- Add the `gitleaks` secret scan hook to `pre-commit-config.yaml`.
