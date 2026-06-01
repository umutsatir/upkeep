# OWNER: MEMBER-1
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.work_order import WorkOrder, WorkOrderStatus
from app.repositories.work_order_repository import WorkOrderRepository
from app.schemas.work_order import WorkOrderCreate, WorkOrderUpdate, WorkOrderStatusTransition


class WorkOrderService:
    """Business logic for work order lifecycle management.

    TODO (MEMBER-1):
    - Implement State pattern classes (OpenState, AssignedState, …) and wire
      them through transition().
    - In transition(), enforce valid transitions and raise a domain exception
      (e.g. InvalidTransitionError) for illegal ones.
    - On transition to COMPLETED, call InventoryService to deduct parts_used
      (MEMBER-4 integration point).
    - On transition to COMPLETED, update the asset's repair_history
      (MEMBER-2 integration point).
    - validate asset_id exists via AssetRepository before creating a work order.
    """

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._repo = WorkOrderRepository(db)

    async def create(self, payload: WorkOrderCreate) -> WorkOrder:
        """TODO (MEMBER-1): Validate asset exists, build WorkOrder, persist."""
        raise NotImplementedError

    async def get(self, work_order_id: str) -> WorkOrder | None:
        """TODO (MEMBER-1)"""
        raise NotImplementedError

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        status: WorkOrderStatus | None = None,
    ) -> list[WorkOrder]:
        """TODO (MEMBER-1)"""
        raise NotImplementedError

    async def update(self, work_order_id: str, payload: WorkOrderUpdate) -> WorkOrder | None:
        """TODO (MEMBER-1): Load → apply patch → persist."""
        raise NotImplementedError

    async def transition(
        self, work_order_id: str, payload: WorkOrderStatusTransition
    ) -> WorkOrder | None:
        """TODO (MEMBER-1): Delegate to the current State object to advance lifecycle."""
        raise NotImplementedError

    async def delete(self, work_order_id: str) -> bool:
        """TODO (MEMBER-1)"""
        raise NotImplementedError
