---
name: codebase-memory
description: "Read before you call a codebase-memory-mcp tool or write Cypher for query_graph. Advanced use of the code graph tools (search_graph, trace_path, get_code_snippet, query_graph, and the rest). Applies to: Cypher queries, graph query syntax, edge types, dead code, fan-in, fan-out, exhaustive or negative claims, index coverage, paging."
---

# Code graph — advanced use

This file covers the advanced use of the `codebase-memory-mcp` tools. Your harness can show each tool with a prefix of the server name. If a result comes from the wrong project, pass `project`. Get the project names from `list_projects`.

## Decision matrix

| Question                 | Call                                                              |
| ------------------------ | ----------------------------------------------------------------- |
| Dead code                | `search_graph` `{max_degree: 0, exclude_entry_points: true}`      |
| High fan-out             | `search_graph` `{min_degree: 10, relationship: "CALLS"}`          |
| Data flow of a parameter | `trace_path` `{function_name, mode: "data_flow", parameter_name}` |
| Cross-service calls      | `trace_path` `{function_name, mode: "cross_service"}`             |
| Symbols in one file      | `get_file_outline` `{file_path}`                                  |
| Architecture overview    | `get_architecture` `{aspects: ["overview"]}`                      |
| Impact of local changes  | `detect_changes`                                                  |
| Node/edge types          | `get_graph_schema`                                                |

## Evidence

- After you have the evidence paths, call `check_index_coverage` once with all of them in `paths`. For a negative or exhaustive claim ("no callers", "dead code", "complete impact"), also pass `scopes`.
- A clean coverage result means no recorded gap. It does not prove completeness.
- For partial, skipped, stale, or unknown coverage, read or text-search the reported ranges before you rely on the graph.
- Page through all results (`has_more`, `offset`, `next_cursor`) before you make an exhaustive claim.
- Read each graph result that you cite. If the graph gives no result for a symbol you expect, check with a text search. If a tool says the repo has no index, use text search and file reads, and say so.

## Gotchas

1. `trace_path` needs an exact function name. Use `search_graph` first.
2. Outbound traces miss cross-service callers. Use `trace_path` with `direction: "both"`.
3. `search_graph` with `relationship: "HTTP_CALLS"` filters nodes by degree. Use `query_graph` to see the edges.
4. Add a Cypher `LIMIT` to broad `query_graph` queries.

## Cypher examples

```
MATCH (a)-[r:HTTP_CALLS]->(b) RETURN a.name, b.name, r.url_path, r.confidence LIMIT 20
MATCH (f:Function) WHERE f.name =~ '.*Handler.*' RETURN f.name, f.file_path
MATCH (a)-[r:CALLS]->(b) WHERE a.name = 'main' RETURN b.name
```
