from collections import defaultdict

def summarize(content):
    definition = content['definition']
    rows = content['tables'][definition['table']]
    groups = defaultdict(lambda: {'rows': 0, 'total': 0})
    for row in rows:
        key = row.get(definition['group'])
        if key is None:
            key = '未分类'
        value = row.get(definition['measure'], 0)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError('度量字段必须为数值')
        groups[str(key)]['rows'] += 1
        groups[str(key)]['total'] += value
    return [{'group': key, **groups[key]} for key in sorted(groups)]
