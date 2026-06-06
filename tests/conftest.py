import os

# Set test environment variables before any app imports so that pydantic-settings
# picks them up at class instantiation time.
os.environ['DB_USER'] = 'test'
os.environ['DB_PASSWORD'] = 'test'
os.environ['DB_NAME'] = 'test'
os.environ['JWT_SECRET_KEY'] = 'test-secret-key-minimum-32-characters!!'
os.environ['EMAIL_NOTIFICATIONS_ENABLED'] = 'false'
os.environ['RATE_LIMIT_AUTH'] = '1000/minute'
os.environ['RATE_LIMIT_DEFAULT'] = '1000/minute'

from typing import Any

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

import app.models  # noqa: F401 — registers all SQLModel metadata
from app.dependencies.services import get_email_service
from app.dependencies.session import get_session
from app.main import app
from app.services.bootstrap import bootstrap_roles_and_permissions


class _MockEmailService:
    async def send_account_confirmation_email(
        self, recipient: EmailStr | str, code: str, user_id: int
    ) -> None:
        pass

    async def send_password_reset_email(
        self, recipient: EmailStr | str, code: str, user_id: int
    ) -> None:
        pass

    async def send_template_email(
        self,
        recipient: EmailStr | str,
        subject: str,
        template_name: str,
        context: dict[str, Any],
    ) -> None:
        pass

TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'


@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        await bootstrap_roles_and_permissions(session)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    session_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(test_engine):
    session_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_email_service] = lambda: _MockEmailService()

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://test',
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
