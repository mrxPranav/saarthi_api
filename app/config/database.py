from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL must be set in app/.env or the environment.
# Example: postgresql+asyncpg://user:password@localhost:5432/saarthi
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Add it to app/.env or the environment.")

class DatabaseConfig:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        self.Base = declarative_base()

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.SessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()

db_config = DatabaseConfig()
Base = db_config.Base
get_db = db_config.get_db
