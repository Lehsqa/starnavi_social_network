from project.app.infrastructure.database import Base
from project.app.infrastructure.database.session import engine


async def generate_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
