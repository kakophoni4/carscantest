import asyncio
import uuid
from datetime import datetime, timezone
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database import Base, get_db
from app.models import Car, User
from app.auth import hash_password
from app.main import app


engine_test = create_async_engine(
    "sqlite+aiosqlite:///./test.db",
    echo=False,
)
TestSessionLocal = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession) -> User:
    user = User(
        username="admin",
        hashed_password=hash_password("admin123"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def sample_cars(db_session: AsyncSession) -> list[Car]:
    cars = []
    for i in range(5):
        car = Car(
            external_id=f"test_{i}",
            brand="Toyota" if i < 3 else "Honda",
            model="Corolla" if i < 3 else "Civic",
            year=2020 + i,
            mileage_km=10000 * (i + 1),
            price_jpy=1000000 + i * 500000,
            transmission="Automatic",
            body_type="Sedan",
            color="White" if i % 2 == 0 else "Black",
            url=f"https://carsensor.net/test/{i}",
        )
        db_session.add(car)
        cars.append(car)
    await db_session.commit()
    for car in cars:
        await db_session.refresh(car)
    return cars


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def auth_token(client: AsyncClient, admin_user: User) -> str:
    resp = await client.post("/api/auth/login", json={
        "username": "admin",
        "password": "admin123",
    })
    return resp.json()["access_token"]


@pytest_asyncio.fixture
async def auth_headers(auth_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {auth_token}"}
