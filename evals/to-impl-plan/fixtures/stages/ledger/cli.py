import sys


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if args[:1] == ["export"]:
        print("not implemented")
        return 1
    print("usage: ledger export --format csv|json <ledger.tsv> <out>")
    return 2
