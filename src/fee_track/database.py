from collections.abc import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class SessionMaker:
    def __init__(self, url: URL) -> None:
        self._engine = create_async_engine(url=url)
        self._session_factory = async_sessionmaker(
            self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Получение сессии БД"""
        session = self._session_factory()

        try:
            yield session
        except Exception:
            await session.rollback()
