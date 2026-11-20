# 12: Export the ledger as CSV or JSON

## What to build

Add the command `ledger export --format csv|json <ledger.tsv> <out>`.

## Acceptance criteria

- `ledger/csv_export.py` has `to_csv(entries) -> str`. The first line is `date,payee,amount`. Each entry is one line. The amount has two decimals, for example `1250` cents is `12.50`. Lines end with `\n`.
- `ledger/json_export.py` has `to_json(entries) -> str`. It returns a JSON array of objects with the keys `date`, `payee`, and `amount`. `amount` is the integer amount in cents.
- `ledger export --format csv <ledger.tsv> <out>` writes `to_csv` of the loaded entries to `<out>` and exits 0. `--format json` writes `to_json`.
- An unknown format prints `unknown format: <name>` and exits 2.
- `ledger export` with a missing argument prints the usage line `usage: ledger export --format csv|json <ledger.tsv> <out>` and exits 2.
- Each module has unit tests in `tests/`.
