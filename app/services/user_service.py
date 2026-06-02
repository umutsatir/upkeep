# OWNER: MEMBER-1
from __future__ import annotations

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.exceptions import DuplicateError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._repo = UserRepository(db)

    async def create_user(self, payload: UserCreate) -> User:
        if await self._repo.get_by_email(payload.email):
            raise DuplicateError("email", payload.email)
        user = User(
            full_name=payload.full_name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
            role=payload.role,
            department=payload.department,
        )
        return await self._repo.create(user)

    async def authenticate(self, email: str, password: str) -> Optional[str]:
        """Returns a JWT access token, or None if credentials are wrong."""
        user = await self._repo.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            return None
        return create_access_token(user.id)

    async def get_user(self, user_id: str) -> Optional[User]:
        return await self._repo.get_by_id(user_id)

    async def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self._repo.list(skip=skip, limit=limit)

    async def update_user(self, user_id: str, payload: UserUpdate) -> Optional[User]:
        user = await self._repo.get_by_id(user_id)
        if user is None:
            return None
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(user, field, value)
        return await self._repo.update(user)

    async def delete_user(self, user_id: str) -> bool:
        return await self._repo.delete(user_id)
