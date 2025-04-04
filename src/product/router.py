from fastapi import APIRouter, Depends, status
from odmantic import ObjectId
from odmantic.session import AIOSession

import src.product.service as product_service
from src.database import get_session
from src.product.schema import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix='/product', tags=['product'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[ProductResponse])
async def get_products(session: AIOSession = Depends(get_session)):
    return await product_service.get_products(session)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def get_products_by_id(id: ObjectId, session: AIOSession = Depends(get_session)):
    return await product_service.get_product_by_id(session, id)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(
    product: ProductCreate, session: AIOSession = Depends(get_session)
):
    return await product_service.create_product(session, product)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def update_product(
    id: ObjectId, product: ProductUpdate, session: AIOSession = Depends(get_session)
):
    return await product_service.update_product(session, product, id)


@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=None)
async def delete_product(id: ObjectId, session: AIOSession = Depends(get_session)):
    return await product_service.delete_product(session, id)
