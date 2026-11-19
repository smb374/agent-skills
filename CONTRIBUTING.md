# Contributing

This repo holds portable skills only. A skill that needs Pi agents goes in the Pi config repo. Before you add a skill, add its row to `docs/catalog.md`.

## Choose how to add a skill

| The skill is | Do this |
| --- | --- |
| an upstream skill that you use unchanged | Add it to `vendor.txt`. |
| an upstream skill that needs changes | Fork it into `skills/<name>/`. |
| your own skill | Write it in `skills/<name>/` with the `skill-writer` skill. |

Do not fork a skill only to pin its version. Fork it when you change its text.

## Add a vendor skill

1. Add the skill name to the line of its repo in `vendor.txt`. For a new repo, add a line: `<owner>/<repo> <skill> [skill ...]`.
2. Set its status to `vendor` in `docs/catalog.md`.
3. Run `./install.sh` to install it.

## Fork a skill

Use two commits, so that `git diff` of the second commit shows only your changes.

1. Copy the upstream skill directory into `skills/<name>/` at a pinned commit. Do not change it.
2. Copy the upstream `LICENSE` into `skills/<name>/`. Also copy `NOTICE` when the upstream repo has one. `npx skills add` installs one skill directory, so the license must be in that directory.
3. Commit: `chore(<name>): vendor <owner>/<repo> @ <short-sha>`. `just check` can fail on this commit, because upstream text can contain banned strings.
4. Make your changes.
5. Add `skills/<name>/PROVENANCE.md`. Use `skills/skill-writer/references/provenance-template.md`.
6. For an Apache-2.0 skill, put a notice line in each file that you changed (Apache-2.0 §4(b)), for example `<!-- Derived from <owner>/<repo> <path> @ <short-sha> (Apache-2.0); modified. -->`.
7. Set its status to `done` in `docs/catalog.md`.
8. Run `just check`, then commit: `feat(<name>): ...`.

## Write your own skill

1. Run the `skill-writer` skill. Give it the target directory `skills/<name>/`.
2. Add `PROVENANCE.md` with status `own`.
3. Set its status to `done` in `docs/catalog.md`.
4. Run `just check`, then commit: `feat(<name>): ...`.

## Checks

`just check` must pass before each commit, except the verbatim commit of a fork. It fails when:

- ruff, nixfmt, or shellcheck reports a problem.
- A test fails.
- `quick_validate.py` finds an error in a skill. For example, `name` is not equal to the directory name, or `description` is longer than 1,024 characters. Pi skips a skill with bad frontmatter and gives no message.
- A file in `skills/` contains `Skill tool`, `setup-matt-pocock-skills`, `${CLAUDE_SKILL_DIR}`, or `$ARGUMENTS`. These work in one harness only. `skill-writer/references/portability.md` is exempt, because it describes them. Each `PROVENANCE.md` is exempt, because it names the upstream source.

## Commits

Use [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). Use the skill name as the scope.
