import pytest
from fastapi.testclient import TestClient

from app.database.db import Base, engine
from app.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


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
    """Tests requiring a database need to use this fixture.

    :return:
    """

    # creates all the tables
    Base.metadata.create_all(bind=engine)
