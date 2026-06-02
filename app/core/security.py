# OWNER: MEMBER-1
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.core.config import settings

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_HOURS = 8
ALGORITHM = "HS256"


def hash_password(plain: str) -> str:
    return _pwd.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd.verify(plain, hashed)


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    """Returns user_id (sub). Raises jwt.InvalidTokenError on failure."""
    payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    return payload["sub"]
