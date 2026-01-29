from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task import Task
from app.schemas.task_dto import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, task: TaskCreate) -> Task:
        db_task = Task(**task.dict())
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def find_all(self, skip: int = 0, limit: int = 100) -> list[Task]:
        result = await self.db.execute(select(Task).offset(skip).limit(limit))
        return result.scalars().all()

    async def find_by_id(self, task_id: int) -> Task | None:
        result = await self.db.execute(select(Task).filter(Task.id == task_id))
        return result.scalars().first()

    async def update(self, task_id: int, task_update: TaskUpdate) -> Task | None:
        db_task = await self.find_by_id(task_id)
        if db_task:
            update_data = task_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task, key, value)
            await self.db.commit()
            await self.db.refresh(db_task)
        return db_task

    async def delete(self, task_id: int) -> bool:
        db_task = await self.find_by_id(task_id)
        if db_task:
            await self.db.delete(db_task)
            await self.db.commit()
            return True
        return False
