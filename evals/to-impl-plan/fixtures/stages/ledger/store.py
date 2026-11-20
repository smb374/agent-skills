from typing import NamedTuple


class Entry(NamedTuple):
    date: str
    payee: str
    amount: int  # cents


def load(path):
    """Read a TSV file with the columns date, payee, and amount in cents."""
    with open(path, encoding="utf-8") as f:
        rows = [line.rstrip("\n").split("\t") for line in f if line.strip()]
    return [Entry(d, p, int(a)) for d, p, a in rows]
