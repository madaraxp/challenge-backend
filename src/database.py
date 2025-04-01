from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from odmantic.session import AIOSession

from src.config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL)
engine = AIOEngine(client=client, database=settings.DATABASE_NAME)


async def get_session() -> AsyncGenerator[AIOSession]:
    session: AIOSession = engine.session()
    try:
        await session.start()
        yield session
    except Exception as exp:
        raise exp
    finally:
        await session.end()
