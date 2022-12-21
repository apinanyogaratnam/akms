import warnings

from http import HTTPStatus
from uuid import uuid4

from akms_hash import hash_api_key
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel, Field

from api.utility import (
    InsertFailedError,
    QueryFailedError,
    disable_api_key,
    is_valid_api_key,
    query_api_keys,
    save_api_key_to_db,
    update_api_key,
    get_api_key,
    NotFoundError,
)

warnings.filterwarnings("ignore")

app = FastAPI()


@app.get("/")
def home():
    return {"status": "running"}


class Item(BaseModel):
    user_id: str
    name: str
    description: str | None = Field(default=None, title="The description of the item")
    role: str


@app.post("/create_api_key")
def create_api_key(item: Item = Body(...)) -> dict:
    api_key = str(uuid4())
    hashed_api_key = hash_api_key(api_key, api_key)
    # save hashed_api_key to db
    try:
        save_api_key_to_db(item.user_id, hashed_api_key, item.name, item.description, item.role)
    except (InsertFailedError, ConnectionError) as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(error)) from error
    return {"api_key": api_key, "status_code": HTTPStatus.CREATED.value}


@app.get("/api_keys")
def get_api_keys(user_id: str) -> dict:
    try:
        api_keys = query_api_keys(user_id)
    except (ConnectionError, QueryFailedError) as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(error)) from error

    return {"api_keys": api_keys, "status_code": HTTPStatus.OK.value}


@app.get("/api_key")
def get_api_key_metadata(api_key_id: int) -> dict:
    try:
        api_key = get_api_key(api_key_id)
    except NotFoundError:
        return {"api_key": None, "status_code": HTTPStatus.NOT_FOUND.value}
    except Exception as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(error)) from error

    return {"api_key": api_key, "status_code": HTTPStatus.OK.value}


class UpdateApiKey(BaseModel):
    api_key_id: int
    name: str
    description: str
    role: str


@app.put("/api_key")
def update_api_key_metadata(item: UpdateApiKey = Body(...)) -> dict:
    try:
        update_api_key(item.api_key_id, item.name, item.description, item.role)
    except Exception as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(error)) from error

    return {"status": "success", "status_code": HTTPStatus.OK.value}


class ApiKey(BaseModel):
    api_key: str


@app.post("/validate_api_key")
def validate_api_key(item: ApiKey = Body(...)) -> dict:
    is_valid_key, role = is_valid_api_key(item.api_key)
    return {"is_valid_key": is_valid_key, "role": role, "status_code": HTTPStatus.OK.value}


class DeleteApiKey(BaseModel):
    api_key_id: int


@app.delete("/delete_api_key")
def delete_api_key(item: DeleteApiKey = Body(...)) -> dict:
    try:
        disable_api_key(item.api_key_id)
    except Exception as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(error)) from error

    return {"status": "success", "status_code": HTTPStatus.OK.value}
