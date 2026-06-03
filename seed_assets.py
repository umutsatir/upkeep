"""
Creates sample assets in the database for testing.
Usage: python seed_assets.py
"""
import asyncio
from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.asset import Asset, AssetStatus


async def seed() -> None:
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client[settings.db_name]

    # Sample assets
    assets = [
        {
            "name": "HVAC Unit - Building A",
            "asset_tag": "HVAC-001",
            "category": "HVAC",
            "status": AssetStatus.ACTIVE,
            "location": "Building A - Floor 2",
            "purchase_date": datetime(2022, 1, 15),
            "warranty_expires_at": datetime(2025, 1, 15),
            "repair_history": [],
        },
        {
            "name": "Electrical Panel - Building B",
            "asset_tag": "ELEC-001",
            "category": "Electrical",
            "status": AssetStatus.ACTIVE,
            "location": "Building B - Basement",
            "purchase_date": datetime(2021, 6, 1),
            "warranty_expires_at": datetime(2024, 6, 1),
            "repair_history": [],
        },
        {
            "name": "Water Pump - Mechanical Room",
            "asset_tag": "PUMP-001",
            "category": "Plumbing",
            "status": AssetStatus.ACTIVE,
            "location": "Mechanical Room",
            "purchase_date": datetime(2023, 3, 10),
            "warranty_expires_at": datetime(2026, 3, 10),
            "repair_history": [],
        },
        {
            "name": "Fire Alarm System",
            "asset_tag": "FIRE-001",
            "category": "Safety",
            "status": AssetStatus.ACTIVE,
            "location": "Main Corridor",
            "purchase_date": datetime(2020, 11, 20),
            "warranty_expires_at": datetime(2024, 11, 20),
            "repair_history": [],
        },
    ]

    for asset_data in assets:
        existing = await db["assets"].find_one({"asset_tag": asset_data["asset_tag"]})
        if existing:
            print(f"[!] Asset zaten mevcut: {asset_data['asset_tag']}")
            continue

        asset = Asset(**asset_data)
        result = await db["assets"].insert_one(asset.to_mongo())
        print(f"[+] Asset oluşturuldu: {asset_data['asset_tag']} (ID: {result.inserted_id})")

    client.close()
    print("\n[✓] Tüm assets seed'lendi!")


if __name__ == "__main__":
    asyncio.run(seed())
