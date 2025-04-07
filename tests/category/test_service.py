from functools import partial
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from mongomock_motor import AsyncMongoMockClient
from odmantic import AIOEngine, ObjectId

import src.category.service as category_service
from src.category.models import Category
from src.category.schema import CategoryCreate, CategoryUpdate


@pytest_asyncio.fixture
async def test_db():
    client = AsyncMongoMockClient()
    engine = AIOEngine(client=client, database='test_db')

    mock_session = AsyncMock(spec=engine)
    mock_session.save = AsyncMock(side_effect=partial(engine._save, session=None))
    mock_session.find = AsyncMock(side_effect=partial(engine.find))
    mock_session.find_one = AsyncMock(side_effect=partial(engine.find_one))
    mock_session.delete = AsyncMock(side_effect=partial(engine.delete))

    return mock_session


@pytest_asyncio.fixture
async def insert_category(test_db):
    category = Category(
        id=ObjectId(),
        title='Test Category',
        description='Test Description',
        owner_id=ObjectId(),
    )
    await test_db.save(category)
    return category


@pytest.mark.asyncio
async def test_get_all_categories(test_db, insert_category):
    response = await category_service.get_categories(test_db)

    assert [cat async for cat in response] == [insert_category]


@pytest.mark.asyncio
async def test_get_category(test_db, insert_category):
    response = await category_service.get_category_by_id(test_db, insert_category.id)

    assert response == insert_category


@pytest.mark.asyncio
async def test_create_category(test_db):
    category = CategoryCreate(
        title='Test Create',
        description='Test Create',
        owner_id=ObjectId(),
    )

    response = await category_service.create_category(test_db, category)

    assert response.title == category.title
    assert response.description == category.description
    assert response.owner_id == category.owner_id
    test_db.save.assert_called_once()


@pytest.mark.asyncio
async def test_get_update_category(test_db, insert_category):
    category_update = CategoryUpdate(
        title='Test Category Update', description='Test Category Description'
    )

    await category_service.update_category(test_db, category_update, insert_category.id)

    result = await test_db.find_one(Category, Category.id == insert_category.id)
    assert result.title == category_update.title
    assert result.description == category_update.description


@pytest.mark.asyncio
async def test_get_update_category_exception(test_db):
    category_update = CategoryUpdate(
        title='Test Category Update', description='Test Category Description'
    )
    category_id = ObjectId()
    test_db.find_one = AsyncMock(return_value=None)

    with pytest.raises(Exception, match='category not found'):
        await category_service.update_category(test_db, category_update, category_id)

    test_db.find_one.assert_called_once_with(Category, Category.id == category_id)
    test_db.save.assert_not_called()


@pytest.mark.asyncio
async def test_get_delete_category(test_db, insert_category):
    response = await category_service.delete_category(test_db, insert_category.id)

    assert response == insert_category
    test_db.find_one.assert_called_once_with(
        Category, Category.id == insert_category.id
    )
    test_db.delete.assert_called_once_with(insert_category)


@pytest.mark.asyncio
async def test_get_delete_category_exception(test_db):
    category_id = ObjectId()

    with pytest.raises(Exception, match='category not found'):
        await category_service.delete_category(test_db, category_id)

    test_db.find_one.assert_called_once_with(Category, Category.id == category_id)
    test_db.delete.assert_not_called()
