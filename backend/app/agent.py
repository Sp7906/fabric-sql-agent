"""Text-to-SQL agent: generate -> validate -> execute -> self-correct."""
import re
from openai import AzureOpenAI
from . import config, db
from .guard import validate, UnsafeSQL

SYSTEM = """You are a careful analytics engineer. Convert the user's question into ONE
SQLite SELECT query over the schema below. Rules: read-only, use only listed tables
and columns, return only SQL with no explanation or markdown.

Schema:
{schema}
"""


def _client():
    if not (config.AOAI_ENDPOINT and config.AOAI_KEY):
        return None
    return AzureOpenAI(azure_endpoint=config.AOAI_ENDPOINT, api_key=config.AOAI_KEY,
                       api_version=config.AOAI_VERSION)


def _clean(text: str) -> str:
    return re.sub(r"^```(?:sql)?|```$", "", text.strip(), flags=re.M).strip()


def _demo_sql(question: str) -> str:
    """Offline fallback so the repo runs without Azure credentials."""
    q = question.lower()
    if "region" in q:
        return ("SELECT c.region, ROUND(SUM(f.revenue),2) AS revenue FROM fact_sales f "
                "JOIN dim_customer c ON f.customer_id=c.customer_id GROUP BY c.region ORDER BY revenue DESC")
    if "month" in q or "trend" in q:
        return ("SELECT substr(order_date,1,7) AS month, ROUND(SUM(revenue),2) AS revenue "
                "FROM fact_sales GROUP BY month ORDER BY month")
    return ("SELECT p.category, ROUND(SUM(f.revenue),2) AS revenue FROM fact_sales f "
            "JOIN dim_product p ON f.product_id=p.product_id GROUP BY p.category ORDER BY revenue DESC")


def ask(question: str) -> dict:
    client = _client()
    allowed = set(db.get_schema())
    messages = [
        {"role": "system", "content": SYSTEM.format(schema=db.schema_prompt())},
        {"role": "user", "content": question},
    ]
    attempts, last_error = [], None

    for i in range(config.MAX_ATTEMPTS):
        raw = (_clean(client.chat.completions.create(
            model=config.AOAI_DEPLOYMENT, messages=messages, temperature=0
        ).choices[0].message.content) if client else _demo_sql(question))
        try:
            safe_sql = validate(raw, allowed, config.MAX_ROWS)
            cols, rows = db.run_query(safe_sql)
            attempts.append({"sql": safe_sql, "error": None})
            return {"sql": safe_sql, "columns": cols, "rows": rows,
                    "attempts": attempts, "mode": "azure" if client else "demo"}
        except (UnsafeSQL, Exception) as e:  # noqa: BLE001
            last_error = str(e)
            attempts.append({"sql": raw, "error": last_error})
            if not client:
                break
            messages += [{"role": "assistant", "content": raw},
                         {"role": "user", "content": f"That failed: {last_error}. Return a corrected SQL query only."}]

    return {"sql": None, "columns": [], "rows": [], "attempts": attempts, "error": last_error}
