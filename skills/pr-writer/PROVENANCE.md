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

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| title types: the repository convention first, then the `config-conventional` types | `docs/catalog.md` asks for Conventional Commits titles. The global agent rules follow the repository convention when one exists | adopted |
| the Sentry-only types `ref`, `meta`, and `license` | not in `config-conventional` | rejected |
| `SPEC.md`, `EVAL.md`, and `evals/` | `PROVENANCE.md` replaces `SPEC.md`, as in `skill-writer`. The evals need AXIS and Codex | rejected |
| a script step that finds the tickets and specs of the branch | `docs/catalog.md` lists it as a separate `own` row | deferred |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing: the upstream AXIS case is not copied | add an eval case in `evals/` of this repo when a PR-body failure shows |

## Local changes

- Add `license: Apache-2.0` to the frontmatter, and add the Apache-2.0 notice of change.
- Add `disable-model-invocation: true`, because `docs/catalog.md` lists `pr-writer` as a flow skill.
- Replace the Sentry type list with Conventional Commits 1.0.0: use the types of the repository when it documents them, else the `config-conventional` types.
- Remove `SPEC.md`, `EVAL.md`, and `evals/`.
