import pytest

from database.db import Base, engine


# TODO: Improve this, for now it works.
@pytest.fixture(scope="session")
def test_db():
    """Tests requiring a database need to use this fixture.

    :return:
    """

    # creates all the tables
    Base.metadata.create_all(bind=engine)
