# agent-skills
Personal skills to use across harness.

See [docs/catalog.md](docs/catalog.md) for the planned skills, and [CONTRIBUTING.md](CONTRIBUTING.md) to add a skill.

## Install

Run `./install.sh`. It needs a POSIX shell, and Node.js for the vendor skills. It does two things:

1. It links each skill in `skills/` into `~/.agents/skills/`.
2. It adds the upstream skills in `vendor.txt` with `npx skills add --global`.

| Flag | Action |
| --- | --- |
| `--link` | Links the skills. This is the default. |
| `--copy` | Copies the skills instead of linking them. |
| `--dir DIR` | Puts the skills of this repo in `DIR`. The default is `~/.agents/skills`. |
| `--agent AGENT` | Sets the agent for `npx skills`. The default is `pi`. `npx skills` selects the directory of that agent, not `DIR`. |
| `--no-vendor` | Does not add the vendor skills. |

The script does not replace a target that exists. It prints `skip:` with the path, and exits 1 at the end. A link that already points to this repo is not a skip.

## Devshell

The recipes need the tools of the devshell. Enter the devshell with `direnv allow`, or run `nix develop`.

## Recipes

| Recipe | Action |
| --- | --- |
| `just fmt` | Formats the Python files with ruff and `flake.nix` with nixfmt. |
| `just check` | Runs the lint, the format check, the tests, and the validator on every skill. |
| `just test` | Runs the unit tests of the validator and of `install.sh`. |
| `just install [flags]` | Runs `./install.sh --copy` with the flags. |
| `just link [flags]` | Runs `./install.sh --link` with the flags. |

`just check` also runs shellcheck on `install.sh`, and fails when a skill contains a banned string. See [CONTRIBUTING.md](CONTRIBUTING.md).
