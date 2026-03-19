from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.session import get_db, Base
from app.core.test_config import test_settings

engine = create_async_engine(
    test_settings.SQLALCHEMY_DATABASE_URI,
    poolclass=NullPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture(scope="function", autouse=True)
def override_base_url(monkeypatch):
    from app.core.config import settings
    monkeypatch.setattr(settings, "BASE_URL", "http://testserver")


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def setup_database() -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def db_session(setup_database: None) -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
def override_get_db(db_session: AsyncSession):
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest_asyncio.fixture(scope="function", loop_scope="session")
async def client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)

    async with AsyncClient(
            transport=transport,
            base_url="http://testserver",
            follow_redirects=False,
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
