"""Root conftest file for pytest.

Main purpose is to set the database up and create useful fixtures for all tests
"""

import pathlib
import shutil
import tempfile
from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient

from app import crud
from app.core.config import settings
from app.database.db import Base
from app.main import app
from app.schemas.user import TestUser, UserCreate

from .db_utils import TestDatabase


@pytest.fixture(scope="session", autouse=True)
def client() -> TestClient:
    """Creates a test client

    :return: Fast API test client fixture
    """

    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def session_test_db():
    """Creates the test database and a clean one for using later.

    We create some users here for use in tests.
    :return: None
    """

    test_db = TestDatabase(settings.test_db_url)

    Base.metadata.create_all(bind=test_db.engine)

    # Now populate the database
    _setup_test_data(test_db)

    _create_clean_copy()


@pytest.fixture(scope="package")
def package_db() -> TestDatabase:
    """Database scoped to a python package.

    :return: Test database
    """

    return _get_clean_database()


@pytest.fixture(scope="module")
def module_db() -> TestDatabase:
    """Database scoped to a python module.

    :return: Test database
    """

    return _get_clean_database()


@pytest.fixture(scope="class")
def class_db() -> TestDatabase:
    """Database scoped to a python class.

    :return: Test database
    """

    return _get_clean_database()


@pytest.fixture(scope="function")
def function_db() -> TestDatabase:
    """Database scoped to a python function.

    :return: Test database
    """

    return _get_clean_database()


@dataclass()
class Users:
    """Test Users for tests."""

    superuser: TestUser
    active_user: TestUser
    inactive_user: TestUser

    def __iter__(self):
        return iter([self.superuser, self.active_user, self.inactive_user])


TestUsers = Users(
    superuser=TestUser(
        email="superuser@email.com",
        password="superuserpassword",
        is_superuser=True,
        full_name="Super User",
    ),
    active_user=TestUser(
        email="active_user@email.com",
        password="activeuserpassword",
        full_name="Active User",
    ),
    inactive_user=TestUser(
        email="inactive_user@email.com",
        password="inactiveuserpassword",
        full_name="Inactive User",
        is_active=False,
    ),
)


def _setup_test_data(test_db: TestDatabase) -> None:
    """Populate the database with users that all tests can use.

    :return: None
    """

    db = test_db.get_db()

    for user_in in TestUsers:
        obj_in = UserCreate(**user_in.dict())
        user = crud.user.create(db, obj_in=obj_in)
        user_in.id = user.id


def _create_clean_copy() -> None:
    """Create a copy of the test database to be used for tests needing isolation

    :return: None
    """

    test_db_dir = pathlib.Path(".") / settings.test_db_path

    test_db_file = test_db_dir / settings.test_db_name

    clean_db = test_db_dir / "test-clean.db"

    shutil.copy(test_db_file, clean_db)

    assert clean_db.exists()


def _get_clean_database() -> TestDatabase:
    """Copies the clean test database to a temporary directory and returns it

    :return: Test Database
    """

    project_root = pathlib.Path(".")
    test_db_location = project_root / settings.test_db_path
    clean_db = test_db_location / "test-clean.db"

    assert clean_db.exists()

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_db = pathlib.Path(tmp_dir) / "module_db.db"

        shutil.copy(clean_db, tmp_db)

        tmp_db_url = settings.get_db_url("module_db.db")

        return TestDatabase(url=tmp_db_url)
