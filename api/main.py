from fastapi import FastAPI
from akms_hash import hash_api_key
from uuid import uuid4
from api.utility import save_api_key_to_db, InsertFailedError
from http import HTTPStatus

app = FastAPI()


@app.get("/")
def read_root():
    return {"data": "api is running"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.post("/create_api_key")
def create_api_key(key: str, name: str, description: str, plan: str):
    api_key = str(uuid4())
    hashed_api_key = hash_api_key(api_key)
    # save hashed_api_key to db
    try:
        save_api_key_to_db(hashed_api_key, name, description, plan)
    except InsertFailedError as error:
        return {"error": str(error)}, HTTPStatus.INTERNAL_SERVER_ERROR.value
    return {"api_key": api_key, "hashed_api_key": hashed_api_key}
