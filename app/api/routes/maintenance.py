# OWNER: MEMBER-3
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db
from app.schemas.maintenance import (
    MaintenanceScheduleCreate,
    MaintenanceScheduleUpdate,
    MaintenanceScheduleResponse,
)
from app.services.maintenance_service import MaintenanceService

router = APIRouter()


def _service(db: AsyncIOMotorDatabase = Depends(get_db)) -> MaintenanceService:
    return MaintenanceService(db)


@router.post("/", response_model=MaintenanceScheduleResponse, status_code=201)
async def create_schedule(
    payload: MaintenanceScheduleCreate, svc: MaintenanceService = Depends(_service)
):
    """TODO (MEMBER-3)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/", response_model=list[MaintenanceScheduleResponse])
async def list_schedules(
    skip: int = 0, limit: int = 100, svc: MaintenanceService = Depends(_service)
):
    """TODO (MEMBER-3)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{schedule_id}", response_model=MaintenanceScheduleResponse)
async def get_schedule(schedule_id: str, svc: MaintenanceService = Depends(_service)):
    """TODO (MEMBER-3)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/{schedule_id}", response_model=MaintenanceScheduleResponse)
async def update_schedule(
    schedule_id: str,
    payload: MaintenanceScheduleUpdate,
    svc: MaintenanceService = Depends(_service),
):
    """TODO (MEMBER-3)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/{schedule_id}", status_code=204)
async def delete_schedule(schedule_id: str, svc: MaintenanceService = Depends(_service)):
    """TODO (MEMBER-3)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/evaluate", tags=["Maintenance"])
async def evaluate_due_schedules(svc: MaintenanceService = Depends(_service)):
    """TODO (MEMBER-3): Trigger evaluation of all due schedules and auto-generate WOs."""
    raise HTTPException(status_code=501, detail="Not implemented yet")
