import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/gold.db")
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AOAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
AOAI_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
MAX_ROWS = 500
MAX_ATTEMPTS = 3
