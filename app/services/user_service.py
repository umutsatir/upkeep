# OWNER: MEMBER-1
from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Business logic for user management and authentication.

    TODO (MEMBER-1):
    - hash passwords with bcrypt before passing to the repository.
    - implement authenticate(email, password) -> User | None.
    - implement generate_token(user) -> str using python-jose / PyJWT.
    - add role-based permission checks (can_user_do(user, action) helper).
    """

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._repo = UserRepository(db)

    async def create_user(self, payload: UserCreate) -> User:
        """TODO (MEMBER-1): hash payload.password, build User, call repo.create."""
        raise NotImplementedError

    async def get_user(self, user_id: str) -> User | None:
        """TODO (MEMBER-1)"""
        raise NotImplementedError

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """TODO (MEMBER-1)"""
        raise NotImplementedError

    async def update_user(self, user_id: str, payload: UserUpdate) -> User | None:
        """TODO (MEMBER-1)"""
        raise NotImplementedError

    async def delete_user(self, user_id: str) -> bool:
        """TODO (MEMBER-1)"""
        raise NotImplementedError
