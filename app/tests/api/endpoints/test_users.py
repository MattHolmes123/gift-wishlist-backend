from typing import TYPE_CHECKING

from fastapi import status

from app import crud, schemas
from app.core.config import settings
from app.tests.api.utils import BearerAuth, login_user

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

    from app.models import User


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


def test_read_users(client: "TestClient", all_users_created, super_auth: "BearerAuth"):

    response = client.get(TestUrls.get_users, auth=super_auth)

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


def test_read_users_not_authorised(client: "TestClient", active_auth: "BearerAuth"):
    response = client.get(TestUrls.get_users, auth=active_auth)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_user_successful(client: "TestClient", super_auth: "BearerAuth"):

    new_user = schemas.user.UserCreate(email="newuser@email.com", password="password")

    response = client.post(TestUrls.create_user, auth=super_auth, json=new_user.dict())

    assert response.status_code == status.HTTP_201_CREATED


def test_create_existing_user(
    client: "TestClient", super_auth: "BearerAuth", active_user: "User"
):
    new_user = schemas.user.UserCreate(
        email=active_user.email, password="activeuserpassword"
    )

    response = client.post(TestUrls.create_user, auth=super_auth, json=new_user.dict())

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_can_update_self(
    client: "TestClient", active_auth: "BearerAuth", active_user: "User"
):

    new_email = "updated_active_user@email.com"
    new_name = "Updated Active User"

    response = client.put(
        TestUrls.update_user_me,
        auth=active_auth,
        json={"password": "new-password", "full_name": new_name, "email": new_email},
    )

    assert response.status_code == status.HTTP_200_OK

    actual = response.json()

    assert actual["id"] == active_user.id
    assert actual["is_active"]
    assert not actual["is_superuser"]

    assert actual["email"] == new_email
    assert actual["full_name"] == new_name


def test_read_user_me(
    client: "TestClient", active_auth: "BearerAuth", active_user: "User"
):

    response = client.get(TestUrls.get_user_me, auth=active_auth)

    assert response.status_code == status.HTTP_200_OK

    actual = response.json()

    assert actual["id"] == active_user.id
    assert actual["is_active"]
    assert not actual["is_superuser"]

    assert actual["email"] == active_user.email
    assert actual["full_name"] == active_user.full_name


def test_read_user_me_inactive(
    client: "TestClient", active_auth: "BearerAuth", active_user: "User", db
):

    # User is marked as inactive before getting user details.
    _ = crud.user.update(
        db,
        db_obj=active_user,
        obj_in=schemas.user.UserUpdate(is_active=False).dict(exclude_unset=True),
    )

    response = client.get(TestUrls.get_user_me, auth=active_auth)

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

    login_data = login_user(client, user, password)
    bearer_auth = BearerAuth(login_data.access_token)

    # Now the user is deleted after we have the login information
    crud.user.remove(db, id=user.id)

    response = client.get(TestUrls.get_user_me, auth=bearer_auth)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_read_user_by_id_successful(
    client: "TestClient",
    super_auth: "BearerAuth",
    active_user: "User",
    superuser: "User",
):

    url = TestUrls.read_user_by_id(active_user.id)

    response = client.get(url, auth=super_auth)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == active_user.id

    # test self
    url = TestUrls.read_user_by_id(superuser.id)
    response = client.get(url, auth=super_auth)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == superuser.id


def test_read_user_by_id_forbidden(
    client: "TestClient", active_auth: "BearerAuth", superuser: "User"
):
    url = TestUrls.read_user_by_id(superuser.id)

    response = client.get(url, auth=active_auth)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_user(client: "TestClient", super_auth: "BearerAuth", active_user):
    url = TestUrls.update_user(active_user.id)

    response = client.put(url, auth=super_auth, json={"password": "new_password"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == active_user.id

    # Reset password until tests are isolated.
    client.put(url, auth=super_auth, json={"password": "activeuserpassword"})


def test_update_user_invalid_user(client: "TestClient", super_auth: "BearerAuth"):
    url = TestUrls.update_user(9999)

    response = client.put(url, auth=super_auth, json={"password": "new_password"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
