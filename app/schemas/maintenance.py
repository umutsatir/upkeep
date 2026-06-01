# OWNER: MEMBER-3
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.maintenance import TriggerType


class MaintenanceScheduleCreate(BaseModel):
    asset_id: str
    title: str
    description: str
    trigger_type: TriggerType = TriggerType.TIME_BASED
    interval_days: Optional[int] = None
    usage_threshold_hours: Optional[float] = None
    generated_wo_priority: str = "medium"
    assigned_to: Optional[str] = None


class MaintenanceScheduleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    interval_days: Optional[int] = None
    usage_threshold_hours: Optional[float] = None
    is_active: Optional[bool] = None
    generated_wo_priority: Optional[str] = None
    assigned_to: Optional[str] = None


class MaintenanceScheduleResponse(BaseModel):
    id: str
    asset_id: str
    title: str
    description: str
    trigger_type: TriggerType
    interval_days: Optional[int]
    usage_threshold_hours: Optional[float]
    is_active: bool
    last_triggered_at: Optional[datetime]
    next_due_at: Optional[datetime]
    generated_wo_priority: str
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
