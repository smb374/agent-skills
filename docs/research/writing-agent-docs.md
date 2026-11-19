# Research: writing-agent-docs skill

Retrieved 2026-11-19 (from the sandbox clock, since no shell was available for `date`). All vendor docs are live pages. They change often, and several name models and versions that I could not check (for example "Claude Fable 5.2", "gpt-5.3-codex"). Re-check version-specific claims before you copy them into the skill.

Base read first: `/home/thomas.chen@canonical.com/.agents/skills/writing-for-agents/SKILL.md` (mattpocock base). Findings below mark what is **NEW** (the base lacks it), **CONFIRMS** (the base already says it, now with a vendor source), or **CONFLICT** (see the Conflicts section).

## Summary

- **Instructions are context, not enforcement.** Claude Code says CLAUDE.md is "context, not enforced configuration". A rule that must always run belongs in a hook. The skill needs a "write it as prose or as a hook?" test. (NEW)
- **`@path` imports do not disclose.** In Claude Code they load eagerly with the importing file and "don't reduce its context cost". A disclosed doc needs a plain-text pointer, not `@`. The base never separates the two. (NEW, and it affects the pointer lever)
- **Harnesses differ in discovery.** Claude Code loads parent-directory files at launch, loads subdirectory files lazily, and concatenates all of them. Codex walks root to cwd, takes one file per directory, and caps the total at 32 KiB. The agents.md spec says "closest wins". Claude Code says conflicting files make Claude "pick one arbitrarily". A portable doc must never rely on override. (NEW)
- **Size limits differ.** Claude Code: under 200 lines per file. Codex: 32 KiB combined (`project_doc_max_bytes`). agents.md: no limit. The skill should give a line target and a byte ceiling. (NEW)
- **Contradictions cost more on newer models.** OpenAI says GPT-5 "expends reasoning tokens searching for a way to reconcile the contradictions". Claude Code says the same, in softer words. This strengthens the base's single-source-of-truth rule. (CONFIRMS, with a stronger reason)
- **Emphasis is model-relative, and it can backfire.** Anthropic: soften "CRITICAL: You MUST" to "Use this tool when". Cursor/OpenAI: a `maximize_` prefix made GPT-5 overuse tools. The base's fix for a weak leading word ("a stronger word") can overtrigger. (CONFLICT)
- **Tool descriptions are the top lever, and they run long.** The API doc says detailed descriptions are "by far the most important factor"; aim for 3-4 sentences or more. But subagent descriptions (always loaded) must stay short, with the detail in the body. The rule is: detail goes where the load is paid only when needed. (NEW, and it ties to the two-loads lever)
- **Error and hook text is a prompt.** Anthropic: write errors that say what went wrong and what to try next. For hooks, only some channels reach the model: exit 2 stderr, and plain stdout on `UserPromptSubmit`/`SessionStart`. Stderr on exit 0 is never seen. (NEW)
- **A subagent sees only its own prompt.** It gets its body text plus basic environment details, not the parent's system prompt. `omitClaudeMd` can also drop CLAUDE.md. A brief must therefore be self-contained. (NEW)
- **Keep the 4-file layout.** Add a harness-delivery table (see Structure impact).

## Findings

### references/levers.md (shared craft)

1. **Write instructions that a reviewer can verify.**
   - Quote: "Write instructions that are concrete enough to verify: 'Use 2-space indentation' instead of 'Format code properly'".
   - Source: [CC-Mem]. CONFIRMS the base's completion-criterion lever; adds worked examples.
2. **Contradictions are costly. Audit for them.**
   - Quote (OpenAI): "poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5 than to other models, as it expends reasoning tokens searching for a way to reconcile the contradictions".
   - Quote (Anthropic): "if two instructions contradict each other, Claude may pick one arbitrarily."
   - Sources: [OAI-GPT5], [CC-Mem]. Strengthens single source of truth. Add a "find contradictions" pass to pruning.
