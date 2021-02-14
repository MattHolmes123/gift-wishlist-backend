from typing import TYPE_CHECKING

from fastapi import status

from app import crud, schemas
from app.core.config import settings
from app.tests.api.utils import BearerAuth, login_user
from app.tests.conftest import TestUsers

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

    from app.models import User
    from app.tests.api.conftest import UserTokens


URL_PREFIX: str = f"{settings.api_v1_str}/users"


class TestUrls:
    get_users: str = f"{URL_PREFIX}/"
    create_user: str = f"{URL_PREFIX}/"
    update_user_me: str = f"{URL_PREFIX}/me"
    get_user_me: str = f"{URL_PREFIX}/me"

    @staticmethod
    def read_user_by_id(pk: int) -> str:
        return f"{URL_PREFIX}/{pk}"

    @staticmethod
    def update_user(pk: int) -> str:
        return f"{URL_PREFIX}/{pk}"


def test_read_users(client: "TestClient", tokens: "UserTokens"):

    response = client.get(TestUrls.get_users, auth=tokens.superuser)

    assert response.status_code == 200

    actual = response.json()

    assert len(actual) == 3

    # Sort by name and check they are correct
    returned_users = sorted(actual, key=lambda x: x["full_name"])
    active_user = returned_users[0]
    inactive_user = returned_users[1]
    super_user = returned_users[2]

    assert active_user["email"] == "active_user@email.com"
    assert inactive_user["email"] == "inactive_user@email.com"
    assert super_user["email"] == "superuser@email.com"

    # Now check keys returned
    expected_keys = sorted(["email", "is_active", "is_superuser", "full_name", "id"])

    for user in returned_users:
        user_attributes = sorted(user.keys())

        assert user_attributes == expected_keys


def test_read_users_not_authorised(client: "TestClient", tokens: "UserTokens"):
    response = client.get(TestUrls.get_users, auth=tokens.active_user)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_user_successful(client: "TestClient", tokens: "UserTokens"):

    new_user = schemas.user.UserCreate(email="newuser@email.com", password="password")

    response = client.post(
        TestUrls.create_user, auth=tokens.superuser, json=new_user.dict()
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_create_existing_user(client: "TestClient", super_auth: "BearerAuth"):
    new_user = schemas.user.UserCreate(
        email=TestUsers.active_user.email, password="activeuserpassword"
    )

    response = client.post(TestUrls.create_user, auth=super_auth, json=new_user.dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_can_update_self(client: "TestClient", tokens: "UserTokens"):

    new_email = "updated_active_user@email.com"
    new_name = "Updated Active User"

    response = client.put(
        TestUrls.update_user_me,
        auth=tokens.active_user,
        json={"password": "new-password", "full_name": new_name, "email": new_email},
    )

    assert response.status_code == status.HTTP_200_OK

    actual = response.json()

    assert actual["id"] == TestUsers.active_user.id
    assert actual["is_active"]
    assert not actual["is_superuser"]

    assert actual["email"] == new_email
    assert actual["full_name"] == new_name

    # TODO: Reset until tests can be isolated
    response = client.put(
        TestUrls.update_user_me,
        auth=tokens.active_user,
        json={
            "password": TestUsers.active_user.password,
            "full_name": TestUsers.active_user.full_name,
            "email": TestUsers.active_user.email,
        },
    )


def test_read_user_me(client: "TestClient", tokens: "UserTokens"):

    response = client.get(TestUrls.get_user_me, auth=tokens.active_user)

    assert response.status_code == status.HTTP_200_OK

    actual = response.json()

    assert actual["id"] == TestUsers.active_user.id
    assert actual["is_active"]
    assert not actual["is_superuser"]

    assert actual["email"] == TestUsers.active_user.email
    assert actual["full_name"] == TestUsers.active_user.full_name


def test_read_user_me_inactive(
    client: "TestClient", tokens: "UserTokens", active_user: "User", db
):

    # User is marked as inactive before getting user details.
    _ = crud.user.update(
        db,
        db_obj=active_user,
        obj_in=schemas.user.UserUpdate(is_active=False).dict(exclude_unset=True),
    )

    response = client.get(TestUrls.get_user_me, auth=tokens.active_user)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    _ = crud.user.update(
        db, db_obj=active_user, obj_in=schemas.user.UserUpdate(is_active=True)
    )


def test_read_user_me_deleted_user(client: "TestClient", db):

    email = "test@email.com"
    password = "password"
    user = crud.user.get_by_email(db, email=email)

    if not user:
        user_in = schemas.user.UserCreate(
            email=email,
            password=password,
            full_name="Test user",
        )

        user = crud.user.create(db, obj_in=user_in)

    login_data = login_user(client, user.email, password)
    bearer_auth = BearerAuth(login_data.access_token)

    # Now the user is deleted after we have the login information
    crud.user.remove(db, id=user.id)

    response = client.get(TestUrls.get_user_me, auth=bearer_auth)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_read_user_by_id_successful(client: "TestClient", tokens: "UserTokens"):

    url = TestUrls.read_user_by_id(TestUsers.active_user.id)

    response = client.get(url, auth=tokens.superuser)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == TestUsers.active_user.id

    # test self
    url = TestUrls.read_user_by_id(TestUsers.superuser.id)
    response = client.get(url, auth=tokens.superuser)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == TestUsers.superuser.id


def test_read_user_by_id_forbidden(client: "TestClient", tokens: "UserTokens"):
    url = TestUrls.read_user_by_id(TestUsers.superuser.id)

    response = client.get(url, auth=tokens.active_user)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_user(client: "TestClient", tokens: "UserTokens"):
    url = TestUrls.update_user(TestUsers.active_user.id)

    response = client.put(url, auth=tokens.superuser, json={"password": "new_password"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == TestUsers.active_user.id

    # TODO: Reset password until tests are isolated.
    client.put(url, auth=tokens.superuser, json={"password": "activeuserpassword"})


def test_update_user_invalid_user(client: "TestClient", tokens: "UserTokens"):
    url = TestUrls.update_user(9999)

    response = client.put(url, auth=tokens.superuser, json={"password": "new_password"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
