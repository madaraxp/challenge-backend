from unittest.mock import AsyncMock

import pytest
from odmantic import ObjectId
from odmantic.session import AIOSession

import src.category.service as category_service
from src.category.models import Category
from src.category.schema import CategoryCreate, CategoryUpdate


@pytest.mark.asyncio
async def test_get_all_categories():
    mock_session = AsyncMock(spec=AIOSession)
    category = Category(
        id=ObjectId(),
        title='Test Category',
        description='Test Description',
        owner_id=ObjectId(),
    )
    mock_session.find = AsyncMock(return_value=[category])
    response = await category_service.get_categories(mock_session)

    assert response == [category]
    mock_session.find.assert_called_once_with(Category)


@pytest.mark.asyncio
async def test_get_category():
    mock_session = AsyncMock(spec=AIOSession)
    category = Category(
        id=ObjectId(),
        title='Test Category',
        description='Test Description',
        owner_id=ObjectId(),
    )
    mock_session.find_one = AsyncMock(return_value=category)
    response = await category_service.get_category_by_id(mock_session, category.id)

    assert response == category
    mock_session.find_one.assert_called_once_with(Category, Category.id == category.id)


@pytest.mark.asyncio
async def test_create_category():
    mock_session = AsyncMock(spec=AIOSession)
    category = CategoryCreate(
        title='Test Category',
        description='Test Description',
        owner_id=ObjectId(),
    )
    mock_session.save = AsyncMock(
        return_value=Category(**category.model_dump(), id=ObjectId())
    )
    response = await category_service.create_category(mock_session, category)

    assert response.title == category.title
    assert response.description == category.description
    assert response.owner_id == category.owner_id
    mock_session.save.assert_called_once()


@pytest.mark.asyncio
async def test_get_update_category():
    mock_session = AsyncMock(spec=AIOSession)
    category = Category(
        id=ObjectId(),
        title='Test Category',
        description='Test Description',
        owner_id=ObjectId(),
    )
    category_update = CategoryUpdate(
        title='Test Category Update', description='Test Category Description'
    )

    mock_session.find_one = AsyncMock(return_value=category)
    mock_session.save = AsyncMock()
    await category_service.update_category(mock_session, category_update, category.id)

    mock_session.find_one.assert_called_once_with(Category, Category.id == category.id)

    category.model_update(category_update)
    mock_session.save.assert_called_once_with(category)


@pytest.mark.asyncio
async def test_get_update_category_exception():
    mock_session = AsyncMock(spec=AIOSession)
    category = Category(
        id=ObjectId(),
        title='Test Category',
        description='Test Description',
        owner_id=ObjectId(),
    )
    category_update = CategoryUpdate(
        title='Test Category Update', description='Test Category Description'
    )

    mock_session.find_one = AsyncMock(return_value=None)

    with pytest.raises(Exception, match='category not found'):
        await category_service.update_category(
            mock_session, category_update, category.id
        )

    mock_session.find_one.assert_called_once_with(Category, Category.id == category.id)
    mock_session.save.assert_not_called()


@pytest.mark.asyncio
async def test_get_delete_category():
    mock_session = AsyncMock(spec=AIOSession)
    category = Category(
        id=ObjectId(),
        title='Test Category',
        description='Test Description',
        owner_id=ObjectId(),
    )
    mock_session.find_one = AsyncMock(return_value=category)
    response = await category_service.delete_category(mock_session, category.id)

    assert response == category
    mock_session.find_one.assert_called_once_with(Category, Category.id == category.id)
    mock_session.delete.assert_called_once_with(category)


@pytest.mark.asyncio
async def test_get_delete_category_exception():
    mock_session = AsyncMock(spec=AIOSession)
    id = ObjectId()
    mock_session.find_one = AsyncMock(return_value=None)

    with pytest.raises(Exception, match='category not found'):
        await category_service.delete_category(mock_session, id)

    mock_session.find_one.assert_called_once_with(Category, Category.id == id)
    mock_session.delete.assert_not_called()
