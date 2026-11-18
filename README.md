# agent-skills
Personal skills to use across harness.

## Devshell

The recipes need the tools of the devshell. Enter the devshell with `direnv allow`, or run `nix develop`.

## Recipes

| Recipe | Action |
| --- | --- |
| `just fmt` | Formats the Python files with ruff and `flake.nix` with nixfmt. |
| `just check` | Runs the lint, the format check, the tests, and the validator on every skill. |
| `just test` | Runs the unit tests of the validator. |
| `just install [dir]` | Copies every skill into `dir`. The default is `~/.agents/skills`. |
| `just link [dir]` | Links every skill into `dir`. The default is `~/.agents/skills`. |

`install` and `link` create `dir` when it is missing. They skip a target that already exists, print its path, and exit non-zero.
