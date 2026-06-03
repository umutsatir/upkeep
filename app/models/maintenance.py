# OWNER: MEMBER-3
from datetime import datetime
from enum import Enum
from typing import Optional

from app.models.base import BaseEntity, PyObjectId
from app.models.work_order import WorkOrderPriority


class TriggerType(str, Enum):
    """Determines which Strategy is used to evaluate whether a schedule is due."""

    TIME_BASED = "time_based"    # e.g. every 30 days
    USAGE_BASED = "usage_based"  # e.g. every 500 operating hours


class MaintenanceSchedule(BaseEntity):
    """A recurring preventive maintenance schedule for an asset."""

    asset_id: PyObjectId
    title: str
    description: str
    trigger_type: TriggerType = TriggerType.TIME_BASED

    # Time-based fields
    interval_days: Optional[int] = None  # e.g. 30 → monthly

    # Usage-based fields
    usage_threshold_hours: Optional[float] = None  # e.g. 500.0
    current_usage_hours: Optional[float] = None

    is_active: bool = True
    last_triggered_at: Optional[datetime] = None
    next_due_at: Optional[datetime] = None  # denormalised for quick queries

    # Work order template fields (used when auto-generating a WO)
    generated_wo_priority: WorkOrderPriority = WorkOrderPriority.MEDIUM
    assigned_to: Optional[PyObjectId] = None  # default assignee for generated WOs

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }
