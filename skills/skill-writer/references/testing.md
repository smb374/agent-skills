<!-- Derived from getsentry/skills skills/skill-writer @ a582c51 (Apache-2.0); modified. -->

# Testing

Use this file in step 6, and again after the release, to test the skill that you wrote. A skill is correct when it changes the output of an agent on real work.

## The minimum bar

1. Baseline. Run 3 realistic prompts with no skill. Write down what goes wrong. If nothing goes wrong, stop the work.
2. With the skill. Run the same prompts again. Read the transcripts: the wasted steps, the files that the agent never opens, the section that it reads again and again.
3. Trigger check. Write 8 to 10 should-trigger prompts and 8 to 10 near-miss should-not-trigger prompts, in the words that users really type. Read the description rules for the query sets.
4. Each harness and each model that you support. A skill that one model needs can over-instruct a stronger model. The trigger rate also differs per harness, because each harness lists the skills in its own way.
5. 5 or more runs for each variant when you test the wording. Treat the variance as a result.

## One-shot runs per harness

| Harness | Headless run | Evidence that the skill loaded |
| --- | --- | --- |
| Claude Code | `claude -p "<prompt>" --output-format stream-json --verbose` | an event with `"skill":"<name>"` |
| OpenCode | `opencode run "<prompt>"` | a `skill` tool call in the session log |
| Copilot CLI | `copilot -p "<prompt>"` | the session log |
| Pi | `pi -p "<prompt>"` | a `read` of the `SKILL.md` of the skill |
| Hermes Agent | the one-shot command or the chat mode of the CLI | the `skill_view` calls |

Only the Claude Code row was tried. Check each other flag with the `--help` of its tool before you script it.

## The two-agent loop

Agent A helps you write the skill. Agent B uses the skill on real work, in a fresh session, on the target harness and model. Take each failure of B back to A.

## Maintenance

- Each listed skill costs context on each turn, in each harness. Turn off the skills that a session does not need: with the settings of the harness, with a permission rule per agent, or with a toolset rule.
- Bad frontmatter fails with no message. One harness loads the skill with empty metadata, and another skips the skill. The model then never invokes it. Run the validator against the specification before you finish.
- Review a skill that an agent wrote. An agent that writes its own skills after a complex task can record a mistake as a rule. Test each draft against a baseline.
- A third-party skill is code. Read it before you install it.

## Output

- the baseline result and the result with the skill
- the trigger sets and their result
- the transcripts that you read, and what they showed
- the harnesses and the models that you did not test
