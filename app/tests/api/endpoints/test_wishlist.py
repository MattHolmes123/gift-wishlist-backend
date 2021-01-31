from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings

client = TestClient(app)


URL_PREFIX: str = f"{settings.api_v1_str}/wishlist"


class TestUrls:
    create_items: str = f"{URL_PREFIX}/items/"

    @staticmethod
    def get_item(pk) -> str:
        return f"{URL_PREFIX}/items/{pk}"

    @staticmethod
    def update_item(pk) -> str:
        return f"{URL_PREFIX}/items/{pk}"


def test_create_get_and_update_wishlist_item(test_db, active_user):
    # Test CREATE
    response = client.post(
        TestUrls.create_items,
        json={
            "name": "Boots",
            "url": "https://i-want-some-boots.com",
            "user_id": active_user.id,
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["url"] == "https://i-want-some-boots.com"
    assert data["name"] == "Boots"

    assert "id" in data
    item_id = data["id"]

    # Test GET
    url = TestUrls.get_item(item_id)
    response = client.get(url)

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["url"] == "https://i-want-some-boots.com"
    assert data["name"] == "Boots"
    assert data["id"] == item_id

    # Test UPDATE
    url = TestUrls.update_item(item_id)
    response = client.put(url, json={"name": "Big Boots"})

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["url"] == "https://i-want-some-boots.com"
    assert data["name"] == "Big Boots"
    assert data["id"] == item_id


def test_unknown_item_returns_correct_status(test_db):

    unknown_get_url = TestUrls.get_item(999)
    response = client.get(unknown_get_url)

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()

    assert data["detail"] == "Wish list item not found"

    unknown_update_url = TestUrls.update_item(999)
    response = client.put(unknown_update_url, json={"name": "Unknown boots"})

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()

    assert data["detail"] == "Wish list item not found"


def test_put_validation(test_db):
    unknown_update_url = TestUrls.update_item(999)
    response = client.put(unknown_update_url)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text
