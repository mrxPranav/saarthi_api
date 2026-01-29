from app.repositories.task_repository import TaskRepository
from app.schemas.task_dto import TaskCreate, TaskUpdate
from app.models.task import Task

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def create_task(self, task: TaskCreate) -> Task:
        return await self.repository.save(task)

    async def get_all_tasks(self, skip: int = 0, limit: int = 100) -> list[Task]:
        return await self.repository.find_all(skip, limit)

    async def get_task_by_id(self, task_id: int) -> Task | None:
        return await self.repository.find_by_id(task_id)

    async def update_task(self, task_id: int, task_update: TaskUpdate) -> Task | None:
        return await self.repository.update(task_id, task_update)

    async def delete_task(self, task_id: int) -> bool:
        return await self.repository.delete(task_id)