3. **Explain the why behind a rule.**
   - Quote: "Providing context or motivation behind your instructions ... can give Claude more information about your goals".
   - Source: [AT-Best]. NEW. The base says comments need a why the code cannot show; this extends it to prompts.
4. **Positive phrasing: Anthropic confirms the base.**
   - Quote: "Tell Claude what to do instead of what not to do. Instead of: 'Do not use markdown in your response' Try: 'Your response should be composed of smoothly flowing prose paragraphs.'"
   - Source: [AT-Best]. CONFIRMS. The same page also says to match prompt style to the output style you want.
5. **Test a doc on a cold reader.**
   - Quote: "Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too."
   - Source: [AT-Best]. NEW as a concrete test. It fits the base's "settle by running it".
6. **Calibrate emphasis per model. Do not stack it.**
   - Quote: "Where you might have said 'CRITICAL: You MUST use this tool when...,' you can use more normal prompting such as 'Use this tool when...' instead."
   - Source: [AT-Best]. See Conflicts for the OpenAI counterpoint.
7. **Re-audit old instructions when the model changes.**
   - Quote: "verification instructions carried over from prompts tuned for earlier models can cause over-verification ... remove these instructions rather than rewriting them."
   - Source: [AT-Best]. NEW. Extends the base's no-op test: an instruction can turn from useful to harmful, not only to a no-op. Claude Code also ships `/doctor prompt-audit`, which looks for "instructions written for older models" ([CC-Mem]).
8. **Prose rules are not enforcement. Use a hook for must-run rules.**
   - Quote: "If the instruction is something that must run at a specific point, such as before every commit or after each file edit, write it as a hook instead."
   - Source: [CC-Mem]. NEW. Also: "To block an action regardless of what Claude decides, use a PreToolUse hook instead."
9. **Name state in files, not in conversation, for long work.**
   - Quote: "Claude's latest models are extremely effective at discovering state from the local filesystem." Use structured formats (JSON) for state, free text for notes.
   - Source: [AT-Best]. Supports the base's "environment as cache". Low priority for this skill.
10. **Comments for maintainers can be free.**
    - Quote: "Block-level HTML comments in CLAUDE.md files are stripped before the content is injected into Claude's context."
    - Source: [CC-Mem]. NEW but Claude-Code-only. Codex and others may not strip them. Do not rely on it in a portable doc.

### references/instructions-files.md

1. **Keep each file short: under 200 lines (Claude Code).**
   - Quote: "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."
   - Source: [CC-Mem]. Codex limit is bytes: "stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)" ([OAI-Agents]). Use "under 200 lines and under 32 KiB combined" as the portable target. (Researcher inference: the two limits measure different things, so state both.)
2. **Imports organize, they do not disclose.**
   - Quote: "Imports help you organize a long file but don't reduce its context cost, because imported files load together with the CLAUDE.md that imports them."
   - Source: [CC-Mem]. NEW. Imports go up to four hops deep. Backticks stop an `@` from importing. A sentence "see docs/x.md" is a plain pointer that the agent may or may not follow ([CC-Mem]: "Claude sees AGENTS.md only if it decides to open the file").
3. **Move part-codebase rules out of the root file.**
   - Quote: "If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a skill or a path-scoped rule instead."
   - Source: [CC-Mem]. Skills are out of scope here. The portable form is a nested AGENTS.md (agents.md and Codex both support it) or a pointer to a disclosed doc.
4. **Nested files: the harnesses differ.**
   - agents.md: "the closest one takes precedence"; "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything." ([AGENTS-MD])
   - Codex: "Codex concatenates files from the root down ... Files closer to your current directory override earlier guidance because they appear later in the combined prompt." It includes "at most one file per directory", and `AGENTS.override.md` wins over `AGENTS.md` in the same directory ([OAI-Agents]).
   - Claude Code: "All discovered files are concatenated into context rather than overriding each other." Subdirectory files load "once Claude reads, writes, or edits another file in that subdirectory" ([CC-Mem]).
   - Portable rule (researcher inference): treat "override" as order, not as removal. A child file adds to the parent. It must not contradict it.
