# skill-writer provenance

The skill is a new, smaller skill. It is a rewrite, and not a vendored copy.

## Upstream

- repository: getsentry/skills, https://github.com/getsentry/skills
- path: `skills/skill-writer`
- commit: a582c51ee29d0f35e6ac321340796f77d43da733 (a582c51)
- license: Apache-2.0, see `LICENSE`
- status: derived (rewrite)

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| [spec] Agent Skills specification, https://agentskills.io/specification | specification | primary | see the note below | the portable core fields, the name pattern, the length limits | none recorded |
| [A] Anthropic skill authoring best practices, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | documentation | primary | see the note below | the baseline, the reference depth, the name rules, the two-agent loop | none recorded |
| [CC] Claude Code skills, https://code.claude.com/docs/en/skills | documentation | primary | see the note below | the harness paths, the fields of one harness, the context cost | none recorded |
| [OC] OpenCode skills, https://opencode.ai/docs/skills/ | documentation | primary | see the note below | the harness paths, the permission rule for a skill | none recorded |
| [GH] GitHub Copilot agent skills, https://docs.github.com/en/copilot/concepts/agents/about-agent-skills | documentation | primary | see the note below | the harness paths, the tool approval | none recorded |
| [Pi] Pi skills, https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md | documentation | primary | see the note below | the harness paths, the skill path in the prompt, the silent drop of bad frontmatter | none recorded |
| [HA] Hermes Agent skills, https://hermes-agent.nousresearch.com/docs/user-guide/features/skills | documentation | primary | see the note below | the harness paths, the load-time secrets, the toolset rules | none recorded |
| [WS] obra/superpowers `writing-skills` 6.4.1, https://github.com/obra/superpowers | code | secondary | see the note below | the form-to-failure table, the nuance clause, the interpreter call | MIT |
| [SC] anthropics/skills `skill-creator` @ d182ca456ca0, https://github.com/anthropics/skills | code | secondary | see the note below | the too-long warning, the examples design | none recorded |

The rules come from the compiled supplement. This rewrite did not fetch the public URLs again, so the retrieval date is not recorded. Check a harness fact before you rely on it.

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| shape: reference-backed router with one script | the upstream router, plus the 7 steps of the supplement | adopted |
| spec sources and decisions merge into `PROVENANCE.md` | one maintenance file costs less than two | adopted |
| the evaluation files of the upstream skill are removed | the skill has no evaluation set of its own | adopted |
| the Claude-only reference files are removed | a portable skill must not depend on one harness | adopted |
| the rules of the supplement merge into the references | the upstream skill does not cover a cross-harness rule | adopted |
| the validator keeps its checks and gains the spec checks | the supplement asks for both validators in the repo gate | adopted |
| a near-miss route to `writing-agent-docs` | the description must route the near-miss case | adopted |
| a one-off fix gets no skill | a skill is not the record of one repair | adopted |
| the prose is in Simplified Technical English | a model parses this text with no human to resolve an ambiguity | adopted |
| a per-harness tool-name reference file | no mapping file exists in this repo yet | deferred |

## Shared rules

`writing-agent-docs` holds a copy of some writing rules of this skill. The list of the shared rules is in `skills/writing-agent-docs/PROVENANCE.md`, section Shared rules. When you change one of them here, check the other copy.

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| the source provenance of the upstream skill | complete | none |
| the precision pass, the writing rules, and the output contracts | complete | none |
| the transformed examples of a skill-authoring skill | partial: the references hold the shapes, and not one full worked example | add one worked example when a second skill under `skills/` shows the need |
| registration and validation | complete | none |
| the one-shot run of each harness | partial: only the Claude Code row was tried | run each other row with its `--help` |

## Local changes

- Remove each reference file that only Claude Code reads, and each router row that named one.
- Remove the evaluation files: `EVAL.md`, `evals/`, and `skill-evals.md`.
- Replace `SPEC.md` and `SOURCES.md` with one `PROVENANCE.md` per skill. The template is `references/provenance-template.md`.
- Merge the rules of the public supplement into the references: the cross-harness paths and fields, the portable core, the description rules, the body forms, the scripts, the testing, and the maintenance.
- Merge the upstream reference files into 8 focused files, and keep one router table in `SKILL.md`.
- Remove the shapes that need one harness: the forked subagent and the hook-backed skill.
- Extend `scripts/quick_validate.py` with the name pattern, the name length, the description length, the line count, and the `PROVENANCE.md` reference.
- Write each file in Simplified Technical English.
- Add the Apache-2.0 notice of change to each derived file.
