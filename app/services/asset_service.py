# OWNER: MEMBER-2
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import DuplicateError, NotFoundError
from app.models.asset import Asset, AssetStatus, RepairRecord
from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import AssetCreate, AssetUpdate


class AssetService:
    """Business logic for asset lifecycle and repair history.

    Pattern: Repository — all persistence goes through AssetRepository.
    The service never constructs raw MongoDB queries directly.
    """

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._repo = AssetRepository(db)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    async def create(self, payload: AssetCreate) -> Asset:
        """Create a new asset. Raises DuplicateError if asset_tag already exists."""
        existing = await self._repo.get_by_tag(payload.asset_tag)
        if existing is not None:
            raise DuplicateError("asset_tag", payload.asset_tag)

        asset = Asset(
            name=payload.name,
            asset_tag=payload.asset_tag,
            category=payload.category,
            location=payload.location,
            assigned_to=payload.assigned_to,
            purchase_date=payload.purchase_date,
            warranty_expires_at=payload.warranty_expires_at,
            model_number=payload.model_number,
            serial_number=payload.serial_number,
            notes=payload.notes,
        )
        return await self._repo.create(asset)

    async def get(self, asset_id: str) -> Optional[Asset]:
        """Return the asset with the given id, or None if not found."""
        return await self._repo.get_by_id(asset_id)

    async def list(self, skip: int = 0, limit: int = 100) -> list[Asset]:
        """Return a paginated list of all assets."""
        return await self._repo.list(skip=skip, limit=limit)

    async def update(self, asset_id: str, payload: AssetUpdate) -> Optional[Asset]:
        """Apply a partial update (load → mutate → save)."""
        asset = await self._repo.get_by_id(asset_id)
        if asset is None:
            return None
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(asset, field, value)
        return await self._repo.update(asset)

    async def delete(self, asset_id: str) -> bool:
        """Delete by id. Returns True if a document was removed."""
        return await self._repo.delete(asset_id)

    # ------------------------------------------------------------------
    # Lifecycle transitions
    # ------------------------------------------------------------------

    async def activate(self, asset_id: str) -> Asset:
        """Transition asset to ACTIVE status."""
        asset = await self._repo.get_by_id(asset_id)
        if asset is None:
            raise NotFoundError("Asset", asset_id)
        asset.status = AssetStatus.ACTIVE
        return await self._repo.update(asset)

    async def decommission(self, asset_id: str) -> Asset:
        """Transition asset to DECOMMISSIONED (terminal state)."""
        asset = await self._repo.get_by_id(asset_id)
        if asset is None:
            raise NotFoundError("Asset", asset_id)
        asset.status = AssetStatus.DECOMMISSIONED
        return await self._repo.update(asset)

    async def send_to_maintenance(self, asset_id: str) -> Asset:
        """Transition asset to UNDER_MAINTENANCE status."""
        asset = await self._repo.get_by_id(asset_id)
        if asset is None:
            raise NotFoundError("Asset", asset_id)
        asset.status = AssetStatus.UNDER_MAINTENANCE
        return await self._repo.update(asset)

    # ------------------------------------------------------------------
    # Repair history — called by M1 (WorkOrderService) on WO completion
    # ------------------------------------------------------------------

    async def add_repair_record(self, asset_id: str, record: RepairRecord) -> Asset:
        """Append a repair record to the asset's history.

        Integration point: called by WorkOrderService.transition() → COMPLETED.
        """
        asset = await self._repo.get_by_id(asset_id)
        if asset is None:
            raise NotFoundError("Asset", asset_id)
        asset.repair_history.append(record)
        return await self._repo.update(asset)

    # ------------------------------------------------------------------
    # Warranty
    # ------------------------------------------------------------------

    async def list_expiring_warranties(self, days_ahead: int = 30) -> list[Asset]:
        """Return assets whose warranty expires within *days_ahead* days."""
        cutoff = datetime.now(timezone.utc) + timedelta(days=days_ahead)
        return await self._repo.list_expiring_warranties(before_date=cutoff)

    def is_warranty_expired(self, asset: Asset) -> bool:
        """Return True if the asset's warranty has already expired."""
        if asset.warranty_expires_at is None:
            return False
        now = datetime.now(timezone.utc)
        expires = asset.warranty_expires_at
        # Make timezone-aware if stored as naive UTC
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        return expires < now
