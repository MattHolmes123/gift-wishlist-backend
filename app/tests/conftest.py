import pathlib
import shutil
import tempfile

import pytest
from fastapi.testclient import TestClient

from app import crud
from app.core.config import settings
from app.database.db import Base
from app.main import app
from app.schemas.user import UserCreate

from .db_utils import TestDatabase


@pytest.fixture(scope="session", autouse=True)
def client():
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
    return _get_clean_database()


@pytest.fixture(scope="module")
def module_db() -> TestDatabase:
    return _get_clean_database()


@pytest.fixture(scope="class")
def class_db() -> TestDatabase:
    return _get_clean_database()


@pytest.fixture(scope="function")
def function_db() -> TestDatabase:
    return _get_clean_database()


def _setup_test_data(test_db: TestDatabase) -> None:
    """Populate the database with users that all tests can use.

    :return: None
    """

    superuser = UserCreate(
        email="superuser@email.com",
        password="superuserpassword",
        is_superuser=True,
        full_name="Super User",
    )

    active_user = UserCreate(
        email="active_user@email.com",
        password="activeuserpassword",
        full_name="Active User",
    )

    inactive_user = UserCreate(
        email="inactive_user@email.com",
        password="inactiveuserpassword",
        full_name="Inactive User",
        is_active=False,
    )

    users_in = [superuser, active_user, inactive_user]

    db = test_db.get_db()

    for user_in in users_in:
        crud.user.create(db, obj_in=user_in)


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

# TODO: Decide what I want this to be...
# TODO: Something to store users and remember their authentication details....
# TODO: Needs to be easy to use in tests and fixtures
# TODO: Also need to call `get_db` function correctly.

# from app.schemas.user import UserCreate
#
# class TestUser(BaseModel):
#     full_name: str
#     email: str
#     password: str
#     is_superuser: bool = False
#     is_inactive: bool = False

# @dataclass()
# class Users:
#     superuser: UserCreate
#     active_user: UserCreate
#     inactive_user: UserCreate
#
#     @staticmethod
#     def get_user(full_name, email, password, *, is_superuser=False, is_active=True) -> UserCreate:
#         return UserCreate(
#             full_name=full_name,
#             email=email,
#             password=password,
#             is_superuser=is_superuser,
#             is_active=is_active,
#         )
#
# @pytest.fixture(scope="session")
# def users() -> Users:
#     return Users(
#         superuser=Users.get_user("Super User", "superuser@email.com", "superuserpassword", is_superuser=True),
#         active_user=Users.get_user("Active User", "active_user@email.com", "activeuserpassword"),
#         inactive_user=Users.get_user("Inactive User", "inactive_user@email.com", "inactiveuserpassword", is_active=False),
#     )
