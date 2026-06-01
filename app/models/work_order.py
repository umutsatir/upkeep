# OWNER: MEMBER-1
from datetime import datetime
from enum import Enum
from typing import Optional

from app.models.base import BaseEntity, PyObjectId


class WorkOrderStatus(str, Enum):
    """Lifecycle states for the State pattern implementation.

    Valid transitions:
        OPEN → ASSIGNED → IN_PROGRESS → COMPLETED → CLOSED
        Any state → CANCELLED
    """

    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class WorkOrderPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorkOrder(BaseEntity):
    """A maintenance task to be carried out by a technician.

    TODO (MEMBER-1):
    - Implement State pattern: create WorkOrderState base class and a concrete
      class for each WorkOrderStatus (OpenState, AssignedState, …).  Each state
      class should guard valid transitions and raise InvalidTransitionError
      for illegal ones.
    - Add transition methods: assign(), start(), complete(), close(), cancel().
    - Integrate with Asset (MEMBER-2): validate asset_id exists before saving.
    - Integrate with Inventory (MEMBER-4): consume parts_used on completion.
    """

    title: str
    description: str
    status: WorkOrderStatus = WorkOrderStatus.OPEN
    priority: WorkOrderPriority = WorkOrderPriority.MEDIUM

    asset_id: PyObjectId
    assigned_to: Optional[PyObjectId] = None  # User.id
    created_by: PyObjectId  # User.id

    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Parts consumed from inventory (MEMBER-4 integration point)
    parts_used: list[dict] = []  # [{"inventory_item_id": ..., "quantity": ...}]

    notes: str = ""
