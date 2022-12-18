import os

from dotenv import load_dotenv

load_dotenv()

host = os.environ.get("DATABASE_HOST")
db = os.environ.get("DATABASE_NAME")
user = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_PASSWORD")
