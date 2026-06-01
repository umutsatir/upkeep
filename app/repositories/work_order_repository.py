# OWNER: MEMBER-1
from typing import Optional

from app.models.work_order import WorkOrder, WorkOrderStatus
from app.repositories.base_repository import BaseRepository


class WorkOrderRepository(BaseRepository[WorkOrder]):
    model_class = WorkOrder
    collection_name = "work_orders"

    async def list_by_asset(self, asset_id: str) -> list[WorkOrder]:
        """TODO (MEMBER-1): Return all work orders for a given asset."""
        return await self.list(filter={"asset_id": asset_id})

    async def list_by_status(self, status: WorkOrderStatus) -> list[WorkOrder]:
        """TODO (MEMBER-1): Return all work orders with a given status."""
        return await self.list(filter={"status": status.value})

    async def list_by_assignee(self, user_id: str) -> list[WorkOrder]:
        """TODO (MEMBER-1): Return all work orders assigned to a user."""
        return await self.list(filter={"assigned_to": user_id})
