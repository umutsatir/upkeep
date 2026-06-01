# OWNER: MEMBER-3
from datetime import datetime
from enum import Enum
from typing import Optional

from app.models.base import BaseEntity, PyObjectId


class TriggerType(str, Enum):
    """Determines which Strategy is used to evaluate whether a schedule is due."""

    TIME_BASED = "time_based"    # e.g. every 30 days
    USAGE_BASED = "usage_based"  # e.g. every 500 operating hours


class MaintenanceSchedule(BaseEntity):
    """A recurring preventive maintenance schedule for an asset.

    TODO (MEMBER-3):
    - Implement Strategy pattern:
        * Create MaintenanceTriggerStrategy abstract base class with
          is_due(schedule) -> bool method.
        * TimeBasedStrategy: compare last_triggered_at + interval_days to today.
        * UsageBasedStrategy: compare asset operating hours to usage_threshold_hours.
    - Add a scheduler (APScheduler or simple cron route) that checks all active
      schedules and calls generate_work_order() when is_due() returns True.
    - generate_work_order() must call WorkOrderService (MEMBER-1) to create a
      new WorkOrder — this is the key integration point.
    - Add last_triggered_at update logic after each auto-generated work order.
    """

    asset_id: PyObjectId
    title: str
    description: str
    trigger_type: TriggerType = TriggerType.TIME_BASED

    # Time-based fields
    interval_days: Optional[int] = None  # e.g. 30 → monthly

    # Usage-based fields
    usage_threshold_hours: Optional[float] = None  # e.g. 500.0

    is_active: bool = True
    last_triggered_at: Optional[datetime] = None
    next_due_at: Optional[datetime] = None  # denormalised for quick queries

    # Work order template fields (used when auto-generating a WO)
    generated_wo_priority: str = "medium"
    assigned_to: Optional[PyObjectId] = None  # default assignee for generated WOs
