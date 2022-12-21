from http import HTTPStatus

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_read_home():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == {"status": "running"}


def __create_api_key():
    user_id = "test@test.com"
    name = "main api key"
    description = "production api key"
    role = "admin"
    response = client.post(
        "/create_api_key", json={"user_id": user_id, "name": name, "description": description, "role": role}
    )
    return response.json()


def __get_api_key(api_key_id: int):
    response = client.get(f"/api_key?api_key_id={api_key_id}")
    return response.json()


def __get_api_keys(user_id: str):
    user_id = "test@test.com"
    response = client.get(f"/api_keys?user_id={user_id}")
    return response.json()


def __update_api_key(api_key_id: int):
    response = client.put(
        "/api_key",
        json={
            "api_key_id": api_key_id,
            "name": "updated name",
            "description": "updated description",
            "role": "updated role",
        },
    )
    return response.json()


def __delete_api_key(api_key_id: int):
    response = client.delete("/api_key", json={"api_key_id": api_key_id})
    return response.json()


def test_create_api_key():
    response = __create_api_key()

    actual_api_key = response.get("api_key")
    actual_status_code = response["status_code"]

    assert actual_status_code == HTTPStatus.CREATED.value
    assert isinstance(actual_api_key, str)
    assert len(response.json()["api_key"]) == 36


def test_get_api_key():
    response = __create_api_key()
    response = __get_api_keys("test@test.com")
    api_key_id = response["api_keys"][0]["api_key_id"]
    response = __get_api_key(api_key_id)

    api_key = response["api_key"]

    assert response["status_code"] == HTTPStatus.OK.value
    assert "name" in api_key
    assert "description" in api_key
    assert "role" in api_key


def test_get_api_keys():
    response = __create_api_key()
    response = __get_api_keys("test@test.com")

    assert response["status_code"] == HTTPStatus.OK.value
    assert isinstance(response["api_keys"], list)
    assert len(response["api_keys"]) > 0

    for _ in response["api_keys"]:
        assert "name" in response
        assert "description" in response
        assert "role" in response


def test_update_api_key():
    response = __create_api_key()
    response = __get_api_keys("test@test.com")
    api_key_id = response["api_keys"][0]["api_key_id"]
    response = __update_api_key(api_key_id)

    api_key = response["api_key"]

    assert response["status_code"] == HTTPStatus.OK.value
    assert "name" in api_key
    assert "description" in api_key
    assert "role" in api_key


def test_validate_api_key():
    response = __create_api_key()
    response = client.post("/validate_api_key", json={"api_key": response["api_key"]})

    assert response["status_code"] == HTTPStatus.OK.value
    assert response["is_valid_key"]
    assert "role" in response


def test_delete_api_key():
    response = __create_api_key()
    response = __create_api_key()
    response = __get_api_keys()
    api_key_id = response["api_keys"][0]["api_key_id"]
    response = __delete_api_key(api_key_id)

    assert response["status_code"] == HTTPStatus.OK.value

    assert response["status"] == "success"
