## Commands

- Format: just fmt
- Test: just test
- Check (lint, format, test, skill validation): just check
- Install the skills: just install (copy) or just link (symlink)
- Eval one skill (costs money): just eval <skill>

## Agent skills

### Issue tracker

GitHub Issues of smb374/agent-skills, through `gh`. See `docs/agents/issue-tracker.md`.

### Issue types

Each issue has one `type:*` label and a matching title prefix: `[Epic]`, `[Bug]`, `[Feature]`, `[Task]`, `[Ticket]`. Wayfinder child issues have no `type:*` label and use `[WF]`. See `docs/agents/issue-types.md`.

### Triage labels

The five default labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the root. See `docs/agents/domain.md`.

### Commits

Conventional Commits with an issue footer (`Refs: #N`, `Fixes #N`). See `CONTRIBUTING.md`.
