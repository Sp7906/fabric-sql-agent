# Fabric Lakehouse + Text-to-SQL Analytics Agent

Ask business questions in plain English and get answers from a governed gold layer.
A Microsoft Fabric medallion pipeline (PySpark) feeds a star schema; a FastAPI agent turns
questions into **validated, read-only SQL**, self-corrects on errors, and a React UI shows the results.

```
Raw CSV -> Bronze (Delta) -> Silver (clean) -> Gold (star schema) -> SQL Agent (FastAPI) -> React UI
                 Fabric Lakehouse notebooks                         Azure OpenAI + guardrails
```

## Features
- Medallion architecture in PySpark notebooks (`pipelines/fabric/`)
- Text-to-SQL agent with schema-aware prompting and a self-correction loop (max 3 attempts)
- Guardrails: single SELECT only, table allow-list, automatic LIMIT, read-only DB connection
- Runs offline in demo mode (no Azure key needed) with a seeded SQLite gold layer
- Dockerised, tested, and CI on GitHub Actions

## Quick start
```bash
git clone https://github.com/<your-username>/fabric-sql-agent.git && cd fabric-sql-agent
cp .env.example .env          # optional: add Azure OpenAI credentials
docker compose up --build     # UI: http://localhost:5173  API docs: http://localhost:8000/docs
```

Without Docker:
```bash
python data/seed.py
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload
cd frontend && npm install && npm run dev
```

## Running the Fabric pipeline
1. Create a Fabric Lakehouse and upload your orders CSV to `Files/raw/orders.csv`
   (columns: order_id, order_date, customer_id, customer_name, region, segment, product_id,
   product_name, category, unit_price, quantity).
2. Import the three notebooks in `pipelines/fabric/` and run them in order.
3. Point the agent at the Lakehouse SQL analytics endpoint by swapping `app/db.py` for a
   `pyodbc` connection (the guard and agent code stay unchanged).

## Design decisions
- **Defence in depth:** parse-level validation (sqlglot) plus a read-only connection.
- **Self-correction:** execution errors are fed back to the model instead of failing immediately.
- **Demo mode:** keeps the repo runnable for reviewers with zero setup.

## Tests
`cd backend && python -m pytest -q`

## Roadmap
Schema embeddings for large warehouses, query result caching, LLM eval suite, Power BI semantic model.
