from typing import Literal, Optional

from pydantic import BaseSettings, PostgresDsn, EmailStr


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

    # Needed to create other users
    first_superuser: Optional[EmailStr]
    first_superuser_password: Optional[str]

    # Project settings not from environment
    test_db_url: str = "sqlite:///./app/tests/test.db"
    api_v1_str: str = "/api/v1"
    access_token_expire_minutes: int = 60 * 24 * 8
    users_open_registration: bool = False

    @property
    def running_tests(self) -> bool:
        return self.environment == "test"


settings: ProjectSettings = ProjectSettings()
