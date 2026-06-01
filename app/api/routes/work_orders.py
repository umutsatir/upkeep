# OWNER: MEMBER-1
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.exceptions import InvalidTransitionError, NotFoundError
from app.models.user import User
from app.models.work_order import WorkOrderStatus
from app.schemas.work_order import (
    WorkOrderCreate,
    WorkOrderResponse,
    WorkOrderStatusTransition,
    WorkOrderUpdate,
)
from app.services.work_order_service import WorkOrderService

router = APIRouter()


def _svc(db: AsyncIOMotorDatabase = Depends(get_db)) -> WorkOrderService:
    return WorkOrderService(db)


@router.post("/", response_model=WorkOrderResponse, status_code=201)
async def create_work_order(
    payload: WorkOrderCreate,
    svc: WorkOrderService = Depends(_svc),
    current_user: User = Depends(get_current_user),
):
    wo = await svc.create(payload, created_by=current_user.id)
    return WorkOrderResponse(**wo.model_dump())


@router.get("/", response_model=list[WorkOrderResponse])
async def list_work_orders(
    skip: int = 0,
    limit: int = 100,
    status: WorkOrderStatus = None,
    svc: WorkOrderService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    wos = await svc.list(skip=skip, limit=limit, status=status)
    return [WorkOrderResponse(**wo.model_dump()) for wo in wos]


@router.get("/{work_order_id}", response_model=WorkOrderResponse)
async def get_work_order(
    work_order_id: str,
    svc: WorkOrderService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    wo = await svc.get(work_order_id)
    if wo is None:
        raise HTTPException(status_code=404, detail="work order not found")
    return WorkOrderResponse(**wo.model_dump())


@router.patch("/{work_order_id}", response_model=WorkOrderResponse)
async def update_work_order(
    work_order_id: str,
    payload: WorkOrderUpdate,
    svc: WorkOrderService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    wo = await svc.update(work_order_id, payload)
    if wo is None:
        raise HTTPException(status_code=404, detail="work order not found")
    return WorkOrderResponse(**wo.model_dump())


@router.post("/{work_order_id}/transition", response_model=WorkOrderResponse)
async def transition_work_order(
    work_order_id: str,
    payload: WorkOrderStatusTransition,
    svc: WorkOrderService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    try:
        wo = await svc.transition(work_order_id, payload)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="work order not found")
    except InvalidTransitionError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    return WorkOrderResponse(**wo.model_dump())


@router.delete("/{work_order_id}", status_code=204)
async def delete_work_order(
    work_order_id: str,
    svc: WorkOrderService = Depends(_svc),
    _: User = Depends(get_current_user),
):
    deleted = await svc.delete(work_order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="work order not found")
