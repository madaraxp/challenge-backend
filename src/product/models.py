from odmantic import Model, ObjectId, Reference

from src.category.models import Category


class Product(Model):
    title: str
    description: str
    price: float
    category: Category = Reference()
    owner_id: ObjectId
