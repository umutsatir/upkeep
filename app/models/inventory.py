# OWNER: MEMBER-4
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel

from app.models.base import BaseEntity, PyObjectId


class ConsumptionRecord(BaseModel):
    """Value object that records a single stock movement (consume or restock)."""

    timestamp: datetime = datetime.now(timezone.utc)
    quantity: int  # positive = restock, negative = consume
    work_order_id: Optional[str] = None
    notes: str = ""
    action: str = "consume"  # "consume" | "restock"


class InventoryItem(BaseEntity):
    """A spare part or consumable tracked in inventory.

    Uses the Decorator pattern for low-stock alerting:
    LowStockNotifier (base) → EmailAlertDecorator → SlackAlertDecorator
    Each decorator adds an alert channel without modifying core logic.
    """

    name: str
    sku: str  # unique stock-keeping unit
    category: str  # e.g. "Filters", "Bearings", "Lubricants"

    quantity_on_hand: int = 0
    low_stock_threshold: int = 5
    unit_cost: float = 0.0
    unit: str = "pcs"  # e.g. "pcs", "litres", "metres"

    supplier: Optional[str] = None
    location: Optional[str] = None  # physical bin / shelf location

    # Usage history (typed embedded log)
    consumption_log: list[dict] = []

    notes: str = ""

    @property
    def is_low_stock(self) -> bool:
        """Check whether current stock is at or below the alert threshold."""
        return self.quantity_on_hand <= self.low_stock_threshold

    @property
    def total_value(self) -> float:
        """Total value of stock on hand."""
        return self.quantity_on_hand * self.unit_cost
