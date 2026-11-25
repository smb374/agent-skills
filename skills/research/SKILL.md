---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a dated Markdown report. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

Spin up a **background agent** to do the research, so you keep working while it reads. Start it with a fresh context window.

When the harness cannot start a background agent, do the research yourself in this session. Tell the user that the research blocks other work until it is done.

The job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it to the place that the user names, in the repo or outside it. When the user names no place, use the place where the repo already keeps such notes. When the repo has no such place, use `docs/research/`. Tell the user the path.
4. Name the file `YYYY-MM-DD-<topic-slug>.md`. The date is the retrieval date: get it with `date +%F`. The date tells a later reader how old the facts are.
