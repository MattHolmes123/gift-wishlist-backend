from typing import TYPE_CHECKING

from requests.auth import AuthBase

from app import schemas
from app.core.config import settings

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from app.models.user import User


class BearerAuth(AuthBase):
    """Auth class for Bearer Token authentication"""

    def __init__(self, token):
        """Load a valid bearer token.

        :param token: Bearer token
        """

        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token

        return r


def login_user(client: "TestClient", user: "User", password: str) -> schemas.Token:
    """Log in the user.

    :param client: Test client
    :param user: User model
    :param password: User password
    :return: Login data
    """

    url = f"{settings.api_v1_str}/login/access-token"

    response = client.post(url, data={"username": user.email, "password": password})

    assert response.status_code == 200

    data = response.json()

    assert data["token_type"] == "bearer"
    assert data["access_token"]

    return schemas.Token(**data)
