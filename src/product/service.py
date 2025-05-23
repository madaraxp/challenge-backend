from odmantic import ObjectId
from odmantic.session import AIOSession

import src.category.service as category_service
from src.aws.sns import publish_topic
from src.product.models import Product
from src.product.schema import ProductCreate, ProductUpdate


async def get_products(db: AIOSession) -> list[Product]:
    return await db.find(Product)


async def get_product_by_id(db: AIOSession, id: ObjectId) -> Product | None:
    product = await db.find_one(Product, Product.id == id)
    if not product:
        raise Exception('product not found')
    return product


async def create_product(db: AIOSession, schema: ProductCreate) -> Product:
    category = await category_service.get_category_by_id(db, schema.category_id)
    if not category:
        raise Exception('category not found')
    new_product = Product(**schema.model_dump(), category=category)
    product = await db.save(new_product)
    publish_topic(product.owner_id)
    return product


async def update_product(
    db: AIOSession, schema_update: ProductUpdate, id: ObjectId
) -> Product | None:
    product = await db.find_one(Product, Product.id == id)
    if not product:
        raise Exception('product not found')
    product.model_update(schema_update)
    if schema_update.category_id:
        new_category = await category_service.get_category_by_id(
            db, id=schema_update.category_id
        )
        product.category = new_category
    product = await db.save(product)
    publish_topic(product.owner_id)
    return product


async def delete_product(db: AIOSession, id: ObjectId) -> Product | None:
    product = await db.find_one(Product, Product.id == id)
    if not product:
        raise Exception('product not found')
    await db.delete(product)
    publish_topic(product.owner_id)
