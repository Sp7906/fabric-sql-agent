import os
from seed import build

db = os.getenv("DB_PATH", "data/gold.db")
if not os.path.exists(db):
    build(db)
