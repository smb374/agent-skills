# code-review provenance

## Upstream

- repository: mattpocock/skills
- path: skills/engineering/code-review/SKILL.md
- commit: 7739eaed7f8f3915437a8def198a6d0d7206dbc7 (7739eae)
- license: MIT
- status: derived

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| [mattpocock/skills code-review @ 7739eae](https://github.com/mattpocock/skills/blob/7739eaed7f8f3915437a8def198a6d0d7206dbc7/skills/engineering/code-review/SKILL.md) | code | primary | 2026-11-26 | the spec and standards axes, no merge or rerank across axes, the Fowler smell baseline, the order to find the spec, the standards files | MIT. `LICENSE` is a copy of the upstream license |
| Pi config repo `skills/agent-handoff/reviewer.md` @ 971c150 | code | primary | 2026-11-26 | the checks table, the finding fields, severity, certainty, guard, probes, the verdict rule, the report shape, the plan axis (moved to `to-impl-plan/references/plan-review.md`) | own |
| Pi config repo `skills/pr-review/SKILL.md` @ 971c150 | code | primary | 2026-11-26 | the Big definition, `claimed` and `context` tickets, the comment amendment rule | own |
| [openai/codex `codex-rs/core/review_prompt.md` @ ba2b67f](https://github.com/openai/codex/blob/ba2b67f9cda954bcdda43c2a65ac58e807b996bd/codex-rs/core/review_prompt.md) | code | primary | 2026-11-26 | the flag bar: introduced by the change, discrete and actionable, provable impact, not intentional, no more rigor than the codebase | Apache-2.0. Ideas only, no text copied |
| [Claude Code: Code Review](https://code.claude.com/docs/en/code-review) | documentation | primary | 2026-11-26 | correctness as the default focus, read the review rules from the base branch and never from the change | ideas only |
| [obra/superpowers `requesting-code-review/code-reviewer.md` @ 5bf4e78](https://github.com/obra/superpowers/blob/5bf4e78011075bcfc0dc295f0724994cd123ee71/skills/requesting-code-review/code-reviewer.md) | code | primary | 2026-11-26 | the Declined to judge list, the read-only rule with a separate worktree | MIT. Ideas only |
| [Google eng-practices: What to look for](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | documentation | primary | 2026-11-26 | the test-quality check: a test must fail when the code is broken | CC-BY 3.0. Ideas only |
| [getsentry/skills code-review](https://github.com/getsentry/skills/blob/main/skills/code-review/SKILL.md) | code | secondary | 2026-11-26 | the correctness areas: runtime errors, queries in a loop, backward compatibility, security | Apache-2.0. Ideas only |
| ponytail skill in this repo | code | primary | 2026-11-26 | the smells Reinvented Helper, Needless Dependency, What Comment | MIT |
| smb374/agent-skills #14 | specification | primary | 2026-11-26 | the scope and the decisions below | none |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| a knowledge skill whose `SKILL.md` is the standard, with a short manual procedure at the end | #14. Most of the content is rules, not steps | adopted |
| three axes: spec, standards, correctness | #14. A defect that breaks no AC and no rule had no reviewer | adopted |
| merge correctness into spec | the spec axis is skipped when no spec exists, so a change with no ticket gets no bug review | rejected |
| spec checks only the literal ACs, plus a Declined to judge list | #14. Flows need literal ACs. The list stops silent drops | adopted |
| the superpowers rule that a reasonable-user expectation is a requirement | #14. It makes pass and fail less exact | rejected |
| ponytail smells in the default baseline | #14 | adopted |
| the Pi finding schema and report shape as the shared shape | #14. No other source has a checkable schema | adopted |
| the Pi brief fields (Skip, Decide, Prior report, Re-review, Gate output path) and the escalation triggers | they are Pi orchestration | rejected, they stay in the Pi config repo |
| confidence scores and P0–P3 priorities from Codex | severity plus certainty plus probes covers the same need | rejected |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | partial: `evals/code-review/` has a case, not run yet | run `just eval code-review` |
| trigger check with near-miss queries | missing | run the trigger loop of skill-writer when a trigger failure shows |
| source of the Anthropic `/code-review` command | missing: the fetch returned no content | read `anthropics/claude-code` `plugins/code-review/commands/code-review.md` |

## Local changes

- Rewrite the upstream text in Simplified Technical English.
- Replace the free-form axis reports with the checks table and the finding fields of the Pi reviewer template.
- Add the correctness axis, the flag bar, the base-ref rule, the Declined to judge list, the Big definition, and the dedup rule.
- Add three ponytail smells to the Fowler baseline.
- Remove the word limits and the foreground subagent rule of the upstream text.
