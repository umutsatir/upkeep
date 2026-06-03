# OWNER: MEMBER-2
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.asset import Asset
from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetService:
    """Business logic for asset lifecycle and repair history.

    TODO (MEMBER-2):
    - create(): validate asset_tag uniqueness before persisting.
    - add_repair_record(asset_id, record): append to repair_history, call repo.update.
    - check_warranty(asset_id): return True/False and raise alert if expired.
    - change_status(): guard against invalid lifecycle transitions.
    - list_expiring_warranties(days_ahead): query repo and return sorted list.
    """

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._repo = AssetRepository(db)

    async def create(self, payload: AssetCreate) -> Asset:
        """Create a new asset (stub for MEMBER-2)."""
        asset = Asset(**payload.model_dump())
        return await self._repo.create(asset)

    async def get(self, asset_id: str) -> Asset | None:
        """Get asset by ID (stub for MEMBER-2)."""
        return await self._repo.get(asset_id)

    async def list(self, skip: int = 0, limit: int = 100) -> list[Asset]:
        """List all assets (stub for MEMBER-2)."""
        return await self._repo.list(skip=skip, limit=limit)

    async def update(self, asset_id: str, payload: AssetUpdate) -> Asset | None:
        """Update asset (stub for MEMBER-2)."""
        return await self._repo.update(asset_id, payload)

    async def delete(self, asset_id: str) -> bool:
        """Delete asset (stub for MEMBER-2)."""
        return await self._repo.delete(asset_id)
