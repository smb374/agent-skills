def rows(entries):
    return [[e["date"], e["payee"], f"{e['amount']:.2f}"] for e in entries]
