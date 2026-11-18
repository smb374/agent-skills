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
    just test
    for d in skills/*/; do python3 skills/skill-writer/scripts/quick_validate.py "$d" || exit 1; done

# Copy every skill to dir and skip a target that exists.
install dir=(env("HOME") / ".agents/skills"):
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p "{{dir}}"
    status=0
    for src in skills/*/; do
        name=$(basename "$src")
        target="{{dir}}/$name"
        if [ -e "$target" ] || [ -L "$target" ]; then
            echo "skip: $target exists"
            status=1
            continue
        fi
        cp -R "$src" "$target"
        echo "install: $target"
    done
    exit "$status"

# Link every skill into dir and skip a target that exists.
link dir=(env("HOME") / ".agents/skills"):
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p "{{dir}}"
    root=$(pwd)
    status=0
    for src in skills/*/; do
        name=$(basename "$src")
        absolute="$root/skills/$name"
        target="{{dir}}/$name"
        if [ -L "$target" ] && [ "$(readlink "$target")" = "$absolute" ]; then
            echo "linked: $target"
            continue
        fi
        if [ -e "$target" ] || [ -L "$target" ]; then
            echo "skip: $target exists"
            status=1
            continue
        fi
        ln -s "$absolute" "$target"
        echo "link: $target -> $absolute"
    done
    exit "$status"
