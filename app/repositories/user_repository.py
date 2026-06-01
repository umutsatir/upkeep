# OWNER: MEMBER-1
from typing import Optional

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    model_class = User
    collection_name = "users"

    async def get_by_email(self, email: str) -> Optional[User]:
        """TODO (MEMBER-1): Used by auth to look up users by email."""
        doc = await self._collection.find_one({"email": email})
        if doc is None:
            return None
        return User.from_mongo(doc)
