import psycopg2
from config import host, db, user, password
from akms_hash import hash_api_key
import pandas as pd


class InsertFailedError(Exception):
    pass


def save_api_key_to_db(user_id: str, hashed_api_key: str, name: str, description: str, plan: str) -> None:
    try:
        connection = psycopg2.connect(
            host=host,
            database=db,
            user=user,
            password=password
        )
        cursor = connection.cursor()
    except psycopg2.Error as error:
        raise ConnectionError(error)

    try:
        insert_query = """
            INSERT INTO api_keys (
                user_id,
                key,
                name,
                description,
                plan
            ) VALUES (
                %s, %s, %s, %s, %s
            );
        """

        cursor.execute(insert_query, (user_id, hashed_api_key, name, description, plan))
        connection.commit()
    except Exception as error:
        connection.rollback()
        raise InsertFailedError(error)
    finally:
        cursor.close()
        connection.close()


def is_valid_api_key(api_key: str) -> bool:
    hashed_api_key = str(hash_api_key(api_key))

    connection = psycopg2.connect(
        host=host,
        database=db,
        user=user,
        password=password
    )
    query_api_key = """
        SELECT key FROM api_keys WHERE key = %s;
    """
    df = pd.read_sql(query_api_key, connection, params=(hashed_api_key,))
    connection.close()

    return not df.empty
