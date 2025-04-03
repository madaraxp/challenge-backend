from fastapi import FastAPI

from src.category.router import router

app = FastAPI()
app.include_router(router)