5. **Claude Code reads AGENTS.md only in some cases.**
   - Quote: "By default Claude reads AGENTS.md only when you have no CLAUDE.md or CLAUDE.local.md in your working directory or above it."
   - Source: [CC-Mem]. Fix: a `CLAUDE.md` containing `@AGENTS.md` (works on Windows; a symlink does not reliably). Do not write "read AGENTS.md" in prose; the doc says that fails.
6. **AGENTS.md has no required structure.**
   - Quote: "No. AGENTS.md is just standard Markdown. Use any headings you like".
   - Source: [AGENTS-MD]. The site's own example lists setup, style and test commands. Per the base's cache lever, those commands are worth listing only when no config file shows them.
7. **Put the rule where it is seen, in a form the agent can run.**
   - Quote: "Will the agent run testing commands found in AGENTS.md automatically? Yes—if you list them."
   - Source: [AGENTS-MD]. A command given in full is a completion criterion.
8. **Add a rule when a mistake repeats, not before.**
   - Quote: "Add to it when: Claude makes the same mistake a second time ... A code review catches something Claude should have known".
   - Source: [CC-Mem]. NEW as a pruning-in rule (a gate on what enters the file). It matches the user's own corrections rule in the global AGENTS.md.
9. **Rules for review need a safe path.**
   - Quote: "Keep rules concise, explain the behavior to flag and any safe path or exception, and reserve formatting and lint checks for CI."
   - Source: [OAI-Agents]. Confirms "ban plus positive target" and "do not restate what a tool enforces".
10. **How the file reaches the model differs.**
    - Claude Code: "CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself" ([CC-Mem]).
    - Codex: "Each discovered file becomes its own user-role message that starts with # AGENTS.md instructions for" ([OAI-Codex]).
    - Same channel in both: a user message. So "system prompt" wording inside AGENTS.md is wrong. Do not tell the agent it is a system prompt.

### references/agent-prompts.md

1. **A subagent's description is a context pointer. Keep it short.**
   - Quote: "Claude uses each subagent's description to decide when to delegate tasks." and "Trim the description fields of your subagents, and move detail into each subagent's system prompt, which only loads when that subagent runs."
   - Source: [CC-Sub]. CONFIRMS the base's pointer lever almost word for word. The example in the same doc is "Expert code reviewer. Use proactively after code changes." (trigger words in the description).
2. **A subagent sees only its own prompt.**
   - Quote: "Subagents receive only this system prompt plus basic environment details like the working directory, not the Claude Code system prompt."
   - Source: [CC-Sub]. So the brief must carry the goal, the scope, the completion criterion and the report shape. `omitClaudeMd`: "Use it for subagents that take everything they need from the delegation prompt."
3. **Context isolation is the reason to delegate.**
   - Quote: "Use one when a side task would flood your main conversation with search results, logs, or file contents you won't reference again: the subagent does that work in its own context and returns only the summary."
   - Source: [CC-Sub]. Supports the base's "hide later steps across a real context boundary". Write the brief so the return is a summary, not a transcript.
4. **Tell the model when not to delegate.**
   - Quote: "Claude Opus 4.6 has a strong tendency to use subagents and might spawn them in situations where a simpler, direct approach would suffice." Sample fix: "For simple tasks, sequential operations, single-file edits ... work directly rather than delegating."
   - Source: [AT-Best]. NEW for an orchestrator prompt. Model-specific; mark it as such.
5. **Be explicit when you want action, or the model only advises.**
   - Quote: "If you say 'can you suggest some changes,' Claude will sometimes provide suggestions rather than implementing them". Be explicit: "Change this function".
   - Source: [AT-Best]. NEW. Brief verbs must be imperative and say whether to edit.
