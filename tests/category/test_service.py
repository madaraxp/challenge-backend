import pytest
from fastapi import status
from odmantic import ObjectId


@pytest.mark.asyncio
async def test_get_all_categories(client):
    response = await client.get('/category/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_all_categories_with_categories(client, inserted_category):
    response = await client.get('/category/')

    assert response.status_code == status.HTTP_200_OK
    expected_response = [
        {
            'id': str(inserted_category.id),
            'title': inserted_category.title,
            'description': inserted_category.description,
            'owner_id': str(inserted_category.owner_id),
        }
    ]
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_category(client, inserted_category):
    response = await client.get(f'/category/{inserted_category.id}')

    expected_response = {
        'id': str(inserted_category.id),
        'title': inserted_category.title,
        'description': inserted_category.description,
        'owner_id': str(inserted_category.owner_id),
    }
    assert response.json() == expected_response


@pytest.mark.asyncio
async def test_create_category(client):
    create_category_payload = {
        'title': 'Test Create',
        'description': 'Test Create',
        'owner_id': str(ObjectId()),
    }

    response = await client.post('/category/', json=create_category_payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['title'] == create_category_payload['title']
    assert response.json()['description'] == create_category_payload['description']
    assert response.json()['owner_id'] == create_category_payload['owner_id']


@pytest.mark.asyncio
async def test_get_update_category(client, inserted_category):
    category_update = {
        'title': 'Test Category Update',
        'description': 'Test Category Description',
    }

    response = await client.put(
        f'/category/{inserted_category.id}', json=category_update
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == str(inserted_category.id)
    assert response.json()['title'] == category_update['title']
    assert response.json()['description'] == category_update['description']
    assert response.json()['owner_id'] == str(inserted_category.owner_id)


@pytest.mark.asyncio
async def test_get_update_category_exception(client):
    category_update = {
        'title': 'Test Category Update',
        'description': 'Test Category Description',
    }
    category_id = ObjectId()

    response = await client.put(f'/category/{category_id}', json=category_update)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'category not found'}


@pytest.mark.asyncio
async def test_get_delete_category(client, inserted_category):
    response = await client.delete(
        f'/category/{inserted_category.id}',
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_get_delete_category_exception(client):
    category_id = ObjectId()

    response = await client.delete(
        f'/category/{category_id}',
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'category not found'}
