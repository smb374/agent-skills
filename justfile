# Recipes for this repo. Run `just --list` to see them.

# The tests import quick_validate.py; without this, `just install` copies its __pycache__.
export PYTHONDONTWRITEBYTECODE := "1"

default: check

# Format the Python files and flake.nix.
fmt:
    ruff format .
    nixfmt flake.nix

# Run the unit tests.
test:
    python3 -m unittest discover -s tests

# Lint, check the format, test, and validate every skill.
check:
    ruff check .
    ruff format --check .
    nixfmt --check flake.nix
    shellcheck install.sh
    just test
    for d in skills/*/; do python3 skills/skill-writer/scripts/quick_validate.py "$d" || exit 1; done
    ! grep -rnF --exclude=portability.md -e 'Skill tool' -e 'setup-matt-pocock-skills' -e '${CLAUDE_SKILL_DIR}' -e '$ARGUMENTS' skills/

# Copy the skills, then add the vendor skills. Pass install.sh flags, for example `--dir DIR --no-vendor`.
install *args:
    ./install.sh --copy {{args}}

# Link the skills, then add the vendor skills. Pass install.sh flags, for example `--dir DIR --no-vendor`.
link *args:
    ./install.sh --link {{args}}
