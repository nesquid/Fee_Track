import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import Connection, engine_from_config, pool
from sqlalchemy.ext.asyncio import create_async_engine

from fee_track.config import PostgreSettings
from fee_track.models import Base

pg_settings = PostgreSettings()

config = context.config
config.set_main_option("sqlalchemy.url", pg_settings.url.render_as_string(False))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


def run_async_migrations_online() -> None:
    db_url = config.get_main_option("sqlalchemy.url")

    if db_url is None:
        raise ValueError("sqlalchemy.url is not set in alembic.ini")

    engine = create_async_engine(
        db_url,
        pool_pre_ping=True,
        pool_use_lifo=True,
        pool_recycle=3600,
        pool_timeout=15,
    )

    async def run_async_migrations() -> None:
        async with engine.connect() as connection:
            await connection.run_sync(do_run_migrations)

    def do_run_migrations(connection: Connection) -> None:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    # run_migrations_online()
    run_async_migrations_online()
