from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from odmantic.session import AIOSession

from src.config import Settings

client = AsyncIOMotorClient(Settings.DATABASE_URL)
engine = AIOEngine(client=client, database=Settings.DATABASE_NAME)


async def get_session() -> AsyncGenerator[AIOSession]:
    session: AIOSession = engine.session()
    await session.start()
    try:
        yield session
    except Exception as exp:
        raise exp
    finally:
        await session.end()
