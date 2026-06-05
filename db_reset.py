"""
Clears all application collections from the database.

Usage:
    python db_reset.py
"""

import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

COLLECTIONS = [
    "users",
    "assets",
    "inventory_items",
    "work_orders",
    "maintenance_schedules",
]


async def reset() -> None:
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client[settings.db_name]

    print(f"Resetting database '{settings.db_name}'…\n")
    for col in COLLECTIONS:
        result = await db[col].delete_many({})
        print(f"  [-] {col}: {result.deleted_count} documents removed")

    client.close()
    print("\nDatabase cleared.")


if __name__ == "__main__":
    confirm = input("This will delete ALL data. Type 'yes' to confirm: ")
    if confirm.strip().lower() == "yes":
        asyncio.run(reset())
    else:
        print("Aborted.")
