from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def create_app_engine(url: str = None) -> Engine:

    connection_url = url or (
        settings.test_db_url if settings.running_tests else settings.pg_dsn
    )
    assert connection_url  # settings.pg_dsn is defined as optional

    connect_args = {"check_same_thread": False} if settings.running_tests else {}

    return create_engine(connection_url, connect_args=connect_args)


def create_session(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
