# OWNER: MEMBER-4
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.inventory import InventoryItem
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.inventory import InventoryItemCreate, InventoryItemUpdate, StockAdjustment


class InventoryService:
    """Business logic for inventory / spare parts management.

    TODO (MEMBER-4):
    - consume(item_id, adjustment): deduct quantity, append to consumption_log,
      emit low-stock alert if quantity_on_hand <= low_stock_threshold.
    - restock(item_id, adjustment): add quantity, update log.
    - Implement Decorator pattern for alert channels:
        * LowStockNotifier (base)
        * EmailAlertDecorator(notifier) — wraps base with email delivery
        * SlackAlertDecorator(notifier) — wraps base with Slack delivery
    - Hook into WorkOrder completion: when a WO is closed, call consume() for
      each item in work_order.parts_used (integration with MEMBER-1).
    - list_low_stock(): return items below threshold, used by dashboard widget.
    """

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._repo = InventoryRepository(db)

    async def create(self, payload: InventoryItemCreate) -> InventoryItem:
        """TODO (MEMBER-4)"""
        raise NotImplementedError

    async def get(self, item_id: str) -> InventoryItem | None:
        """TODO (MEMBER-4)"""
        raise NotImplementedError

    async def list(self, skip: int = 0, limit: int = 100) -> list[InventoryItem]:
        """TODO (MEMBER-4)"""
        raise NotImplementedError

    async def update(self, item_id: str, payload: InventoryItemUpdate) -> InventoryItem | None:
        """TODO (MEMBER-4)"""
        raise NotImplementedError

    async def delete(self, item_id: str) -> bool:
        """TODO (MEMBER-4)"""
        raise NotImplementedError

    async def consume(self, item_id: str, adjustment: StockAdjustment) -> InventoryItem:
        """TODO (MEMBER-4): Deduct stock and record consumption against a WO."""
        raise NotImplementedError

    async def restock(self, item_id: str, adjustment: StockAdjustment) -> InventoryItem:
        """TODO (MEMBER-4): Increase stock and record the restock event."""
        raise NotImplementedError

    async def list_low_stock(self) -> list[InventoryItem]:
        """TODO (MEMBER-4)"""
        raise NotImplementedError
