from typing import TYPE_CHECKING

import pytest

from app import crud

if TYPE_CHECKING:
    from app.models.user import User
    from fastapi.testclient import TestClient
    from ..conftest import TestDatabase

from app.api.deps import get_db
from app.main import app

from .utils import BearerAuth, login_user


@pytest.fixture(scope="package")
def db(package_db: "TestDatabase"):
    """Gets the database session

    :param package_db: clean database session class
    :return: Database session
    """

    app.dependency_overrides[get_db] = package_db

    return package_db.get_db()


@pytest.fixture(scope="package")
def super_auth(db, client: "TestClient") -> BearerAuth:
    """Login a superuser and return a request BearerAuth to be used in tests.

    :param db: Database connection
    :param client: Test Client
    :return: Requests Bearer Auth class
    """

    login_data = login_user(client, "superuser@email.com", "superuserpassword")

    bearer_auth = BearerAuth(login_data.access_token)

    return bearer_auth


@pytest.fixture(scope="package")
def active_auth(db, client: "TestClient") -> BearerAuth:
    """Login an active test user and return a request BearerAuth to be used in tests.

    :param db: Database connection
    :param client: Test Client
    :return: Requests Bearer Auth class
    """

    login_data = login_user(client, "active_user@email.com", "activeuserpassword")

    bearer_auth = BearerAuth(login_data.access_token)

    return bearer_auth


@pytest.fixture()
def superuser(db) -> "User":
    """Gets the sample super user

    :param db: Database connection
    :return: Super User model
    """

    return _get_user(db, "superuser@email.com")


@pytest.fixture()
def active_user(db) -> "User":
    """Gets the sample active user.

    :param db: Database connection
    :return: Active user model
    """

    return _get_user(db, "active_user@email.com")


@pytest.fixture()
def inactive_user(db) -> "User":
    """Gets the sample active user.

    :param db: Database connection
    :return: Active user model
    """

    return _get_user(db, "inactive_user@email.com")


def _get_user(db, email):
    user = crud.user.get_by_email(db, email=email)

    assert user

    return user


@pytest.fixture()
def invalid_auth() -> BearerAuth:
    return BearerAuth("totally-made-up-and-invalid")
