#!/usr/bin/env bash
# Claude Code PreToolUse hook for the Bash tool.
input=$(cat)
if echo "$input" | grep -q 'push --force'; then
  echo "Denied"
  exit 1
fi
exit 0
