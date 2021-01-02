from typing import Literal

from pydantic import (
    BaseSettings,
    PostgresDsn,
)


class ProjectSettings(BaseSettings):

    # .env settings
    environment: Literal["local", "test", "production"]
    pg_dsn: PostgresDsn
    test_db_url: str = "sqlite:///./tests/test.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def running_tests(self) -> bool:
        return self.environment == "test"


settings: ProjectSettings = ProjectSettings()
