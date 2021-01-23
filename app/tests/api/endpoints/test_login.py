from typing import TYPE_CHECKING

from app.core.config import settings
from app.tests.api.utils import login_user

if TYPE_CHECKING:
    from app.models.user import User
    from fastapi.testclient import TestClient


URL_PREFIX: str = f"{settings.api_v1_str}/login"


# TODO: Import the urls from the modules rather than TestUrls
class TestUrls:
    get_login_token: str = f"{URL_PREFIX}/access-token"
    test_token: str = f"{URL_PREFIX}/test-token"


def test_get_login_token_as_superuser(client: "TestClient", superuser: "User"):
    # login_user has its own assertions
    login_user(client, superuser, "superuserpassword")


def test_get_login_token_with_valid_user_but_invalid_password(
    client: "TestClient", superuser: "User"
):
    response = client.post(
        TestUrls.get_login_token,
        data={"username": superuser.email, "password": "Incorrect Password"},
    )

    assert response.status_code == 400


def test_get_login_token_with_inactive_user(
    client: "TestClient", inactive_user: "User"
):
    response = client.post(
        TestUrls.get_login_token,
        data={"username": inactive_user.email, "password": "inactiveuserpassword"},
    )

    assert response.status_code == 400


def test_get_login_token_with_invalid_user(client: "TestClient"):
    response = client.post(
        TestUrls.get_login_token,
        data={"username": "notarealuser@email.com", "password": "invaliduserpassword"},
    )

    assert response.status_code == 400


def test_test_token_for_superuser(client: "TestClient", super_auth, superuser: "User"):
    response = client.post(TestUrls.test_token, auth=super_auth)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == superuser.id

    assert data["is_superuser"]
    assert data["is_active"]

    assert data["email"] == superuser.email
    assert data["full_name"] == superuser.full_name


def test_test_token_for_active_user(
    client: "TestClient", active_auth, active_user: "User"
):
    response = client.post(TestUrls.test_token, auth=active_auth)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == active_user.id

    assert not data["is_superuser"]
    assert data["is_active"]

    assert data["email"] == active_user.email
    assert data["is_active"] == active_user.is_active
    assert data["full_name"] == active_user.full_name


def test_test_token_with_invalid_auth(client: "TestClient", invalid_auth):
    response = client.post(TestUrls.test_token, auth=invalid_auth)

    assert response.status_code == 403
