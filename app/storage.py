import json
from pathlib import Path
import re
import sqlite3

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
    connection = sqlite3.connect(':memory:')
    for name, rows in content['tables'].items():
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise DataError('数据表格式错误：' + str(name))
        if not re.fullmatch(r'[a-z][a-z0-9_]*', name):
            raise DataError('数据表名称无效')
        columns = sorted({column for row in rows for column in row})
        if not columns:
            continue
        if any(not re.fullmatch(r'[a-z][a-z0-9_]*', column) for column in columns):
            raise DataError('字段名称无效：' + str(name))
        table_sql = ', '.join('"' + column + '"' for column in columns)
        connection.execute('CREATE TABLE "' + name + '" (' + table_sql + ')')
        placeholders = ', '.join('?' for _ in columns)
        insert_sql = 'INSERT INTO "' + name + '" VALUES (' + placeholders + ')'
        connection.executemany(insert_sql, [[row.get(column) for column in columns] for row in rows])
    for name in content['tables']:
        if connection.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)).fetchone():
            cursor = connection.execute('SELECT * FROM "' + name + '"')
            columns = [entry[0] for entry in cursor.description]
            content['tables'][name] = [dict(zip(columns, row)) for row in cursor.fetchall()]
    connection.close()
    return content
