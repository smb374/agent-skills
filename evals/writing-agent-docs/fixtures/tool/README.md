# Notes for the humans

- `run_sql` runs one SQL statement on a read-only connection. `s` is the SQL text. `db` is `replica` (default, production data, read-only) or `analytics` (a nightly copy with extra rollup tables). It returns at most 200 rows and drops the rest with no message. Large tables (`events`, `orders`) have more than 100 million rows, so a query with no `WHERE` and no `LIMIT` runs for minutes.
- To see the columns of a table, use `describe_table`. Agents keep running `SELECT * FROM x LIMIT 1` with `run_sql` for that.
- `guard-push.sh` is a Claude Code PreToolUse hook on the Bash tool. It must stop a force push to `main`. A force push to a feature branch with `git push --force-with-lease` is fine.
