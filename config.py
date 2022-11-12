import os
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get("DATABASE_HOST") or "localhost"
db = os.environ.get("DATABASE_NAME") or "postgres"
user = os.environ.get("DATABASE_USER") or "postgres"
password = os.environ.get("DATABASE_PASSWORD") or "postgres"
