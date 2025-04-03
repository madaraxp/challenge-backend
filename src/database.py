from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from odmantic.session import AIOSession

from src.config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL)
engine = AIOEngine(client=client, database=settings.DATABASE_NAME)


async def get_session() -> AsyncGenerator[AIOSession]:
    async with engine.session() as session:
        yield session
