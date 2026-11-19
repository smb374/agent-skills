# writing-agent-docs provenance

The skill is a rewrite of the mattpocock `writing-for-agents` skill, without its skill-specific parts. Research from vendor docs extends it. The rewrite is close to the upstream text in `references/levers.md`, so the upstream MIT license is in `LICENSE`.

## Upstream

- repository: mattpocock/skills, https://github.com/mattpocock/skills
- path: `skills/productivity/writing-for-agents`
- commit: 321658273cb1d20b76026717d027d505790106d4 (3216582)
- license: MIT, see `LICENSE`
- status: derived (rewrite)

## Sources

The research brief `docs/research/writing-agent-docs.md` (repo root) holds the quotes and the full source table. The tags below match it.

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| [MP] mattpocock/skills `writing-for-agents` @ 3216582 | code | secondary | 2026-11-19 | the levers: pointers, two loads, hierarchy, completion criteria, leading words, negation, pruning | MIT |
| [CC-Mem] https://docs.claude.com/en/docs/claude-code/memory | documentation | primary | 2026-11-19 | the 200-line advice, `@path` loads eagerly, AGENTS.md handling, prose is not enforcement, add a rule on a repeated mistake | none recorded |
| [OAI-Agents] https://developers.openai.com/codex/guides/agents-md | documentation | primary | 2026-11-19 | the Codex discovery, merge order, and 32 KiB cap | none recorded |
| [AGENTS-MD] https://agents.md/ | specification | primary | 2026-11-19 | the closest file wins, no required structure | none recorded |
| [Pi] Pi `docs/configuration.md`, lines 18 and 43-45 | documentation | primary | 2026-11-19 | the Pi file names, discovery, and override rule | none recorded |
| [CC-Sub] https://docs.claude.com/en/docs/claude-code/sub-agents | documentation | primary | 2026-11-19 | the description as trigger, the body as prompt, the cold start of a subagent | none recorded |
| [AT-Best] https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices | documentation | primary | 2026-11-19 | soften emphasis, positive phrasing, explain why, explicit action, over-delegation, stale prompts | none recorded |
| [OAI-GPT5] https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide | documentation | primary | 2026-11-19 | the cost of a contradiction, stop conditions, the missing-facts policy, the over-emphasis case | none recorded |
| [OAI-Codex] https://cookbook.openai.com/examples/gpt-5/codex_prompting_guide | documentation | primary | 2026-11-19 | AGENTS.md as user messages, tool names, model-specific status rules | none recorded |
| [AT-Tools] https://www.anthropic.com/engineering/writing-tools-for-agents | documentation | primary | 2026-11-19 | the new-hire framing, names, truncation lines, fix misuse in the description | none recorded |
| [AT-ToolUse] https://docs.claude.com/en/docs/agents-and-tools/tool-use/implement-tool-use | documentation | primary | 2026-11-19 | the description parts, 3-4 sentences, input examples, explanation not reasoning | none recorded |
| [AT-Handle] https://docs.claude.com/en/docs/agents-and-tools/tool-use/handle-tool-calls | documentation | primary | 2026-11-19 | the instructive error message | none recorded |
| [CC-Hooks] https://docs.claude.com/en/docs/claude-code/hooks | documentation | primary | 2026-11-19 | the hook channels that reach the model | none recorded |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| shape: reference-backed router, 5 steps, 4 references, no script | the 4 document groups have different loads and channels | adopted |
| system prompts and briefs share `agent-prompts.md` | an agent body is a system prompt, and a brief is its first message | adopted |
| `levers.md` is a separate copy, not shared with `skill-writer` | a skill must stand alone. See Shared rules | adopted |
| emphasis is model-relative: strengthen on under-action, soften on over-action | [AT-Best], [OAI-GPT5]. Replaces the [MP] rule "use a stronger word" | adopted |
| prose-or-enforcement lever | [CC-Mem] | adopted |
| contradiction check and model audit in the pruning pass | [OAI-GPT5], [AT-Best] | adopted |
| the cache lever wins over the agents.md advice to list commands | [MP], [CC-Mem]. agents.md and `/init` disagree | adopted |
| size target: 200 lines and 32 KiB, marked as vendor advice | [CC-Mem], [OAI-Agents]. No measured study | adopted |
| one harness table for instructions files. A portable rule for hooks, with Claude Code as one example | the hook channels differ by harness and change often | adopted |
| tiered test bar | the cost of a test must scale with the change | adopted |
| one inline STE rule, no runtime use of `asd-ste100` | a skill must stand alone | adopted |
| Pi templates for briefs stay in the Pi `agent-handoff` skill | this repo holds portable skills only | adopted |
| MCP server instructions | out of scope | rejected |
| the trigger split with `asd-ste100` | see `docs/catalog.md` Open decisions | deferred |
| the skill mechanics of [MP] (`SKILL-MECHANICS.md`) | `skill-writer` covers skills | rejected |

## Shared rules

`skill-writer` holds a copy of these rules. When you change one here, check the other copy.

| Rule | Here | In skill-writer |
| --- | --- | --- |
| Simplified Technical English | `SKILL.md` Critical rules | `references/writing-rules.md` Simplified Technical English |
| placement: skill, instructions file, hook, nothing | `SKILL.md` Step 2 | `SKILL.md` Step 1 |
| replaced, narrowed, moved, deleted, added | `SKILL.md` Step 4 | `references/writing-rules.md` The precision pass |
| positive target, ban with a safe path | `references/levers.md` The positive target | `references/writing-rules.md` Match the form to the failure |
| emphasis and all-caps words | `references/levers.md` Emphasis is model-relative | `references/writing-rules.md` State the reason, and its strength |
| one sentence of reason | `references/levers.md` The reason behind a rule | `references/writing-rules.md` State the reason, and its strength |
| one meaning in one place | `references/levers.md` Single source of truth | `references/writing-rules.md` Keep or cut |
| do not restate the environment | `references/levers.md` The environment is a cache source | `references/writing-rules.md` Structure troubleshooting |
| `@path` loads eagerly | `references/instructions-files.md` Disclosed docs | `references/writing-rules.md` Structure rules |
| test with and without the document | `SKILL.md` Step 5 | `references/testing.md` |
| the four-part output contract | `SKILL.md` Output contract | `SKILL.md` Output contract |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| instructions files: Claude Code, Codex, Pi, agents.md | complete | none |
| instructions files: Cursor, Gemini CLI, Copilot | partial: not researched | read their docs when a user needs them |
| hook channels other than Claude Code | partial: a portable rule only | add a row when a second harness needs it |
| agent briefs: "Building effective agents" and the Claude Code best-practices page | partial: not read | read both, and compare with `agent-prompts.md` |
| a measured study of file length and adherence | missing | search for one study, then keep or drop the size target |
| baseline runs with and without the skill | missing | run 2 or 3 prompts per document type |

## Local changes

- Remove the skill-specific parts of [MP]: `SKILL-MECHANICS.md`, invocation, and router skills.
- Rewrite each lever in Simplified Technical English, and add one bad and one good example to each.
- Replace the [MP] rule "use a stronger word" with model-relative emphasis.
- Add 3 levers from the research: prose or enforcement, the contradiction check, and the model audit.
- Add the steps, the router, and the references for instructions files, agent prompts, and tool messages.
