from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

BASE_DIR = Path(__file__).parent.parent.parent


class PostgreSettings(BaseSettings):
    """Данные БД"""

    HOST: str = Field(default="localhost")
    PORT: int = Field(default=5432)
    USER: str = Field(default="postgres")
    PASSWORD: str = Field(default="")
    DATABASE: str = Field(default="postgres")

    @property
    def url(self) -> URL:
        return URL.create(
            "postgresql+asyncpg",
            self.USER,
            self.PASSWORD,
            self.HOST,
            self.PORT,
            self.DATABASE,
        )


class RedisSettings(BaseSettings):
    """Параметры redis"""

    HOST: str = Field(default="localhost")
    PORT: int = Field(default=6379)
    PASSWORD: str = Field(default="")
    DB: int = Field(default=0)

    @property
    def url(self) -> str:
        base_url = f"redis://:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"

        params = (
            "?socket_timeout=5"
            "&socket_connect_timeout=5"
            "&socket_keepalive=true"
            "&retry_on_timeout=true"
        )

        return base_url + params

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_prefix="REDIS_",
    )
