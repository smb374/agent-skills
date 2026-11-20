# codebase-memory provenance

## Upstream

- repository: none
- path: none
- commit: none
- license: none
- status: own

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| Pi config `codebase-memory` skill | note | primary | 2026-11-20 | the decision matrix, the evidence rules, gotchas 1 to 4, the Cypher examples | none |
| smb374/agent-skills #2, section "codebase-memory skill" | specification | primary | 2026-11-20 | the MCP names, and the parts to remove | none |
| [DeusData/codebase-memory-mcp README](https://github.com/DeusData/codebase-memory-mcp/blob/main/README.md) | documentation | primary | 2026-11-20 | the `project` parameter and `list_projects`, from the troubleshooting table | MIT |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| refer to the tools by their MCP names | #2 | adopted |
| a listed knowledge skill | #2 | adopted |
| tell the agent to pass `project` when a result comes from the wrong project | the README troubleshooting table. The Pi `cbmem` wrapper fills `project` from the git root, and an MCP client does not | adopted |
| the `cbmem` wrapper name, the Subagents section, and gotcha 5 (index refresh by the wrapper) | #2. They move to the Pi `cbmem` extension guideline | rejected |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | missing: the user waived the eval for this port, because the change is wording only. #2 puts eval cases for this skill out of scope | add an eval case on user request |
| trigger check with near-miss queries | missing | run the trigger loop of skill-writer when a trigger failure shows |

## Local changes

- Replace each `cbmem` call with the MCP tool name.
- Replace the Pi tool names `read`, `ffgrep`, and `fffind` with "read", "text search", and "file reads".
- Replace the intro about the wrapper with a note on the tool prefix and the `project` parameter.
- Remove the Subagents section, gotcha 5, and "stale index" and "subagent handoff" from the description.
