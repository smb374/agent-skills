<!-- Derived from getsentry/skills skills/skill-writer @ a582c51 (Apache-2.0); modified. -->

# Provenance template

Use this file in step 4, when you create `PROVENANCE.md` for the target skill. `PROVENANCE.md` is the maintenance contract of the skill: the sources, the decisions, the coverage, the gaps, and the local changes. It replaces a separate specification file and a separate source file.

## Template

````markdown
# <skill name> provenance

## Upstream

- repository: the repository that holds the source
- path: the path of the source in that repository
- commit: the full SHA, and the short form in brackets
- license: the SPDX name
- status: verbatim | modified | derived | own

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| <URL or path> | specification, documentation, code, issue, commit, or note | primary or secondary | <date> | what it shaped | license, notice, or excerpt limit |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| <the class, the shape, a harness-specific mechanic, or a deferred gap> | <source row> | adopted, rejected, or deferred |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| <a required dimension of the skill class> | complete or partial | <the action, or `none`> |

## Local changes

- <each change to the source text, and the reason>
````

## Rules

1. Keep it concise. Link to a source, and do not copy it.
2. Write one row for each source. Give the trust tier, the retrieval date, and the contribution.
3. Use `verbatim` when the files are an exact copy, `modified` when you changed a copy, `derived` when the text is a rewrite, and `own` when the skill has no upstream.
4. Record each decision with the evidence that supports it, and one status.
5. State the gaps. A gap with no next retrieval action is a gap that nobody will close.
6. Redact the secrets, the customer data, and the private identifiers.
7. Update the file when the scope, the trigger strategy, the evidence model, the reference architecture, or the validation gate changes. For a wording-only fix, add one line to the local changes.

## What goes where

| File or directory | Purpose |
| --- | --- |
| `SKILL.md` | the runtime router: what the agent reads to act |
| `PROVENANCE.md` | the maintenance contract: the sources, the decisions, and the gaps |
| `references/` | the optional depth, loaded by a route |
| `references/evidence/` | the durable examples of the iteration |
