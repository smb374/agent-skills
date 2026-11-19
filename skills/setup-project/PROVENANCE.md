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
| grilling session with the user | note | primary | 2026-11-19 | every decision below that cites the user | none recorded |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| fork `setup-matt-pocock-skills` and name it `setup-project` | the vendored skills read its `docs/agents/` files. The user chose the fork and the name | adopted |
| trackers: GitHub and "other" only | the user's choice. "Other" covers GitLab by description | adopted |
| `issue-tracker-gitlab.md`, `issue-tracker-local.md`, `agents/openai.yaml` | not used, or Codex UI metadata only | rejected |
| create the triage and `wayfinder:*` labels with `gh label create` | upstream docs: `gh issue create --label <missing>` fails | adopted |
| always write `AGENTS.md`. Offer to move `CLAUDE.md` into it, with `@AGENTS.md` as the only line of `CLAUDE.md` | upstream docs: the block can land in a file that the harness does not read. The user's choice | adopted |
| a new `AGENTS.md` holds the found commands and the `## Agent skills` block only | the user's choice | adopted |
| `CONTRIBUTING.md`: Conventional Commits, issue footer, `<type>/<issue>-<slug>` branch name, `pre-commit install` | the user's choice. `pr-writer` reads the issue from the branch name and the footers | adopted |
| enforce the header and the footer with pre-commit `commit-msg` hooks | the user's choice over a convention only, commitlint, or a CI check | adopted |
| no footer needed for `docs`, `chore`, `ci`, `build`, `style`, `revert`, git `Merge`, and `fixup!`/`squash!`/`amend!` | the user's choice. `revert` replaces git's `Revert "..."`, which `conventional-pre-commit` rejects | adopted |
| stop and ask on husky, lefthook, commitlint, or `core.hooksPath` | the user's choice. `pre-commit install` refuses to run with `core.hooksPath` | adopted |
| ask the user to install pre-commit when it is not on the `PATH` | the user's choice | adopted |
| remove the `/improve-codebase-architecture` mention from `domain.md` | the catalog does not keep that skill | adopted |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| commit-msg hooks | tested: 14 sample messages give the expected pass or fail with `pre-commit run --hook-stage commit-msg` | add a case when a real message is classified wrong |
| a full run of the skill in a new repo | not tested | run it in a scratch GitHub repo |
| baseline runs with and without the skill | missing | add an eval when a setup failure shows |

## Local changes

- Rename to `setup-project`, add `license: MIT`, and rewrite the description.
- Keep only the GitHub and "other" trackers. Remove the GitLab and local templates, and `agents/openai.yaml`.
- Explore the project commands, `CONTRIBUTING.md`, the git hook managers, and `pre-commit`.
- Add Section D (commit rules and git hooks) with its preconditions.
- Always write `AGENTS.md`. Add a `### Commits` sub-block to `## Agent skills`.
- Create the triage and `wayfinder:*` labels on GitHub.
- Add the templates `contributing.md` and `pre-commit-config.yaml`.
- Remove the `/improve-codebase-architecture` mention from `domain.md`.
