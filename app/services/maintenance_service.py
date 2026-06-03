# OWNER: MEMBER-3
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.maintenance import MaintenanceSchedule, TriggerType
from app.models.work_order import WorkOrderStatus
from app.repositories.maintenance_repository import MaintenanceRepository
from app.schemas.maintenance import MaintenanceScheduleCreate, MaintenanceScheduleUpdate
from app.schemas.work_order import WorkOrderCreate, WorkOrderStatusTransition
from app.services.maintenance_strategies import get_trigger_strategy
from app.services.work_order_service import WorkOrderService
from app.models.base import PyObjectId


class MaintenanceService:
    """Business logic for preventive maintenance scheduling."""

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._repo = MaintenanceRepository(db)
        self._work_order_service = WorkOrderService(db)

    @staticmethod
    def _utcnow() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def _resolve_object_id(value: Optional[str]) -> Optional[PyObjectId]:
        if not value or not value.strip():
            return None
        try:
            return PyObjectId(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _validate_schedule(schedule: MaintenanceSchedule) -> None:
        if schedule.trigger_type == TriggerType.TIME_BASED:
            if schedule.interval_days is None or schedule.interval_days <= 0:
                raise ValueError("time-based schedules require a positive interval_days")
        elif schedule.trigger_type == TriggerType.USAGE_BASED:
            if schedule.usage_threshold_hours is None or schedule.usage_threshold_hours <= 0:
                raise ValueError("usage-based schedules require a positive usage_threshold_hours")

    def _compute_next_due_at(self, schedule: MaintenanceSchedule) -> Optional[datetime]:
        if schedule.trigger_type == TriggerType.TIME_BASED and schedule.interval_days is not None:
            anchor = schedule.last_triggered_at or schedule.created_at or self._utcnow()
            return anchor + timedelta(days=schedule.interval_days)
        return schedule.next_due_at

    async def create(self, payload: MaintenanceScheduleCreate) -> MaintenanceSchedule:
        # TODO (MEMBER-3): Remove hardcoded FIRE-001 after MEMBER-2 implements asset management
        FIRE_001_ID = "6a20a6f8ed6858a4bc9bfcfd"  # Hardcoded FIRE-001 asset ID for testing
        asset_id = payload.asset_id or FIRE_001_ID

        schedule = MaintenanceSchedule(
            asset_id=PyObjectId(asset_id),
            title=payload.title,
            description=payload.description,
            trigger_type=payload.trigger_type,
            interval_days=payload.interval_days,
            usage_threshold_hours=payload.usage_threshold_hours,
            current_usage_hours=payload.current_usage_hours,
            is_active=True,
            generated_wo_priority=payload.generated_wo_priority,
            assigned_to=self._resolve_object_id(payload.assigned_to),
        )
        self._validate_schedule(schedule)
        schedule.next_due_at = self._compute_next_due_at(schedule)
        return await self._repo.create(schedule)

    async def get(self, schedule_id: str) -> MaintenanceSchedule | None:
        return await self._repo.get_by_id(schedule_id)

    async def list(self, skip: int = 0, limit: int = 100) -> list[MaintenanceSchedule]:
        return await self._repo.list(skip=skip, limit=limit)

    async def list_by_asset(self, asset_id: str) -> list[MaintenanceSchedule]:
        return await self._repo.list_by_asset(asset_id)

    async def update(
        self, schedule_id: str, payload: MaintenanceScheduleUpdate
    ) -> MaintenanceSchedule | None:
        schedule = await self._repo.get_by_id(schedule_id)
        if schedule is None:
            return None

        patched = payload.model_dump(exclude_none=True)
        if "assigned_to" in patched:
            patched["assigned_to"] = self._resolve_object_id(patched["assigned_to"])

        for field, value in patched.items():
            setattr(schedule, field, value)

        self._validate_schedule(schedule)
        schedule.next_due_at = self._compute_next_due_at(schedule)
        return await self._repo.update(schedule)

    async def delete(self, schedule_id: str) -> bool:
        return await self._repo.delete(schedule_id)

    async def evaluate_due_schedules(
        self,
        asset_usage: Optional[dict[str, float]] = None,
        created_by: str = "system",
    ) -> list[str]:
        active_schedules = await self._repo.list_active()
        generated_ids: list[str] = []
        now = self._utcnow()

        for schedule in active_schedules:
            strategy = get_trigger_strategy(schedule.trigger_type)
            current_usage = None
            if schedule.trigger_type == TriggerType.USAGE_BASED:
                if asset_usage is not None:
                    current_usage = asset_usage.get(str(schedule.asset_id))
                if current_usage is None:
                    current_usage = schedule.current_usage_hours

            if not strategy.is_due(schedule, now=now, current_usage_hours=current_usage):
                continue

            work_order = await self._generate_work_order(schedule, created_by)
            schedule.last_triggered_at = now
            schedule.next_due_at = self._compute_next_due_at(schedule)
            await self._repo.update(schedule)
            generated_ids.append(work_order.id)

        return generated_ids

    async def _generate_work_order(self, schedule: MaintenanceSchedule, created_by: str):
        payload = WorkOrderCreate(
            title=f"PM: {schedule.title}",
            description=schedule.description,
            asset_id=str(schedule.asset_id),
            priority=schedule.generated_wo_priority,
            notes=f"Auto-generated from maintenance schedule {schedule.id}",
        )
        work_order = await self._work_order_service.create(payload, created_by=created_by)

        if schedule.assigned_to is not None:
            transition = WorkOrderStatusTransition(
                new_status=WorkOrderStatus.ASSIGNED,
                assigned_to=str(schedule.assigned_to),
            )
            work_order = await self._work_order_service.transition(work_order.id, transition)

        return work_order
