def exposures(events, cutoff, units):
    by_arm = {}
    for event in events:
        if event['at'] >= cutoff or event['unit'] not in units:
            continue
        row = by_arm.setdefault(event['arm'], {'sent': 0, 'opened': 0})
        row['sent'] += 1
        row['opened'] += int(event['opened'])
    return by_arm
