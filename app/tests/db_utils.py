from sqlalchemy.orm import Session

from app.database.db import create_app_engine, create_session, engine


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

        db = self.get_db()

        try:
            yield db

        finally:
            db.close()

    def get_db(self):
        """When the tests need to create data directly"""

        return self.session()
