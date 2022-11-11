import psycopg2
from config import host, db, user, password


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
        print("Record inserted successfully.")
    except Exception as error:
        connection.rollback()
        print("Error while connecting to PostgreSQL", error)
        print("Record insertion failed.")

        raise InsertFailedError("Storing the API key failed to insert into the database.")
    finally:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed.")
