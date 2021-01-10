from typing import Literal, Optional

from pydantic import (
    BaseSettings,
    PostgresDsn,
)


class ProjectSettings(BaseSettings):
    """Settings class, they are all environment variables.

    Order of presedence is as follows:
      1. Environment variables e.g. export FOO="bar"
      2. entries in .env
    """

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # This is optional as when testing this environment variable is not set.
    pg_dsn: Optional[PostgresDsn]
    environment: Literal["local", "test", "production"]
    secret_key: str

    # Project settings not from environment
    test_db_url: str = "sqlite:///./app/tests/test.db"

    @property
    def running_tests(self) -> bool:
        return self.environment == "test"


settings: ProjectSettings = ProjectSettings()
