from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy import URL


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
