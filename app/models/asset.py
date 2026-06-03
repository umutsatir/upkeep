# OWNER: MEMBER-2
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.models.base import BaseEntity, PyObjectId


class AssetStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNDER_MAINTENANCE = "under_maintenance"
    DECOMMISSIONED = "decommissioned"


class RepairRecord(BaseModel):
    """Embedded value object representing a single repair entry on an asset."""

    date: datetime
    description: str
    cost: float = 0.0
    work_order_id: Optional[PyObjectId] = None  # link back to the WO that triggered the repair


class Asset(BaseEntity):
    """A physical asset tracked by the CMMS.

    Lifecycle: ACTIVE → UNDER_MAINTENANCE → ACTIVE
                     → INACTIVE
                     → DECOMMISSIONED  (terminal)
    """

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "protected_namespaces": (),
    }

    name: str
    asset_tag: str  # unique human-readable identifier e.g. "HVAC-001"
    category: str  # e.g. "HVAC", "Electrical", "Plumbing"
    status: AssetStatus = AssetStatus.ACTIVE

    # Location
    location: Optional[str] = None

    # Ownership
    assigned_to: Optional[PyObjectId] = None  # User.id of responsible technician

    # Warranty
    purchase_date: Optional[datetime] = None
    warranty_expires_at: Optional[datetime] = None

    # Repair history (embedded documents)
    repair_history: list[RepairRecord] = []

    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    notes: str = ""
