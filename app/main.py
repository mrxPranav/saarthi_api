from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.note_controller import router as note_router
from app.controllers.health_controller import router as health_router
from app.config.database import db_config

app = FastAPI(title="Saarthi API", description="CRUD API for Notes using FastAPI and OOP Architecture")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(note_router)
app.include_router(health_router)

@app.on_event("startup")
async def startup_event():
    # In production, we'd use Alembic. For this simple example, we create tables directly.
    async with db_config.engine.begin() as conn:
        await conn.run_sync(db_config.Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to Saarthi API"}
