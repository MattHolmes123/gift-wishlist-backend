from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_put_validation():
    response = client.get("/playground/get-app-state")

    assert response.status_code == status.HTTP_200_OK, response.text

    assert response.json() == {
        "count": 42,
        "playground_list_data": [
            {"msg": "First message", "foo": 1, "bar": 2, "baz": 3},
            {"msg": "Second message", "foo": 11, "bar": 22, "baz": 33},
        ],
    }
