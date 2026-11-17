---
name: add-crud-feature
description: Add a new CRUD resource (database model, DTO schemas, repository, service, controller and router registration) to the Saarthi API FastAPI project. Use when the user asks to add a new table, entity, resource, or set of create/read/update/delete endpoints.
---

# Add a CRUD feature to Saarthi API

This project is FastAPI + SQLAlchemy (async) + Pydantic, with one folder per layer.
Every feature (`note`, `task`, `health_check`) follows the same 5 layers. Copy that
pattern exactly. Use `app/models/task.py`, `app/schemas/task_dto.py`,
`app/repositories/task_repository.py`, `app/services/task_service.py` and
`app/controllers/task_controller.py` as the reference files.

## Layer order

Build the files in this order, because each layer depends on the one before it:

1. Model (`app/models/<name>.py`)
2. Schemas (`app/schemas/<name>_dto.py`)
3. Repository (`app/repositories/<name>_repository.py`)
4. Service (`app/services/<name>_service.py`)
5. Controller (`app/controllers/<name>_controller.py`)
6. Register the router in `app/main.py`

## 1. Model

- Inherit from `Base` imported from `app.config.database`.
- Set `__tablename__` in plural, lowercase snake case (`tasks`, `notes`).
- Primary key: `id = Column(Integer, primary_key=True, index=True, autoincrement=True)`.
- Use `String` for text fields. Use `nullable=False` only for required fields.
- Timestamp: `Column(DateTime(timezone=True), server_default=func.now())`.

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

Tables are created automatically at startup (`Base.metadata.create_all` in `app/main.py`).
There is no Alembic. Because of this, the new model file **must be imported** before startup.
The repository import does this, so do not skip step 3. Note that a new column on an
existing table will NOT be added automatically. Tell the user this if they change an existing model.

## 2. Schemas (DTOs)

Use this 4-class pattern from `task_dto.py`:

- `XBase`: shared fields. Required fields have no default (`name: str`). Optional fields use `Optional[...] = None`.
- `XCreate(XBase)`: `pass`.
- `XUpdate`: every field `Optional[...] = None`, so partial updates work.
- `XResponse(XBase)`: adds `id: int` and the timestamp field, plus `class Config: from_attributes = True`.

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

## 3. Repository

Copy `task_repository.py`. The class takes `db: AsyncSession` in `__init__`.
Methods: `save`, `find_all(skip, limit)`, `find_by_id`, `update`, `delete`.

- `save`: `Model(**data.dict())`, `add`, `commit`, `refresh`, return the object.
- `update`: find by id, then `setattr` only the fields from `dict(exclude_unset=True)`, commit, refresh. Return `None` if not found.
- `delete`: find, `db.delete`, commit, return `True`/`False`.

Use `.dict()` as the existing code does. Do not change to another style inside one feature.

## 4. Service

Copy `task_service.py`. It is a thin wrapper that passes each call to the repository.
Keep business rules here, not in the controller. Do not put SQL in the service.

## 5. Controller

Copy `task_controller.py`:

- `router = APIRouter(prefix="/<plural-name>", tags=["<Tag Name>"])`
- A `get_<name>_service(db: AsyncSession = Depends(get_db))` function that builds the repository and then the service.
- Endpoints (all `async`):

| Method | Path | Success status | Not found |
|---|---|---|---|
| POST | `/` | `201` (`status.HTTP_201_CREATED`) | — |
| GET | `/` (with `skip: int = 0`, `limit: int = 100`) | `200` | — |
| GET | `/{id}` | `200` | `404`, `detail="<Name> not found"` |
| PUT | `/{id}` (body is the `XUpdate` schema) | `200` | `404` |
| DELETE | `/{id}` | `204` (`status.HTTP_204_NO_CONTENT`), return `None` | `404` |

- Always set `response_model=` to the Response schema (or `list[...]` for lists).
- The error message must use the same wording as the others: `"Task not found"`, `"Note not found"`.

## 6. Register the router

In `app/main.py`:

```python
from app.controllers.project_controller import router as project_router
...
app.include_router(project_router)
```

## Checks before you finish

- [ ] Model import works: run `python -c "import app.main"` from the project root. It must not crash.
- [ ] `DATABASE_URL` is needed. It is read from `app/.env` or the environment. Never write the real value into code or docs.
- [ ] Start the server with `uvicorn app.main:app --reload` and open `http://127.0.0.1:8000/docs`. The new tag must appear.
- [ ] Try the 5 operations (create, list, get, update, delete) and a missing id (should return 404).
- [ ] Optional: add a `verify_<name>.py` script in the root, in the same style as `verify_health.py`.

## Do not

- Do not add a new folder structure. Use the 5 existing layer folders.
- Do not use `HTTPException` in the repository or service. Only the controller raises HTTP errors.
- Do not commit `app/.env` or any secret.
- Do not commit or push unless the user asks.
