from typing import TYPE_CHECKING

import pytest

from app import crud
from app.database.db import SessionLocal
from app.schemas.user import UserCreate

if TYPE_CHECKING:
    from app.models.user import User
    from fastapi.testclient import TestClient
    from ..conftest import TestDatabase

from .utils import BearerAuth, login_user

from app.main import app
from app.api.deps import get_db


@pytest.fixture()
def db(module_db: "TestDatabase"):
    """Gets the database session

    :param module_db: clean database session class
    :return: Database session
    """

    app.dependency_overrides[get_db] = module_db

    return module_db.get_db()


@pytest.fixture()
def superuser(db) -> "User":
    """Gets the sample super user

    :param db: Database connection
    :return: Super User model
    """

    superuser_email = "superuser@email.com"

    user = crud.user.get_by_email(db, email=superuser_email)

    if user:
        return user

    user_in = UserCreate(
        email="superuser@email.com",
        password="superuserpassword",
        is_superuser=True,
        full_name="Super User",
    )

    return crud.user.create(db, obj_in=user_in)


@pytest.fixture()
def super_auth(client: "TestClient", superuser: "User") -> BearerAuth:
    """Login a superuser and return a request BearerAuth to be used in tests.

    :param client: Test Client
    :param superuser: A superuser model
    :return: Requests Bearer Auth class
    """

    login_data = login_user(client, superuser, "superuserpassword")

    bearer_auth = BearerAuth(login_data.access_token)

    return bearer_auth


@pytest.fixture()
def active_user(db) -> "User":
    """Gets the sample active user.

    :param db: Database connection
    :return: Active user model
    """

    active_user_email = "active_user@email.com"

    user = crud.user.get_by_email(db, email=active_user_email)

    if user:
        return user

    user_in = UserCreate(
        email=active_user_email, password="activeuserpassword", full_name="Active User"
    )

    return crud.user.create(db, obj_in=user_in)


@pytest.fixture()
def active_auth(client: "TestClient", active_user: "User") -> BearerAuth:
    """Login an active test user and return a request BearerAuth to be used in tests.

    :param client: Test Client
    :param active_user: An active user model
    :return: Requests Bearer Auth class
    """

    login_data = login_user(client, active_user, "activeuserpassword")

    bearer_auth = BearerAuth(login_data.access_token)

    return bearer_auth


@pytest.fixture()
def inactive_user(db) -> "User":
    """Gets the sample active user.

    :param db: Database connection
    :return: Active user model
    """

    inactive_user_email = "inactive_user@email.com"

    user = crud.user.get_by_email(db, email=inactive_user_email)

    if user:
        return user

    user_in = UserCreate(
        email=inactive_user_email,
        password="inactiveuserpassword",
        full_name="Inactive User",
        is_active=False,
    )

    return crud.user.create(db, obj_in=user_in)


@pytest.fixture()
def all_users_created(db, superuser, active_user, inactive_user) -> None:
    """Ensures all users have been created.

    :param db: Database connection
    :param superuser: Superuser user model
    :param active_user: Active user model
    :param inactive_user: Inactive  user model
    :return: None
    """
    ...


@pytest.fixture()
def invalid_auth() -> BearerAuth:
    return BearerAuth("totally-made-up-and-invalid")
