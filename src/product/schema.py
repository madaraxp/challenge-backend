from odmantic import ObjectId
from pydantic import BaseModel, ConfigDict

from src.category.schema import CategoryResponse


class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    owner_id: ObjectId


class ProductCreate(ProductBase):
    category_id: ObjectId


class ProductUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    category_id: ObjectId | None = None


class ProductResponse(ProductBase):
    id: ObjectId
    category: CategoryResponse
    model_config = ConfigDict(from_attributes=True)
