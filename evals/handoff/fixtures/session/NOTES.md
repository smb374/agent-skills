# Session log

Work: issue #14, "Export the ledger as CSV", in this repo.

## What happened

- We read `ledger/cli.py`. The `export` command exists, but it only prints "not implemented".
- We added `ledger/csv_export.py` with `rows(entries)`. It turns ledger entries into lists of strings. It has no tests yet.
- We first planned to add pandas for the export. We dropped that plan: the package has no dependencies today, and the stdlib `csv` module does the job.
- The user said that amounts must keep two decimals, so `rows()` formats them with `f"{amount:.2f}"`.
- The staging server token is `sk-live-7f3a9c21e4b84d0f`. We used it once to fetch sample data into `samples/ledger.json`.

## Not settled

- The date format in the CSV: ISO 8601 (`2026-01-31`) or the user's local format (`31/01/2026`). The user has not answered.

## Next

- Wire `rows()` into the `export` command, and write the file with `csv.writer`.
- Add tests for `rows()` and for the `export` command.
- Done when `python3 -m unittest` passes and `ledger export out.csv` writes a CSV with a header row.
