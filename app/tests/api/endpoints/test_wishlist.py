from typing import TYPE_CHECKING

from fastapi import status

from app.core.config import settings
from app.tests.conftest import TestUsers

if TYPE_CHECKING:
    from app.tests.api.conftest import UserTokens


URL_PREFIX: str = f"{settings.api_v1_str}/wishlist"


class TestUrls:
    all_items: str = f"{URL_PREFIX}/items/"
    create_items: str = f"{URL_PREFIX}/items/"

    @staticmethod
    def get_item(pk) -> str:
        return f"{URL_PREFIX}/items/{pk}"

    @staticmethod
    def update_item(pk) -> str:
        return f"{URL_PREFIX}/items/{pk}"


def test_create_get_and_update_wishlist_item(client, db, tokens: "UserTokens"):
    # Test CREATE
    response = client.post(
        TestUrls.create_items,
        auth=tokens.active_user,
        json={
            "name": "Boots",
            "url": "https://i-want-some-boots.com",
            "user_id": TestUsers.active_user.id,
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
    response = client.get(url, auth=tokens.active_user)

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["url"] == "https://i-want-some-boots.com"
    assert data["name"] == "Boots"
    assert data["id"] == item_id

    # Test UPDATE
    url = TestUrls.update_item(item_id)
    response = client.put(url, auth=tokens.active_user, json={"name": "Big Boots"})

    assert response.status_code == 200, response.text
    data = response.json()

    assert data["url"] == "https://i-want-some-boots.com"
    assert data["name"] == "Big Boots"
    assert data["id"] == item_id


def test_unknown_item_returns_correct_status(client, db, tokens: "UserTokens"):

    unknown_get_url = TestUrls.get_item(999)
    response = client.get(unknown_get_url, auth=tokens.active_user)

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()

    assert data["detail"] == "Wish list item not found"

    unknown_update_url = TestUrls.update_item(999)
    response = client.put(
        unknown_update_url, auth=tokens.active_user, json={"name": "Unknown boots"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
    data = response.json()

    assert data["detail"] == "Wish list item not found"


def test_put_validation(client, db, tokens: "UserTokens"):
    unknown_update_url = TestUrls.update_item(999)
    response = client.put(unknown_update_url, auth=tokens.active_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


def test_get_items(client, db, tokens: "UserTokens"):

    # A user creates several items
    for item_id in range(5):
        client.post(
            TestUrls.create_items,
            auth=tokens.active_user,
            json={
                "name": f"Item {item_id}",
                "url": f"https://i-want-item-{item_id}.com",
                "user_id": TestUsers.active_user.id,
            },
        )

    # The superuser can view them all
    response = client.get(TestUrls.all_items, auth=tokens.superuser)

    assert response.status_code == status.HTTP_200_OK

    items = response.json()

    assert isinstance(items, list)

    # we created 5 items
    assert len(items) >= 5

    first_two = items[:2]
    next_three = items[2:5]

    # Limit to two and compare against all results
    first_two_items_url = f"{TestUrls.all_items}?limit=2"
    response = client.get(first_two_items_url, auth=tokens.superuser)
    assert response.status_code == status.HTTP_200_OK
    two_limited_items = response.json()

    assert two_limited_items == first_two

    # Limit to three and skip the ones we have already checked
    next_three_items_url = f"{TestUrls.all_items}?limit=3&skip=2"
    response = client.get(next_three_items_url, auth=tokens.superuser)
    assert response.status_code == status.HTTP_200_OK
    three_limited_items = response.json()

    assert three_limited_items == next_three
