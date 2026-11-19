# ponytail provenance

## Upstream

- repository: DietrichGebert/ponytail, https://github.com/DietrichGebert/ponytail
- path: `skills/ponytail/SKILL.md`
- commit: 96608e078b2d5ea607c5c3b8b5a54d1c1fba6846 (96608e0)
- license: MIT, see `LICENSE`
- status: modified

## Sources

| Source | Type | Trust tier | Retrieved | Contribution | Usage constraints |
| --- | --- | --- | --- | --- | --- |
| DietrichGebert/ponytail `skills/ponytail/SKILL.md` @ 96608e0 | code | primary | 2026-11-19 | the full skill | MIT |
| Pi config fork of `ponytail` | note | secondary | 2026-11-19 | the local changes below | none recorded |

## Decisions

| Decision | Evidence | Status |
| --- | --- | --- |
| keep the full mode only, and remove the levels | the levels need the upstream `/ponytail` command and hooks, which this repo does not install | adopted |
| the companion skills (`ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`, `ponytail-review`) | not in `docs/catalog.md` | rejected |

## Coverage and gaps

| Dimension | Status | Next retrieval action |
| --- | --- | --- |
| baseline runs with and without the skill | partial: upstream `benchmarks/` covers the upstream skill with levels, not this fork | add an eval when a ponytail failure shows |

## Local changes

- Remove the levels: the `Levels:` sentence in `description`, `argument-hint`, the session and level-switch line, and the Levels table.
- Change the shortcut marker from `shortcut: <the limit>, <when to upgrade>` to `shortcut: <limit>, <upgrade path>`, as in the Pi config fork.
