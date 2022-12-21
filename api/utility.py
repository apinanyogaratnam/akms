from typing import List, Tuple

import pandas as pd
import psycopg2
from akms_hash import hash_api_key

from config import db, host, password, user


class InsertFailedError(Exception):
    pass


class QueryFailedError(Exception):
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


def disable_api_key(api_key_id: int) -> None:
    connection = psycopg2.connect(host=host, database=db, user=user, password=password)
    cursor = connection.cursor()
    query = f"""
        UPDATE api_keys
        SET is_active = FALSE
        WHERE api_key_id = {api_key_id};
    """
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()


def query_api_keys(user_id: str) -> List[dict]:
    connection = psycopg2.connect(host=host, database=db, user=user, password=password)
    query_api_keys = """
        SELECT api_key_id, name, description, role, EXTRACT(EPOCH FROM created)::bigint AS created
        FROM api_keys
        WHERE user_id = %s
        AND is_active = TRUE;
    """
    return pd.read_sql(query_api_keys, connection, params=(user_id,)).to_dict(orient="records")


def update_api_key(api_key_id: int, name: str, description: str, role: str) -> dict:
    connection = psycopg2.connect(host=host, database=db, user=user, password=password)
    cursor = connection.cursor()
    update_api_key_query = """
        UPDATE api_keys
        SET name = %s, description = %s, role = %s
        WHERE api_key_id = %s
        AND is_active = True;
    """
    record_to_insert = (name, description, role, api_key_id)
    cursor.execute(update_api_key_query, record_to_insert)
    connection.commit()
    cursor.close()
    connection.close()

    return {"name": name, "description": description, "role": role}


class NotFoundError(Exception):
    pass


def get_api_key(api_key_id: int) -> dict:
    connection = psycopg2.connect(host=host, database=db, user=user, password=password)
    query_api_key = """
        SELECT
            name,
            description,
            role
        FROM api_keys
        WHERE api_key_id = %s
        AND is_active = True;
    """

    if result := pd.read_sql(query_api_key, connection, params=(api_key_id,)).to_dict(orient="records"):
        return result[0]

    raise NotFoundError(f"Api Key with api_key_id: {api_key_id} not found in our records.")
