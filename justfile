# Recipes for this repo. Run `just --list` to see them.

# The tests import quick_validate.py; without this, `just install` copies its __pycache__.
export PYTHONDONTWRITEBYTECODE := "1"

# `just eval` reads the settings and the API key from .env. See .env.example.
set dotenv-load

default: check

# Format the Python files and flake.nix.
fmt:
    ruff format .
    nixfmt flake.nix

# Run the unit tests, or only those whose name matches `name`.
test name="":
    python3 -m unittest discover -s tests {{ if name == "" { "" } else { "-k " + name } }}

# Lint the Python files and shell scripts. These are the static checks; there is no type checker.
typecheck:
    ruff check .
    shellcheck install.sh

# Lint, check the format, test, and validate every skill.
check:
    just typecheck
    ruff format --check .
    nixfmt --check flake.nix
    just test
    d=$(mktemp -d) && trap 'rm -rf "$d"' EXIT && ./install.sh --src . --dir "$d" --no-vendor && for s in "$d"/*/; do python3 skills/skill-writer/scripts/quick_validate.py "$s" || exit 1; done
    ! grep -rnF --exclude=portability.md --exclude=PROVENANCE.md -e 'Skill tool' -e 'setup-matt-pocock-skills' -e '${CLAUDE_SKILL_DIR}' -e '$ARGUMENTS' skills/

# Copy the skills of this repo, then add the vendor skills. Pass install.sh flags, for example `--dir DIR --no-vendor`.
install *args:
    ./install.sh --src . {{args}}

# Run the eval cases of one skill with headless pi. Costs money. Pass run.py flags, for example `--runs 1 --case brief`.
eval skill *args:
    python3 evals/run.py {{skill}} {{args}}
