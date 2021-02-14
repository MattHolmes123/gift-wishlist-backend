from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from .utils import create_app_engine, create_session

# What all models derive from
Base = declarative_base()

# The database connection
engine = create_app_engine()
SessionLocal = create_session(engine)


def get_db() -> Session:
    """Yields a database connection.

    When running unit tests this is a sqlite db.
    :return: Database connection
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
