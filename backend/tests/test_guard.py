import pytest
from app.guard import validate, UnsafeSQL

TABLES = {"fact_sales", "dim_customer"}


def test_select_gets_limit():
    assert "LIMIT 500" in validate("SELECT * FROM fact_sales", TABLES)


@pytest.mark.parametrize("sql", [
    "DROP TABLE fact_sales",
    "DELETE FROM fact_sales",
    "UPDATE fact_sales SET revenue = 0",
    "SELECT 1; DROP TABLE fact_sales",
    "SELECT * FROM secret_table",
])
def test_blocks_unsafe(sql):
    with pytest.raises(UnsafeSQL):
        validate(sql, TABLES)


def test_cte_allowed():
    sql = "WITH t AS (SELECT * FROM fact_sales) SELECT * FROM t"
    assert validate(sql, TABLES)
