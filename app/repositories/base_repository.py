# OWNER: MEMBER-1
from typing import Generic, TypeVar, Optional, Type
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.base import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(Generic[T]):
    """Generic async CRUD repository (Repository pattern).

    All database access lives here — services and routes must NEVER import
    motor or touch raw MongoDB documents directly.

    Subclasses only need to provide:
        model_class  — the concrete BaseEntity subclass
        collection_name — the MongoDB collection name (string)
    """

    model_class: Type[T]
    collection_name: str

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db
        self._collection = db[self.collection_name]

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    async def create(self, entity: T) -> T:
        """Persist a new entity and return it (id is already set on the model)."""
        entity.touch()
        await self._collection.insert_one(entity.to_mongo())
        return entity

    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Return the entity with the given id, or None if not found."""
        if not ObjectId.is_valid(entity_id):
            return None
        doc = await self._collection.find_one({"_id": ObjectId(entity_id)})
        if doc is None:
            return None
        return self.model_class.from_mongo(doc)  # type: ignore[return-value]

    async def list(
        self,
        filter: Optional[dict] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[T]:
        """Return a page of entities matching *filter* (default: all)."""
        cursor = self._collection.find(filter or {}).skip(skip).limit(limit)
        return [self.model_class.from_mongo(doc) async for doc in cursor]  # type: ignore[misc]

    async def update(self, entity: T) -> T:
        """Persist mutations to an existing entity.

        Replaces the entire document — callers should load → mutate → update.
        """
        entity.touch()
        await self._collection.replace_one(
            {"_id": ObjectId(entity.id)},
            entity.to_mongo(),
        )
        return entity

    async def delete(self, entity_id: str) -> bool:
        """Delete by id.  Returns True if a document was removed."""
        if not ObjectId.is_valid(entity_id):
            return False
        result = await self._collection.delete_one({"_id": ObjectId(entity_id)})
        return result.deleted_count > 0

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def exists(self, entity_id: str) -> bool:
        if not ObjectId.is_valid(entity_id):
            return False
        count = await self._collection.count_documents(
            {"_id": ObjectId(entity_id)}, limit=1
        )
        return count > 0

    async def count(self, filter: Optional[dict] = None) -> int:
        return await self._collection.count_documents(filter or {})
