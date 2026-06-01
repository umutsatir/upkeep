# OWNER: MEMBER-1
from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db
from app.schemas.work_order import (
    WorkOrderCreate,
    WorkOrderUpdate,
    WorkOrderStatusTransition,
    WorkOrderResponse,
)
from app.services.work_order_service import WorkOrderService

router = APIRouter()


def _service(db: AsyncIOMotorDatabase = Depends(get_db)) -> WorkOrderService:
    return WorkOrderService(db)


@router.post("/", response_model=WorkOrderResponse, status_code=201)
async def create_work_order(payload: WorkOrderCreate, svc: WorkOrderService = Depends(_service)):
    """TODO (MEMBER-1)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/", response_model=list[WorkOrderResponse])
async def list_work_orders(
    skip: int = 0, limit: int = 100, svc: WorkOrderService = Depends(_service)
):
    """TODO (MEMBER-1)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{work_order_id}", response_model=WorkOrderResponse)
async def get_work_order(work_order_id: str, svc: WorkOrderService = Depends(_service)):
    """TODO (MEMBER-1)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.patch("/{work_order_id}", response_model=WorkOrderResponse)
async def update_work_order(
    work_order_id: str, payload: WorkOrderUpdate, svc: WorkOrderService = Depends(_service)
):
    """TODO (MEMBER-1)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/{work_order_id}/transition", response_model=WorkOrderResponse)
async def transition_work_order(
    work_order_id: str,
    payload: WorkOrderStatusTransition,
    svc: WorkOrderService = Depends(_service),
):
    """TODO (MEMBER-1): State-pattern transition endpoint."""
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/{work_order_id}", status_code=204)
async def delete_work_order(work_order_id: str, svc: WorkOrderService = Depends(_service)):
    """TODO (MEMBER-1)"""
    raise HTTPException(status_code=501, detail="Not implemented yet")
