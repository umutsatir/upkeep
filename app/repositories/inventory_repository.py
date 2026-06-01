# OWNER: MEMBER-4
from app.models.inventory import InventoryItem
from app.repositories.base_repository import BaseRepository


class InventoryRepository(BaseRepository[InventoryItem]):
    model_class = InventoryItem
    collection_name = "inventory"

    async def get_by_sku(self, sku: str):
        """TODO (MEMBER-4): Look up an item by its SKU."""
        doc = await self._collection.find_one({"sku": sku})
        if doc is None:
            return None
        return InventoryItem.from_mongo(doc)

    async def list_low_stock(self) -> list[InventoryItem]:
        """TODO (MEMBER-4): Return items where quantity_on_hand <= low_stock_threshold."""
        # MongoDB can compare two fields with $expr
        return await self.list(
            filter={"$expr": {"$lte": ["$quantity_on_hand", "$low_stock_threshold"]}}
        )
