from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

if TYPE_CHECKING:
    from sqlalchemy.engine.base import Engine


def create_app_engine(url: str = None) -> "Engine":
    if url is None:
        url = settings.test_db_url if settings.running_tests else settings.pg_dsn

    connect_args = {"check_same_thread": False} if settings.running_tests else {}

    return create_engine(url, connect_args=connect_args)


def create_session(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
