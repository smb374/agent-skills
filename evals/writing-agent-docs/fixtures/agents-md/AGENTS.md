# AGENTS.md

You are an AI coding assistant. This file is your system prompt.

## About

`ledger` is a Python service that imports bank statements. The code is in `ledger/`. The ML categorizer is in `services/ml/`.
Write clean, idiomatic Python. Be thorough and double-check your work.

## Environment

Use uv to manage dependencies.
All code targets Python 3.9.

To install dependencies, run `pip install -r requirements.txt`.

## Commands

- Tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Types: `uv run mypy ledger`
- Format: `uv run ruff format .`

## Testing

IMPORTANT: You MUST ALWAYS add tests. NEVER commit code without tests.
The tests need Redis on localhost:6379. Run `docker compose up -d redis` first, or the tests hang for 5 minutes and then fail with a timeout.

## Formatting

Run `uv run ruff format` on every file you touch before you finish. Do not forget.

## Deploying

To deploy to production:
1. Check that CI on main is green.
2. Run `uv run alembic upgrade head --sql > migration.sql` and attach it to the deploy ticket.
3. Ask a second engineer to approve the ticket.
4. Run `flyctl deploy --app ledger-prod --strategy bluegreen`.
5. Watch the `ledger-prod` dashboard for 15 minutes.
6. If the error rate goes above 1%, run `flyctl releases rollback --app ledger-prod`.
7. Post the release notes in #ledger-deploys.

## Code rules

Don't use print for logging. Don't use bare except. Don't use mutable default arguments.
