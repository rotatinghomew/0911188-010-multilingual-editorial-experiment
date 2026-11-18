import json
import sqlite3
from contextlib import closing


def packet(database, kind, key, value=None):
    """读回已保存的业务凭证；同一编号不能改作他用。"""
    with closing(sqlite3.connect(database)) as connection, connection:
        if value is not None:
            connection.execute("CREATE TABLE IF NOT EXISTS packets (kind TEXT, key TEXT, body TEXT NOT NULL, PRIMARY KEY(kind, key))")
        try:
            row = connection.execute("SELECT body FROM packets WHERE kind=? AND key=?", (kind, key)).fetchone()
        except sqlite3.OperationalError as error:
            if "no such table" not in str(error):
                raise
            raise ValueError("没有这份凭证") from error
        if value is None:
            if row is None:
                raise ValueError("没有这份凭证")
            return json.loads(row[0])
        body = json.dumps(value, ensure_ascii=False, sort_keys=True)
        connection.execute("INSERT OR IGNORE INTO packets VALUES (?, ?, ?)", (kind, key, body))
        recorded = connection.execute("SELECT body FROM packets WHERE kind=? AND key=?", (kind, key)).fetchone()[0]
        if recorded != body:
            raise ValueError("凭证编号已用于不同内容")
        return json.loads(recorded)
