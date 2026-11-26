import sys

from ledger.store import load


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args[:1] == ["total"]:
        cents = sum(e.amount for e in load(args[1]))
        print(f"total: {cents // 100}.{cents % 100:02d}")
        return 0
    print("usage: ledger total <ledger.tsv>")
    return 2
