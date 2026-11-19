# pr-writer provenance

## Upstream

- repository: getsentry/skills, https://github.com/getsentry/skills
- path: `skills/pr-writer`
- commit: a582c51ee29d0f35e6ac321340796f77d43da733 (a582c51)
- license: Apache-2.0, see `LICENSE`. The upstream repository has no `NOTICE` file.
- status: modified

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| getsentry/skills `skills/pr-writer` @ a582c51 | code | primary | 2026-11-19 | the full skill | Apache-2.0: keep the notice of change in `SKILL.md` |
| https://www.conventionalcommits.org/en/v1.0.0/ | specification | primary | 2026-11-19 | the title format | none recorded |
| conventional-changelog/commitlint `@commitlint/config-conventional/src/index.ts` @ ca77d36, `type-enum` | code | primary | 2026-11-19 | the default type list | MIT |
| GitHub REST `GET /repos/{owner}/{repo}/issues/{issue_number}/sub_issues`, checked with `gh api repos/cli/cli/issues/1/sub_issues` | documentation | primary | 2026-11-19 | the sub-issue command | none recorded |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| title types: the repository convention first, then the `config-conventional` types | `docs/catalog.md` asks for Conventional Commits titles. The global agent rules follow the repository convention when one exists | adopted |
| the Sentry-only types `ref`, `meta`, and `license` | not in `config-conventional` | rejected |
| `SPEC.md`, `EVAL.md`, and `evals/` | `PROVENANCE.md` replaces `SPEC.md`, as in `skill-writer`. The evals need AXIS and Codex | rejected |
| find the target issue and its sub-issues, with commands in `SKILL.md`, not a script | two `gh` commands. A script adds a file to maintain and no check | adopted |
| no target issue: ask the user. When the user has none, or another workflow started the skill, use the branch commits | the user request of 2026-11-19 | adopted |
| the model can start the skill, but the description limits it to a user request or a call from another workflow | other workflows call it | adopted |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing: the upstream AXIS case is not copied | add an eval case in `evals/` of this repo when a PR-body failure shows |

## Local changes

- Add `license: Apache-2.0` to the frontmatter, and add the Apache-2.0 notice of change.
- Change the description: the user or another workflow starts the skill, not the model after a commit or a push.
- Add "Find the Target Issue": the issue of the PR, its sub-issues, and the fallback to the user or to the branch commits.
- Replace the Sentry type list with Conventional Commits 1.0.0: use the types of the repository when it documents them, else the `config-conventional` types.
- Remove `SPEC.md`, `EVAL.md`, and `evals/`.
