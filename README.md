# agent-skills
Personal skills to use across harness.

See [docs/catalog.md](docs/catalog.md) for the planned skills, and [CONTRIBUTING.md](CONTRIBUTING.md) to add a skill.

## Install

Install from the `main` branch with one line:

```sh
curl -fsSL https://raw.githubusercontent.com/smb374/agent-skills/main/install.sh | sh
```

Or run `./install.sh --src .` in a clone. The script needs a POSIX shell, curl or wget (when you pass no `--src`), and Node.js for the vendor skills. It does two things:

1. It copies each skill in `skills/` into `~/.agents/skills/`. With no `--src`, it downloads the `main` tarball of this repo and copies from that.
2. It adds the upstream skills in `vendor.txt` with `npx skills add --global`.

| Flag | Action |
| --- | --- |
| `--src DIR` | Copies the skills, and reads `vendor.txt`, from `DIR`. The default is the download of `main`. |
| `--dir DIR` | Puts the skills of this repo in `DIR`. The default is `~/.agents/skills`. |
| `--agent AGENT` | Sets the agent for `npx skills`. The default is `pi`. `npx skills` selects the directory of that agent, not `DIR`. |
| `--no-vendor` | Does not add the vendor skills. |
| `--force` | Deletes a target that exists, and copies again. The vendor step does not change. |

The script does not replace a target that exists. It prints `skip:` with the path, and exits 1 at the end. Any other flag exits 2 with the usage line.

## Devshell

The recipes need the tools of the devshell. Enter the devshell with `direnv allow`, or run `nix develop`.

## Recipes

| Recipe | Action |
| --- | --- |
| `just fmt` | Formats the Python files with ruff and `flake.nix` with nixfmt. |
| `just check` | Runs the lint, the format check, the tests, and the validator on every skill. |
| `just test` | Runs the unit tests of the validator and of `install.sh`. |
| `just install [flags]` | Runs `./install.sh --src .` with the flags. |

`just check` also runs shellcheck on `install.sh`, and fails when a skill contains a banned string. See [CONTRIBUTING.md](CONTRIBUTING.md).
