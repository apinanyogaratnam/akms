import warnings
from http import HTTPStatus
from uuid import uuid4

from akms_hash import hash_api_key
from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel, Field

from api.utility import InsertFailedError, is_valid_api_key, save_api_key_to_db

warnings.filterwarnings("ignore")

app = FastAPI()


class Item(BaseModel):
    user_id: str
    name: str
    description: str | None = Field(default=None, title="The description of the item")
    role: str


@app.post("/create_api_key")
def create_api_key(item: Item = Body(...)):
    api_key = str(uuid4())
    hashed_api_key = hash_api_key(api_key, api_key)
    # save hashed_api_key to db
    try:
        save_api_key_to_db(item.user_id, hashed_api_key, item.name, item.description, item.role)
    except (InsertFailedError, ConnectionError) as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=str(error))
    return {"api_key": api_key, "status_code": HTTPStatus.OK.value}


class ApiKey(BaseModel):
    api_key: str


@app.post("/validate_api_key")
def validate_api_key(item: ApiKey = Body(...)):
    is_valid_key, role = is_valid_api_key(item.api_key)
    return {"is_valid_key": is_valid_key, "role": role, "status_code": HTTPStatus.OK.value}
