import psycopg2
from dotenv import load_dotenv

from config import db, host, password, user

load_dotenv()

table_name = "api_keys"
drop_table = f"""DROP TABLE IF EXISTS {table_name};"""

create_table = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        api_key_id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY NOT NULL,
        created TIMESTAMPTZ DEFAULT timezone('utc', NOW()) NOT NULL,
        user_id TEXT UNIQUE NOT NULL,
        key BYTEA NOT NULL,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        plan TEXT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE NOT NULL
    );
"""

indexes = [
    f"CREATE INDEX IF NOT EXISTS {table_name}_key_idx ON {table_name} (key);",
]

try:
    connection = psycopg2.connect(
        host=host,
        database=db,
        user=user,
        password=password,
    )

    cursor = connection.cursor()
except psycopg2.Error as error:
    print("Error while connecting to PostgreSQL", error)
    exit()

try:
    cursor.execute(drop_table)
    cursor.execute(create_table)
    for index in indexes:
        cursor.execute(index)
    connection.commit()
    print("Table created successfully.")
except Exception as error:
    connection.rollback()
    print("Error while connecting to PostgreSQL", error)
    print("Table creation failed.")
finally:
    cursor.close()
    connection.close()
