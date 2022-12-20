from fastapi.testclient import TestClient
from api.main import app
from http import HTTPStatus

client = TestClient(app)


def test_read_home():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK.value
    assert response.json() == {'status': 'running'}


def test_create_api_key():
    user_id = 'test@test.com'
    name = 'main api key'
    description = 'production api key'
    role = 'admin'

    response = client.post("/create_api_key", json={'user_id': user_id, 'name': name, 'description': description, 'role': role})

    actual_api_key = response.json()['api_key']
    actual_status_code = response.json()['status_code']

    assert actual_status_code == HTTPStatus.CREATED.value
    assert isinstance(actual_api_key, str)
    assert len(response.json()['api_key']) == 36
