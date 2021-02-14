from typing import TYPE_CHECKING

from app.core.config import settings
from app.tests.api.utils import login_user

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from app.tests.api.conftest import UserTokens

from app.tests.conftest import TestUsers

URL_PREFIX: str = f"{settings.api_v1_str}/login"


# TODO: Import the urls from the modules rather than TestUrls
class TestUrls:
    get_login_token: str = f"{URL_PREFIX}/access-token"
    test_token: str = f"{URL_PREFIX}/test-token"


def test_get_login_token_as_superuser(client: "TestClient"):
    # login_user has its own assertions
    login_user(client, TestUsers.superuser.email, "superuserpassword")


def test_get_login_token_with_valid_user_but_invalid_password(client: "TestClient"):
    response = client.post(
        TestUrls.get_login_token,
        data={"username": TestUsers.superuser.email, "password": "Incorrect Password"},
    )

    assert response.status_code == 400


def test_get_login_token_with_inactive_user(client: "TestClient"):
    response = client.post(
        TestUrls.get_login_token,
        data={
            "username": TestUsers.inactive_user.email,
            "password": "inactiveuserpassword",
        },
    )

    assert response.status_code == 400


def test_get_login_token_with_invalid_user(client: "TestClient"):
    response = client.post(
        TestUrls.get_login_token,
        data={"username": "notarealuser@email.com", "password": "invaliduserpassword"},
    )

    assert response.status_code == 400


def test_test_token_for_superuser(client: "TestClient", tokens: "UserTokens"):
    response = client.post(TestUrls.test_token, auth=tokens.superuser)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == TestUsers.superuser.id

    assert data["is_superuser"]
    assert data["is_active"]

    assert data["email"] == TestUsers.superuser.email
    assert data["full_name"] == TestUsers.superuser.full_name


def test_test_token_for_active_user(client: "TestClient", tokens: "UserTokens"):
    response = client.post(TestUrls.test_token, auth=tokens.active_user)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == TestUsers.active_user.id

    assert not data["is_superuser"]
    assert data["is_active"]

    assert data["email"] == TestUsers.active_user.email
    assert data["is_active"] == TestUsers.active_user.is_active
    assert data["full_name"] == TestUsers.active_user.full_name


def test_test_token_with_invalid_auth(client: "TestClient", tokens: "UserTokens"):
    response = client.post(TestUrls.test_token, auth=tokens.inactive_user)

    assert response.status_code == 403
