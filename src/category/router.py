from fastapi import APIRouter, Depends, status
from odmantic import ObjectId
from odmantic.session import AIOSession

import src.category.service as category_service
from src.category.schema import CategoryCreate, CategoryResponse, CategoryUpdate
from src.database import get_session

router = APIRouter(prefix='/category', tags=['category'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[CategoryResponse])
async def get_categories(session: AIOSession = Depends(get_session)):
    return await category_service.get_categories(session)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def get_category_by_id(id: ObjectId, session: AIOSession = Depends(get_session)):
    return await category_service.get_category_by_id(session, id)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate, session: AIOSession = Depends(get_session)
):
    return await category_service.create_category(session, category)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=CategoryResponse)
async def update_category(
    id: ObjectId, category: CategoryUpdate, session: AIOSession = Depends(get_session)
):
    return await category_service.update_category(session, category, id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_category(id: ObjectId, session: AIOSession = Depends(get_session)):
    return await category_service.delete_category(session, id)
