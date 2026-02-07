from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.health_check import HealthCheck
from app.schemas.health_check_dto import HealthCheckCreate

class HealthCheckRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, health_check_data: HealthCheckCreate) -> HealthCheck:
        db_health_check = HealthCheck(
            request_time=health_check_data.request_time,
            response_time=health_check_data.response_time,
            difference=health_check_data.difference,
            status=health_check_data.status
        )
        self.db.add(db_health_check)
        await self.db.commit()
        await self.db.refresh(db_health_check)
        return db_health_check

    async def get_by_id(self, health_check_id: int) -> HealthCheck | None:
        result = await self.db.execute(select(HealthCheck).where(HealthCheck.id == health_check_id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[HealthCheck]:
        result = await self.db.execute(select(HealthCheck).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(self, health_check_id: int, health_check_data: HealthCheckCreate) -> HealthCheck | None:
        db_health_check = await self.get_by_id(health_check_id)
        if db_health_check:
            db_health_check.request_time = health_check_data.request_time
            db_health_check.response_time = health_check_data.response_time
            db_health_check.difference = health_check_data.difference
            db_health_check.status = health_check_data.status
            await self.db.commit()
            await self.db.refresh(db_health_check)
        return db_health_check

    async def delete(self, health_check_id: int) -> bool:
        db_health_check = await self.get_by_id(health_check_id)
        if db_health_check:
            await self.db.delete(db_health_check)
            await self.db.commit()
            return True
        return False
