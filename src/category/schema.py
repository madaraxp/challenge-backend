from odmantic import ObjectId
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    title: str
    description: str
    owner_id: ObjectId


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
