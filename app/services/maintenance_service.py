# OWNER: MEMBER-3
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.maintenance import MaintenanceSchedule
from app.repositories.maintenance_repository import MaintenanceRepository
from app.schemas.maintenance import MaintenanceScheduleCreate, MaintenanceScheduleUpdate


class MaintenanceService:
    """Business logic for preventive maintenance scheduling.

    TODO (MEMBER-3):
    - create(): compute initial next_due_at from trigger_type + interval.
    - evaluate_due_schedules(): iterate list_due(), call generate_work_order() for each.
    - generate_work_order(schedule): call WorkOrderService.create() with the
      schedule's template fields — key cross-module integration point with MEMBER-1.
    - Implement Strategy pattern:
        * abstract MaintenanceTriggerStrategy with is_due(schedule) -> bool
        * TimeBasedStrategy, UsageBasedStrategy as concrete classes
        * MaintenanceService selects the strategy based on schedule.trigger_type
    - After generating a WO, update schedule.last_triggered_at and
      recalculate next_due_at.
    """

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._repo = MaintenanceRepository(db)

    async def create(self, payload: MaintenanceScheduleCreate) -> MaintenanceSchedule:
        """TODO (MEMBER-3)"""
        raise NotImplementedError

    async def get(self, schedule_id: str) -> MaintenanceSchedule | None:
        """TODO (MEMBER-3)"""
        raise NotImplementedError

    async def list(self, skip: int = 0, limit: int = 100) -> list[MaintenanceSchedule]:
        """TODO (MEMBER-3)"""
        raise NotImplementedError

    async def update(
        self, schedule_id: str, payload: MaintenanceScheduleUpdate
    ) -> MaintenanceSchedule | None:
        """TODO (MEMBER-3)"""
        raise NotImplementedError

    async def delete(self, schedule_id: str) -> bool:
        """TODO (MEMBER-3)"""
        raise NotImplementedError

    async def evaluate_due_schedules(self) -> list[str]:
        """TODO (MEMBER-3): Run evaluations and return list of generated WO ids."""
        raise NotImplementedError
