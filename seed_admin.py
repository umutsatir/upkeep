"""
Creates an admin user in the database.
Usage: python seed_admin.py [--email EMAIL] [--password PASSWORD] [--name NAME]
"""
import asyncio
import argparse

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import Role, User


async def seed(email: str, password: str, full_name: str) -> None:
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client[settings.db_name]

    existing = await db["users"].find_one({"email": email})
    if existing:
        print(f"[!] Kullanıcı zaten mevcut: {email}")
        client.close()
        return

    user = User(
        full_name=full_name,
        email=email,
        hashed_password=hash_password(password),
        role=Role.ADMIN,
    )
    await db["users"].insert_one(user.to_mongo())
    print(f"[+] Admin oluşturuldu: {email}")
    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Admin kullanıcı oluştur")
    parser.add_argument("--email", default="admin@upkeep.com")
    parser.add_argument("--password", default="admin123")
    parser.add_argument("--name", default="Admin")
    args = parser.parse_args()

    asyncio.run(seed(args.email, args.password, args.name))
