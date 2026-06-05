# OWNER: MEMBER-4
from __future__ import annotations

import logging
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.inventory import InventoryItem
from app.repositories.inventory_repository import InventoryRepository
from app.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemUpdate,
    StockAdjustment,
)
from app.services.notifiers import LowStockNotifier, build_default_notifier

logger = logging.getLogger("upkeep.inventory")


class InventoryService:
    """Business logic for inventory / spare parts management.

    Implements the Decorator pattern for low-stock alerting:
    When stock drops at or below the threshold after a consume() call,
    the composed notifier chain fires (Log → Email → Slack).
    """

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        notifier: LowStockNotifier | None = None,
    ) -> None:
        self._repo = InventoryRepository(db)
        self._notifier = notifier or build_default_notifier()

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    async def create(self, payload: InventoryItemCreate) -> InventoryItem:
        """Create a new inventory item. Raises ValueError on duplicate SKU."""
        existing = await self._repo.get_by_sku(payload.sku)
        if existing is not None:
            raise ValueError(f"An item with SKU '{payload.sku}' already exists")

        item = InventoryItem(**payload.model_dump())
        return await self._repo.create(item)

    async def get(self, item_id: str) -> InventoryItem | None:
        """Return a single item by ID, or None."""
        return await self._repo.get_by_id(item_id)

    async def list(self, skip: int = 0, limit: int = 100) -> list[InventoryItem]:
        """Return a paginated list of all items."""
        return await self._repo.list(skip=skip, limit=limit)

    async def update(
        self, item_id: str, payload: InventoryItemUpdate
    ) -> InventoryItem | None:
        """Partial-update an existing item.  Returns None if not found."""
        item = await self._repo.get_by_id(item_id)
        if item is None:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        return await self._repo.update(item)

    async def delete(self, item_id: str) -> bool:
        """Delete an item by ID. Returns True if deleted."""
        return await self._repo.delete(item_id)

    # ------------------------------------------------------------------
    # Stock operations
    # ------------------------------------------------------------------

    async def consume(
        self, item_id: str, adjustment: StockAdjustment
    ) -> InventoryItem:
        """Deduct stock, log consumption against a WO, fire notifier if low.

        Raises ValueError if item not found or insufficient stock.
        """
        item = await self._repo.get_by_id(item_id)
        if item is None:
            raise ValueError(f"Inventory item '{item_id}' not found")

        if adjustment.quantity <= 0:
            raise ValueError("Consume quantity must be positive")

        if item.quantity_on_hand < adjustment.quantity:
            raise ValueError(
                f"Insufficient stock: {item.quantity_on_hand} {item.unit} "
                f"available, {adjustment.quantity} requested"
            )

        # Deduct
        item.quantity_on_hand -= adjustment.quantity

        # Log the consumption
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "quantity": -adjustment.quantity,
            "work_order_id": adjustment.work_order_id,
            "notes": adjustment.notes,
            "action": "consume",
        }
        item.consumption_log.append(record)

        updated = await self._repo.update(item)

        # Fire low-stock alert if threshold crossed
        if updated.is_low_stock:
            try:
                channels = self._notifier.notify(updated)
                logger.info(
                    "Low-stock alert fired for '%s' via: %s",
                    updated.name,
                    ", ".join(channels),
                )
            except Exception:
                logger.exception("Failed to send low-stock notification")

        return updated

    async def restock(
        self, item_id: str, adjustment: StockAdjustment
    ) -> InventoryItem:
        """Increase stock and record the restock event.

        Raises ValueError if item not found or quantity invalid.
        """
        item = await self._repo.get_by_id(item_id)
        if item is None:
            raise ValueError(f"Inventory item '{item_id}' not found")

        if adjustment.quantity <= 0:
            raise ValueError("Restock quantity must be positive")

        # Add stock
        item.quantity_on_hand += adjustment.quantity

        # Log the restock
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "quantity": adjustment.quantity,
            "work_order_id": adjustment.work_order_id,
            "notes": adjustment.notes,
            "action": "restock",
        }
        item.consumption_log.append(record)

        return await self._repo.update(item)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    async def list_low_stock(self) -> list[InventoryItem]:
        """Return items where quantity_on_hand <= low_stock_threshold."""
        return await self._repo.list_low_stock()
