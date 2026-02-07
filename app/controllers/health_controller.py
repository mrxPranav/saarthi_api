from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.schemas.health_check_dto import HealthCheckCreate, HealthCheckResponse
from app.repositories.health_check_repository import HealthCheckRepository
from app.services.health_check_service import HealthCheckService
from typing import List

router = APIRouter(prefix="/health", tags=["Health"])

async def get_service(db: AsyncSession = Depends(get_db)) -> HealthCheckService:
    repository = HealthCheckRepository(db)
    return HealthCheckService(repository)

@router.get("/", response_model=dict)
async def health_check():
    return {"status": "ok", "message": "Service is healthy"}

@router.post("/checks", response_model=HealthCheckResponse, status_code=status.HTTP_201_CREATED)
async def create_health_check(
    item: HealthCheckCreate,
    service: HealthCheckService = Depends(get_service)
):
    return await service.create_health_check(item)

@router.get("/checks", response_model=List[HealthCheckResponse])
async def read_health_checks(
    skip: int = 0,
    limit: int = 100,
    service: HealthCheckService = Depends(get_service)
):
    return await service.get_all_health_checks(skip, limit)

@router.get("/checks/{health_check_id}", response_model=HealthCheckResponse)
async def read_health_check(
    health_check_id: int,
    service: HealthCheckService = Depends(get_service)
):
    db_health_check = await service.get_health_check(health_check_id)
    if db_health_check is None:
        raise HTTPException(status_code=404, detail="Health check not found")
    return db_health_check

@router.put("/checks/{health_check_id}", response_model=HealthCheckResponse)
async def update_health_check(
    health_check_id: int,
    item: HealthCheckCreate,
    service: HealthCheckService = Depends(get_service)
):
    db_health_check = await service.update_health_check(health_check_id, item)
    if db_health_check is None:
        raise HTTPException(status_code=404, detail="Health check not found")
    return db_health_check

@router.delete("/checks/{health_check_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_health_check(
    health_check_id: int,
    service: HealthCheckService = Depends(get_service)
):
    success = await service.delete_health_check(health_check_id)
    if not success:
        raise HTTPException(status_code=404, detail="Health check not found")
