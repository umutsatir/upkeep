# OWNER: MEMBER-3
from app.models.maintenance import MaintenanceSchedule
from app.repositories.base_repository import BaseRepository


class MaintenanceRepository(BaseRepository[MaintenanceSchedule]):
    model_class = MaintenanceSchedule
    collection_name = "maintenance_schedules"

    async def list_active(self) -> list[MaintenanceSchedule]:
        """TODO (MEMBER-3): Return all active schedules (used by the scheduler)."""
        return await self.list(filter={"is_active": True})

    async def list_by_asset(self, asset_id: str) -> list[MaintenanceSchedule]:
        """TODO (MEMBER-3): Return schedules attached to a specific asset."""
        return await self.list(filter={"asset_id": asset_id})

    async def list_due(self, as_of) -> list[MaintenanceSchedule]:
        """TODO (MEMBER-3): Return time-based schedules where next_due_at <= as_of."""
        return await self.list(
            filter={"is_active": True, "next_due_at": {"$lte": as_of}}
        )
