from app.repositories.health_check_repository import HealthCheckRepository
from app.schemas.health_check_dto import HealthCheckCreate
from app.models.health_check import HealthCheck

class HealthCheckService:
    def __init__(self, repository: HealthCheckRepository):
        self.repository = repository

    async def create_health_check(self, item: HealthCheckCreate) -> HealthCheck:
        return await self.repository.create(item)

    async def get_health_check(self, health_check_id: int) -> HealthCheck | None:
        return await self.repository.get_by_id(health_check_id)

    async def get_all_health_checks(self, skip: int = 0, limit: int = 100) -> list[HealthCheck]:
        return await self.repository.get_all(skip, limit)

    async def update_health_check(self, health_check_id: int, item: HealthCheckCreate) -> HealthCheck | None:
        return await self.repository.update(health_check_id, item)

    async def delete_health_check(self, health_check_id: int) -> bool:
        return await self.repository.delete(health_check_id)
