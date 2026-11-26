def format_cents(cents):
    """Return cents as dollars with two decimals, for example -150 -> "-1.50"."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{cents // 100}.{cents % 100:02d}"
