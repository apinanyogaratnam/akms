from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field
from akms_hash import hash_api_key
from uuid import uuid4
from api.utility import save_api_key_to_db, InsertFailedError, is_valid_api_key
from http import HTTPStatus

app = FastAPI()


@app.get("/")
def read_root():
    return {"data": "api is running"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


class Item(BaseModel):
    user_id: str
    name: str
    description: str | None = Field(default=None, title="The description of the item")
    plan: str


@app.post("/create_api_key")
def create_api_key(item: Item = Body(...)):
    api_key = str(uuid4())
    hashed_api_key = str(hash_api_key(api_key))
    # save hashed_api_key to db
    try:
        save_api_key_to_db(item.user_id, hashed_api_key, item.name, item.description, item.plan)
    except (InsertFailedError, ConnectionError) as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(error))
    return {"api_key": api_key, "status_code": HTTPStatus.OK.value}


class ApiKey(BaseModel):
    api_key: str


@app.post("/validate_api_key")
def validate_api_key(item: ApiKey = Body(...)):
    return {"is_valid": is_valid_api_key(item.api_key)}
