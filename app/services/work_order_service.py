# OWNER: MEMBER-1
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import InvalidTransitionError, NotFoundError
from app.models.asset import RepairRecord
from app.models.work_order import WorkOrder, WorkOrderStatus
from app.repositories.work_order_repository import WorkOrderRepository
from app.schemas.inventory import StockAdjustment
from app.schemas.work_order import WorkOrderCreate, WorkOrderStatusTransition, WorkOrderUpdate
from app.services.asset_service import AssetService
from app.services.inventory_service import InventoryService
from app.services.work_order_states import get_state


class WorkOrderService:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._repo = WorkOrderRepository(db)
        self._inventory_svc = InventoryService(db)
        self._asset_svc = AssetService(db)

    async def create(self, payload: WorkOrderCreate, created_by: str) -> WorkOrder:
        wo = WorkOrder(
            title=payload.title,
            description=payload.description,
            asset_id=payload.asset_id,
            created_by=created_by,
            priority=payload.priority,
            due_date=payload.due_date,
            notes=payload.notes,
        )
        return await self._repo.create(wo)

    async def get(self, work_order_id: str) -> Optional[WorkOrder]:
        return await self._repo.get_by_id(work_order_id)

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[WorkOrderStatus] = None,
    ) -> list[WorkOrder]:
        if status is not None:
            return await self._repo.list_by_status(status)
        return await self._repo.list(skip=skip, limit=limit)

    async def update(self, work_order_id: str, payload: WorkOrderUpdate) -> Optional[WorkOrder]:
        wo = await self._repo.get_by_id(work_order_id)
        if wo is None:
            return None
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(wo, field, value)
        return await self._repo.update(wo)

    async def transition(
        self, work_order_id: str, payload: WorkOrderStatusTransition
    ) -> WorkOrder:
        wo = await self._repo.get_by_id(work_order_id)
        if wo is None:
            raise NotFoundError("WorkOrder", work_order_id)
        # State pattern: each state enforces its own allowed transitions
        state = get_state(wo.status)
        state.transition(wo, payload.new_status, assigned_to=payload.assigned_to)

        if payload.new_status == WorkOrderStatus.COMPLETED:
            wo.parts_used = [p.model_dump() for p in payload.parts_used]

            for part in payload.parts_used:
                await self._inventory_svc.consume(
                    part.inventory_item_id,
                    StockAdjustment(
                        quantity=part.quantity,
                        work_order_id=str(wo.id),
                    ),
                )

            await self._asset_svc.add_repair_record(
                str(wo.asset_id),
                RepairRecord(
                    date=datetime.now(timezone.utc),
                    description=f"Work order completed: {wo.title}",
                    work_order_id=wo.id,
                ),
            )

        return await self._repo.update(wo)

    async def delete(self, work_order_id: str) -> bool:
        return await self._repo.delete(work_order_id)
