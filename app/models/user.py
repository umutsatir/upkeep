# OWNER: MEMBER-1
from enum import Enum
from typing import Optional

from app.models.base import BaseEntity


class Role(str, Enum):
    ADMIN = "admin"
    TECHNICIAN = "technician"
    SUPERVISOR = "supervisor"
    VIEWER = "viewer"


class User(BaseEntity):
    """Represents a system user.

    TODO (MEMBER-1): Add password hashing, JWT token generation, and
    role-based access control (RBAC) middleware.
    """

    full_name: str
    email: str
    hashed_password: str
    role: Role = Role.VIEWER
    is_active: bool = True
    department: Optional[str] = None
