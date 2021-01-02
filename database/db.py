from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from settings import settings

db_url = settings.test_db_url if settings.running_tests else settings.pg_dsn
connect_args = {"check_same_thread": False} if settings.running_tests else {}

engine = create_engine(db_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


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
