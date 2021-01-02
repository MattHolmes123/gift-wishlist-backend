from typing import Literal

from pydantic import (
    BaseSettings,
    PostgresDsn,
)


class ProjectSettings(BaseSettings):

    # .env settings
    environment: Literal["local", "test", "production"]
    pg_dsn: PostgresDsn

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings: ProjectSettings = ProjectSettings()
