from collections import Counter


def eligible(rows):
    active = {row['unit']: row for row in rows if row['active']}
    return active, dict(Counter(row['arm'] for row in active.values()))
