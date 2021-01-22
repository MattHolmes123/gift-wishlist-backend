import pytest
from fastapi.testclient import TestClient

from app.database.db import Base, engine
from app.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


# TODO: Improve this, for now it works.
@pytest.fixture(scope="session")
def test_db():
    """Tests requiring a database need to use this fixture.

    :return:
    """

    # creates all the tables
    Base.metadata.create_all(bind=engine)
