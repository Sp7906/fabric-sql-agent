FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY data/seed.py ./seed.py
CMD ["sh", "-c", "python seed_if_missing.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
