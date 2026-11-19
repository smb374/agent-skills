# Skill catalog

This file is the list of skills that this repo installs or plans to install. It replaces the Notion page "Curated personal agent skills".

## Selection rules

1. **Prove the gap.** Keep a skill only when the agent does the job worse without it.
2. **Two kinds of skill.**
   - **Flow**: the user starts it. Its frontmatter has `disable-model-invocation: true`. It costs no listing context.
   - **Knowledge**: the model starts it. Its name and description cost context on every turn. Keep this set small.
3. **Mechanical rules go to tools, not prose.** Use a hook, a permission rule, a linter, or a script for a rule that a regex or a command can check.

## Status values

| Status | Meaning |
| --- | --- |
| done | The skill is in `skills/`. |
| vendor | `install.sh` adds the upstream skill unchanged. The skill is listed in `vendor.txt`. |
| fork | Todo. Copy the upstream skill into `skills/`, then change it. See `CONTRIBUTING.md`. |
| own | Todo. Write the skill with `skill-writer`. |
| pi-config | The skill lives in the Pi config repo, because it needs Pi agents. This repo does not install it. |
| undecided | Not decided yet. See Open decisions. |
| none | The step needs no skill. |

## Lifecycle

| Stage | Step | Skill | Kind | Source | Status |
| --- | --- | --- | --- | --- | --- |
| 0 Bootstrap | AGENTS.md, CONTRIBUTING.md, issue tracker, docs layout | `setup-project` (name TBD) | flow | Own. Reuse the tracker and label part of `setup-matt-pocock-skills`. | own |
| 1 Intake | Epic to specs | `wayfinder` | flow | mattpocock/skills | vendor |
| 1 Intake | Interview, used in every stage | `grilling` | knowledge | mattpocock/skills, with the Pi fork changes in harness-neutral words | done |
| 1 Intake | Interview entry points | `grill-me`, `grill-with-docs` | flow | mattpocock/skills | vendor |
| 1 Intake | Glossary and ADRs | `domain-modeling` | knowledge | mattpocock/skills | vendor |
| 1 Intake | Spec, then tickets | `to-spec`, `to-tickets` | flow | mattpocock/skills | vendor |
| 2 Tickets | Scout, brief, worker, verify, review, commit | `implement-flow`, `implement-spec-flow`, `plan-ticket-impl`, `agent-handoff` | flow | Pi config repo | pi-config |
| 2 Tickets | Code writing | `tdd`, `diagnosing-bugs`, `codebase-design` | knowledge | mattpocock/skills | vendor |
| 3 PR | Find the target issue and its sub-issues. Else ask the user, or use the branch commits | A step in `pr-writer`, with `gh` commands | — | Own | done |
| 3 PR | PR body | `pr-writer` | knowledge, started by the user or another flow | getsentry/skills (Apache-2.0). Change it to Conventional Commits titles. | done |
| 3 PR | PR operations | No skill. The model already knows `gh`. | — | — | none |
| 3 PR | PR review | `pr-review` | flow | Pi config repo | pi-config |
| 4 Issues | Triage, then tickets, then stage 2 | `triage`, then `to-tickets` | flow | mattpocock/skills | vendor |
| Meta | Skill authoring | `skill-writer` | knowledge | getsentry/skills (Apache-2.0), with the public supplement | done |
| Meta | AGENTS.md, CLAUDE.md, disclosed docs, agent briefs, system prompts, tool descriptions, error and hook messages | `writing-agent-docs` | knowledge | mattpocock/skills `writing-for-agents` (MIT), rewritten and extended with vendor research. `skill-writer` sends these requests to it. | done |

## Cross-cutting skills

| Group | Skill | Kind | Source | Status |
| --- | --- | --- | --- | --- |
| Writing and coding style | `asd-ste100` | knowledge | danyuchn/asd-ste100-skill (MIT). Narrow the description: it rewrites given text, and `writing-agent-docs` writes whole agent documents. | done |
| Writing and coding style | `ponytail` | knowledge | DietrichGebert/ponytail @ `96608e0` (MIT), with the Pi config changes | done |
| Misc | `teach` | flow | mattpocock/skills | vendor |
| Misc | `research` | knowledge | mattpocock/skills. Add a fallback for a harness with no subagent tool. | done |
| Misc | `wait-what` | flow | mattpocock/skills | undecided |

## Not kept

ask-matt, code-review, feature-plan, find-skills, handoff, implement, implement-spec, improve-codebase-architecture, pr, prototype, resolving-merge-conflicts, retro, to-questionnaire, typesafe-ai, wizard, writing-for-agents.

- `feature-plan` duplicates `to-spec` and `plan-ticket-impl`.
- `code-review` duplicates the review in `pr-review` and `implement-flow`.
- `writing-for-agents` splits into `skill-writer` (skills) and `writing-agent-docs` (other agent documents).
- The Pi flows and agents replace `implement`, `implement-spec`, and `handoff`.

## Open decisions

1. The name of the setup skill. The suggestion is `setup-project`.
2. `wayfinder`, `to-spec`, `to-tickets`, and `triage` tell the user to run `/setup-matt-pocock-skills` when no tracker is configured. That skill is not kept. Options:
   - `setup-project` writes the same tracker and label docs, so the message does not show.
   - Fork the four skills, and change the message to name `setup-project`.
   - Keep `setup-matt-pocock-skills` as a vendor skill until `setup-project` exists.
3. Branch to tickets: should `setup-project` enforce a `Refs: #N` commit footer with a hook or commitlint, or only write a CONTRIBUTING.md convention?
4. Keep `wait-what`?
5. Skill-to-skill references. Sentry `design-principles.md` says "Do not require another skill by name at runtime." But `grill-me` and `grill-with-docs` exist only to start `grilling`. Options: refer by name and accept the coupling, use a sibling path, or merge the entry points into `grilling`.
6. `plan-ticket-impl`: a separate skill, or a step in `implement-flow`? The Pi config repo decides this.

## Install target

`install.sh` puts the skills in `~/.agents/skills/`. Pi, OpenCode, Codex, Copilot CLI, and Hermes read that directory. For Claude Code, run `./install.sh --dir ~/.claude/skills --agent claude-code`.

## Sources

- [vercel-labs/skills: supported agents](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) (the global directory of each agent)
- [vercel-labs/skills: creating-skills.md](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md) (the discovery layout)
- [getsentry/skills skill-writer @ a582c51](https://github.com/getsentry/skills/tree/a582c51ee29d0f35e6ac321340796f77d43da733/skills/skill-writer)
- Licenses checked with `gh repo view`: mattpocock/skills MIT, getsentry/skills Apache-2.0, obra/superpowers MIT.
