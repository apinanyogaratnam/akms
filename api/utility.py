import pandas as pd
import psycopg2
from akms_hash import hash_api_key
from typing import Tuple

from config import db, host, password, user


class InsertFailedError(Exception):
    pass


def save_api_key_to_db(user_id: str, hashed_api_key: str, name: str, description: str, role: str) -> None:
    try:
        connection = psycopg2.connect(host=host, database=db, user=user, password=password)
        cursor = connection.cursor()
    except psycopg2.Error as error:
        raise ConnectionError(error)

    try:
        insert_query = """
            INSERT INTO api_keys (
                user_id,
                hashed_api_key,
                name,
                description,
                role
            ) VALUES (
                %s, %s, %s, %s, %s
            );
        """
        cursor.execute(insert_query, (user_id, hashed_api_key, name, description, role))
        connection.commit()
    except Exception as error:
        connection.rollback()
        raise InsertFailedError(error)
    finally:
        cursor.close()
        connection.close()


def is_valid_api_key(api_key: str) -> Tuple[bool, str]:
    hashed_api_key = hash_api_key(api_key, api_key)
    connection = psycopg2.connect(host=host, database=db, user=user, password=password)
    query_api_key = f"""
        SELECT hashed_api_key, role
        FROM api_keys
        WHERE hashed_api_key = '{hashed_api_key}'
        AND is_active = TRUE;
    """
    results = pd.read_sql(query_api_key, connection)
    connection.close()
    is_valid_key = not results.empty
    role = results["role"].values[0] if is_valid_key else None
    return is_valid_key, role
