# OWNER: MEMBER-3
from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.exceptions import NotFoundError
from app.models.user import User
from app.schemas.maintenance import (
    MaintenanceScheduleCreate,
    MaintenanceScheduleUpdate,
    MaintenanceScheduleResponse,
)
from app.services.maintenance_service import MaintenanceService

router = APIRouter()


def _service(db: AsyncIOMotorDatabase = Depends(get_db)) -> MaintenanceService:
    return MaintenanceService(db)


@router.post("", response_model=MaintenanceScheduleResponse, status_code=201)
async def create_schedule(
    payload: MaintenanceScheduleCreate,
    svc: MaintenanceService = Depends(_service),
    _: User = Depends(get_current_user),
):
    schedule = await svc.create(payload)
    return MaintenanceScheduleResponse(**schedule.model_dump())


@router.get("", response_model=list[MaintenanceScheduleResponse])
async def list_schedules(
    skip: int = 0,
    limit: int = 100,
    asset_id: Optional[str] = None,
    svc: MaintenanceService = Depends(_service),
    _: User = Depends(get_current_user),
):
    if asset_id is not None:
        schedules = await svc.list_by_asset(asset_id)
    else:
        schedules = await svc.list(skip=skip, limit=limit)
    return [MaintenanceScheduleResponse(**schedule.model_dump()) for schedule in schedules]


@router.post("/evaluate")
async def evaluate_due_schedules(
    svc: MaintenanceService = Depends(_service),
    current_user: User = Depends(get_current_user),
):
    generated = await svc.evaluate_due_schedules(created_by=current_user.id)
    return {"generated_work_orders": generated}


@router.get("/{schedule_id}", response_model=MaintenanceScheduleResponse)
async def get_schedule(
    schedule_id: str,
    svc: MaintenanceService = Depends(_service),
    _: User = Depends(get_current_user),
):
    schedule = await svc.get(schedule_id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="maintenance schedule not found")
    return MaintenanceScheduleResponse(**schedule.model_dump())


@router.patch("/{schedule_id}", response_model=MaintenanceScheduleResponse)
async def update_schedule(
    schedule_id: str,
    payload: MaintenanceScheduleUpdate,
    svc: MaintenanceService = Depends(_service),
    _: User = Depends(get_current_user),
):
    schedule = await svc.update(schedule_id, payload)
    if schedule is None:
        raise HTTPException(status_code=404, detail="maintenance schedule not found")
    return MaintenanceScheduleResponse(**schedule.model_dump())


@router.delete("/{schedule_id}", status_code=204)
async def delete_schedule(
    schedule_id: str,
    svc: MaintenanceService = Depends(_service),
    _: User = Depends(get_current_user),
):
    deleted = await svc.delete(schedule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="maintenance schedule not found")
