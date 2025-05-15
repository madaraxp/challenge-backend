from fastapi import HTTPException, status
from odmantic import ObjectId
from odmantic.session import AIOSession

from src.category.models import Category
from src.category.schema import CategoryCreate, CategoryUpdate


async def get_categories(db: AIOSession) -> list[Category]:
    return await db.find(Category)


async def get_category_by_id(db: AIOSession, id: ObjectId) -> Category | None:
    return await db.find_one(Category, Category.id == id)


async def create_category(db: AIOSession, schema: CategoryCreate) -> Category:
    return await db.save(Category(**schema.model_dump(exclude_unset=True)))


async def update_category(
    db: AIOSession, schema_update: CategoryUpdate, id: ObjectId
) -> Category | None:
    actual_model = await db.find_one(Category, Category.id == id)
    if not actual_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='category not found'
        )
    actual_model.model_update(schema_update)
    return await db.save(actual_model)


async def delete_category(db: AIOSession, id: ObjectId) -> None:
    actual_model = await db.find_one(Category, Category.id == id)
    if not actual_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='category not found'
        )
    await db.delete(actual_model)
