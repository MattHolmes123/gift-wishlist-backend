import tempfile
import shutil
from app.core.config import settings
import pytest
from fastapi.testclient import TestClient
import pathlib

from sqlalchemy.orm import Session

from app.database.db import create_app_engine, create_session, Base, engine
from app.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


PROJECT_ROOT = pathlib.Path(".")
TEST_DB_DIR = PROJECT_ROOT / settings.test_db_path
CLEAN_DB_NAME = "test-clean.db"


class TestDatabase:
    """Create a test database - To be used when mocking dependencies"""

    def __init__(self, url):
        self.url = url
        self.engine = create_app_engine(url)
        self.session = create_session(engine)

    def __call__(self) -> Session:
        """This is how it is used as a dependency

        :return:
        """

        db = self.session()

        try:
            yield db

        finally:
            db.close()

    def get_db(self):
        """When the tests need to create data directly"""

        return self.session()


# TODO: Improve this, for now it works.
# We want to do the following:
# - Create the tables once per test session
# - Have a db that is isolated to each of the following fixture scopes
#   function: the default scope, the fixture is destroyed at the end of the test.
#   class: the fixture is destroyed during teardown of the last test in the class.
#   module: the fixture is destroyed during teardown of the last test in the module.
#   package: the fixture is destroyed during teardown of the last test in the package.
#   session: the fixture is destroyed at the end of the test session.
@pytest.fixture(scope="session")
def test_db():
    """Creates the test database and a clean one for using later.

    :return: None
    """

    # creates all the tables (by default this will have created the test database
    Base.metadata.create_all(bind=engine)

    test_db = TEST_DB_DIR / settings.test_db_name

    assert test_db.exists()
    
    # Now create a new test db
    clean_db = TEST_DB_DIR / "test-clean.db"

    assert not clean_db.exists()

    shutil.copy(test_db, clean_db)

    assert clean_db.exists()
    

@pytest.fixture(scope="module")
def module_db(test_db):
    """Create a module scoped database"""

    return _get_clean_database()


def _get_clean_database():
    project_root = pathlib.Path(".")
    test_db_location = project_root / settings.test_db_path
    clean_db = test_db_location / CLEAN_DB_NAME

    assert clean_db.exists()

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_db = pathlib.Path(tmp_dir) / "module_db.db"

        shutil.copy(clean_db, tmp_db)

        tmp_db_url = settings.get_db_url("module_db.db")

        return TestDatabase(url=tmp_db_url)
