from fractions import Fraction


def select(metrics, treatment, control, minimum):
    if any(metrics.get(key, {}).get('sent', 0) < minimum for key in (treatment, control)):
        return 'undecided'
    rates = {key: Fraction(metrics[key]['opened'], metrics[key]['sent']) for key in (treatment, control)}
    return treatment if rates[treatment] > rates[control] else control
