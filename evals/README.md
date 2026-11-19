# Evals

The eval suite runs the prompts of one skill with headless pi, once with the skill and once without it, and grades the result. Use it to prove the gap of a skill, and to check a change to a skill.

## Run

1. Copy `.env.example` to `.env`. Set the API key of your provider, and `EVAL_MODEL` as `<provider>/<model id>`. The runner checks no key: pi reports a missing key itself.
2. Run `just eval <skill>`. Add `--runs N`, `--case ID` (repeatable), or `--jobs N` (default 4).
3. Follow the progress on stderr, or in another terminal with `tail -f evals/results/<timestamp>-<skill>-<suffix>/progress.log`. The runner writes one line when a run starts and one line when it ends, with the check count and the time.
4. Read `evals/results/<timestamp>-<skill>-<suffix>/summary.md`.

Each run costs money. `just check` never runs the suite.

The command exits 0 when the suite ran, 1 when a pi call failed, and 2 when a setting or a case file is bad. The exit code does not grade the skill. Read the summary.

## What one run does

1. Copy the fixture to a temp directory outside the repo.
2. Set `PI_CODING_AGENT_DIR` to an empty temp directory, so no user skill, instructions file, extension, or setting applies.
3. Run `pi --mode json --no-session -nc -ne --no-mcp --model $EVAL_MODEL --tools read,edit,write,grep,find,ls`, with `--no-skills` (arm `baseline`) or `--skill skills/<skill>` (arm `skill`).
4. Apply each check to the temp directory.
5. Save `events.jsonl` and the final `workdir/` under `evals/results/` (gitignored).

The summary shows, for each case, the pass count of each check in each arm, and the tokens and the cost of the agent calls. It does not count the judge calls.

## Add cases for a skill

Put the cases in `evals/<skill>/cases.json`, and the fixtures in `evals/<skill>/fixtures/<name>/`. The name `<skill>` must equal a directory in `skills/`.

```json
[
  {
    "id": "agents-md",
    "fixture": "fixtures/agents-md",
    "prompt": "Shorten and improve this AGENTS.md.",
    "bash": false,
    "checks": [
      {"id": "no-pip", "type": "file_not_matches", "path": "AGENTS.md", "pattern": "pip install"}
    ]
  }
]
```

| Field | Meaning |
| --- | --- |
| `id` | a unique name for the case |
| `fixture` | a directory relative to `evals/<skill>/`. The agent starts in a copy of it |
| `prompt` | the user message to the agent |
| `bash` | optional. `true` adds the `bash` tool. The default is no bash, because a run is unattended |
| `checks` | the checks, each with a unique `id` |

| Check type | Fields | Passes when |
| --- | --- | --- |
| `file_matches` | `path`, `pattern` | the file exists, and the Python regex matches |
| `file_not_matches` | `path`, `pattern` | the file exists, and the regex does not match |
| `file_exists` | `path` | the file exists |
| `command` | `run`, `exit` (default 0), `stdout` (optional regex) | `bash -c run` in the workdir exits with `exit`, and its stdout matches |
| `judge` | `question`, `paths` (optional) | `EVAL_JUDGE_MODEL` answers yes. It reads the listed files, or each file in the workdir |

Use a regex or a command check when it can decide. Use a judge check only for a question that needs reading, because the judge costs tokens and can vary.

Write fixtures whose faults do not copy the examples in the skill. A copied example measures recall of the example, not the method.

## Open items

- A case with `"bash": true` runs shell commands on your machine. An OS sandbox that limits writes to the fixture directory does not exist yet.
- The suite tests the content of a skill only. It does not test the trigger, because the skill arm forces the skill with `--skill`.
