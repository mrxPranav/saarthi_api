import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Add it to app/.env or the environment.")

async def migrate():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        print("Adding 'title' column to 'notes' table...")
        try:
            await conn.execute(text("ALTER TABLE notes ADD COLUMN title VARCHAR;"))
            print("Successfully added 'title' column.")
        except Exception as e:
            if "already exists" in str(e):
                print("Column 'title' already exists.")
            else:
                print(f"Error: {e}")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(migrate())