6. **Say how far to go. Do not assume.**
   - Quote: "If you want Claude to do more than the task strictly requires, explicitly request it rather than relying on the model to infer this from vague prompts."
   - Source: [AT-Best]. This is the base's "demand" lever with vendor backing.
7. **State stop conditions and when to hand back.**
   - Quote: "it can be helpful to clearly state the stop conditions of the agentic tasks, outline safe versus unsafe actions, and define when, if ever, it's acceptable for the model to hand back to the user."
   - Source: [OAI-GPT5]. CONFIRMS "completion criterion". Adds "safe vs unsafe actions" and a hand-back rule, which the base lacks.
8. **Set autonomy on purpose.** Two opposite recipes exist.
   - Less eager: tell the agent to stop and report when unsure ([OAI-GPT5], "If you think that you need more time to investigate, update the user with your latest findings and open questions").
   - More eager: "decide what the most reasonable assumption is, proceed with it, and document it" ([OAI-GPT5]).
   - Researcher inference: a brief should name one of the two for the case where information is missing. The default differs by model.
9. **Status-update instructions are model-specific.**
   - Codex-Max guide: "remove all prompting for the model to communicate an upfront plan, preambles, or other status updates during the rollout, as this can cause the model to stop abruptly" ([OAI-Codex]).
   - Claude guide: one model "writes fewer user-facing updates between tool calls. Ask for progress text explicitly" ([AT-Best]).
   - Do not put either rule in a portable skill. Say "check the target model's guide".
10. **Use XML or other structure to separate parts.**
    - Quote: "Wrapping each type of content in its own tag ... reduces misinterpretation." Also: "Put long-form data at the top".
    - Source: [AT-Best]. Optional for the skill. Plain headings do the same job in a short brief.
11. **Agent definition frontmatter: unknown fields fail silently.**
    - Quote: "Claude Code ignores a field it doesn't recognize without reporting an error." Only `name` and `description` are required.
    - Source: [CC-Sub]. Harness-specific. Mention once in agent-prompts as a "check the field names" note, not as craft.

### references/tool-descriptions.md

1. **Describe a tool like a briefing to a new hire.**
   - Quote: "think of how you would describe your tool to a new hire on your team. Consider the context that you might implicitly bring—specialized query formats, definitions of niche terminology, relationships between underlying resources—and make it explicit."
   - Source: [AT-Tools]. Matches the "environment as cache" lever: cache what the agent cannot find.
2. **Cover what, when, when not, each parameter, and limits.**
   - Quote: "Provide extremely detailed descriptions. This is by far the most important factor in tool performance." List: what it does, "When it should be used (and when it shouldn't)", what each parameter means, caveats. "Aim for at least 3–4 sentences".
   - Source: [AT-ToolUse]. See Conflicts: length versus pruning.
3. **Name parameters so they cannot be misread.**
   - Quote: "input parameters should be unambiguously named: instead of a parameter named `user`, try a parameter named `user_id`."
   - Source: [AT-Tools]. Codex adds: "'search' is ambiguous but 'semantic_search' clearly indicates what the tool does" ([OAI-Codex]) and that names close to the underlying command are "as in-distribution as possible".
4. **Use examples for complex inputs.**
   - Quote: "Clear descriptions are most important, but for tools with complex inputs, nested objects, or format-sensitive parameters, you can use the `input_examples` field".
   - Source: [AT-ToolUse]. Examples are second to the description.
5. **Fix agent misuse through the description. Measure it.**
   - Quote: "Claude was needlessly appending `2025` to the tool's `query` parameter ... (we steered Claude in the right direction by improving the tool description)."
   - Source: [AT-Tools]. The repair for a repeated wrong call is a description edit. Also: "Even small refinements to tool descriptions can yield dramatic improvements."
