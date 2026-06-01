# OWNER: MEMBER-4
from typing import Optional

from app.models.base import BaseEntity, PyObjectId


class InventoryItem(BaseEntity):
    """A spare part or consumable tracked in inventory.

    TODO (MEMBER-4):
    - Implement consume(quantity, work_order_id) method that deducts stock and
      records the consumption against a WorkOrder (MEMBER-1 integration point).
    - Implement restock(quantity, notes) method.
    - Add low-stock alerting: emit an alert (log / notification) when
      quantity_on_hand <= low_stock_threshold.
    - Add Decorator pattern for alert channels: EmailAlertDecorator,
      SlackAlertDecorator wrap a base LowStockAlert notifier.
    - Consider an Observer that watches WorkOrder completion events to auto-
      deduct parts from parts_used list (MEMBER-1 integration point).
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

    # Usage history (lightweight embedded log)
    consumption_log: list[dict] = []  # TODO: type as list[ConsumptionRecord]

    notes: str = ""
