from fastapi import FastAPI

from src.category.router import router as category_router
from src.product.router import router as product_router

app = FastAPI()
app.include_router(category_router)
app.include_router(product_router)
