"""Configure the Database."""

from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from uprn_mangle.backend.config import get_settings

settings = get_settings()

# This is a temporary hack since the Import script is SYNC database and the API
# is ASYNC database. I will later use Async database for the import
# script as well.
DATABASE_BASE_SYNC = "postgresql://"
DATABASE_BASE_ASYNC = "postgresql+asyncpg://"

DATABASE_URL = (
    f"{DATABASE_BASE_SYNC}{settings.db_user}:"
    f"{settings.db_password}@"
    f"{settings.db_host}:"
    f"{settings.db_port}/"
    f"{settings.db_name}"
)

DATABASE_URL_ASYNC = (
    f"{DATABASE_BASE_ASYNC}{settings.db_user}:"
    f"{settings.db_password}@"
    f"{settings.db_host}:"
    f"{settings.db_port}/"
    f"{settings.db_name}"
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


# sync engine and session used for the import script where we don't need async
sync_engine = create_engine(DATABASE_URL, echo=False)
session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=sync_engine
)

# async engine and session used for the API where we need async
async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    """Get a database session.

    To be used for dependency injection.
    """
    async with async_session() as session, session.begin():
        yield session


async def init_models() -> None:
    """Create tables if they don't already exist.

    Really we should use Alembic to manage migrations, this wil be added once
    the API is functional.
    """
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # noqa: ERA001
        await conn.run_sync(Base.metadata.create_all)
