# OWNER: MEMBER-1
from __future__ import annotations

from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

_client: Optional[AsyncIOMotorClient] = None


async def connect_db() -> None:
    global _client
    _client = AsyncIOMotorClient(settings.mongo_uri)
    # Verify connection on startup
    await _client.admin.command("ping")


async def close_db() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


def get_db() -> AsyncIOMotorDatabase:
    if _client is None:
        raise RuntimeError("Database client is not initialised. Call connect_db() first.")
    return _client[settings.db_name]
