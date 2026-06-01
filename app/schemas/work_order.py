# OWNER: MEMBER-1
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.work_order import WorkOrderPriority, WorkOrderStatus


class WorkOrderCreate(BaseModel):
    title: str
    description: str
    asset_id: str
    created_by: str
    priority: WorkOrderPriority = WorkOrderPriority.MEDIUM
    due_date: Optional[datetime] = None
    notes: str = ""


class WorkOrderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[WorkOrderPriority] = None
    due_date: Optional[datetime] = None
    notes: Optional[str] = None


class WorkOrderStatusTransition(BaseModel):
    """Used by status-transition endpoints (assign, start, complete, …)."""

    new_status: WorkOrderStatus
    assigned_to: Optional[str] = None  # required when transitioning to ASSIGNED


class WorkOrderResponse(BaseModel):
    id: str
    title: str
    description: str
    status: WorkOrderStatus
    priority: WorkOrderPriority
    asset_id: str
    assigned_to: Optional[str]
    created_by: str
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    parts_used: list[dict]
    notes: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
