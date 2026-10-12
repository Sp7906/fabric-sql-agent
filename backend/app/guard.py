"""SQL guardrails: only a single read-only SELECT over allowed tables."""
import sqlglot
from sqlglot import exp
from sqlglot.errors import ParseError

FORBIDDEN = (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Create,
             exp.Alter, exp.Command, exp.Merge)


class UnsafeSQL(ValueError):
    pass


def validate(sql: str, allowed_tables: set[str], max_rows: int = 500) -> str:
    try:
        statements = sqlglot.parse(sql, read="sqlite")
    except ParseError as e:
        raise UnsafeSQL(f"Could not parse SQL: {e}") from e

    statements = [s for s in statements if s is not None]
    if len(statements) != 1:
        raise UnsafeSQL("Exactly one statement is allowed.")
    tree = statements[0]

    if not isinstance(tree, (exp.Select, exp.Union)):
        raise UnsafeSQL("Only SELECT queries are allowed.")
    if tree.find(*FORBIDDEN):
        raise UnsafeSQL("Write or DDL operations are not allowed.")

    ctes = {c.alias for c in tree.find_all(exp.CTE)}
    used = {t.name for t in tree.find_all(exp.Table)} - ctes
    unknown = used - allowed_tables
    if unknown:
        raise UnsafeSQL(f"Unknown or disallowed tables: {sorted(unknown)}")

    if not tree.args.get("limit"):
        tree = tree.limit(max_rows)
    return tree.sql(dialect="sqlite")
