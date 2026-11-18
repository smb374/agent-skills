<!-- Derived from getsentry/skills skills/skill-writer @ a582c51 (Apache-2.0); modified. -->

# Portability

Use this file in step 1 or step 4, when the skill must work in more than one harness. Each harness reads the same `SKILL.md`, and each one lists, invokes, and restricts a skill in its own way. A portable skill works with the portable core fields only, and it names each extra field as optional.

## Contents

- [Where skills live](#where-skills-live)
- [The portable layout](#the-portable-layout)
- [The portable core fields](#the-portable-core-fields)
- [Harness-specific fields](#harness-specific-fields)
- [Side effects on a harness without the switch](#side-effects-on-a-harness-without-the-switch)
- [Name actions, not tools](#name-actions-not-tools)
- [MCP tools](#mcp-tools)
- [Body features of one harness](#body-features-of-one-harness)
- [Checklist](#checklist)

## Where skills live

| Harness | Project paths | User paths | Start by the user | Start by the model |
| --- | --- | --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `/name` | the `Skill` tool, from the listing |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | — | the `skill` tool, from its description |
| Copilot CLI | `.github/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.copilot/skills/`, `~/.agents/skills/` | — | injects `SKILL.md` when the description matches |
| Pi | the Pi project directory, `.agents/skills/` up to the repo root | the Pi user directory, `~/.agents/skills/` | `/skill:name args` | the name, the description, and the path in the system prompt |
| Hermes Agent | `.hermes/skills/`, `.agents/skills/` | `~/.hermes/skills/`, plus the configured external directories | `/name` | `skills_list`, then `skill_view` |

## The portable layout

`.agents/skills/` is read by OpenCode, Copilot, Pi, and Hermes. `.claude/skills/` is read by Claude Code, OpenCode, and Copilot.

To serve the five harnesses, keep one source directory and symlink each skill into both locations. Check that each harness follows a symlink before you rely on it.

## The portable core fields

| Field | Rule |
| --- | --- |
| `name` | Required. 1 to 64 characters, and `^[a-z0-9]+(-[a-z0-9]+)*$`. Keep it equal to the directory name. |
| `description` | Required. 1 to 1,024 characters. One harness allows 1,536 with an extra field, but 1,024 is the portable limit. |
| `license` | Optional. |
| `compatibility` | Optional, up to 500 characters. Write the runtime needs here: "Needs `gh` and Python 3.10+". |
| `metadata` | Optional map from string to string. Put the data of one tool here, and not in a new top-level key. |
| `allowed-tools` | Optional, experimental. The syntax and the enforcement differ per harness. |

## Harness-specific fields

Another harness ignores these fields, so the skill must work without them.

| Field | Harness | Effect |
| --- | --- | --- |
| `when_to_use` | Claude Code | More trigger text after the description, inside the 1,536 limit |
| `disable-model-invocation: true` | Claude Code, Pi, OpenCode | Only the user can start the skill. Use it for a skill with side effects. OpenCode also accepts `metadata.opencode/autoinvoke: false`. |
| `user-invocable: false` | Claude Code | Hidden from the menu, and started by the model only |
| `allowed-tools` | Claude Code, Copilot, Pi (experimental) | Pre-approves the tools. OpenCode ignores it, and uses its own permission rule. |
| `context: fork`, `agent`, `paths`, `model`, `effort`, `arguments`, `argument-hint`, `hooks` | Claude Code | Isolated context, path scope, model override, and named arguments |
| `version`, `platforms`, `required_environment_variables`, `metadata.hermes.*` | Hermes | OS filter, secrets prompted at load, and visibility by toolset |

## Side effects on a harness without the switch

The `disable-model-invocation` field is missing on Copilot CLI. The skill must limit its own side effects there.

- OpenCode: use `disable-model-invocation`, or add a rule to the `permissions` array with the action `skill`, the skill ID as the resource, and the effect `ask` or `deny`. A wildcard works.
- Copilot CLI: there is no documented switch for one skill. Put the risky step behind a tool that needs approval.

## Name actions, not tools

The tool names differ per harness. Write "run a command", "read the file", "dispatch a subagent", and "track the todos".

| Action | Claude Code | OpenCode | Copilot CLI | Pi | Hermes |
| --- | --- | --- | --- | --- | --- |
| Run a shell command | `Bash` | `bash` | the shell tool | `bash` | `terminal` |
| Read or edit a file | `Read` / `Edit` | `read` / `edit` | the file view and edit tools | `read` / `edit` | `read_file` / `patch` |
| Dispatch a subagent | `Agent` | `task` | sub-agents | an extension only | `delegate_task` |
| Track the todos | `TodoWrite` | `todowrite` | — | an extension or `TODO.md` | `todo` |

When a capability can be missing, give the fallback: "If no subagent tool is available, do the steps in sequence."

## MCP tools

Name the server and the tool in prose. Do not hard-code one format for an MCP tool name, because the format differs per harness.

## Body features of one harness

Claude Code reads these body features. The other harnesses ignore them, or they show them as literal text. Use them only behind a fallback, or do not use them at all in a portable skill.

| Feature | What Claude Code does | Portable use |
| --- | --- | --- |
| `${CLAUDE_SKILL_DIR}` | Expands to the skill directory | Also write "the directory that contains this SKILL.md". Pi gives the model the skill path, so a relative path works. |
| `$ARGUMENTS`, `$0`, a named `$arg` | Substitutes the arguments of the call | Document the arguments in prose, and define the behaviour with no argument. Pi appends the arguments after `/skill:name` as a user request. |
| `!` then a command in backticks | Shell preprocessing. It injects the live output. | Run the command as a normal step instead. |
| `context: fork`, `agent`, `paths`, `model`, `effort` | Isolated context, path scope, model override | Name the action ("dispatch a subagent"), and give the fallback. |
| `hooks` | Deterministic enforcement | Use a hook only when a portable instruction cannot hold the rule. |

A skill that names the tools of one harness also needs a mapping for the other harnesses. Each of those mappings is a reference file of its own.

## Checklist

- [ ] The skill works with `name`, `description`, `license`, `compatibility`, and `metadata` only.
- [ ] Each extra field is optional, and the skill states its fallback.
- [ ] The body names actions, and not the tools of one harness.
- [ ] The paths are relative to the skill directory.
- [ ] The runtime needs are in `compatibility`.
- [ ] A skill with side effects is user-only, or it explains the guard for each harness.
