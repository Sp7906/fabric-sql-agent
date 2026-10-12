import sqlite3
from .config import DB_PATH


def connect():
    """Read-only connection: the database itself refuses writes."""
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)


def get_schema() -> dict[str, list[dict]]:
    con = connect()
    try:
        tables = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
        return {
            t: [{"name": c[1], "type": c[2]} for c in con.execute(f"PRAGMA table_info({t})")]
            for t in tables
        }
    finally:
        con.close()


def schema_prompt() -> str:
    return "\n".join(
        f"{t}({', '.join(c['name'] + ' ' + c['type'] for c in cols)})"
        for t, cols in get_schema().items()
    )


def run_query(sql: str):
    con = connect()
    try:
        cur = con.execute(sql)
        cols = [d[0] for d in cur.description]
        return cols, [list(r) for r in cur.fetchall()]
    finally:
        con.close()
