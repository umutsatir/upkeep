# OWNER: MEMBER-3
from bson import ObjectId

from app.models.maintenance import MaintenanceSchedule
from app.repositories.base_repository import BaseRepository


class MaintenanceRepository(BaseRepository[MaintenanceSchedule]):
    model_class = MaintenanceSchedule
    collection_name = "maintenance_schedules"

    async def list_active(self) -> list[MaintenanceSchedule]:
        return await self.list(filter={"is_active": True})

    async def list_by_asset(self, asset_id: str) -> list[MaintenanceSchedule]:
        if not ObjectId.is_valid(asset_id):
            return []
        return await self.list(filter={"asset_id": ObjectId(asset_id)})

    async def list_due(self, as_of) -> list[MaintenanceSchedule]:
        return await self.list(
            filter={"is_active": True, "next_due_at": {"$lte": as_of}}
        )
