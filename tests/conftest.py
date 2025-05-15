from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from async_asgi_testclient import TestClient
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, ObjectId
from testcontainers.mongodb import MongoDbContainer

from src.category.models import Category
from src.database import get_session
from src.main import app
from src.product.models import Product


@pytest.fixture(scope='session')
def mongo_url():
    with MongoDbContainer('mongo:7.0.7') as mongo:
        mongo.start()
        yield mongo.get_connection_url()


@pytest_asyncio.fixture
async def engine(mongo_url):
    client = AsyncIOMotorClient(mongo_url)
    engine = AIOEngine(client=client, database='test_db')
    return engine


@pytest_asyncio.fixture
async def session(engine):
    async with engine.session() as session:
        yield session


@pytest_asyncio.fixture
async def client(session) -> AsyncGenerator[TestClient, None]:
    async def get_session_override():
        return session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client


@pytest_asyncio.fixture
async def inserted_category(session):
    category = Category(
        id=ObjectId(),
        title='Test Category',
        description='Test Description',
        owner_id=ObjectId(),
    )
    await session.save(category)
    return category


@pytest_asyncio.fixture
async def insert_product(session, insert_category):
    product = Product(
        id=ObjectId(),
        title='Test Product',
        description='Test Description',
        price=110.1,
        category=insert_category,
        owner_id=ObjectId(),
    )
    await session.save(product)
    return product
