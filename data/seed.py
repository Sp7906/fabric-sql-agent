"""Builds a local SQLite 'gold' layer that mirrors the Fabric gold tables."""
import os, random, sqlite3
from datetime import date, timedelta


def build(path="data/gold.db"):
    random.seed(7)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.executescript("""
    CREATE TABLE dim_customer(customer_id INTEGER PRIMARY KEY, name TEXT, region TEXT, segment TEXT);
    CREATE TABLE dim_product(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, unit_price REAL);
    CREATE TABLE fact_sales(order_id INTEGER PRIMARY KEY, order_date TEXT, customer_id INTEGER,
                            product_id INTEGER, quantity INTEGER, revenue REAL);
    """)
    regions = ["North", "South", "East", "West"]
    segments = ["Consumer", "Corporate", "SMB"]
    cats = {"Laptops": 900, "Phones": 600, "Accessories": 40, "Software": 120}
    con.executemany("INSERT INTO dim_customer VALUES (?,?,?,?)",
                    [(i, f"Customer {i}", random.choice(regions), random.choice(segments)) for i in range(1, 101)])
    products = [(i, f"{c} {i}", c, round(p * random.uniform(0.8, 1.3), 2))
                for i, (c, p) in enumerate(list(cats.items()) * 5, start=1)]
    con.executemany("INSERT INTO dim_product VALUES (?,?,?,?)", products)
    start = date(2025, 1, 1)
    rows = []
    for oid in range(1, 5001):
        pid = random.randint(1, len(products))
        qty = random.randint(1, 5)
        d = start + timedelta(days=random.randint(0, 600))
        rows.append((oid, d.isoformat(), random.randint(1, 100), pid, qty,
                     round(products[pid - 1][3] * qty, 2)))
    con.executemany("INSERT INTO fact_sales VALUES (?,?,?,?,?,?)", rows)
    con.commit()
    con.close()
    print(f"Seeded {path}")


if __name__ == "__main__":
    build()
