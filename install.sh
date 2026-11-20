#!/bin/sh
# Copy the skills of this repo into a skills directory, then add the upstream skills in vendor.txt.
set -eu

# Each of these skills gets a copy of fill/fill.py as scripts/fill.py.
fill_skills="handoff"

usage() {
    echo "usage: install.sh [--src DIR] [--dir DIR] [--agent AGENT] [--no-vendor] [--force]" >&2
    exit 2
}

src=
dir="$HOME/.agents/skills"
agent=pi
vendor=1
force=0
while [ $# -gt 0 ]; do
    case $1 in
    --src)
        [ $# -ge 2 ] || usage
        src=$2
        shift
        ;;
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
    --force) force=1 ;;
    *) usage ;;
    esac
    shift
done

if [ -z "$src" ]; then
    url=https://github.com/smb374/agent-skills/archive/refs/heads/main.tar.gz
    tmp=$(mktemp -d)
    trap 'rm -rf "$tmp"' EXIT
    if command -v curl >/dev/null; then
        curl -fsSL -o "$tmp/main.tar.gz" "$url"
    elif command -v wget >/dev/null; then
        wget -q -O "$tmp/main.tar.gz" "$url"
    else
        echo "error: curl and wget not found; install one, or pass --src DIR" >&2
        exit 1
    fi
    mkdir "$tmp/src"
    tar -xzf "$tmp/main.tar.gz" -C "$tmp/src" --strip-components=1
    src=$tmp/src
fi

status=0

mkdir -p "$dir"
for skill in "$src"/skills/*/; do
    skill=${skill%/}
    name=$(basename "$skill")
    target="$dir/$name"
    if [ -e "$target" ] || [ -L "$target" ]; then
        if [ "$force" = 1 ]; then
            rm -rf "$target"
        else
            echo "skip: $target"
            status=1
            continue
        fi
    fi
    cp -R "$skill" "$target"
    case " $fill_skills " in
    *" $name "*)
        mkdir -p "$target/scripts"
        cp "$src/fill/fill.py" "$target/scripts/fill.py"
        ;;
    esac
    echo "install: $target"
done

if [ "$vendor" = 1 ]; then
    command -v npx >/dev/null || {
        echo "error: npx not found; install Node.js, or pass --no-vendor" >&2
        exit 1
    }
    # npx picks the directory from --agent, not from --dir.
    grep -v -e '^#' -e '^[[:space:]]*$' "$src/vendor.txt" | while read -r repo skills; do
        # shellcheck disable=SC2086 # $skills is a space-separated list of names.
        npx --yes skills add "$repo" --global --agent "$agent" --skill $skills --yes </dev/null
    done
fi

exit "$status"
