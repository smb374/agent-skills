# 21: Print the ledger total

## What to build

Add the command `ledger total <ledger.tsv>`.

## Acceptance criteria

- For a ledger file with the entries `1250` and `300` cents, `ledger total <ledger.tsv>` prints `total: 15.50` and exits 0.
- For an empty ledger file it prints `total: 0.00` and exits 0.
- `ledger total` with no file argument prints `usage: ledger total <ledger.tsv>` and exits 2.
- `tests/test_cli.py` tests the command.
