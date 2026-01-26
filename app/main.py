from fastapi import FastAPI
from app.controllers.note_controller import router as note_router
from app.config.database import db_config

app = FastAPI(title="Saarthi API", description="CRUD API for Notes using FastAPI and OOP Architecture")

app.include_router(note_router)

@app.on_event("startup")
async def startup_event():
    # In production, we'd use Alembic. For this simple example, we create tables directly.
    async with db_config.engine.begin() as conn:
        await conn.run_sync(db_config.Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to Saarthi API"}
