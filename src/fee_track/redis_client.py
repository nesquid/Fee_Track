import redis.asyncio as aioredis
from loguru import logger


class RedisClient:
    def __init__(self) -> None:
        self.pool: aioredis.ConnectionPool | None = None
        self.client: aioredis.Redis | None = None

    def init(self, redis_url: str) -> None:
        """Инициализация пулла подключений и клиента

        Args:
            redis_url (str): Строка подключения redis
        """
        logger.info("Инициализация пулла соединений Redis...")
        self.pool = aioredis.ConnectionPool.from_url(  # pyright: ignore[reportUnknownMemberType]
            redis_url, decode_responses=True, max_connections=20
        )
        self.client = aioredis.Redis(connection_pool=self.pool)

    async def close(self) -> None:
        """Закрытие пулла соединений"""
        if self.pool:
            logger.info("Закрытие пулла соединений Redis...")
            await self.pool.disconnect()
            self.pool = None
            self.client = None

    def get_client(self) -> aioredis.Redis:
        """Получение клиента redis"""
        if not self.client:
            raise RuntimeError("Клиент редис не инициализирован. Выполните init.")
        return self.client