6. **Errors must say what went wrong and what to do next.**
   - Quote: "Write instructive error messages. Instead of generic errors such as 'failed', include what went wrong and what Claude should try next (for example, 'Rate limit exceeded. Retry after 60 seconds.')"
   - Source: [AT-Handle]. And [AT-Tools]: "clearly communicate specific and actionable improvements, rather than opaque error codes or tracebacks."
7. **Truncation text is a steering prompt.**
   - Quote: "If you choose to truncate responses, be sure to steer agents with helpful instructions" (for example, "making many small and targeted searches instead of a single, broad search").
   - Source: [AT-Tools]. Claude Code's default cap is 25,000 tokens per tool response.
8. **Return names, not opaque IDs.**
   - Quote: "resolving arbitrary alphanumeric UUIDs to more semantically meaningful and interpretable language (or even a 0-indexed ID scheme) significantly improves Claude's precision".
   - Source: [AT-Tools]. This is for tool output, not for descriptions. Keep it to one line in the skill, since output design is a code topic.
9. **Do not ask a parameter for the model's reasoning.**
   - Quote: "Ask for an explanation, not reasoning. ... A parameter that asks for the model's thinking or step-by-step reasoning might lead to a `reasoning_extraction` refusal."
   - Source: [AT-ToolUse]. NEW.
10. **Fewer, clearer tools beat many overlapping ones.**
    - Quote: "Too many tools or overlapping tools can also distract agents from pursuing efficient strategies."
    - Source: [AT-Tools]. Also [AT-ToolUse]: consolidate related operations behind an `action` parameter. This is a tool-design point; keep it to one line, with a note that it is a design choice, not a wording one.
11. **Hook output reaches the model only on some paths.**
    - Exit 2: "The message that comes with the block is your hook's stderr." ([CC-Hooks])
    - Exit 0: "Claude never sees stderr from a hook that exits 0." ([CC-Hooks])
    - Plain stdout is context on four events: "`UserPromptSubmit`, `UserPromptExpansion`, `SessionStart`, and `PostModelSwitch`: Claude Code adds plain-text stdout as context that Claude can see and act on." ([CC-Hooks])
    - `PostToolUse`: exit 2 "Shows stderr to Claude; the tool already ran." `Notification`: "Exit code and stderr are ignored."
    - `Stop` with exit 2 "Prevents Claude from stopping, continues the conversation", so the stderr text is the next instruction. Write it as one.
    - Rule for the skill: before you write a hook message, find the channel that reaches the model. Then write the message as an instruction with the next action.
