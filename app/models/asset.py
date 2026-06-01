# OWNER: MEMBER-2
from datetime import datetime
from enum import Enum
from typing import Optional

from app.models.base import BaseEntity, PyObjectId


class AssetStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNDER_MAINTENANCE = "under_maintenance"
    DECOMMISSIONED = "decommissioned"


class Asset(BaseEntity):
    """A physical asset tracked by the CMMS.

    TODO (MEMBER-2):
    - Implement full asset lifecycle (activate, decommission, send_to_maintenance).
    - Add repair history as a list of embedded RepairRecord value objects.
    - Add warranty expiry alerting logic (check warranty_expires_at vs today).
    - Implement location tracking (building / floor / room) as a nested Location VO.
    - Consider Observer pattern to notify Work Order service when asset goes
      UNDER_MAINTENANCE so related open orders are flagged.
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
    location: Optional[str] = None  # TODO: replace with Location value object

    # Ownership
    assigned_to: Optional[PyObjectId] = None  # User.id of responsible technician

    # Warranty
    purchase_date: Optional[datetime] = None
    warranty_expires_at: Optional[datetime] = None

    # Repair history (embedded documents)
    repair_history: list[dict] = []  # TODO: type as list[RepairRecord]

    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    notes: str = ""
