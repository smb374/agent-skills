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
| 0 Bootstrap | AGENTS.md, CONTRIBUTING.md, issue tracker, labels, docs layout, commit hooks | `setup-project` | flow | mattpocock/skills `setup-matt-pocock-skills` (MIT). GitHub or "other" tracker only. Add AGENTS.md, CONTRIBUTING.md, GitHub labels, and pre-commit hooks for the commit header and the issue footer. | done |
| 1 Intake | Epic to specs | `wayfinder` | flow | mattpocock/skills. Point it at `setup-project`. Load skills by name, not with the Skill tool. | done |
| 1 Intake | Interview, used in every stage | `grilling` | knowledge | mattpocock/skills, with the Pi fork changes in harness-neutral words | done |
| 1 Intake | Interview entry points | `grill-me`, `grill-with-docs` | flow | mattpocock/skills | vendor |
| 1 Intake | Glossary and ADRs | `domain-modeling` | knowledge | mattpocock/skills | vendor |
| 1 Intake | Spec, then tickets | `to-spec`, `to-tickets` | flow | mattpocock/skills. Point them at `setup-project`. | done |
| 2 Tickets | Scout, brief, worker, verify, review, commit | `implement-flow`, `implement-spec-flow`, `plan-ticket-impl` | flow | Pi config repo. `plan-ticket-impl` wraps `to-impl-plan` with the plan review and the Pi Builder contract. | pi-config |
| 2 Tickets | Plan in builder stages, for a ticket too big for one builder run or a run that went wrong | `to-impl-plan` | knowledge, started by the user or a flow | Own, ported from the Pi `plan-ticket-impl`. Ships the plan template, the contract partial, and `fill`. | done |
| 2 Tickets | Code writing | `tdd`, `diagnosing-bugs`, `codebase-design` | knowledge | mattpocock/skills | vendor |
| 3 PR | Find the target issue and its sub-issues. Else ask the user, or use the branch commits | A step in `pr-writer`, with `gh` commands | — | Own | done |
| 3 PR | PR body | `pr-writer` | knowledge, started by the user or another flow | getsentry/skills (Apache-2.0). Change it to Conventional Commits titles. | done |
| 3 PR | PR operations | No skill. The model already knows `gh`. | — | — | none |
| 3 PR | PR review | `pr-review` | flow | Pi config repo | pi-config |
| 4 Issues | Triage, then tickets, then stage 2 | `triage`, then `to-tickets` | flow | mattpocock/skills. Point `triage` at `setup-project`. Load skills by name, not with the Skill tool. | done |
| Meta | Skill authoring | `skill-writer` | knowledge | getsentry/skills (Apache-2.0), with the public supplement | done |
| Meta | AGENTS.md, CLAUDE.md, disclosed docs, agent briefs, system prompts, tool descriptions, error and hook messages | `writing-agent-docs` | knowledge | mattpocock/skills `writing-for-agents` (MIT), rewritten and extended with vendor research. `skill-writer` sends these requests to it. | done |

## Cross-cutting skills

| Group | Skill | Kind | Source | Status |
| --- | --- | --- | --- | --- |
| Writing and coding style | `asd-ste100` | knowledge | danyuchn/asd-ste100-skill (MIT). Narrow the description: it rewrites given text, and `writing-agent-docs` writes whole agent documents. | done |
| Writing and coding style | `ponytail` | knowledge | DietrichGebert/ponytail @ `96608e0` (MIT), with the Pi config changes | done |
| Code graph | `codebase-memory` | knowledge | Own, ported from the Pi config skill. It names the `codebase-memory-mcp` tools by their MCP names. | done |
| Agent handoff | `handoff` | knowledge | Own, derived from mattpocock/skills `handoff` (MIT). Ships the session template and `fill`. | done |
| Misc | `teach` | flow | mattpocock/skills | vendor |
| Misc | `research` | knowledge | mattpocock/skills. Add a fallback for a harness with no subagent tool. | done |
| Misc | `wait-what` | flow | mattpocock/skills | vendor |

## Not kept

ask-matt, code-review, feature-plan, find-skills, handoff, implement, implement-spec, improve-codebase-architecture, pr, prototype, resolving-merge-conflicts, retro, to-questionnaire, typesafe-ai, wizard, writing-for-agents.

- `feature-plan` duplicates `to-spec` and `plan-ticket-impl`.
- `code-review` duplicates the review in `pr-review` and `implement-flow`.
- `writing-for-agents` splits into `skill-writer` (skills) and `writing-agent-docs` (other agent documents).
- The Pi flows and agents replace `implement` and `implement-spec`.
- The own `handoff` replaces upstream `handoff`.

## Open decisions

None.

## Resolved decisions

1. Skill-to-skill references. Sentry `design-principles.md` says "Do not require another skill by name at runtime." Decision: refer by name and accept the coupling. The forks `wayfinder`, `to-spec`, `to-tickets`, and `triage` tell the user to run `/setup-project`, a setup workflow, not knowledge. The vendored `grill-me`, `grill-with-docs`, and `tdd` keep "call the Skill tool", because they work in Pi as intended.
2. `plan-ticket-impl`: a separate skill, or a step in `implement-flow`? Decision: it splits into the portable `to-impl-plan` in this repo and a Pi wrapper `plan-ticket-impl` in the Pi config repo.

## Install target

`install.sh` puts the skills in `~/.agents/skills/`. Pi, OpenCode, Codex, Copilot CLI, and Hermes read that directory. For Claude Code, run `./install.sh --dir ~/.claude/skills --agent claude-code`.

## Sources

- [vercel-labs/skills: supported agents](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) (the global directory of each agent)
- [vercel-labs/skills: creating-skills.md](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md) (the discovery layout)
- [getsentry/skills skill-writer @ a582c51](https://github.com/getsentry/skills/tree/a582c51ee29d0f35e6ac321340796f77d43da733/skills/skill-writer)
- Licenses checked with `gh repo view`: mattpocock/skills MIT, getsentry/skills Apache-2.0, obra/superpowers MIT.