12. **A hook can carry a reason for a denial.** The official example uses `permissionDecisionReason: "Destructive command blocked by hook"` and the stderr example "Blocked: rm commands are not allowed" ([CC-Hooks]). Both state the ban and give no next step. (Researcher inference: they would be stronger as "rm is blocked here. Use `trash <path>` or ask the user." This is the vendor's own example failing its own error-message advice. See Conflicts.)

## Conflicts

1. **Description length.**
   - [AT-ToolUse]: "extremely detailed", "at least 3–4 sentences", "by far the most important factor".
   - [CC-Sub]: subagent descriptions "take up context, so keep them short"; warning above 15,000 combined tokens.
   - The base: every always-loaded word "earns even harder pruning".
   - Resolution (inference): they agree on the principle. A tool description is the only guide to the tool, so it carries the detail. A subagent description is a trigger, and the body carries the detail. Write the skill as "detail where the load is paid on use; trigger words where it is paid always". Prune no-ops in both.
2. **Emphasis and stronger words.**
   - Base: a no-op leading word "is a stronger word (_relentless_), not a different technique".
   - [AT-Best]: "The fix is to soften any aggressive language", because newer Claude models overtrigger.
   - [OAI-GPT5] (Cursor case): the `maximize_` prefix "was counterproductive" and caused repeated searches; they "softened the language around thoroughness". The same guide also contains strong examples ("extremely thoroughly", "100% certain") for other cases.
   - Resolution: strengthen a word only after you see under-action in a run. Soften when you see over-action. Name the model in the note. The skill should say "model-relative" on both sides.
3. **Override semantics.** agents.md and Codex say the closest file "wins" or "overrides". Claude Code concatenates and warns that conflicts get "picked arbitrarily". The base has no view. See Instructions finding 4.
4. **Pointer wording versus import.** The base: a must-have target behind a weak pointer is a variance bug; sharpen the wording first. Claude Code adds: an `@` import is not a pointer, it is inlining. The base's advice "inline only if sharpening fails" maps to `@import` in Claude Code and to pasting text in Codex.
5. **Cache lever versus the spec.** agents.md and `/init` push build/test commands into the file. The base: restate the environment only when the lookup is expensive. Claude Code's own `/doctor` "cuts content Claude can derive from the" code (text truncated in my fetch). Vendors disagree with each other here, and the base sides with the stricter one. Keep the base.
6. **Vendor example versus vendor advice.** The hooks doc's block examples give a ban with no next step, while [AT-Handle] says to give "what Claude should try next". Treat the hooks examples as syntax demos, not as style guides.
7. **Status updates.** Opposite instructions for different models (Findings, agent-prompts 9). Not a true contradiction, but a portable skill cannot hold a fixed rule.
8. **Mild: negation.** The base bans steering by prohibition; Codex's own review-rules example uses "Do not filter treatment comparisons ..." and then adds "Safe path: ...". That is consistent with the base's "pair the guardrail with the positive target". No change needed. I did not find a source that tests the "elephant" claim; [AT-Best] gives guidance but no data.

## Structure impact

**Keep the four references. Make five small changes inside them.**

- Reason to keep: each source group maps to one file, and the guidance does not cross files. Instructions files, agent prompts and tool text have different delivery channels and different loads.
- Add to `levers.md`: (a) "prose or hook?" (instruction versus enforcement); (b) "model-relative emphasis: soften and strengthen"; (c) "contradiction audit"; (d) "re-audit when the model changes".
- Add to `instructions-files.md`: a harness table (Claude Code, Codex, agents.md spec) with columns for file names, discovery, nesting, merge/override, size limit, import syntax. Include the `CLAUDE.md` containing `@AGENTS.md` bridge. Keep the table to rules that change what the author writes.
- Add to `agent-prompts.md`: split "agent definition" into two parts: the description (a pointer; short) and the body (the system prompt; detailed). Say that a subagent starts cold, so the brief is the whole world.
- Put the delivery-channel table for hooks at the top of `tool-descriptions.md`, before the writing advice. Writing the message is useless if the channel never reaches the model.
- Optional: the "error and hook messages" section may later move to its own file if it grows beyond about 80 lines. Not needed now.

## Missing evidence

- I did not fetch Anthropic's "Building effective agents" (agent-computer interface section), or Claude Code's best-practices page. They may add agent-brief advice. The first pass found enough for the brief.
- The hooks doc is 4,481 lines. I read the exit-code table and the per-event exit-2 table. I did not read each event's `additionalContext` or decision fields, so claims about `PreToolUse` deny reasons rely on the doc's example only.
- The `/doctor` trim text in [CC-Mem] was cut off in my fetch ("cuts content Claude can derive from th..."). I did not retrieve the rest.
- Model names and numbers in the live docs ("Fable 5.2", "Opus 5", "gpt-5.3-codex") could not be checked against anything outside the pages. I treat them as vendor claims. I used them only when the rule is described as model-specific.
- No benchmark or independent study on AGENTS.md length versus agent success was retrieved. The 200-line and 32 KiB figures are vendor settings and advice, not measured thresholds. The claim "negation raises the banned behavior" (base) has no source in this set.
- Cursor, Gemini CLI, Copilot and other harnesses use AGENTS.md ([AGENTS-MD] lists them), but I did not check their discovery rules. The harness table covers only Claude Code and Codex.

## Environment limitations

- No shell: I could not run `date`. The retrieval date comes from the JavaScript clock in the sandbox (2026-11-19).
- `web_fetch` truncated the hooks page (49.9 KB of 256 KB shown) and returned the rest in a temp file, which I read in part. The memory page `/doctor` passage was cut off.
- I did not fetch the Claude Code "extension overview", which [CC-Mem] cites for "when to use each mechanism".
- Nothing else failed.

## Sources

| Tag | Title | URL | Type | Trust | Retrieved | Contributed |
| --- | --- | --- | --- | --- | --- | --- |
| AT-Tools | Writing effective tools for AI agents (Anthropic Engineering, 2025-09-11) | https://www.anthropic.com/engineering/writing-tools-for-agents | Vendor engineering blog | Primary | 2026-11-19 | New-hire framing, parameter naming, truncation and error steering, eval-driven edits |
| AT-ToolUse | How to implement tool use (Claude docs) | https://docs.claude.com/en/docs/agents-and-tools/tool-use/implement-tool-use | Vendor docs | Primary | 2026-11-19 | Description checklist, 3-4 sentences, `input_examples`, "explanation not reasoning" |
| AT-Handle | Handle tool calls (Claude docs) | https://docs.claude.com/en/docs/agents-and-tools/tool-use/handle-tool-calls | Vendor docs | Primary | 2026-11-19 | `is_error`, "instructive error messages" |
| CC-Hooks | Hooks reference (Claude Code docs) | https://docs.claude.com/en/docs/claude-code/hooks | Vendor docs | Primary | 2026-11-19 | Exit codes, which channels reach Claude, per-event exit-2 table |
| CC-Mem | How Claude remembers your project (Claude Code docs) | https://docs.claude.com/en/docs/claude-code/memory | Vendor docs | Primary | 2026-11-19 | Locations, load order, imports, 200-line target, AGENTS.md handling, troubleshooting |
| AGENTS-MD | AGENTS.md | https://agents.md/ | Open spec / site | Primary | 2026-11-19 | Format, nesting, "closest wins", no required fields |
| OAI-Agents | Custom instructions with AGENTS.md (OpenAI Codex docs) | https://developers.openai.com/codex/guides/agents-md | Vendor docs | Primary | 2026-11-19 | Discovery chain, merge order, 32 KiB cap, override file, review rules |
| AT-Best | Prompting best practices / Claude 4 best practices (Claude docs) | https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices | Vendor docs | Primary | 2026-11-19 | Positive phrasing, soften emphasis, explain why, explicit action, subagent overuse, stale prompts |
| CC-Sub | Create custom subagents (Claude Code docs) | https://docs.claude.com/en/docs/claude-code/sub-agents | Vendor docs | Primary | 2026-11-19 | Description as trigger, body as prompt, isolation, `omitClaudeMd`, frontmatter |
| OAI-GPT5 | GPT-5 prompting guide (OpenAI Cookbook) | https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide | Vendor guide | Primary | 2026-11-19 | Contradictions cost, stop conditions, eagerness, Cursor over-emphasis case |
| OAI-Codex | Codex prompting guide (OpenAI Cookbook) | https://cookbook.openai.com/examples/gpt-5/codex_prompting_guide | Vendor guide | Primary | 2026-11-19 | AGENTS.md as user messages, tool naming, drop preamble prompts |

Rejected or deprioritized: none by trust. Third-party blog posts on "good AGENTS.md" were not searched, because the vendor docs covered every requested group. That also means no secondary evidence exists in this brief to test the vendors' claims.

## Next steps

1. Fetch the Claude Code best-practices page and the Anthropic "Building effective agents" ACI section. Check them for brief-writing advice that adds to agent-prompts.
2. Read the hooks doc's `PreToolUse`, `UserPromptSubmit`, `PostToolUse` and `Stop` sections to confirm the exact model-visible fields before you write the hook-message part of `tool-descriptions.md`.
3. Optional: find one measured study of instruction-file length versus agent success, to back or drop the 200-line and 32 KiB targets.
