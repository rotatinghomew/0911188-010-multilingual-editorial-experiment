import json
from pathlib import Path

class DataError(ValueError):
    pass

def load(root):
    path = Path(root) / 'data.json'
    try:
        content = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as error:
        raise DataError('无法读取本地业务数据') from error
    if not isinstance(content, dict) or not isinstance(content.get('tables'), dict):
        raise DataError('数据必须包含 tables 对象')
    for name, rows in content['tables'].items():
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise DataError('数据表格式错误：' + str(name))
    return content
