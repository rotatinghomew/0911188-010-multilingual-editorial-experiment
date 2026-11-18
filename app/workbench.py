import json
from .editor import select
from .enrollment import eligible
from .journal import packet
from .measurement import exposures


def run_workbench(action, directory, key, ledger):
    if action == 'broadcast' and key:
        return packet(ledger, 'experiment', key)
    source = json.loads((directory / 'workbench.json').read_text())
    units, assigned = eligible(source['assignment'])
    if action == 'enrollment':
        return {'assigned': assigned}
    results = exposures(source['exposures'], source['stop'], units)
    if action == 'metrics':
        return results
    decision = select(results, source['treatment'], source['control'], source['minimum'])
    recommendation = {'variant': decision, 'metrics': results, 'stop': source['stop']}
    if action == 'broadcast':
        if decision == 'undecided':
            raise ValueError('曝光量不足，暂不发推广通知')
        return packet(ledger, 'experiment', source['experiment'], recommendation)
    return recommendation
