#!/bin/sh
# Put the skills of this repo into a skills directory, then add the upstream skills in vendor.txt.
set -eu

usage() {
    echo "usage: install.sh [--link | --copy] [--dir DIR] [--agent AGENT] [--no-vendor]" >&2
    exit 2
}

mode="link"
dir="$HOME/.agents/skills"
agent=pi
vendor=1
while [ $# -gt 0 ]; do
    case $1 in
    --link) mode="link" ;;
    --copy) mode="copy" ;;
    --dir)
        [ $# -ge 2 ] || usage
        dir=$2
        shift
        ;;
    --agent)
        [ $# -ge 2 ] || usage
        agent=$2
        shift
        ;;
    --no-vendor) vendor=0 ;;
    *) usage ;;
    esac
    shift
done

root=$(cd "$(dirname "$0")" && pwd)
status=0

mkdir -p "$dir"
for src in "$root"/skills/*/; do
    src=${src%/}
    target="$dir/$(basename "$src")"
    if [ "$mode" = link ] && [ -L "$target" ] && [ "$(readlink "$target")" = "$src" ]; then
        echo "linked: $target"
        continue
    fi
    if [ -e "$target" ] || [ -L "$target" ]; then
        echo "skip: $target exists"
        status=1
        continue
    fi
    if [ "$mode" = copy ]; then
        cp -R "$src" "$target"
        echo "install: $target"
    else
        ln -s "$src" "$target"
        echo "link: $target -> $src"
    fi
done

if [ "$vendor" = 1 ]; then
    command -v npx >/dev/null || {
        echo "error: npx not found; install Node.js, or pass --no-vendor" >&2
        exit 1
    }
    # npx picks the directory from --agent, not from --dir.
    grep -v -e '^#' -e '^[[:space:]]*$' "$root/vendor.txt" | while read -r repo skills; do
        # shellcheck disable=SC2086 # $skills is a space-separated list of names.
        npx --yes skills add "$repo" --global --agent "$agent" --skill $skills --yes </dev/null
    done
fi

exit "$status"
