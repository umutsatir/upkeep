# OWNER: MEMBER-2
from app.models.asset import Asset, AssetStatus
from app.repositories.base_repository import BaseRepository


class AssetRepository(BaseRepository[Asset]):
    model_class = Asset
    collection_name = "assets"

    async def get_by_tag(self, asset_tag: str):
        """TODO (MEMBER-2): Look up an asset by its human-readable tag."""
        doc = await self._collection.find_one({"asset_tag": asset_tag})
        if doc is None:
            return None
        return Asset.from_mongo(doc)

    async def list_by_status(self, status: AssetStatus) -> list[Asset]:
        """TODO (MEMBER-2): Filter assets by lifecycle status."""
        return await self.list(filter={"status": status.value})

    async def list_expiring_warranties(self, before_date) -> list[Asset]:
        """TODO (MEMBER-2): Return assets whose warranty expires before *before_date*."""
        return await self.list(
            filter={"warranty_expires_at": {"$lt": before_date}}
        )
