"""Generates data/raw/orders.csv: sample input for the Fabric bronze notebook."""
import csv
import os
import random
from datetime import date, timedelta

random.seed(7)
regions = ["North", "South", "East", "West"]
segments = ["Consumer", "Corporate", "SMB"]
cats = {"Laptops": 900, "Phones": 600, "Accessories": 40, "Software": 120}
customers = [(i, f"Customer {i}", random.choice(regions), random.choice(segments)) for i in range(1, 101)]
products = [(i, f"{c} {i}", c, round(p * random.uniform(0.8, 1.3), 2))
            for i, (c, p) in enumerate(list(cats.items()) * 5, start=1)]

os.makedirs("data/raw", exist_ok=True)
with open("data/raw/orders.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["order_id", "order_date", "customer_id", "customer_name", "region", "segment",
                "product_id", "product_name", "category", "unit_price", "quantity"])
    for oid in range(1, 5001):
        c, p = random.choice(customers), random.choice(products)
        d = date(2025, 1, 1) + timedelta(days=random.randint(0, 600))
        w.writerow([oid, d.isoformat(), c[0], c[1], c[2], c[3], p[0], p[1], p[2], p[3], random.randint(1, 5)])
print("Wrote data/raw/orders.csv")
